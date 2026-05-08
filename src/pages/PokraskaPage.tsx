import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import {
  Phone, ArrowDown, Paintbrush, Shield, Clock, CheckCircle2,
  Contact2, MapPin, Mail, HelpCircle, ChevronDown, ChevronUp, FileCheck, ArrowRight,
} from 'lucide-react';
import { applySeo } from '../seo';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';
import CallbackModal from '../components/CallbackModal';
import { API_LEAD_URL, formatPhoneMask, getPhoneDigits } from '../lib/phone';

const PHONE = '+7 (495) 005-01-45';
const EMAIL = 'info@artemadera.ru';
const ADDRESS = 'Москва, ВДНХ, ул. Ярославская';

const navLinks = [
  { label: 'Цены', href: '#prices' },
  { label: 'Материалы', href: '#materials' },
  { label: 'Этапы', href: '#process' },
  { label: 'FAQ', href: '#faq' },
  { label: 'Контакты', href: '#contact' },
];

const priceItems = [
  { title: 'Антисептирование', price: 'от 60 ₽/м²' },
  { title: 'Грунтование', price: 'от 65 ₽/м²' },
  { title: 'Покраска', price: 'от 80 ₽/м²' },
  { title: 'Промежуточная шлифовка', price: 'от 80 ₽/м²' },
];

const services = [
  { title: 'Подготовка поверхности', description: 'Удаляем старые слои, выравниваем и готовим древесину под финиш.', img: '/service-1.jpg' },
  { title: 'Грунтование основы', description: 'Наносим грунт в 1-2 слоя для адгезии и защиты.', img: '/service-2.jpg' },
  { title: 'Покраска под ключ', description: 'Финишная покраска фасада и внутренних стен в выбранной системе.', img: '/service-3.jpg' },
  { title: 'Защитные составы', description: 'Антисептики, антипирены и составы от влаги/УФ.', img: '/portfolio-1.jpg' },
];

const materials = [
  { title: 'Акрилатные', description: 'Устойчивы к погоде и не мешают естественному воздухообмену древесины.' },
  { title: 'Масляные', description: 'Классика для дерева: глубокое проникновение и хорошая стойкость.' },
  { title: 'Алкидные', description: 'Водоотталкивающие покрытия, подходят для фасадных задач.' },
];

const processSteps = [
  { num: '01', title: 'Заявка', description: 'Вы оставляете заявку на выезд менеджера.' },
  { num: '02', title: 'Смета', description: 'Оцениваем объём и формируем прозрачную смету.' },
  { num: '03', title: 'Работы', description: 'Выполняем покраску в сроки по договору.' },
  { num: '04', title: 'Сдача', description: 'Сдаём объект и даём рекомендации по эксплуатации.' },
];

const faqItems = [
  { question: 'Нужно ли красить деревянный дом изнутри?', answer: 'Да, даже бесцветные составы защищают древесину от загрязнений и продлевают срок службы.' },
  { question: 'Можно ли покрасить старый дом?', answer: 'Да. Мы подбираем подходящую систему подготовки и красок под состояние поверхности.' },
  { question: 'Сложно ли сделать покраску самостоятельно?', answer: 'Без опыта сложно добиться ровного и долговечного результата. Важны подготовка, техника нанесения и правильные материалы.' },
  { question: 'Работаете в рассрочку?', answer: 'Да, работы можно согласовать в формате рассрочки.' },
];

function scrollToSection(href: string) {
  const el = document.querySelector(href);
  if (el) el.scrollIntoView({ behavior: 'smooth' });
}

