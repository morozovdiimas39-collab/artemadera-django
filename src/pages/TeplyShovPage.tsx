import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import {
  Phone, ArrowDown, Shield, Award, Clock, Layers, ThermometerSun,
  ArrowRight, CheckCircle2, Wrench, Leaf, HelpCircle, ChevronDown, ChevronUp,
  Contact2, MapPin, Mail, FileCheck, Send, Images, Quote, Star, Droplets, Zap,
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
  { label: 'До и после', href: '#comparison' },
  { label: 'Этапы', href: '#process' },
  { label: 'Работы', href: '#gallery' },
  { label: 'Почему мы', href: '#whyus' },
  { label: 'FAQ', href: '#faq' },
  { label: 'Контакты', href: '#contact' },
];

const services = [
  { icon: Layers, title: 'Герметизация межвенцовых швов', description: 'Акриловые герметики для сруба и бруса. Заполняем швы, устраняем продувы и мостики холода.', price: 'от 350 ₽/м.п.', img: '/portfolio-2.jpg' },
  { icon: ThermometerSun, title: 'Утепление сруба', description: 'Теплый шов по всей коробке. Снижаем теплопотери и расходы на отопление.', price: 'от 400 ₽/м.п.', img: '/portfolio-1.jpg' },
  { icon: Wrench, title: 'Ремонт старых швов', description: 'Замена конопатки, восстановление разрушенных швов. Работаем с любыми типами домов.', price: 'от 300 ₽/м.п.', img: '/before.jpg' },
  { icon: Leaf, title: 'Эластичные материалы', description: 'Используем паропроницаемые составы. Шов двигается вместе с деревом — не трескается.', price: 'под ключ', img: '/after.jpg' },
];

const processSteps = [
  { num: '01', title: 'Осмотр и замер', description: 'Выезжаем на объект, считаем погонные метры швов и оцениваем состояние.' },
  { num: '02', title: 'Подготовка швов', description: 'Очистка, при необходимости конопатка или выравнивание. Шов готов к герметику.' },
  { num: '03', title: 'Нанесение герметика', description: 'Заполняем швы эластичным составом. Аккуратно, без подтёков.' },
  { num: '04', title: 'Контроль и сдача', description: 'Проверяем качество. Даём рекомендации по уходу. Гарантия на работы.' },
];

const reasons = [
  { icon: Award, title: 'Опыт 10+ лет', description: 'Сотни объектов в Москве и области.' },
  { icon: FileCheck, title: 'Сертифицированные материалы', description: 'Работаем с проверенными герметиками для дерева.' },
  { icon: Shield, title: 'Гарантия на работы', description: 'Письменная гарантия на герметизацию.' },
];

const faqItems = [
  { question: 'Что такое «тёплый шов»?', answer: 'Это герметизация межвенцовых швов эластичным составом. Убирает продувы, сохраняет паропроницаемость и двигается вместе с деревом при усадке.' },
  { question: 'Сколько служит?', answer: 'При правильной подготовке — 15–25 лет. Зависит от материала и условий.' },
  { question: 'Когда лучше делать?', answer: 'После основной усадки сруба (обычно через 1–2 года). Можно и в старом доме — для ремонта и утепления.' },
  { question: 'Как считается стоимость?', answer: 'По погонным метрам шва. Точная смета после замера на объекте.' },
];

const comparisonItems = [
  { aspect: 'Швы', before: 'Щели, продувы, конопатка выкрошилась', after: 'Ровный эластичный шов, без продувов', icon: Layers },
  { aspect: 'Тепло', before: 'Мостики холода, сквозняки', after: 'Тепло сохраняется, меньше расход на отопление', icon: ThermometerSun },
  { aspect: 'Внешний вид', before: 'Тёмные щели, неравномерность', after: 'Аккуратный шов в тон древесине', icon: Leaf },
];

