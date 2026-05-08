import { useEffect, useMemo, useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Phone, Mail, MapPin, CheckCircle2 } from 'lucide-react';
import { ARTEMADERA_PAGES } from '../content/artemaderaStructure';
import { applySeo } from '../seo';
import Navbar from '../components/Navbar';
import CallbackModal from '../components/CallbackModal';
import Footer from '../components/Footer';

import { API_LEAD_URL, formatPhoneMask, getPhoneDigits } from '../lib/phone';

const PHONE = '+7 (495) 005-01-45';
const EMAIL = 'info@artemadera.ru';
const ADDRESS = 'Москва, ВДНХ, ул. Ярославская';

export default function ArtemaderaSectionPage() {
  const { pathname } = useLocation();
  const page = useMemo(() => ARTEMADERA_PAGES.find((p) => p.path === pathname), [pathname]);
  const related = useMemo(
    () => ARTEMADERA_PAGES.filter((p) => p.category === page?.category && p.path !== page?.path).slice(0, 6),
    [page],
  );

  const [phone, setPhone] = useState('');
  const [sent, setSent] = useState(false);
  const [callbackOpen, setCallbackOpen] = useState(false);

  if (!page) return null;

  useEffect(() => {
    applySeo({
      title: `${page.title} — ArteMadera`,
      description: page.subtitle,
      path: page.path,
      image: page.heroImage || '/hero-bg.jpg',
    });
  }, [page]);

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    const digits = getPhoneDigits(phone);
    if (digits.length < 11) return;
    try {
      await fetch(API_LEAD_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ phone: digits, type: `page:${page.path}` }),
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
        <div
          className="absolute inset-0 bg-cover bg-center bg-no-repeat"
          style={{ backgroundImage: `url(${page.heroImage || '/hero-bg.jpg'})` }}
        >
          <div className="absolute inset-0 bg-gradient-to-b from-black/70 via-black/50 to-background" />
        </div>
        <div className="relative z-10 container mx-auto px-4 sm:px-6 lg:px-8 pt-20 pb-16 text-center">
          <Link to="/" className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white/10 border border-white/20 mb-8 text-sm text-white/90">
            ← На главную
          </Link>
          <div className="mb-3 text-xs text-gray-300">
            <Link to="/" className="hover:text-amber-300">Главная</Link> / <span>{page.category || 'Раздел'}</span> / <span className="text-amber-200">{page.title}</span>
          </div>
          <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold mb-5">
            <span className="text-white">{page.title}</span>
          </h1>
          <p className="text-lg text-gray-200 max-w-3xl mx-auto">{page.subtitle}</p>
        </div>
      </section>

      <section className="py-20 lg:py-24 reveal-soft">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-14">
            {page.bullets.map((b, i) => (
              <div key={i} className="p-6 rounded-2xl bg-card/40 border border-border/30 hover-lift reveal-up">
                <div className="flex items-start gap-3">
                  <CheckCircle2 className="w-5 h-5 text-amber-400 flex-shrink-0 mt-0.5" />
                  <p className="text-gray-200">{b}</p>
                </div>
              </div>
            ))}
          </div>

          {page.priceHints && page.priceHints.length > 0 && (
            <div className="mb-14">
              <h2 className="text-2xl sm:text-3xl font-bold text-white mb-6">Ориентировочные цены</h2>
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                {page.priceHints.map((p, i) => (
                  <div key={i} className="p-4 rounded-xl bg-amber-500/10 border border-amber-500/30 text-amber-200 hover-lift reveal-up">
                    {p}
                  </div>
                ))}
              </div>
            </div>
          )}

          <div className="mb-14">
            <h2 className="text-2xl sm:text-3xl font-bold text-white mb-6">Разделы сайта</h2>
            <div className="flex flex-wrap gap-3">
              <Link to="/" className="px-4 py-2 rounded-full border border-border/40 bg-card/30 text-gray-200 hover:border-amber-500/40 hover:text-amber-300 transition-colors">
                Главная
              </Link>
              <Link to="/pokraska" className="px-4 py-2 rounded-full border border-border/40 bg-card/30 text-gray-200 hover:border-amber-500/40 hover:text-amber-300 transition-colors">
                Покраска
              </Link>
              <Link to="/teplyy-shov" className="px-4 py-2 rounded-full border border-border/40 bg-card/30 text-gray-200 hover:border-amber-500/40 hover:text-amber-300 transition-colors">
                Теплый шов
              </Link>
              {related.map((r) => (
                <Link
                  key={r.path}
                  to={r.path}
                  className="px-4 py-2 rounded-full border border-border/40 bg-card/30 text-gray-200 hover:border-amber-500/40 hover:text-amber-300 transition-colors"
                >
                  {r.title}
                </Link>
              ))}
            </div>
          </div>

          <div className="max-w-md mx-auto rounded-2xl border-2 border-amber-500/30 bg-amber-500/10 p-6 sm:p-8">
            {sent ? (
              <div className="py-8 text-center">
                <div className="w-14 h-14 rounded-full bg-green-500/30 flex items-center justify-center mx-auto mb-3">
                  <CheckCircle2 className="w-7 h-7 text-green-400" />
                </div>
                <h4 className="text-xl font-bold text-white mb-1">Заявка отправлена</h4>
                <p className="text-amber-200/90">Мы перезвоним в ближайшее время.</p>
              </div>
            ) : (
              <form onSubmit={submit} className="space-y-4">
                <label htmlFor="page-phone" className="block text-gray-300 text-sm">Телефон</label>
                <input
                  id="page-phone"
                  type="tel"
                  placeholder="+7 (999) 999-99-99"
                  value={phone}
                  onChange={(e) => setPhone(formatPhoneMask(e.target.value))}
                  className="w-full px-4 py-3 rounded-xl bg-background/80 border border-amber-500/30 focus:border-amber-500 focus:outline-none text-white placeholder:text-gray-500"
                />
                <button type="submit" disabled={getPhoneDigits(phone).length < 11} className="w-full flex items-center justify-center gap-2 bg-amber-600 hover:bg-amber-500 disabled:opacity-50 text-white py-3.5 rounded-xl font-bold">
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
