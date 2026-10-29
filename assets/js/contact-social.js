(function () {
  'use strict';
  const ko = document.documentElement.lang === 'ko';
  const social = window.SCROLLREALM_SOCIAL_URLS || {};
  const httpsUrl = value => {
    if (typeof value !== 'string' || !value.trim()) return '';
    try {
      const u = new URL(value);
      return u.protocol === 'https:' && !u.username && !u.password ? u.href : '';
    } catch { return ''; }
  };
  let toast, toastTimer;
  const notify = message => {
    if (!toast) {
      toast = document.createElement('div');
      toast.className = 'social-link-toast';
      toast.setAttribute('role', 'status');
      toast.setAttribute('aria-live', 'polite');
      document.body.append(toast);
    }
    toast.textContent = message;
    toast.classList.add('is-visible');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => toast.classList.remove('is-visible'), 4200);
  };
  const links = [...document.querySelectorAll('[data-social]')];
  let configured = 0;
  links.forEach(link => {
    const url = httpsUrl(social[link.dataset.social]);
    if (url) {
      link.href = url;
      link.target = '_blank';
      link.rel = 'noopener noreferrer';
      link.removeAttribute('aria-describedby');
      configured++;
    } else {
      const name = link.textContent.trim();
      link.title = ko ? `${name} 채널 연결 준비 중` : `${name} link coming soon`;
      link.addEventListener('click', event => {
        event.preventDefault();
        notify(ko ? `${name} 채널 연결을 준비하고 있습니다.` : `The ${name} link is not available yet.`);
      });
    }
  });
  document.querySelectorAll('[data-social-status]').forEach(note => {
    note.hidden = links.length > 0 && configured === links.length;
    if (configured && configured < links.length) note.textContent = ko ? '일부 SNS 채널은 연결 준비 중' : 'Some channels are coming soon';
  });

  const form = document.querySelector('[data-contact-form]');
  if (!form) return;
  const categories = {
    general: { ko:'일반·제품 문의', en:'General & products', helpKo:'게임과 제품에 관한 질문을 남겨주세요. 관련 게임명을 함께 적어주시면 도움이 됩니다.', helpEn:'Questions about our games or products? Please include the game name.' },
    retail: { ko:'입점·유통', en:'Retail & distribution', helpKo:'입점이나 유통을 제안해 주세요. 회사·매장명과 관심 있는 제품을 함께 남겨주세요.', helpEn:'For retail or distribution inquiries, please include your company or store name and the products you are interested in.' },
    press: { ko:'취재·미디어', en:'Press & media', helpKo:'취재, 인터뷰, 리뷰 또는 자료 요청 내용을 남겨주세요. 매체명과 필요한 일정도 알려주세요.', helpEn:'For interviews, reviews or media assets, please include your publication and any relevant deadlines.' },
    other: { ko:'기타 제안', en:'Other proposals', helpKo:'협업 아이디어나 그 밖의 제안을 자유롭게 남겨주세요.', helpEn:'Tell us about a collaboration idea or any other proposal.' }
  };
  const radios = [...form.querySelectorAll('[name="category"]')];
  const helper = document.getElementById('contact-type-help');
  const selected = () => radios.find(input => input.checked)?.value || 'general';
  function updateCategory() {
    const category = categories[selected()];
    helper.textContent = ko ? category.helpKo : category.helpEn;
  }
  radios.forEach(input => input.addEventListener('change', updateCategory));
  // Direct links may preselect a type while retaining the same inquiry form.
  const preset = new URLSearchParams(location.search).get('type');
  if (Object.prototype.hasOwnProperty.call(categories, preset)) radios.find(input => input.value === preset).checked = true;
  updateCategory();
  const endpoint = httpsUrl(window.SCROLLREALM_CONTACT_ENDPOINT);
  const button = form.querySelector('[type="submit"]');
  const status = form.querySelector('.sr-form-status');
  const notice = document.querySelector('[data-contact-notice]');
  function readyButton() {
    button.disabled = !endpoint;
    button.textContent = endpoint ? (ko ? '문의 보내기 ↗' : 'Send inquiry ↗') : (ko ? '문의 접수 준비 중 ↗' : 'Inquiry delivery coming soon ↗');
  }
  readyButton();
  if (endpoint && notice) notice.hidden = true;
  let sending = false;
  form.addEventListener('submit', async event => {
    event.preventDefault();
    if (sending) return;
    if (!endpoint) {
      status.textContent = ko ? '문의 접수 기능을 준비하고 있습니다. 입력한 내용은 전송·저장되지 않았습니다.' : 'Inquiry delivery is not configured. Nothing has been sent or saved.';
      return;
    }
    if (!form.reportValidity()) return;
    const category = selected();
    const label = ko ? categories[category].ko : categories[category].en;
    const data = new FormData(form);
    const subject = `[${label}] ${String(data.get('topic') || '').trim()}`;
    data.set('category', category);
    data.set('category_label', label);
    data.set('subject', subject);
    data.set('_subject', subject);
    data.set('_replyto', String(data.get('email') || ''));
    data.set('locale', ko ? 'ko' : 'en');
    sending = true;
    button.disabled = true;
    button.textContent = ko ? '전송 중…' : 'Sending…';
    status.textContent = '';
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 20000);
    try {
      const response = await fetch(endpoint, { method:'POST', body:data, headers:{ Accept:'application/json' }, signal:controller.signal });
      if (!response.ok) throw new Error('Inquiry delivery failed');
      status.textContent = ko ? '문의가 접수되었습니다. 남겨주신 이메일로 답변드리겠습니다.' : 'Your inquiry has been received. We will reply to the email you provided.';
      form.reset();
      updateCategory();
    } catch {
      status.textContent = ko ? '접수 여부를 확인하지 못했습니다. 입력 내용은 유지됩니다. 잠시 후 다시 시도해 주세요.' : 'We could not confirm delivery. Your message is still here; please try again shortly.';
    } finally {
      clearTimeout(timeout);
      sending = false;
      readyButton();
    }
  });
})();
