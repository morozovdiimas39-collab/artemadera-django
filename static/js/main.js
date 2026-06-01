document.addEventListener('DOMContentLoaded', () => {
  // --- 1. Dropdown "Услуги" ---
  const navServicesWrap = document.getElementById('nav-services-wrap');
  const servicesDropdown = document.getElementById('services-dropdown');
  const servicesChevron = document.getElementById('nav-services-chevron');

  if (navServicesWrap && servicesDropdown) {
    const showDropdown = () => {
      servicesDropdown.style.opacity = '1';
      servicesDropdown.style.transform = 'scaleY(1)';
      servicesDropdown.style.pointerEvents = 'auto';
      servicesDropdown.style.visibility = 'visible';
      if (servicesChevron) servicesChevron.style.transform = 'rotate(180deg)';
    };
    const hideDropdown = () => {
      servicesDropdown.style.opacity = '0';
      servicesDropdown.style.transform = 'scaleY(0.9)';
      servicesDropdown.style.pointerEvents = 'none';
      servicesDropdown.style.visibility = 'hidden';
      if (servicesChevron) servicesChevron.style.transform = 'rotate(0deg)';
    };
    navServicesWrap.addEventListener('mouseenter', showDropdown);
    navServicesWrap.addEventListener('mouseleave', hideDropdown);
  }

  // --- 2. Anchors & Scrolling ---
  const scrollTo = (targetId) => {
    const el = document.querySelector(targetId);
    if (el) {
      const offset = 100;
      const bodyRect = document.body.getBoundingClientRect().top;
      const elementRect = el.getBoundingClientRect().top;
      const elementPosition = elementRect - bodyRect;
      const offsetPosition = elementPosition - offset;

      window.scrollTo({
        top: offsetPosition,
        behavior: 'smooth'
      });
    }
  };

  document.querySelectorAll('.scrollTo').forEach(btn => {
    btn.addEventListener('click', () => {
      const target = btn.getAttribute('data-target');
      if (target) scrollTo(target);
    });
  });

  // Legacy anchor map
  const anchorMap = {
    'Калькулятор': '#quiz',
    'Этапы': '#process',
    'До/После': '#comparison',
    'Почему мы': '#whyus',
    'Работы': '#portfolio',
    'FAQ': '#faq',
    'Контакты': '#contact'
  };

  document.querySelectorAll('button, a').forEach(el => {
    const text = el.textContent.trim();
    if (anchorMap[text]) {
      el.addEventListener('click', (e) => {
        if (el.tagName === 'A') {
          const href = el.getAttribute('href');
          if (href && !href.startsWith('#')) return;
        }
        e.preventDefault();
        scrollTo(anchorMap[text]);
      });
    }
  });

  // --- 3. Mobile Menu Toggle ---
  const menuToggleBtn = document.getElementById('mobile-menu-toggle');
  const mobileMenuOverlay = document.getElementById('mobile-menu-overlay');

  if (menuToggleBtn && mobileMenuOverlay) {
    const closeMenu = () => {
      mobileMenuOverlay.classList.remove('is-open');
      document.body.style.overflow = '';
    };
    menuToggleBtn.addEventListener('click', () => {
      mobileMenuOverlay.classList.add('is-open');
      document.body.style.overflow = 'hidden';
    });
    document.getElementById('mob-backdrop')?.addEventListener('click', closeMenu);
    mobileMenuOverlay.querySelectorAll('a').forEach(el => el.addEventListener('click', closeMenu));
  }

  // --- 4. Callback Modal ---
  const modal = document.getElementById('callback-modal');
  if (modal) {
    const openModal = () => {
      modal.classList.add('is-open');
      document.body.style.overflow = 'hidden';
    };
    const closeModal = () => {
      modal.classList.remove('is-open');
      document.body.style.overflow = '';
    };

    document.querySelectorAll('[data-open-modal="callback"], .open-callback-modal').forEach(btn => {
      btn.addEventListener('click', openModal);
    });

    document.querySelectorAll('a[href="#contact"], a[href$="#contact"]').forEach((link) => {
      if (
        link.classList.contains('nav-link') ||
        link.classList.contains('mob-nav-link') ||
        link.closest('.site-footer') ||
        link.closest('.contact-section')
      ) {
        return;
      }
      link.addEventListener('click', (e) => {
        e.preventDefault();
        openModal();
      });
    });

    const callbackOpenBtn = document.getElementById('callback-open');
    if (callbackOpenBtn) callbackOpenBtn.addEventListener('click', openModal);

    const mobileCallbackBtn = document.getElementById('mobile-callback-open');
    if (mobileCallbackBtn) mobileCallbackBtn.addEventListener('click', () => {
      document.getElementById('mobile-menu-overlay')?.classList.add('opacity-0', 'pointer-events-none');
      document.getElementById('mobile-menu-content')?.classList.add('-translate-y-6', 'opacity-0');
      document.body.style.overflow = '';
      setTimeout(openModal, 200);
    });

    modal.querySelectorAll('.modal-close').forEach(btn => btn.addEventListener('click', closeModal));
    modal.addEventListener('click', (e) => {
      if (e.target === modal || e.target.classList.contains('cb-modal__backdrop')) closeModal();
    });
    document.addEventListener('keydown', (e) => { if (e.key === 'Escape') closeModal(); });
  }

  // --- 4b. Успешная заявка (все формы с form_type=contact — AJAX, без перезагрузки) ---
  const leadSuccessModal = document.getElementById('lead-success-modal');
  const closeLeadSuccess = () => {
    if (!leadSuccessModal) return;
    leadSuccessModal.classList.remove('is-open');
    document.body.style.overflow = '';
  };
  const openLeadSuccess = () => {
    if (!leadSuccessModal) return;
    document.getElementById('callback-modal')?.classList.remove('is-open');
    leadSuccessModal.classList.add('is-open');
    document.body.style.overflow = 'hidden';
  };
  if (leadSuccessModal) {
    leadSuccessModal.querySelectorAll('.lead-modal-close').forEach((btn) => {
      btn.addEventListener('click', closeLeadSuccess);
    });
    leadSuccessModal.addEventListener('click', (e) => {
      if (e.target === leadSuccessModal || e.target.classList.contains('cb-modal__backdrop')) {
        closeLeadSuccess();
      }
    });
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && leadSuccessModal.classList.contains('is-open')) closeLeadSuccess();
    });
  }

  document.addEventListener('submit', async (e) => {
    const form = e.target;
    if (!(form instanceof HTMLFormElement)) return;
    if (!form.querySelector('input[name="form_type"][value="contact"]')) return;
    e.preventDefault();
    const submitBtn = form.querySelector('button[type="submit"], input[type="submit"]');
    const fd = new FormData(form);
    let postPath = form.getAttribute('action') || window.location.pathname;
    if (postPath) {
      try {
        const u = new URL(postPath, window.location.origin);
        postPath = u.pathname + u.search;
      } catch {
        postPath = window.location.pathname;
      }
    } else {
      postPath = window.location.pathname;
    }
    const csrf = form.querySelector('input[name="csrfmiddlewaretoken"]')?.value;
    if (submitBtn) submitBtn.disabled = true;
    try {
      const res = await fetch(postPath, {
        method: 'POST',
        body: fd,
        credentials: 'same-origin',
        headers: {
          'X-Requested-With': 'XMLHttpRequest',
          ...(csrf ? { 'X-CSRFToken': csrf } : {}),
        },
      });
      const ct = res.headers.get('content-type') || '';
      if (res.ok && ct.includes('application/json')) {
        const data = await res.json();
        if (data.ok) {
          form.reset();
          openLeadSuccess();
        }
      } else if (res.status === 400 && ct.includes('application/json')) {
        try {
          const err = await res.json();
          if (err.error === 'phone_required') {
            window.alert('Укажите номер телефона.');
          } else {
            window.alert('Не удалось отправить заявку. Попробуйте ещё раз или позвоните нам.');
          }
        } catch {
          window.alert('Не удалось отправить заявку. Попробуйте ещё раз или позвоните нам.');
        }
      } else {
        window.alert('Не удалось отправить заявку. Попробуйте ещё раз или позвоните нам.');
      }
    } catch {
      window.alert('Ошибка сети. Проверьте подключение и попробуйте снова.');
    } finally {
      if (submitBtn) submitBtn.disabled = false;
    }
  });

  // --- 5. Online calculator (per-page profiles + home service picker) ---
  const calcRoot = document.getElementById('quiz');
  if (calcRoot) {
    const formatRub = (amount) =>
      new Intl.NumberFormat('ru-RU', { maximumFractionDigits: 0 }).format(Math.round(amount)) + ' ₽';

    const stepPicker = calcRoot.querySelector('[data-calc-step="picker"]');
    const stepCalc = calcRoot.querySelector('[data-calc-step="calc"]');
    const backBtn = calcRoot.querySelector('.calc-back-btn');
    const profilesEl = document.getElementById('calc-profiles-data');
    const profilesData = profilesEl ? JSON.parse(profilesEl.textContent || '{}') : {};

    const calcArea = calcRoot.querySelector('.calc-area');
    const calcAreaValue = calcRoot.querySelector('.calc-area-value');
    const calcTotal = calcRoot.querySelector('.calc-total');
    const calcUnitLabel = calcRoot.querySelector('.calc-unit-label');
    const calcOptionsGrid = calcRoot.querySelector('.calc-options-grid');
    const calcOptionsLabel = calcRoot.querySelector('.calc-options-label');
    const calcSliderWrap = calcRoot.querySelector('.calc-slider-wrap');
    const calcSliderLabel = calcRoot.querySelector('.calc-slider-label');
    const calcRangeLabels = calcRoot.querySelector('.calc-range-labels');
    const calcProfileInput = calcRoot.querySelector('.calc-profile-input');
    const calcBadge = calcRoot.querySelector('.calc-badge');
    const calcTitle = calcRoot.querySelector('.calc-title');
    const calcDesc = calcRoot.querySelector('.calc-desc');
    const perkEls = [
      calcRoot.querySelector('.calc-perk-1'),
      calcRoot.querySelector('.calc-perk-2'),
      calcRoot.querySelector('.calc-perk-3'),
    ];

    const INACTIVE =
      'bg-white/5 border-white/10 text-gray-300 hover:bg-white/10 hover:border-white/20';
    const ACTIVE = 'calc-material--active';

    let unitType = 'sqm';
    let selectedMaterial = '';
    let prices = {};

    const showStep = (name) => {
      if (stepPicker) stepPicker.classList.toggle('calc-step--hidden', name !== 'picker');
      if (stepCalc) stepCalc.classList.toggle('calc-step--hidden', name !== 'calc');
    };

    const bindMaterials = () => {
      const calcMaterials = calcRoot.querySelectorAll('.calc-material');
      prices = {};
      calcMaterials.forEach((btn) => {
        if (btn.dataset.material) {
          prices[btn.dataset.material] = Number(btn.dataset.price) || 0;
        }
      });
      selectedMaterial =
        calcRoot.querySelector('.calc-material--active')?.dataset.material ||
        calcMaterials[0]?.dataset.material ||
        '';

      const setMaterialActive = (btn) => {
        calcMaterials.forEach((b) => {
          b.classList.remove(ACTIVE);
          INACTIVE.split(' ').forEach((c) => b.classList.add(c));
        });
        INACTIVE.split(' ').forEach((c) => btn.classList.remove(c));
        btn.classList.add(ACTIVE);
      };

      const updateTotal = () => {
        const price = prices[selectedMaterial] ?? 0;
        let total = price;
        if (unitType !== 'fixed' && calcArea) {
          const area = Number(calcArea.value);
          if (calcAreaValue) calcAreaValue.textContent = String(area);
          total = area * price;
        }
        if (calcTotal) calcTotal.textContent = formatRub(total);
      };

      calcMaterials.forEach((btn) => {
        btn.addEventListener('click', () => {
          selectedMaterial = btn.dataset.material;
          setMaterialActive(btn);
          updateTotal();
        });
      });

      if (calcArea) {
        calcArea.addEventListener('input', updateTotal);
        calcArea.addEventListener('change', updateTotal);
      }
      updateTotal();
    };

    const applyProfile = (profile) => {
      if (!profile) return;
      unitType = profile.unit_type || 'sqm';
      calcRoot.dataset.calcSlug = profile.slug;
      if (calcProfileInput) calcProfileInput.value = profile.slug;
      if (calcBadge) calcBadge.textContent = profile.badge_text || '';
      if (calcTitle) calcTitle.textContent = profile.title || '';
      if (calcDesc) calcDesc.textContent = profile.description || '';
      const perks = [profile.perk_1, profile.perk_2, profile.perk_3];
      perkEls.forEach((el, i) => {
        if (el && perks[i]) el.textContent = perks[i];
      });
      if (calcOptionsLabel) calcOptionsLabel.textContent = profile.options_label || '';

      const sliderHidden = unitType === 'fixed';
      if (calcSliderWrap) calcSliderWrap.classList.toggle('calc-slider-wrap--hidden', sliderHidden);
      if (calcSliderLabel) {
        calcSliderLabel.textContent =
          unitType === 'linear' ? 'Длина швов' : 'Площадь по полу';
      }
      if (calcUnitLabel) calcUnitLabel.textContent = profile.unit_label || 'м²';
      if (calcArea && !sliderHidden) {
        calcArea.min = String(profile.area_min);
        calcArea.max = String(profile.area_max);
        calcArea.step = String(profile.area_step);
        calcArea.value = String(profile.area_default);
        if (calcAreaValue) calcAreaValue.textContent = String(profile.area_default);
      }
      if (calcRangeLabels) {
        const spans = calcRangeLabels.querySelectorAll('span');
        const unit = profile.unit_label || '';
        if (spans[0]) spans[0].textContent = `${profile.area_min} ${unit}`.trim();
        if (spans[1]) spans[1].textContent = `${profile.area_max} ${unit}`.trim();
      }

      if (calcOptionsGrid) {
        const defaultKey = profile.default_option || (profile.options[0] && profile.options[0].key);
        calcOptionsGrid.innerHTML = (profile.options || [])
          .map((opt) => {
            const isActive = opt.key === defaultKey;
            const base = isActive
              ? ACTIVE
              : 'bg-white/5 border-white/10 text-gray-300 hover:bg-white/10 hover:border-white/20';
            return `<button type="button" class="calc-material p-4 rounded-xl border transition-all text-left flex items-center gap-3 ${base}" data-material="${opt.key}" data-price="${opt.price}">
              <span class="calc-material-label text-sm font-bold leading-tight">${opt.label}</span>
            </button>`;
          })
          .join('');
      }

      if (calcTotal && profile.initial_total != null) {
        calcTotal.textContent =
          typeof profile.initial_total === 'number'
            ? formatRub(profile.initial_total)
            : profile.initial_total;
      }

      bindMaterials();
    };

    if (stepPicker && Object.keys(profilesData).length) {
      calcRoot.querySelectorAll('.calc-service-pick').forEach((btn) => {
        btn.addEventListener('click', () => {
          const slug = btn.dataset.targetProfile;
          const profile = profilesData[slug];
          if (!profile) return;
          calcRoot.querySelectorAll('.calc-service-pick').forEach((b) => {
            b.classList.remove('calc-service-pick--active');
          });
          btn.classList.add('calc-service-pick--active');
          applyProfile(profile);
          showStep('calc');
          stepCalc?.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        });
      });
      if (backBtn) {
        backBtn.addEventListener('click', () => {
          showStep('picker');
          calcRoot.querySelectorAll('.calc-service-pick').forEach((b) => {
            b.classList.remove('calc-service-pick--active');
          });
        });
      }
    } else {
      bindMaterials();
    }
  }

  // --- 6. FAQ accordion ---
  document.querySelectorAll('#faq .faq-item').forEach(item => {
    const btn = item.querySelector('.faq-question');
    const answer = item.querySelector('.faq-answer');
    if (!btn || !answer) return;

    btn.addEventListener('click', () => {
      const isOpen = item.classList.contains('faq-item--open');

      document.querySelectorAll('#faq .faq-item').forEach(other => {
        if (other === item) return;
        other.classList.remove('faq-item--open');
        const otherBtn = other.querySelector('.faq-question');
        const otherAnswer = other.querySelector('.faq-answer');
        if (otherBtn) otherBtn.setAttribute('aria-expanded', 'false');
        if (otherAnswer) otherAnswer.hidden = true;
      });

      if (isOpen) {
        item.classList.remove('faq-item--open');
        btn.setAttribute('aria-expanded', 'false');
        answer.hidden = true;
      } else {
        item.classList.add('faq-item--open');
        btn.setAttribute('aria-expanded', 'true');
        answer.hidden = false;
      }
    });
  });

  // --- 7. Before / After sliders ---
  document.querySelectorAll('[data-ba-slider]').forEach(slider => {
    const wrap = slider.querySelector('.ba-before-wrap');
    const range = slider.querySelector('.ba-range');
    const beforeImg = slider.querySelector('.ba-before');
    if (!wrap || !range) return;

    const syncWidth = () => {
      const w = slider.offsetWidth;
      if (beforeImg && w) beforeImg.style.width = `${w}px`;
    };

    const setPosition = (pct) => {
      const value = Math.min(100, Math.max(0, Number(pct)));
      slider.style.setProperty('--ba-pct', String(value));
      wrap.style.width = `${value}%`;
    };

    range.addEventListener('input', () => setPosition(range.value));
    window.addEventListener('resize', syncWidth);
    syncWidth();
    setPosition(range.value);
  });

  // --- 8. Shlifovka mobile sticky bar ---
  const shlifovkaSticky = document.getElementById('shlifovka-mobile-sticky');
  if (shlifovkaSticky) {
    const contactSection = document.getElementById('contact');
    const showAfter = 320;

    const updateSticky = () => {
      const scrolled = window.scrollY > showAfter;
      let hideNearContact = false;
      if (contactSection) {
        const rect = contactSection.getBoundingClientRect();
        hideNearContact = rect.top < window.innerHeight * 0.55;
      }
      const visible = scrolled && !hideNearContact;
      shlifovkaSticky.classList.toggle('is-visible', visible);
      shlifovkaSticky.setAttribute('aria-hidden', visible ? 'false' : 'true');
    };

    shlifovkaSticky.querySelectorAll('[data-scroll-target]').forEach(btn => {
      btn.addEventListener('click', () => {
        const target = btn.getAttribute('data-scroll-target');
        if (target) scrollTo(target);
      });
    });

    window.addEventListener('scroll', updateSticky, { passive: true });
    updateSticky();
  }

  // --- 9. Portfolio cases (inline expand) ---
  const portfolioDetail = document.getElementById('portfolio-detail');
  if (portfolioDetail) {
    const triggers = document.querySelectorAll('[data-portfolio-case-trigger]');
    const portfolioItems = document.querySelectorAll('[data-portfolio-item]');
    const showMoreBtn = document.querySelector('[data-portfolio-show-more]');
    const panes = portfolioDetail.querySelectorAll('[data-portfolio-case-panel]');
    let activeId = null;
    const revealStep = 9;

    const setGallerySlide = (pane, index) => {
      const slides = pane.querySelectorAll('.portfolio-detail-slide');
      const thumbs = pane.querySelectorAll('[data-gallery-thumb]');
      slides.forEach((slide, i) => {
        slide.classList.toggle('is-active', i === index);
      });
      thumbs.forEach((thumb, i) => {
        thumb.classList.toggle('is-active', i === index);
      });
    };

    const bindGallery = (pane) => {
      const slides = pane.querySelectorAll('.portfolio-detail-slide');
      if (slides.length <= 1) return;

      let index = 0;
      const show = (next) => {
        index = (next + slides.length) % slides.length;
        setGallerySlide(pane, index);
      };

      pane.querySelector('[data-gallery-prev]')?.addEventListener('click', (e) => {
        e.stopPropagation();
        show(index - 1);
      });
      pane.querySelector('[data-gallery-next]')?.addEventListener('click', (e) => {
        e.stopPropagation();
        show(index + 1);
      });
      pane.querySelectorAll('[data-gallery-thumb]').forEach((thumb) => {
        thumb.addEventListener('click', (e) => {
          e.stopPropagation();
          show(Number(thumb.getAttribute('data-gallery-thumb')));
        });
      });
    };

    panes.forEach(bindGallery);

    const closeDetail = () => {
      activeId = null;
      portfolioDetail.hidden = true;
      panes.forEach((pane) => { pane.hidden = true; });
      triggers.forEach((btn) => {
        btn.classList.remove('is-active');
        btn.setAttribute('aria-expanded', 'false');
      });
    };

    const openDetail = (id) => {
      if (activeId === id) {
        closeDetail();
        return;
      }
      const activeTrigger = Array.from(triggers).find((btn) => btn.getAttribute('data-portfolio-case-trigger') === id);
      if (activeTrigger) {
        activeTrigger.insertAdjacentElement('afterend', portfolioDetail);
      }
      activeId = id;
      portfolioDetail.hidden = false;
      panes.forEach((pane) => {
        const match = pane.getAttribute('data-portfolio-case-panel') === id;
        pane.hidden = !match;
        if (match) setGallerySlide(pane, 0);
      });
      triggers.forEach((btn) => {
        const match = btn.getAttribute('data-portfolio-case-trigger') === id;
        btn.classList.toggle('is-active', match);
        btn.setAttribute('aria-expanded', match ? 'true' : 'false');
      });

      const offset = 100;
      const top = portfolioDetail.getBoundingClientRect().top + window.scrollY - offset;
      window.scrollTo({ top, behavior: 'smooth' });
    };

    triggers.forEach((btn) => {
      btn.addEventListener('click', () => {
        openDetail(btn.getAttribute('data-portfolio-case-trigger'));
      });
    });

    portfolioDetail.querySelectorAll('[data-portfolio-case-close]').forEach((btn) => {
      btn.addEventListener('click', closeDetail);
    });

    const updateShowMore = () => {
      if (!showMoreBtn) return;
      const hiddenCount = Array.from(portfolioItems).filter((item) => item.classList.contains('is-hidden')).length;
      showMoreBtn.hidden = hiddenCount === 0;
    };

    if (showMoreBtn) {
      showMoreBtn.addEventListener('click', () => {
        const hiddenItems = Array.from(portfolioItems).filter((item) => item.classList.contains('is-hidden'));
        hiddenItems.slice(0, revealStep).forEach((item) => {
          item.classList.remove('is-hidden');
        });
        updateShowMore();
      });
      updateShowMore();
    }
  }

  // --- Home Quiz ---
  const quizForm = document.getElementById('home-quiz');
  if (quizForm) {
    const steps = Array.from(quizForm.querySelectorAll('.hq-step'));
    const progressFill = document.getElementById('hq-progress-fill');
    const stepLabel   = document.getElementById('hq-step-label');
    const stepPct     = document.getElementById('hq-step-pct');
    const inputService = document.getElementById('hq-input-service');
    const inputHouse   = document.getElementById('hq-input-house');
    const inputArea    = document.getElementById('hq-input-area');
    const quizImage    = document.getElementById('hq-quiz-image');
    const summary      = document.getElementById('hq-summary');
    const slider       = document.getElementById('hq-area-slider');
    const numInput     = document.getElementById('hq-area-num');

    const TOTAL = 3;
    const LABELS = {
      service: { shlifovka: 'Шлифовка', pokraska: 'Покраска', 'teplyy-shov': 'Тёплый шов', okosyachka: 'Окосячка', obsada: 'Обсада', kryshi: 'Крыши', injeneriya: 'Инженерия' },
      house:   { srub: 'Сруб', brus: 'Брус', kleen: 'Клееный брус', ocil: 'Оцилиндровка', lafet: 'Лафет', banya: 'Баня' },
    };

    let currentStep = 1;
    const answers = { service: '', house: '', area: '100' };

    const setProgress = (n) => {
      const pct = Math.round((n / (TOTAL + 1)) * 100);
      if (progressFill) progressFill.style.width = pct + '%';
      if (stepLabel) {
        if (n <= TOTAL) stepLabel.textContent = `ВОПРОС ${n} ИЗ ${TOTAL}`;
        else stepLabel.textContent = 'ПОСЛЕДНИЙ ШАГ';
      }
      if (stepPct) stepPct.textContent = pct + '%';
    };

    const showStep = (n) => {
      steps.forEach((s) => {
        s.classList.toggle('hq-step--hidden', parseInt(s.dataset.step, 10) !== n);
      });
      currentStep = n;
      setProgress(n);
    };

    const updateSummary = () => {
      if (!summary) return;
      const pills = [];
      if (answers.service) pills.push(LABELS.service[answers.service] || answers.service);
      if (answers.house)   pills.push(LABELS.house[answers.house] || answers.house);
      if (answers.area)    pills.push(answers.area + ' м²');
      summary.innerHTML = pills.map((p) => `<span class="hq-summary__pill">${p}</span>`).join('');
    };

    // Option buttons
    quizForm.querySelectorAll('.hq-option').forEach((btn) => {
      btn.addEventListener('click', () => {
        const s = parseInt(btn.dataset.step, 10);
        const val = btn.dataset.value;
        quizForm.querySelectorAll(`.hq-option[data-step="${s}"]`).forEach((b) => b.classList.remove('hq-option--active'));
        btn.classList.add('hq-option--active');
        if (s === 1) {
          answers.service = val;
          if (inputService) inputService.value = val;
          if (quizImage) {
            const src = quizImage.getAttribute('data-img-' + val) || quizImage.getAttribute('data-img-default');
            if (src) quizImage.src = src;
          }
        }
        if (s === 2) { answers.house   = val; if (inputHouse)   inputHouse.value   = val; }
      });
    });

    // Next buttons
    quizForm.querySelectorAll('.hq-btn-next').forEach((btn) => {
      btn.addEventListener('click', () => {
        const goto = parseInt(btn.dataset.goto, 10);
        if (goto === 4) updateSummary();
        showStep(goto);
      });
    });

    // Slider ↔ number sync
    if (slider && numInput) {
      const syncSlider = () => {
        numInput.value = slider.value;
        answers.area = slider.value;
        if (inputArea) inputArea.value = slider.value;
      };
      const syncNum = () => {
        let v = Math.max(20, Math.min(600, parseInt(numInput.value, 10) || 20));
        numInput.value = v; slider.value = v;
        answers.area = String(v);
        if (inputArea) inputArea.value = String(v);
      };
      slider.addEventListener('input', syncSlider);
      numInput.addEventListener('input', syncNum);
      numInput.addEventListener('blur', syncNum);
      syncSlider();
    }

    // Back buttons (inline in footer)
    const back2 = document.getElementById('hq-back-2');
    const back3 = document.getElementById('hq-back-3');
    const back4 = document.getElementById('hq-back-4');
    if (back2) back2.addEventListener('click', () => showStep(1));
    if (back3) back3.addEventListener('click', () => showStep(2));
    if (back4) back4.addEventListener('click', () => showStep(3));

    showStep(1);
  }

  // --- Phone mask: +7 (999) 999-99-99 ---
  function applyPhoneMask(input) {
    input.addEventListener('focus', () => {
      if (!input.value) input.value = '+7 ';
    });
    input.addEventListener('input', (e) => {
      let digits = input.value.replace(/\D/g, '');
      if (digits.startsWith('8')) digits = '7' + digits.slice(1);
      if (!digits.startsWith('7')) digits = '7' + digits;
      digits = digits.slice(0, 11);

      let result = '+7';
      if (digits.length > 1) result += ' (' + digits.slice(1, 4);
      if (digits.length >= 4) result += ') ' + digits.slice(4, 7);
      if (digits.length >= 7) result += '-' + digits.slice(7, 9);
      if (digits.length >= 9) result += '-' + digits.slice(9, 11);

      input.value = result;
    });
    input.addEventListener('keydown', (e) => {
      if (e.key === 'Backspace' && input.value === '+7 ') {
        e.preventDefault();
      }
    });
    input.addEventListener('blur', () => {
      if (input.value === '+7 ' || input.value === '+7') input.value = '';
    });
  }

  document.querySelectorAll('input[type="tel"]').forEach(applyPhoneMask);
});