export default function PokraskaPage() {
  const [callbackOpen, setCallbackOpen] = useState(false);
  const [faqOpen, setFaqOpen] = useState<number | null>(0);
  const [formData, setFormData] = useState({ phone: '' });
  const [formSent, setFormSent] = useState(false);

  useEffect(() => {
    applySeo({
      title: 'Покраска деревянного дома — ArteMadera',
      description: 'Профессиональная покраска деревянных домов: подбор системы, выкрасы, нанесение в 2-3 слоя и гарантия по договору.',
      path: '/pokraska',
      image: '/service-3.jpg',
    });
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const digits = getPhoneDigits(formData.phone);
    if (digits.length < 11) return;
    try {
      await fetch(API_LEAD_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ phone: digits, type: 'pokraska' }),
      });
      setFormSent(true);
      setFormData({ phone: '' });
      setTimeout(() => setFormSent(false), 3000);
    } catch {
      setFormSent(true);
      setTimeout(() => setFormSent(false), 3000);
    }
  };

  return (
    <div className="min-h-screen">
      <Navbar
        onCallbackClick={() => setCallbackOpen(true)}
        transparent
      />
      <CallbackModal open={callbackOpen} onClose={() => setCallbackOpen(false)} />

      <section id="hero" className="relative min-h-screen flex items-center justify-center overflow-hidden">
        <div className="absolute inset-0 bg-cover bg-center bg-no-repeat" style={{ backgroundImage: 'url(/service-3.jpg)' }}>
          <div className="absolute inset-0 bg-gradient-to-b from-black/70 via-black/50 to-background" />
        </div>
        <div className="relative z-10 container mx-auto px-4 sm:px-6 lg:px-8 pt-20 pb-16">
          <div className="max-w-4xl mx-auto text-center">
            <div className="mb-4 text-xs text-gray-300">
              <Link to="/" className="hover:text-amber-300">Главная</Link> / <span>Отделочные работы</span> / <span className="text-amber-200">Покраска</span>
            </div>
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-amber-500/20 border border-amber-500/30 mb-8">
              <Paintbrush className="w-4 h-4 text-amber-400" />
              <span className="text-sm text-amber-200">Покраска деревянных домов под ключ</span>
            </div>
            <h1 className="text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-bold mb-6 leading-tight">
              <span className="text-white">Покраска</span>
              <br />
              <span className="text-gradient">деревянного дома</span>
            </h1>
            <p className="text-lg sm:text-xl text-gray-300 mb-10 max-w-2xl mx-auto">
              Подготовка поверхности, грунтование и финишная покраска материалами ведущих производителей.
            </p>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-6 max-w-3xl mx-auto">
              <div className="flex items-center justify-center gap-3 text-gray-300">
                <div className="w-12 h-12 rounded-xl bg-amber-500/20 flex items-center justify-center"><Shield className="w-6 h-6 text-amber-400" /></div>
                <div className="text-left"><div className="font-semibold text-white">По договору</div><div className="text-sm text-gray-400">Фиксируем обязательства</div></div>
              </div>
              <div className="flex items-center justify-center gap-3 text-gray-300">
                <div className="w-12 h-12 rounded-xl bg-amber-500/20 flex items-center justify-center"><Clock className="w-6 h-6 text-amber-400" /></div>
                <div className="text-left"><div className="font-semibold text-white">В срок</div><div className="text-sm text-gray-400">По согласованному плану</div></div>
              </div>
              <div className="flex items-center justify-center gap-3 text-gray-300">
                <div className="w-12 h-12 rounded-xl bg-amber-500/20 flex items-center justify-center"><FileCheck className="w-6 h-6 text-amber-400" /></div>
                <div className="text-left"><div className="font-semibold text-white">Качественные ЛКМ</div><div className="text-sm text-gray-400">Проверенные бренды</div></div>
              </div>
            </div>
          </div>
        </div>
        <div className="absolute bottom-8 left-1/2 -translate-x-1/2 animate-bounce">
          <ArrowDown className="w-6 h-6 text-amber-400" />
        </div>
      </section>

      <section id="prices" className="py-20 lg:py-24">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-3xl mx-auto mb-12">
            <h2 className="text-3xl sm:text-4xl font-bold mb-4"><span className="text-white">Расценки на </span><span className="text-gradient">покраску</span></h2>
            <p className="text-gray-400">Цены со страницы услуги ArteMadera, точная смета после осмотра.</p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {priceItems.map((item, i) => (
              <div key={i} className="p-6 rounded-2xl bg-card/40 border border-border/30 text-center">
                <h3 className="text-lg font-semibold text-white mb-3">{item.title}</h3>
                <p className="text-2xl font-bold text-gradient">{item.price}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section id="services" className="py-20 lg:py-32 reveal-soft">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-3xl mx-auto mb-16">
            <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold mb-6"><span className="text-white">Что входит в </span><span className="text-gradient">покраску</span></h2>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {services.map((s, i) => (
              <div key={i} className="group rounded-2xl overflow-hidden border border-border/30 bg-card/30 hover:border-amber-500/30 transition-all">
                <div className="relative h-40">
                  <img src={s.img} alt={s.title} className="absolute inset-0 w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" />
                </div>
                <div className="p-5">
                  <h3 className="text-lg font-bold text-white mb-2">{s.title}</h3>
                  <p className="text-gray-400 text-sm">{s.description}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section id="materials" className="py-20 lg:py-32">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-3xl mx-auto mb-16">
            <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold mb-6"><span className="text-white">Типы </span><span className="text-gradient">покрытий</span></h2>
            <p className="text-gray-400">Используем акрилатные, масляные и алкидные составы под задачу объекта.</p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {materials.map((m, i) => (
              <div key={i} className="p-6 rounded-2xl bg-card/30 border border-border/30">
                <h3 className="text-lg font-bold text-white mb-3">{m.title}</h3>
                <p className="text-gray-400 text-sm">{m.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section id="process" className="py-20 lg:py-32">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-3xl mx-auto mb-16">
            <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold mb-6"><span className="text-white">Как мы </span><span className="text-gradient">работаем</span></h2>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {processSteps.map((step) => (
              <div key={step.num} className="p-6 rounded-2xl bg-card/30 border border-border/30">
                <div className="text-4xl font-bold text-amber-500">{step.num}</div>
                <h3 className="text-xl font-bold text-white mt-2 mb-2">{step.title}</h3>
                <p className="text-gray-400 text-sm">{step.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section id="faq" className="py-20 lg:py-32">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-3xl mx-auto mb-12">
            <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold mb-6"><span className="text-white">Частые </span><span className="text-gradient">вопросы</span></h2>
          </div>
          <div className="max-w-3xl mx-auto space-y-4">
            {faqItems.map((item, i) => (
              <div key={i} className={`rounded-2xl border border-border/30 overflow-hidden ${faqOpen === i ? 'border-amber-500/30' : ''}`}>
                <button onClick={() => setFaqOpen(faqOpen === i ? null : i)} className="w-full p-5 flex items-start gap-4 text-left">
                  <div className={`w-10 h-10 rounded-lg flex items-center justify-center flex-shrink-0 ${faqOpen === i ? 'bg-amber-500/20' : 'bg-card/50'}`}>
                    <HelpCircle className={`w-5 h-5 ${faqOpen === i ? 'text-amber-400' : 'text-gray-500'}`} />
                  </div>
                  <h3 className="text-lg font-semibold text-white flex-1">{item.question}</h3>
                  {faqOpen === i ? <ChevronUp className="w-5 h-5 text-amber-400" /> : <ChevronDown className="w-5 h-5 text-gray-500" />}
                </button>
                {faqOpen === i && <div className="px-5 pb-5 pl-[4.5rem]"><p className="text-gray-400">{item.answer}</p></div>}
              </div>
            ))}
          </div>
        </div>
      </section>

      <section id="contact" className="py-20 lg:py-32">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-3xl mx-auto mb-16">
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-amber-500/10 border border-amber-500/20 mb-6">
              <Contact2 className="w-4 h-4 text-amber-400" />
              <span className="text-sm text-amber-300">Контакты</span>
            </div>
            <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold mb-6"><span className="text-white">Рассчитать </span><span className="text-gradient">покраску</span></h2>
          </div>
          <div className="max-w-md mx-auto rounded-2xl border-2 border-amber-500/30 bg-amber-500/10 p-6 sm:p-8">
            {formSent ? (
              <div className="py-10 text-center">
                <div className="w-16 h-16 rounded-full bg-green-500/30 flex items-center justify-center mx-auto mb-4"><CheckCircle2 className="w-8 h-8 text-green-400" /></div>
                <h4 className="text-xl font-bold text-white mb-2">Спасибо!</h4>
                <p className="text-amber-200/90">Мы перезвоним в ближайшее время.</p>
              </div>
            ) : (
              <form onSubmit={handleSubmit} className="space-y-4">
                <label htmlFor="pokraska-phone" className="block text-gray-300 text-sm mb-1.5">Телефон</label>
                <input id="pokraska-phone" type="tel" placeholder="+7 (999) 999-99-99" value={formData.phone} onChange={(e) => setFormData({ phone: formatPhoneMask(e.target.value) })} className="w-full px-4 py-3 rounded-xl bg-background/80 border border-amber-500/30 focus:border-amber-500 focus:outline-none text-white placeholder:text-gray-500" />
                <button type="submit" disabled={getPhoneDigits(formData.phone).length < 11} className="w-full flex items-center justify-center gap-2 bg-amber-600 hover:bg-amber-500 disabled:opacity-50 text-white py-3.5 rounded-xl font-bold premium-cta">
                  <Phone className="w-5 h-5" /> Отправить заявку
                </button>
              </form>
            )}
          </div>
          <div className="mt-12 flex flex-wrap justify-center gap-6 text-gray-400 text-sm">
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
