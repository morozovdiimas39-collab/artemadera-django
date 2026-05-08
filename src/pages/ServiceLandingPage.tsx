import { useEffect, useMemo, useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Phone, CheckCircle2, Mail, MapPin, HelpCircle, ChevronDown, ChevronUp } from 'lucide-react';
import { SERVICE_LANDING_CONTENT } from '../content/serviceLandingContent';
import { applySeo } from '../seo';
import Navbar from '../components/Navbar';
import CallbackModal from '../components/CallbackModal';
import Footer from '../components/Footer';

import { API_LEAD_URL, formatPhoneMask, getPhoneDigits } from '../lib/phone';

const PHONE = '+7 (495) 005-01-45';
const EMAIL = 'info@artemadera.ru';
const ADDRESS = 'Москва, ВДНХ, ул. Ярославская';

export default function ServiceLandingPage() {
  const { pathname } = useLocation();
  const content = useMemo(() => SERVICE_LANDING_CONTENT.find((p) => p.path === pathname), [pathname]);
  const [phone, setPhone] = useState('');
  const [sent, setSent] = useState(false);
  const [faqOpen, setFaqOpen] = useState<number | null>(0);
  const [callbackOpen, setCallbackOpen] = useState(false);

  if (!content) return null;

  const groupLabel = pathname.startsWith('/proizvodstvo')
    ? 'Производство'
    : pathname.startsWith('/obsada')
      ? 'Обсада'
      : pathname.startsWith('/otdelka')
        ? 'Отделочные работы'
        : pathname === '/kryshi'
          ? 'Крыши'
          : pathname === '/injeneriya'
            ? 'Инженерия'
            : 'Раздел';

  useEffect(() => {
    applySeo({
      title: `${content.title} — ArteMadera`,
      description: content.subtitle,
      path: content.path,
      image: content.heroImage,
    });
  }, [content]);

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    const digits = getPhoneDigits(phone);
    if (digits.length < 11) return;
    try {
      await fetch(API_LEAD_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ phone: digits, type: `service:${content.path}` }),
      });
      setSent(true);
      setPhone('');
      setTimeout(() => setSent(false), 3000);
    } catch {
      setSent(true);
      setTimeout(() => setSent(false), 3000);
    }
  };

  return (
    <div className="min-h-screen">
      <Navbar onCallbackClick={() => setCallbackOpen(true)} transparent />
      <CallbackModal open={callbackOpen} onClose={() => setCallbackOpen(false)} />

      <section className="relative min-h-[70vh] flex items-center justify-center overflow-hidden">
        <div className="absolute inset-0 bg-cover bg-center bg-no-repeat" style={{ backgroundImage: `url(${content.heroImage})` }}>
          <div className="absolute inset-0 bg-gradient-to-b from-black/70 via-black/50 to-background" />
        </div>
        <div className="relative z-10 container mx-auto px-4 sm:px-6 lg:px-8 pt-28 pb-16 text-center">
          <Link to="/" className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white/10 border border-white/20 mb-8 text-sm text-white/90">
            ← На главную
          </Link>
          <div className="mb-3 text-xs text-gray-300">
            <Link to="/" className="hover:text-amber-300">Главная</Link> / <span>{groupLabel}</span> / <span className="text-amber-200">{content.title}</span>
          </div>
          <div className="mb-4">
            <span className="px-3 py-1 rounded-full bg-amber-500/25 border border-amber-500/35 text-amber-100 text-xs uppercase tracking-wide">{groupLabel}</span>
          </div>
          <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold mb-5 text-white">{content.title}</h1>
          <p className="text-lg text-gray-200 max-w-3xl mx-auto">{content.subtitle}</p>
          <div className="mt-8 flex flex-wrap justify-center gap-3">
            {content.badges.map((b, i) => (
              <span key={i} className="px-4 py-2 rounded-full bg-amber-500/20 border border-amber-500/30 text-amber-100 text-sm">{b}</span>
            ))}
          </div>
        </div>
      </section>

      <section className="py-20 lg:py-24 reveal-soft">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-2xl sm:text-3xl font-bold text-white mb-6">Цены</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-16">
            {content.prices.map((p, i) => (
              <div key={i} className="p-5 rounded-xl bg-amber-500/10 border border-amber-500/30 hover-lift reveal-up">
                <p className="text-gray-200 text-sm mb-1">{p.label}</p>
                <p className="text-amber-300 text-2xl font-bold">{p.value}</p>
              </div>
            ))}
          </div>

          <h2 className="text-2xl sm:text-3xl font-bold text-white mb-6">Что входит</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-16">
            {content.features.map((f, i) => (
              <div key={i} className="group rounded-2xl overflow-hidden border border-border/30 bg-card/30">
                <div className="relative h-40">
                  <img src={f.image} alt={f.title} className="absolute inset-0 w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" />
                </div>
                <div className="p-5">
                  <h3 className="text-lg font-bold text-white mb-2">{f.title}</h3>
                  <p className="text-gray-400 text-sm">{f.text}</p>
                </div>
              </div>
            ))}
          </div>

          <h2 className="text-2xl sm:text-3xl font-bold text-white mb-6">Этапы работ</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-16">
            {content.process.map((s) => (
              <div key={s.num} className="p-6 rounded-2xl bg-card/30 border border-border/30 hover-lift reveal-up">
                <div className="text-4xl font-bold text-amber-500">{s.num}</div>
                <h3 className="text-xl font-bold text-white mt-2 mb-2">{s.title}</h3>
                <p className="text-gray-400 text-sm">{s.text}</p>
              </div>
            ))}
          </div>

          <h2 className="text-2xl sm:text-3xl font-bold text-white mb-6">FAQ</h2>
          <div className="max-w-3xl mb-16 space-y-4">
            {content.faq.map((item, i) => (
              <div key={i} className={`rounded-2xl border border-border/30 overflow-hidden ${faqOpen === i ? 'border-amber-500/30' : ''}`}>
                <button onClick={() => setFaqOpen(faqOpen === i ? null : i)} className="w-full p-5 flex items-start gap-4 text-left">
                  <div className={`w-10 h-10 rounded-lg flex items-center justify-center flex-shrink-0 ${faqOpen === i ? 'bg-amber-500/20' : 'bg-card/50'}`}>
                    <HelpCircle className={`w-5 h-5 ${faqOpen === i ? 'text-amber-400' : 'text-gray-500'}`} />
                  </div>
                  <h3 className="text-lg font-semibold text-white flex-1">{item.q}</h3>
                  {faqOpen === i ? <ChevronUp className="w-5 h-5 text-amber-400" /> : <ChevronDown className="w-5 h-5 text-gray-500" />}
                </button>
                {faqOpen === i && <div className="px-5 pb-5 pl-[4.5rem]"><p className="text-gray-400">{item.a}</p></div>}
              </div>
            ))}
          </div>

          <div id="service-contact" className="max-w-md mx-auto rounded-2xl border-2 border-amber-500/30 bg-amber-500/10 p-6 sm:p-8">
            {sent ? (
              <div className="py-8 text-center">
                <div className="w-14 h-14 rounded-full bg-green-500/30 flex items-center justify-center mx-auto mb-3"><CheckCircle2 className="w-7 h-7 text-green-400" /></div>
                <h4 className="text-xl font-bold text-white mb-1">Заявка отправлена</h4>
                <p className="text-amber-200/90">Мы перезвоним в ближайшее время.</p>
              </div>
            ) : (
              <form onSubmit={submit} className="space-y-4">
                <label htmlFor="service-phone" className="block text-gray-300 text-sm">Телефон</label>
                <input id="service-phone" type="tel" placeholder="+7 (999) 999-99-99" value={phone} onChange={(e) => setPhone(formatPhoneMask(e.target.value))} className="w-full px-4 py-3 rounded-xl bg-background/80 border border-amber-500/30 focus:border-amber-500 focus:outline-none text-white placeholder:text-gray-500" />
                <button type="submit" disabled={getPhoneDigits(phone).length < 11} className="w-full flex items-center justify-center gap-2 bg-amber-600 hover:bg-amber-500 disabled:opacity-50 text-white py-3.5 rounded-xl font-bold premium-cta">
                  <Phone className="w-5 h-5" /> Получить консультацию
                </button>
              </form>
            )}
          </div>

          <div className="mt-10 flex flex-wrap justify-center gap-6 text-gray-400 text-sm">
            <a href={`tel:${PHONE.replace(/\s/g, '')}`} className="flex items-center gap-2 hover:text-amber-400"><Phone className="w-5 h-5" /> {PHONE}</a>
            <a href={`mailto:${EMAIL}`} className="flex items-center gap-2 hover:text-amber-400"><Mail className="w-5 h-5" /> {EMAIL}</a>
            <span className="flex items-center gap-2"><MapPin className="w-5 h-5" /> {ADDRESS}</span>
          </div>
        </div>
      </section>
      <Footer />
    </div>
  );
}