const galleryItems = [
  { image: '/portfolio-2.jpg', title: 'Герметизация швов сруба', location: 'Новая Рига', description: 'Теплый шов по периметру дома.' },
  { image: '/portfolio-1.jpg', title: 'Обработка углов', location: 'Истра', description: 'Герметик в зонах стыков.' },
  { image: '/after.jpg', title: 'Сруб после герметизации', location: 'Рублёвка', description: 'Финишная отделка швов.' },
  { image: '/portfolio-3.jpg', title: 'Фасад с теплым швом', location: 'Одинцово', description: 'Полный цикл работ.' },
  { image: '/service-1.jpg', title: 'Подготовка швов', location: 'Московская область', description: 'Очистка перед нанесением.' },
  { image: '/service-2.jpg', title: 'Нанесение герметика', location: 'Подмосковье', description: 'Акриловый состав.' },
];

const stats = [
  { value: '300+', label: 'Объектов по швам' },
  { value: '10+', label: 'Лет опыта' },
  { value: '15–25', label: 'Лет срок службы' },
  { value: '3', label: 'Года гарантия' },
];

const materials = [
  { icon: Droplets, title: 'Акриловые герметики', description: 'Паропроницаемые, эластичные. Не трескаются при усадке.' },
  { icon: Zap, title: 'Уплотнительный шнур', description: 'Где нужно — ставим в полость шва перед герметиком.' },
  { icon: Leaf, title: 'Экологичность', description: 'Безопасные составы для жилых домов и бань.' },
];

const testimonials = [
  { name: 'Сергей М.', role: 'Сруб в Подмосковье', content: 'Сделали теплый шов по всему дому. Продувы исчезли, зимой заметно теплее. Рекомендую.', rating: 5 },
  { name: 'Ольга К.', role: 'Дом из бруса', content: 'Старая конопатка осыпалась. Заменили на герметизацию — аккуратно и надолго.', rating: 5 },
  { name: 'Андрей В.', role: 'Новая Рига', content: 'Приехали, посчитали метры, сделали за 3 дня. Цена как в смете.', rating: 5 },
];

function scrollToSection(href: string) {
  const el = document.querySelector(href);
  if (el) el.scrollIntoView({ behavior: 'smooth' });
}

