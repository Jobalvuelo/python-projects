import { experiences } from './src/experiences.js';

const state = { vibe: 'garden', days: 5 };
const $ = (selector, root = document) => root.querySelector(selector);
const $$ = (selector, root = document) => [...root.querySelectorAll(selector)];

function renderExperience() {
  const experience = experiences[state.vibe];
  const stay = experience.durations[state.days];
  $('#result-icon').textContent = experience.icon;
  $('#result-label').textContent = `Your ${state.days}-day experience`;
  $('#result-title').textContent = experience.name;
  $('#result-description').textContent = experience.description;
  $('#included-list').innerHTML = stay.includes.map(item => `<li><span>✓</span>${item}</li>`).join('');
  const note = $('#result-note');
  note.hidden = !experience.note;
  note.textContent = experience.note || '';
  $$('.vibe-card').forEach(card => { const active = card.dataset.vibe === state.vibe; card.classList.toggle('active', active); card.setAttribute('aria-checked', active); });
  $$('.duration-tabs button').forEach(button => { const active = Number(button.dataset.days) === state.days; button.classList.toggle('active', active); button.setAttribute('aria-checked', active); });
}

$$('.vibe-card').forEach(card => card.addEventListener('click', () => { state.vibe = card.dataset.vibe; renderExperience(); $('#builder').scrollIntoView({ behavior: 'smooth', block: 'center' }); }));
$$('.duration-tabs button').forEach(button => button.addEventListener('click', () => { state.days = Number(button.dataset.days); renderExperience(); }));

const dialog = $('#booking-dialog');
$$('.open-booking').forEach(button => button.addEventListener('click', () => {
  const experience = experiences[state.vibe];
  $('#booking-choice').textContent = `${experience.icon} ${experience.name} · ${state.days} days / ${state.days - 1} nights`;
  $('[name="vibe"]', dialog).value = state.vibe;
  $('[name="duration"]', dialog).value = state.days;
  $('.form-status', dialog).textContent = '';
  dialog.showModal();
}));
$('.close-dialog').addEventListener('click', () => dialog.close());
dialog.addEventListener('click', event => { if (event.target === dialog) dialog.close(); });

const arrival = $('[name="arrival"]');
arrival.min = new Date().toISOString().slice(0, 10);
$('#booking-form').addEventListener('submit', async event => {
  event.preventDefault();
  const form = event.currentTarget;
  const button = $('button[type="submit"]', form);
  const status = $('.form-status', form);
  const data = Object.fromEntries(new FormData(form));
  data.guests = Number(data.guests); data.duration = Number(data.duration);
  button.disabled = true; $('.submit-label', button).textContent = 'Preparing secure checkout…'; status.textContent = '';
  try {
    const response = await fetch('/api/checkout', { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify(data) });
    const result = await response.json();
    if (!response.ok) throw new Error(result.message || 'We could not start the booking.');
    window.location.assign(result.url);
  } catch (error) {
    status.textContent = error.message;
  } finally {
    button.disabled = false; $('.submit-label', button).textContent = 'Continue to booking';
  }
});

const menu = $('.menu');
menu.addEventListener('click', () => { const open = $('#nav').classList.toggle('open'); menu.setAttribute('aria-expanded', open); document.body.classList.toggle('menu-open', open); });
$$('#nav a').forEach(link => link.addEventListener('click', () => { $('#nav').classList.remove('open'); document.body.classList.remove('menu-open'); }));

const observer = new IntersectionObserver(entries => entries.forEach(entry => { if (entry.isIntersecting) entry.target.classList.add('visible'); }), { threshold: .1 });
$$('section:not(.hero), .vibe-card, .photo-placeholder').forEach(element => { element.classList.add('reveal'); observer.observe(element); });
$('#year').textContent = new Date().getFullYear();
const bookingState = new URLSearchParams(location.search).get('booking');
if (bookingState) {
  const banner = $('#booking-banner');
  $('span', banner).textContent = bookingState === 'success' ? 'Thank you — your payment was received and your Garden House request is confirmed.' : 'Your payment was cancelled. Nothing was charged, and you can continue planning whenever you’re ready.';
  banner.hidden = false;
  $('button', banner).addEventListener('click', () => { banner.hidden = true; history.replaceState({}, '', location.pathname); });
}
renderExperience();
