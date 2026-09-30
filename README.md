# Taghazout Garden House

A warm, editorial website and booking-ready Cloudflare Worker for the Garden House experience in Taghazout.

## What is included

- The complete **3 vibes × 3 durations** experience builder
- Large, clearly labelled placeholders for original Garden House photography
- Responsive Moroccan/Berber-inspired visual system
- Booking form prepared for Stripe Checkout
- Cloudflare Worker API with server-side Stripe communication
- D1 booking schema and Stripe webhook handling
- No stock or AI-generated photography

## Architecture

```text
Browser → Cloudflare Worker → D1
                 │
                 └→ Stripe Checkout
                         │
                         └→ signed webhook → D1 booking status
```

Stripe secret keys are used only inside the Worker. They must never be added to the frontend or committed to Git.

## Local preview

For a frontend-only preview:

```bash
python -m http.server 8000 --directory public
```

For the complete Worker and a local D1 database:

```bash
npm install
npm run db:local
npm run dev
```

The booking form intentionally shows a helpful setup message until Stripe prices and secrets are configured.

## Cloudflare setup

1. Install dependencies with `npm install`.
2. Authenticate using `npx wrangler login`.
3. Create the database: `npx wrangler d1 create taghazout-garden-house`.
4. Copy the returned database ID into `wrangler.jsonc`.
5. Apply the schema with `npm run db:remote`.
6. Replace `PUBLIC_SITE_URL` in `wrangler.jsonc` with the production domain.
7. Add secrets (never put their values in this repository):

```bash
npx wrangler secret put STRIPE_SECRET_KEY
npx wrangler secret put STRIPE_WEBHOOK_SECRET
```

8. Create nine Stripe Prices, then add their IDs as Worker secrets:

```text
STRIPE_PRICE_GARDEN_3    STRIPE_PRICE_GARDEN_5    STRIPE_PRICE_GARDEN_7
STRIPE_PRICE_SURF_3      STRIPE_PRICE_SURF_5      STRIPE_PRICE_SURF_7
STRIPE_PRICE_RESET_3     STRIPE_PRICE_RESET_5     STRIPE_PRICE_RESET_7
```

Use `npx wrangler secret put <NAME>` for each value. Configure the Stripe webhook endpoint as:

```text
https://YOUR_DOMAIN/api/stripe/webhook
```

Subscribe it to `checkout.session.completed`, `checkout.session.async_payment_succeeded`, and `checkout.session.async_payment_failed`.

## Add the real photography

Place original photos under `public/images/`. Replace each `.photo-placeholder` element in `public/index.html` with an `<img>` using the same container class. The layouts already support landscape, portrait, full-width and asymmetrical formats.

## Safety notes

- Checkout sessions are created server-side.
- Webhook signatures are checked before a booking can become `paid`.
- Package/price selection is allowlisted server-side; the browser cannot submit arbitrary Stripe Price IDs.
- D1 stores booking details and Stripe references, but no card data.