export default function TeplyShovPage() {
  const [callbackOpen, setCallbackOpen] = useState(false);
  const [faqOpen, setFaqOpen] = useState<number | null>(0);
  const [formData, setFormData] = useState({ phone: '' });
  const [formSent, setFormSent] = useState(false);

  useEffect(() => {
    applySeo({
      title: 'Теплый шов для деревянного дома — ArteMadera',
      description: 'Герметизация межвенцовых швов по технологии теплый шов: снижение продувания, аккуратный вид и защита древесины.',
      path: '/teplyy-shov',
      image: '/teply-shov-hero.jpg',
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
        body: JSON.stringify({ phone: digits, type: 'teplyy-shov-contact' }),
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
        <div className="absolute inset-0 bg-cover bg-center bg-no-repeat" style={{ backgroundImage: 'url(/teply-shov-hero.jpg), url(/portfolio-2.jpg)' }}>
          <div className="absolute inset-0 bg-gradient-to-b from-black/70 via-black/50 to-background" />
        </div>
        <div className="relative z-10 container mx-auto px-4 sm:px-6 lg:px-8 pt-20 pb-16">
          <div className="max-w-4xl mx-auto text-center">
            <div className="mb-4 text-xs text-gray-300">
              <Link to="/" className="hover:text-amber-300">Главная</Link> / <span>Отделочные работы</span> / <span className="text-amber-200">Теплый шов</span>
            </div>
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-amber-500/20 border border-amber-500/30 mb-8">
              <Layers className="w-4 h-4 text-amber-400" />
              <span className="text-sm text-amber-200">Герметизация швов в Москве и области</span>
            </div>
            <h1 className="text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-bold mb-6 leading-tight">
              <span className="text-white">Теплый шов</span>
              <br />
              <span className="text-gradient">для деревянного дома</span>
            </h1>
            <p className="text-lg sm:text-xl text-gray-300 mb-10 max-w-2xl mx-auto">
              Герметизация межвенцовых швов. Устраняем продувы, сохраняем паропроницаемость. Гарантия на работы.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center mb-12">
              <button type="button" onClick={() => setCallbackOpen(true)} className="inline-flex items-center justify-center gap-2 bg-amber-600 hover:bg-amber-700 text-white px-8 py-4 rounded-xl text-lg font-medium premium-cta">
                <Phone className="w-5 h-5" /> Бесплатный расчёт
              </button>
              <button onClick={() => scrollToSection('#services')} className="inline-flex items-center justify-center border border-amber-500/50 text-amber-200 hover:bg-amber-500/10 px-8 py-4 rounded-xl text-lg">
                Услуги и цены
              </button>
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-6 max-w-3xl mx-auto">
              <div className="flex items-center justify-center gap-3 text-gray-300">
                <div className="w-12 h-12 rounded-xl bg-amber-500/20 flex items-center justify-center"><Shield className="w-6 h-6 text-amber-400" /></div>
                <div className="text-left"><div className="font-semibold text-white">Гарантия</div><div className="text-sm text-gray-400">На герметизацию</div></div>
              </div>
              <div className="flex items-center justify-center gap-3 text-gray-300">
                <div className="w-12 h-12 rounded-xl bg-amber-500/20 flex items-center justify-center"><Clock className="w-6 h-6 text-amber-400" /></div>
                <div className="text-left"><div className="font-semibold text-white">От 2 дней</div><div className="text-sm text-gray-400">Под ключ</div></div>
              </div>
              <div className="flex items-center justify-center gap-3 text-gray-300">
                <div className="w-12 h-12 rounded-xl bg-amber-500/20 flex items-center justify-center"><ThermometerSun className="w-6 h-6 text-amber-400" /></div>
                <div className="text-left"><div className="font-semibold text-white">Тепло и тихо</div><div className="text-sm text-gray-400">Без продувов</div></div>
              </div>
            </div>
          </div>
        </div>
        <div className="absolute bottom-8 left-1/2 -translate-x-1/2 animate-bounce">
          <ArrowDown className="w-6 h-6 text-amber-400" />
        </div>
      </section>

      <section id="services" className="py-20 lg:py-32 relative reveal-soft">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-3xl mx-auto mb-16">
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-amber-500/10 border border-amber-500/20 mb-6">
              <Layers className="w-4 h-4 text-amber-400" />
              <span className="text-sm text-amber-300">Услуги</span>
            </div>
            <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold mb-6">
              <span className="text-white">Что входит в </span>
              <span className="text-gradient">теплый шов</span>
            </h2>
            <p className="text-gray-400 text-lg">Герметизация, утепление и ремонт межвенцовых швов.</p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {services.map((s, i) => (
              <div key={i} className="group rounded-2xl border border-border/50 hover:border-amber-500/30 bg-card/50 overflow-hidden transition-all">
                <div className="relative h-40">
                  <img src={s.img} alt={s.title} className="absolute inset-0 w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" />
                  <div className="absolute inset-0 bg-gradient-to-t from-card to-transparent" />
                  <div className="absolute top-3 right-3 px-2 py-1 rounded-full bg-amber-500 text-white text-xs font-semibold">{s.price}</div>
                </div>
                <div className="p-5">
                  <div className="w-10 h-10 rounded-xl bg-amber-500/20 flex items-center justify-center mb-3">
                    <s.icon className="w-5 h-5 text-amber-400" />
                  </div>
                  <h3 className="text-lg font-bold text-white mb-2">{s.title}</h3>
                  <p className="text-gray-400 text-sm mb-3">{s.description}</p>
                  <button type="button" onClick={() => setCallbackOpen(true)} className="inline-flex items-center gap-2 text-amber-400 hover:text-amber-300 font-medium text-sm">
                    Заказать <ArrowRight className="w-4 h-4" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section id="comparison" className="py-20 lg:py-32 relative">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-3xl mx-auto mb-16">
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-amber-500/10 border border-amber-500/20 mb-6">
              <ArrowRight className="w-4 h-4 text-amber-400" />
              <span className="text-sm text-amber-300">До и после</span>
            </div>
            <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold mb-6">
              <span className="text-white">Как меняется дом </span>
              <span className="text-gradient">после теплого шва</span>
            </h2>
            <p className="text-gray-400 text-lg">Герметизация убирает продувы и сохраняет тепло.</p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-4xl mx-auto">
            {comparisonItems.map((item, i) => (
              <div key={i} className="p-6 rounded-2xl bg-card/30 border border-border/30">
                <div className="w-12 h-12 rounded-xl bg-amber-500/20 flex items-center justify-center mb-4">
                  <item.icon className="w-6 h-6 text-amber-400" />
                </div>
                <h4 className="text-lg font-bold text-white mb-3">{item.aspect}</h4>
                <div className="text-sm text-gray-500 mb-1 flex items-start gap-2">
                  <span className="text-red-400">До:</span> {item.before}
                </div>
                <div className="text-sm text-gray-300 flex items-start gap-2">
                  <CheckCircle2 className="w-4 h-4 text-green-400 flex-shrink-0 mt-0.5" /> {item.after}
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section id="process" className="py-20 lg:py-32 relative overflow-hidden">
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-amber-500/5 rounded-full blur-3xl" />
        <div className="container mx-auto px-4 sm:px-6 lg:px-8 relative">
          <div className="text-center max-w-3xl mx-auto mb-16">
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-amber-500/10 border border-amber-500/20 mb-6">
              <Clock className="w-4 h-4 text-amber-400" />
              <span className="text-sm text-amber-300">Как мы работаем</span>
            </div>
            <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold mb-6">
              <span className="text-white">Этапы </span>
              <span className="text-gradient">работы</span>
            </h2>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-5xl mx-auto">
            {processSteps.map((step) => (
              <div key={step.num} className="rounded-2xl border border-border/30 bg-card/50 p-6 sm:p-8">
                <span className="text-4xl font-bold text-amber-500 tabular-nums">{step.num}</span>
                <h3 className="text-xl font-bold text-white mt-3 mb-2">{step.title}</h3>
                <p className="text-gray-400 text-sm leading-relaxed">{step.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section id="whyus" className="py-20 lg:py-32 relative">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-3xl mx-auto mb-16">
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-amber-500/10 border border-amber-500/20 mb-6">
              <Award className="w-4 h-4 text-amber-400" />
              <span className="text-sm text-amber-300">Почему мы</span>
            </div>
            <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold mb-6">
              <span className="text-white">Почему выбирают </span>
              <span className="text-gradient">нас</span>
            </h2>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-4xl mx-auto">
            {reasons.map((r, i) => (
              <div key={i} className="p-6 rounded-2xl bg-card/30 border border-border/30 text-center">
                <div className="w-14 h-14 rounded-xl bg-amber-500/20 flex items-center justify-center mx-auto mb-4">
                  <r.icon className="w-7 h-7 text-amber-400" />
                </div>
                <h3 className="text-lg font-bold text-white mb-2">{r.title}</h3>
                <p className="text-gray-400 text-sm">{r.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section id="gallery" className="py-20 lg:py-32 relative">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-3xl mx-auto mb-16">
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-amber-500/10 border border-amber-500/20 mb-6">
              <Images className="w-4 h-4 text-amber-400" />
              <span className="text-sm text-amber-300">Наши работы</span>
            </div>
            <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold mb-6">
              <span className="text-white">Примеры </span>
              <span className="text-gradient">герметизации швов</span>
            </h2>
            <p className="text-gray-400 text-lg">Результаты работ на объектах в Москве и области.</p>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {galleryItems.map((item, i) => (
              <div key={i} className="group rounded-2xl overflow-hidden border border-border/30 hover:border-amber-500/30 transition-all">
                <div className="relative aspect-[4/3]">
                  <img src={item.image} alt={item.title} className="absolute inset-0 w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" />
                  <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity" />
                </div>
                <div className="p-4 bg-card/50">
                  <h3 className="font-bold text-white mb-1">{item.title}</h3>
                  <p className="text-gray-400 text-sm">{item.location}. {item.description}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section id="stats" className="py-16 lg:py-20 relative overflow-hidden">
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[500px] h-[500px] bg-amber-500/10 rounded-full blur-3xl" />
        <div className="container mx-auto px-4 sm:px-6 lg:px-8 relative">
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 max-w-4xl mx-auto">
            {stats.map((s, i) => (
              <div key={i} className="text-center p-6 rounded-2xl bg-gradient-to-br from-amber-500/15 to-amber-600/5 border border-amber-500/20">
                <div className="text-3xl sm:text-4xl font-bold text-gradient mb-1">{s.value}</div>
                <div className="text-sm text-gray-400">{s.label}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section id="materials" className="py-20 lg:py-32 relative">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-3xl mx-auto mb-16">
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-amber-500/10 border border-amber-500/20 mb-6">
              <Droplets className="w-4 h-4 text-amber-400" />
              <span className="text-sm text-amber-300">Материалы и технология</span>
            </div>
            <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold mb-6">
              <span className="text-white">Чем работаем </span>
              <span className="text-gradient">и как</span>
            </h2>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-4xl mx-auto">
            {materials.map((m, i) => (
              <div key={i} className="p-6 rounded-2xl bg-card/30 border border-border/30 flex items-start gap-4">
                <div className="w-14 h-14 rounded-xl bg-amber-500/20 flex items-center justify-center flex-shrink-0">
                  <m.icon className="w-7 h-7 text-amber-400" />
                </div>
                <div>
                  <h3 className="text-lg font-bold text-white mb-2">{m.title}</h3>
                  <p className="text-gray-400 text-sm">{m.description}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section id="testimonials" className="py-20 lg:py-32 relative">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-3xl mx-auto mb-16">
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-amber-500/10 border border-amber-500/20 mb-6">
              <Quote className="w-4 h-4 text-amber-400" />
              <span className="text-sm text-amber-300">Отзывы</span>
            </div>
            <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold mb-6">
              <span className="text-white">Что говорят </span>
              <span className="text-gradient">клиенты</span>
            </h2>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-5xl mx-auto">
            {testimonials.map((t, i) => (
              <div key={i} className="p-6 rounded-2xl bg-card/30 border border-border/30 hover:border-amber-500/20 transition-all">
                <Quote className="w-10 h-10 text-amber-500/30 mb-4" />
                <div className="flex gap-1 mb-4">
                  {[...Array(t.rating)].map((_, j) => (
                    <Star key={j} className="w-5 h-5 fill-amber-400 text-amber-400" />
                  ))}
                </div>
                <p className="text-gray-300 mb-4">&quot;{t.content}&quot;</p>
                <div className="font-semibold text-white">{t.name}</div>
                <div className="text-sm text-gray-500">{t.role}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section id="cta" className="py-20 lg:py-32 relative">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="max-w-4xl mx-auto rounded-2xl bg-amber-600/20 border-2 border-amber-500/40 p-8 sm:p-12 text-center">
            <h2 className="text-2xl sm:text-3xl font-bold text-white mb-4">Заказать бесплатный замер</h2>
            <p className="text-amber-200/90 mb-6 max-w-xl mx-auto">Выезжаем на объект, считаем погонные метры швов и называем точную стоимость. Без обязательств.</p>
            <button type="button" onClick={() => setCallbackOpen(true)} className="inline-flex items-center justify-center gap-2 bg-amber-600 hover:bg-amber-700 text-white px-8 py-4 rounded-xl text-lg font-medium premium-cta">
              <MapPin className="w-5 h-5" /> Вызвать замерщика
            </button>
          </div>
        </div>
      </section>

      <section id="faq" className="py-20 lg:py-32 relative">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-3xl mx-auto mb-12">
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-amber-500/10 border border-amber-500/20 mb-6">
              <HelpCircle className="w-4 h-4 text-amber-400" />
              <span className="text-sm text-amber-300">Вопросы и ответы</span>
            </div>
            <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold mb-6">
              <span className="text-white">Частые </span>
              <span className="text-gradient">вопросы</span>
            </h2>
          </div>
          <div className="max-w-3xl mx-auto space-y-4">
            {faqItems.map((item, i) => (
              <div key={i} className={`rounded-2xl border border-border/30 overflow-hidden transition-all ${faqOpen === i ? 'border-amber-500/30' : ''}`}>
                <button onClick={() => setFaqOpen(faqOpen === i ? null : i)} className="w-full p-5 flex items-start gap-4 text-left">
                  <div className={`w-10 h-10 rounded-lg flex items-center justify-center flex-shrink-0 ${faqOpen === i ? 'bg-amber-500/20' : 'bg-card/50'}`}>
                    <HelpCircle className={`w-5 h-5 ${faqOpen === i ? 'text-amber-400' : 'text-gray-500'}`} />
                  </div>
                  <h3 className="text-lg font-semibold text-white mt-1 flex-1">{item.question}</h3>
                  {faqOpen === i ? <ChevronUp className="w-5 h-5 text-amber-400" /> : <ChevronDown className="w-5 h-5 text-gray-500" />}
                </button>
                {faqOpen === i && (
                  <div className="px-5 pb-5 pl-[4.5rem]">
                    <p className="text-gray-400 leading-relaxed">{item.answer}</p>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      </section>

      <section id="contact" className="py-20 lg:py-32 relative">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-3xl mx-auto mb-16">
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-amber-500/10 border border-amber-500/20 mb-6">
              <Contact2 className="w-4 h-4 text-amber-400" />
              <span className="text-sm text-amber-300">Контакты</span>
            </div>
            <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold mb-6">
              <span className="text-white">Заказать </span>
              <span className="text-gradient">расчёт</span>
            </h2>
            <p className="text-gray-400 text-lg">Оставьте номер — перезвоним и рассчитаем стоимость по вашим метрам.</p>
          </div>
          <div className="max-w-md mx-auto rounded-2xl border-2 border-amber-500/30 bg-amber-500/10 p-6 sm:p-8">
            {formSent ? (
              <div className="py-10 text-center">
                <div className="w-16 h-16 rounded-full bg-green-500/30 flex items-center justify-center mx-auto mb-4">
                  <CheckCircle2 className="w-8 h-8 text-green-400" />
                </div>
                <h4 className="text-xl font-bold text-white mb-2">Спасибо!</h4>
                <p className="text-amber-200/90">Мы перезвоним в ближайшее время.</p>
              </div>
            ) : (
              <form onSubmit={handleSubmit} className="space-y-4">
                <label htmlFor="phone" className="block text-gray-300 text-sm mb-1.5">Телефон</label>
                <input id="phone" type="tel" placeholder="+7 (999) 999-99-99" value={formData.phone} onChange={(e) => setFormData({ phone: formatPhoneMask(e.target.value) })} className="w-full px-4 py-3 rounded-xl bg-background/80 border border-amber-500/30 focus:border-amber-500 focus:outline-none text-white placeholder:text-gray-500" />
                <button type="submit" disabled={getPhoneDigits(formData.phone).length < 11} className="w-full flex items-center justify-center gap-2 bg-amber-600 hover:bg-amber-500 disabled:opacity-50 text-white py-3.5 rounded-xl font-bold premium-cta">
                  <Send className="w-5 h-5" /> Отправить заявку
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
