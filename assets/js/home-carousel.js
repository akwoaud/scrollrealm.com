(function () {
  'use strict';
  const root = document.querySelector('[data-home-carousel]');
  if (!root) return;
  const slides = [...root.querySelectorAll('[data-slide]')];
  const controls = root.querySelector('[data-carousel-controls]');
  const number = root.querySelector('[data-slide-number]');
  const announcement = root.querySelector('[data-slide-announcement]');
  if (slides.length < 2 || !controls) return;
  const total = root.querySelector('[data-slide-total]');
  if (total) total.textContent = String(slides.length).padStart(2, '0');
  let current = 0;
  function show(index) {
    if (slides[current].contains(document.activeElement)) root.focus({ preventScroll: true });
    current = (index + slides.length) % slides.length;
    slides.forEach((slide, i) => {
      const active = i === current;
      slide.classList.toggle('is-active', active);
      slide.setAttribute('aria-hidden', String(!active));
      slide.inert = !active;
    });
    root.classList.toggle('is-light', slides[current].dataset.theme === 'light');
    number.textContent = String(current + 1).padStart(2, '0');
    announcement.textContent = slides[current].getAttribute('aria-label');
  }
  controls.hidden = false;
  root.querySelector('[data-slide-prev]').addEventListener('click', () => show(current - 1));
  root.querySelector('[data-slide-next]').addEventListener('click', () => show(current + 1));
  root.addEventListener('keydown', event => {
    if (event.key !== 'ArrowLeft' && event.key !== 'ArrowRight') return;
    event.preventDefault();
    show(current + (event.key === 'ArrowRight' ? 1 : -1));
  });
  let touchStart = null;
  root.addEventListener('touchstart', event => {
    if (event.touches.length !== 1 || event.target.closest('a, button')) {
      touchStart = null;
      return;
    }
    touchStart = { x: event.touches[0].clientX, y: event.touches[0].clientY };
  }, { passive: true });
  root.addEventListener('touchend', event => {
    if (!touchStart || !event.changedTouches.length) return;
    const dx = event.changedTouches[0].clientX - touchStart.x;
    const dy = event.changedTouches[0].clientY - touchStart.y;
    touchStart = null;
    if (Math.abs(dx) >= 50 && Math.abs(dx) > Math.abs(dy) * 1.3) {
      show(current + (dx < 0 ? 1 : -1));
    }
  }, { passive: true });
  root.addEventListener('touchcancel', () => { touchStart = null; }, { passive: true });
})();
