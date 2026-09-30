const json = (data, status = 200) => new Response(JSON.stringify(data), { status, headers: { 'content-type': 'application/json; charset=utf-8' } });

const PACKAGE_KEYS = new Set(['garden-3', 'garden-5', 'garden-7', 'surf-3', 'surf-5', 'surf-7', 'reset-3', 'reset-5', 'reset-7']);
const PRICE_BINDINGS = { 'garden-3': 'STRIPE_PRICE_GARDEN_3', 'garden-5': 'STRIPE_PRICE_GARDEN_5', 'garden-7': 'STRIPE_PRICE_GARDEN_7', 'surf-3': 'STRIPE_PRICE_SURF_3', 'surf-5': 'STRIPE_PRICE_SURF_5', 'surf-7': 'STRIPE_PRICE_SURF_7', 'reset-3': 'STRIPE_PRICE_RESET_3', 'reset-5': 'STRIPE_PRICE_RESET_5', 'reset-7': 'STRIPE_PRICE_RESET_7' };

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (request.method === 'POST' && url.pathname === '/api/checkout') return createCheckout(request, env, url.origin);
    if (request.method === 'POST' && url.pathname === '/api/stripe/webhook') return handleWebhook(request, env);
    if (request.method === 'GET' && url.pathname === '/api/health') return json({ ok: true, database: Boolean(env.DB), stripe: Boolean(env.STRIPE_SECRET_KEY) });
    return env.ASSETS.fetch(request);
  }
};

async function createCheckout(request, env, origin) {
  let body;
  try { body = await request.json(); } catch { return json({ message: 'Please check the booking details and try again.' }, 400); }
  const packageKey = `${body.vibe}-${Number(body.duration)}`;
  if (!PACKAGE_KEYS.has(packageKey) || !/^\d{4}-\d{2}-\d{2}$/.test(body.arrival || '') || !/^\S+@\S+\.\S+$/.test(body.email || '') || !String(body.name || '').trim() || !Number.isInteger(body.guests) || body.guests < 1 || body.guests > 6) return json({ message: 'Please complete all required booking details.' }, 400);
  const priceId = env[PRICE_BINDINGS[packageKey]];
  if (!env.STRIPE_SECRET_KEY || !priceId) return json({ message: 'Online booking is being prepared. Package prices still need to be connected before payment can begin.' }, 503);
  if (!env.DB) return json({ message: 'The booking database is not connected yet.' }, 503);

  const id = crypto.randomUUID();
  await env.DB.prepare('INSERT INTO bookings (id, package_key, arrival_date, guests, guest_name, guest_email, message, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?)').bind(id, packageKey, body.arrival, body.guests, String(body.name).trim(), body.email.toLowerCase(), String(body.message || '').slice(0, 2000), 'pending').run();
  const form = new URLSearchParams({ mode: 'payment', 'line_items[0][price]': priceId, 'line_items[0][quantity]': '1', client_reference_id: id, customer_email: body.email, success_url: `${env.PUBLIC_SITE_URL || origin}/?booking=success&session_id={CHECKOUT_SESSION_ID}`, cancel_url: `${env.PUBLIC_SITE_URL || origin}/?booking=cancelled`, 'metadata[booking_id]': id, 'metadata[package_key]': packageKey, 'metadata[arrival]': body.arrival, 'metadata[guests]': String(body.guests) });
  const stripe = await fetch('https://api.stripe.com/v1/checkout/sessions', { method: 'POST', headers: { authorization: `Bearer ${env.STRIPE_SECRET_KEY}`, 'content-type': 'application/x-www-form-urlencoded' }, body: form });
  const session = await stripe.json();
  if (!stripe.ok) { await env.DB.prepare('UPDATE bookings SET status = ? WHERE id = ?').bind('checkout_failed', id).run(); return json({ message: 'Secure checkout could not be started. Please try again.' }, 502); }
  await env.DB.prepare('UPDATE bookings SET stripe_session_id = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?').bind(session.id, id).run();
  return json({ url: session.url });
}

async function handleWebhook(request, env) {
  if (!env.STRIPE_WEBHOOK_SECRET || !env.DB) return json({ message: 'Webhook is not configured.' }, 503);
  const raw = await request.text();
  if (!await verifyStripeSignature(raw, request.headers.get('stripe-signature'), env.STRIPE_WEBHOOK_SECRET)) return json({ message: 'Invalid signature.' }, 400);
  const event = JSON.parse(raw);
  if (event.type === 'checkout.session.completed' || event.type === 'checkout.session.async_payment_succeeded') {
    const session = event.data.object;
    await env.DB.prepare('UPDATE bookings SET status = ?, stripe_payment_intent_id = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?').bind('paid', session.payment_intent || null, session.client_reference_id).run();
  }
  if (event.type === 'checkout.session.async_payment_failed') await env.DB.prepare('UPDATE bookings SET status = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?').bind('payment_failed', event.data.object.client_reference_id).run();
  return json({ received: true });
}

async function verifyStripeSignature(payload, header, secret) {
  if (!header) return false;
  const parts = Object.fromEntries(header.split(',').map(item => item.split('=')));
  if (!parts.t || !parts.v1 || Math.abs(Date.now() / 1000 - Number(parts.t)) > 300) return false;
  const key = await crypto.subtle.importKey('raw', new TextEncoder().encode(secret), { name: 'HMAC', hash: 'SHA-256' }, false, ['sign']);
  const signed = await crypto.subtle.sign('HMAC', key, new TextEncoder().encode(`${parts.t}.${payload}`));
  const expected = [...new Uint8Array(signed)].map(byte => byte.toString(16).padStart(2, '0')).join('');
  if (expected.length !== parts.v1.length) return false;
  let difference = 0; for (let i = 0; i < expected.length; i++) difference |= expected.charCodeAt(i) ^ parts.v1.charCodeAt(i);
  return difference === 0;
}
