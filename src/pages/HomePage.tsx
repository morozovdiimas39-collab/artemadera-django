import { useState, useEffect } from 'react';
import {
  Phone, Menu, X, ArrowDown, Shield, Award, Clock, Settings, Sparkles, Paintbrush,
  ArrowRight, ChevronRight, ChevronLeft, CheckCircle2, Home, Ruler, Calendar, Calculator,
  ArrowRightLeft, Eye, Droplets, Layers, XCircle, Send,
  Contact2, MapPin, Mail, Users, Wrench, ThumbsUp, Leaf, BadgeCheck, Zap, Star, Heart,
  HelpCircle, ChevronDown, ChevronUp, MessageCircleQuestion, MessageSquare,
  Calendar as CalIcon, MapPin as MapPinIcon, TrendingUp, Images, Maximize2,
  FileCheck, Stamp, Quote, Rocket,
} from 'lucide-react';
import Navbar from '../components/Navbar';
import CallbackModal from '../components/CallbackModal';

const PHONE = '+7 (495) 005-01-45';
const EMAIL = 'info@artemadera.ru';
const ADDRESS = 'Москва, ВДНХ, ул. Ярославская';
const API_LEAD_URL = '/api/lead';

/** Маска телефона: +7 (999) 999-99-99. Возвращает отформатированную строку для инпута. */
function formatPhoneMask(value: string): string {
  const digits = value.replace(/\D/g, '');
  const d = digits.startsWith('7') || digits.startsWith('8') ? digits.slice(1) : digits;
  const s = d.slice(0, 10);
  if (s.length === 0) return '';
  if (s.length <= 3) return `+7 (${s}`;
  if (s.length <= 6) return `+7 (${s.slice(0, 3)}) ${s.slice(3)}`;
  return `+7 (${s.slice(0, 3)}) ${s.slice(3, 6)}-${s.slice(6, 8)}-${s.slice(8, 10)}`;
}

/** Из маски в цифры для API: 79991234567 */
function getPhoneDigits(masked: string): string {
  const digits = masked.replace(/\D/g, '');
  if (digits.startsWith('8')) return '7' + digits.slice(1, 11);
  if (digits.startsWith('7')) return digits.slice(0, 11);
  return '7' + digits.slice(0, 10);
}

const navLinks = [
  { label: 'Услуги', href: '#services' },
  { label: 'Калькулятор', href: '#quiz' },
  { label: 'Этапы', href: '#process' },
  { label: 'До/После', href: '#comparison' },
  { label: 'Почему мы', href: '#whyus' },
  { label: 'Работы', href: '#recent-projects' },
  { label: 'Гарантии', href: '#certificates' },
  { label: 'FAQ', href: '#faq' },
  { label: 'Отзывы', href: '#testimonials' },
  { label: 'Контакты', href: '#contact' },
];

const services = [
  { icon: Settings, title: 'Шлифовка срубов', description: 'Профессиональная шлифовка бревенчатых и брусовых домов.', price: 'от 1 200 ₽/м²', img: '/service-1.jpg' },
  { icon: Sparkles, title: 'Консьержная шлифовка', description: 'Тонкая шлифовка для финишной обработки древесины.', price: 'от 800 ₽/м²', img: '/service-2.jpg' },
  { icon: Paintbrush, title: 'Покраска и пропитка', description: 'Нанесение масел, лаков и антисептиков.', price: 'от 600 ₽/м²', img: '/service-3.jpg' },
  { icon: Shield, title: 'Антисептирование', description: 'Защита от гнили, плесени и насекомых.', price: 'от 400 ₽/м²', img: '/portfolio-1.jpg' },
  { icon: Layers, title: 'Ремонт швов', description: 'Конопатка и герметизация швов.', price: 'от 350 ₽/м.п.', img: '/portfolio-2.jpg' },
  { icon: Droplets, title: 'Мытьё фасада', description: 'Очистка деревянных стен.', price: 'от 200 ₽/м²', img: '/portfolio-3.jpg' },
];

const quizSteps = [
  {
    id: 1, question: 'Какой тип дома у вас?', icon: Home, multiple: false, options: [
      { value: 'srub', label: 'Сруб (бревенчатый)', price: 1200, img: '/quiz/quiz_srub_1776809774832.png', fallback: '/before.jpg' },
      { value: 'brus', label: 'Дом из бруса', price: 1000, img: '/quiz/quiz_brus_1776809793588.png', fallback: '/after.jpg' },
      { value: 'kleyeny', label: 'Клееный брус', price: 900, img: '/quiz/quiz_kleyeny_1776809809396.png', fallback: '/portfolio-1.jpg' },
      { value: 'banja', label: 'Баня/сауна', price: 1100, img: '/quiz/quiz_banja_modern_1776810582042.png', fallback: '/portfolio-2.jpg' },
    ]
  },
  {
    id: 2, question: 'Какая примерная площадь?', icon: Ruler, multiple: false, stepImg: '/quiz/quiz_area_1776809914472.png', options: [
      { value: 'small', label: 'До 50 м²', multiplier: 1 },
      { value: 'medium', label: '50-100 м²', multiplier: 1 },
      { value: 'large', label: '100-150 м²', multiplier: 0.95 },
      { value: 'xlarge', label: 'Более 150 м²', multiplier: 0.9 },
    ]
  },
  {
    id: 3, question: 'Какие работы нужны?', icon: Paintbrush, multiple: true, options: [
      { value: 'shlifovka', label: 'Шлифовка', price: 0, img: '/quiz/quiz_works_1776809930737.png', fallback: '/service-1.jpg' },
      { value: 'pokraska', label: 'Покраска/пропитка', price: 600, img: '/quiz/quiz_works_1776809930737.png', fallback: '/service-3.jpg' },
      { value: 'antiseptik', label: 'Антисептирование', price: 400, img: '/quiz/quiz_works_1776809930737.png', fallback: '/portfolio-1.jpg' },
      { value: 'konopatka', label: 'Конопатка швов', price: 350, img: '/quiz/quiz_works_1776809930737.png', fallback: '/portfolio-2.jpg' },
    ]
  },
  {
    id: 4, question: 'Когда планируете начать?', icon: Calendar, multiple: false, stepImg: '/quiz/quiz_time_1776809945393.png', options: [
      { value: 'asap', label: 'Как можно скорее' },
      { value: 'week', label: 'В течение недели' },
      { value: 'month', label: 'В течение месяца' },
      { value: 'later', label: 'Пока присматриваюсь' },
    ]
  },
];

const processSteps = [
  { num: '01', title: 'Замер и выкрас', description: 'Приезжаем на объект, считаем точный метраж и делаем бесплатные пробные выкрасы прямо на вашем доме.' },
  { num: '02', title: 'Без проживания', description: 'Работаем мобильными бригадами. Вам не нужно организовывать быт и спальные места — мы полностью автономны и мобильны.' },
  { num: '03', title: 'Честная цена', description: 'Работаем по фиксированной смете. Стоимость прописывается в договоре до начала работ и не меняется ни на рубль в процессе сотрудничества.' },
  { num: '04', title: 'Многоуровневый контроль', description: 'Проверяем качество на каждом этапе работ. Это исключает брак и гарантирует результат.' },
];

const comparisons = [
  { aspect: 'Внешний вид', before: 'Потемневшая древесина с мхом', after: 'Яркая, золотистая древесина', icon: Eye },
  { aspect: 'Защита', before: 'Нет защиты', after: 'Защита на 5-10 лет', icon: Shield },
  { aspect: 'Долговечность', before: 'Трещины и разрушение', after: 'Срок службы +15-20 лет', icon: Clock },
  { aspect: 'Уход', before: 'Постоянный ремонт', after: 'Минимальный уход', icon: Sparkles },
];

const problems = ['Потемнение древесины', 'Мох и плесень', 'Трещины', 'Вредители', 'Потеря теплоизоляции', 'Непрезентабельный вид'];
const solutions = ['Глубокая шлифовка', 'Антисептирование', 'Конопатка и герметизация', 'Защитное покрытие', 'Восстановление теплоизоляции', 'Гладкая поверхность'];

const houseTypes = [
  { value: 'srub', label: 'Сруб (бревенчатый)', price: 1200, icon: Home },
  { value: 'brus', label: 'Дом из бруса', price: 1000, icon: Home },
  { value: 'kleyeny', label: 'Клееный брус', price: 900, icon: Home },
  { value: 'banja', label: 'Баня/сауна', price: 1100, icon: Droplets },
];

const additionalServices = [
  { id: 'pokraska', label: 'Покраска/пропитка', price: 600, icon: Paintbrush },
  { id: 'antiseptik', label: 'Антисептирование', price: 400, icon: Droplets },
  { id: 'konopatka', label: 'Конопатка швов', price: 350, icon: Layers },
  { id: 'gruntovka', label: 'Грунтовка', price: 200, icon: Layers },
];

const reasons = [
  { icon: Users, title: 'Опытная команда', stat: '15+', statLabel: 'специалистов', description: 'Мастера с опытом от 7 лет.', features: ['Сертифицированные', 'Обучение', 'Отбор'], img: '/whyus_team_1776809465370.png' },
  { icon: Wrench, title: 'Оборудование', stat: '50+', statLabel: 'единиц', description: 'Профессиональная техника.', features: ['Festool', 'Hilti', 'Bosch'], img: '/whyus_tools_1776809484018.png' },
  { icon: Clock, title: 'Точные сроки', stat: '99%', statLabel: 'в срок', description: 'Работаем по графику.', features: ['План работ', 'Без выходных'], img: '/whyus_time_1776809500549.png' },
  { icon: Shield, title: 'Гарантия', stat: '3', statLabel: 'года', description: 'Письменная гарантия.', features: ['Гарантия', 'Ремонт', 'Страхование'], img: '/whyus_quality_1776809515137.png' },
  { icon: ThumbsUp, title: 'Честные цены', stat: '0', statLabel: 'скрытых платежей', description: 'Цена в договоре.', features: ['Смета', 'Фикс цена'], img: '/whyus_price_1776809529581.png' },
  { icon: Leaf, title: 'Экологичность', stat: '100%', statLabel: 'безопасность', description: 'Экологичные материалы.', features: ['Сертификаты', 'Безопасно'], img: '/whyus_eco_1776809551533.png' },
];

const achievements = [
  { value: '500+', label: 'Проектов' },
  { value: '10+', label: 'Лет на рынке' },
  { value: '98%', label: 'Довольных клиентов' },
  { value: '4.9', label: 'Рейтинг' },
];

const projects = [
  { id: 1, title: 'Реставрация сруба', location: 'Новая Рига', date: 'Декабрь 2024', area: 120, duration: '5 дней', services: ['Шлифовка', 'Конопатка', 'Покраска'], beforeState: 'Потемневший сруб', afterState: 'Золотистый цвет', testimonial: 'Дом преобразился!', client: 'Александр П.', featured: true, img: '/before.jpg' },
  { id: 2, title: 'Дом из бруса', location: 'Рублёвка', date: 'Ноябрь 2024', area: 200, duration: '4 дня', services: ['Консьержная шлифовка', 'Масло'], beforeState: 'Финишная обработка', afterState: 'Идеально гладко', testimonial: 'Профессионалы!', client: 'Дмитрий В.', featured: false, img: '/after.jpg' },
];

const advantages = [
  { icon: Zap, title: 'Современное оборудование', description: 'Hilti, Festool, Bosch.' },
  { icon: Users, title: 'Опытные мастера', description: 'Специалисты с опытом от 7 лет.' },
  { icon: Wrench, title: 'Материалы', description: 'Tikkurila, Teknos, Belinka, Osmo.' },
  { icon: Leaf, title: 'Экологичность', description: 'Безопасные материалы.' },
  { icon: BadgeCheck, title: 'Гарантия', description: '3 года на все работы.' },
  { icon: CheckCircle2, title: 'Чистота', description: 'Убираем после работ.' },
];

const stats = [{ value: '500+', label: 'Проектов' }, { value: '10+', label: 'Лет' }, { value: '50+', label: 'Клиентов' }, { value: '98%', label: 'Отзывов' }];

const guarantees = [
  { title: 'Гарантия на работы', period: '3 года', description: 'Устранение дефектов бесплатно.', features: ['Шлифовка', 'Покраска', 'Конопатка'] },
  { title: 'Гарантия на материалы', period: '5 лет', description: 'От производителей.', features: ['Tikkurila', 'Teknos', 'Belinka'] },
  { title: 'Сервис', period: '10 лет', description: 'Скидки на повторные работы.', features: ['Скидка 15%', 'Приоритет'] },
];

const certificates = [
  { icon: FileCheck, title: 'Сертификаты', description: 'Материалы с сертификатами.' },
  { icon: Shield, title: 'Страхование', description: 'Имущество под защитой.' },
  { icon: BadgeCheck, title: 'СРО', description: 'Член СРО.' },
  { icon: Award, title: 'Награды', description: 'Лауреат премий.' },
];

const partners = ['Tikkurila', 'Teknos', 'Belinka', 'Osmo', 'Pinotex', 'Dulux'];

const portfolioItems = [
  { image: '/after.jpg', title: 'Деревянный дом', location: 'Рублёвка', year: '2024', description: 'Финишная шлифовка и масло.' },
  { image: '/portfolio-1.jpg', title: 'Сруб с террасой', location: 'Истра', year: '2024', description: 'Полный комплекс реставрации.' },
  { image: '/portfolio-2.jpg', title: 'Фасад бани', location: 'Одинцово', year: '2023', description: 'Шлифовка фасада.' },
  { image: '/portfolio-3.jpg', title: 'Деревянная усадьба', location: 'Дмитров', year: '2023', description: 'Комплексные работы.' },
  { image: '/service-1.jpg', title: 'Гостевой дом', location: 'Новая Рига', year: '2023', description: 'Шлифовка и покраска.' },
  { image: '/service-2.jpg', title: 'Охотничий домик', location: 'Звенигород', year: '2022', description: 'Глубокая реставрация.' },
  { image: '/service-3.jpg', title: 'Коттедж', location: 'Барвиха', year: '2024', description: 'Отбеливание и масло.' },
  { image: '/hero-bg.jpg', title: 'Бревенчатый дом', location: 'Чехов', year: '2024', description: 'Снятие старого лака.' },
  { image: '/before.jpg', title: 'Старый сруб', location: 'Клин', year: '2023', description: 'До реставрации.' },
];

const faqItems = [
  { question: 'Сколько времени занимает шлифовка?', answer: 'Небольшой дом 2-3 дня, средний 3-5 дней, большой 5-7 дней. Точные сроки после осмотра.', category: 'Сроки' },
  { question: 'Какая гарантия?', answer: '3 года на все работы. Устранение дефектов бесплатно.', category: 'Гарантия' },
  { question: 'Нужно ли выезжать из дома?', answer: 'Нет. Используем пылесосы с HEPA. Работаем поэтапно.', category: 'Процесс' },
  { question: 'Масло, лак или антисептик?', answer: 'Масло — текстура, лак — прочность, антисептик — базовая защита.', category: 'Материалы' },
  { question: 'Как часто шлифовать?', answer: 'Полная шлифовка раз в 10-15 лет. Освежение каждые 3-5 лет.', category: 'Уход' },
  { question: 'Работаете зимой?', answer: 'Да. Зимой при температуре выше -10°C.', category: 'Сезонность' },
];

const testimonials = [
  { name: 'Александр П.', role: 'Новая Рига', content: 'Дом преобразился, как заново построили. Чистота после работы — отдельный плюс. Рекомендую!', rating: 5, date: 'дек 2024' },
  { name: 'Елена С.', role: 'Истра', content: 'Второй раз обращаемся. Первый раз 5 лет назад — дом до сих пор отлично выглядит.', rating: 5, date: 'ноя 2024' },
  { name: 'Дмитрий В.', role: 'Рублёвка', content: 'Профессионалы. Быстро, качественно, без сюрпризов. Буду рекомендовать.', rating: 5, date: 'окт 2024' },
  { name: 'Мария И.', role: 'Звенигород', content: 'Сделали шлифовку и покраску бани. Результат превзошел ожидания!', rating: 5, date: 'сен 2024' },
  { name: 'Иван К.', role: 'Одинцово', content: 'Отличная работа. Никакой пыли и мусора после себя не оставили.', rating: 5, date: 'авг 2024' },
  { name: 'Светлана М.', role: 'Дмитров', content: 'Цены как в договоре, мастера вежливые. Очень довольна сотрудничеством.', rating: 5, date: 'июл 2024' },
];

const footerServices = [
  { label: 'Шлифовка срубов', href: '#services' },
  { label: 'Консьержная шлифовка', href: '#services' },
  { label: 'Покраска и пропитка', href: '#services' },
  { label: 'Антисептирование', href: '#services' },
  { label: 'Ремонт швов', href: '#services' },
];

const footerCompany = [
  { label: 'О нас', href: '#advantages' },
  { label: 'Работы', href: '#portfolio' },
  { label: 'Отзывы', href: '#testimonials' },
  { label: 'Контакты', href: '#contact' },
];

function scrollToSection(href: string) {
  const el = document.querySelector(href);
  if (el) el.scrollIntoView({ behavior: 'smooth' });
}

export default function HomePage() {
  const [navScrolled, setNavScrolled] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  // Quiz
  const [quizStep, setQuizStep] = useState(0);
  const [quizAnswers, setQuizAnswers] = useState<Record<number, string | string[]>>({});
  const [quizDone, setQuizDone] = useState(false);
  const [estimatedPrice, setEstimatedPrice] = useState(0);
  // Comparison

  // Calculator
  const [calcHouseType, setCalcHouseType] = useState('srub');
  const [calcArea, setCalcArea] = useState(75);
  const [calcServices, setCalcServices] = useState<string[]>([]);
  // Portfolio lightbox
  const [lightboxIndex, setLightboxIndex] = useState<number | null>(null);
  // FAQ
  const [faqOpen, setFaqOpen] = useState<number | null>(0);
  const [faqCategory, setFaqCategory] = useState('Все');
  // Contact
  const [formData, setFormData] = useState({ name: '', phone: '', email: '', message: '' });
  const [formSent, setFormSent] = useState(false);
  // Модалка «Перезвоните мне»
  const [callbackOpen, setCallbackOpen] = useState(false);

  useEffect(() => {
    const onScroll = () => setNavScrolled(window.scrollY > 100);
    window.addEventListener('scroll', onScroll, { passive: true });
    return () => window.removeEventListener('scroll', onScroll);
  }, []);

  return (
    <div className="min-h-screen">
      <Navbar scrolled={navScrolled} onCallback={() => setCallbackOpen(true)} />

      <CallbackModal open={callbackOpen} onClose={() => setCallbackOpen(false)} />

      {/* Hero */}
      <section id="hero" className="relative min-h-screen flex items-center justify-center overflow-hidden">
        <div className="absolute inset-0 bg-cover bg-center bg-no-repeat" style={{ backgroundImage: 'url(/hero-bg.jpg)' }}>
          <div className="absolute inset-0 bg-gradient-to-b from-black/70 via-black/50 to-background" />
        </div>
        <div className="relative z-10 container mx-auto px-4 sm:px-6 lg:px-8 pt-20 pb-16">
          <div className="max-w-4xl mx-auto text-center">
            <h1 className="text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-bold mb-6 leading-tight">
              <span className="text-white">Профессиональная</span>
              <br />
              <span className="text-gradient">шлифовка деревянных домов</span>
            </h1>
            <p className="text-lg sm:text-xl text-gray-300 mb-10 max-w-2xl mx-auto font-light">
              Восстановим красоту и долговечность вашего деревянного дома. Гарантия на все виды работ.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center mb-12">
              <button type="button" onClick={() => setCallbackOpen(true)} className="inline-flex items-center justify-center gap-2 bg-amber-600 hover:bg-amber-700 text-white px-6 py-3 sm:px-8 sm:py-4 rounded-xl text-base sm:text-lg font-black uppercase tracking-wider shadow-lg shadow-amber-900/20 w-full sm:w-auto">
                <Phone className="w-5 h-5" /> Бесплатная консультация
              </button>
              <button onClick={() => scrollToSection('#portfolio')} className="inline-flex items-center justify-center border border-amber-500/50 text-amber-200 hover:bg-amber-500/10 px-6 py-3 sm:px-8 sm:py-4 rounded-xl text-base sm:text-lg font-bold w-full sm:w-auto">
                Посмотреть работы
              </button>
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-6 max-w-3xl mx-auto">
              <div className="flex items-center justify-center gap-3 text-gray-300">
                <div className="w-12 h-12 rounded-xl bg-amber-500/20 flex items-center justify-center"><Shield className="w-6 h-6 text-amber-400" /></div>
                <div className="text-left"><div className="font-bold text-white uppercase tracking-wider text-xs">Гарантия 3 года</div><div className="text-xs text-gray-500 uppercase tracking-widest mt-0.5">На все работы</div></div>
              </div>
              <div className="flex items-center justify-center gap-3 text-gray-300">
                <div className="w-12 h-12 rounded-xl bg-amber-500/20 flex items-center justify-center"><Clock className="w-6 h-6 text-amber-400" /></div>
                <div className="text-left"><div className="font-bold text-white uppercase tracking-wider text-xs">Работаем быстро</div><div className="text-xs text-gray-500 uppercase tracking-widest mt-0.5">От 3 дней</div></div>
              </div>
              <div className="flex items-center justify-center gap-3 text-gray-300">
                <div className="w-12 h-12 rounded-xl bg-amber-500/20 flex items-center justify-center"><Award className="w-6 h-6 text-amber-400" /></div>
                <div className="text-left"><div className="font-bold text-white uppercase tracking-wider text-xs">500+ домов</div><div className="text-xs text-gray-500 uppercase tracking-widest mt-0.5">Отреставрировано</div></div>
              </div>
            </div>
          </div>
        </div>
        <div className="absolute bottom-8 left-1/2 -translate-x-1/2 animate-bounce">
          <ArrowDown className="w-6 h-6 text-amber-400" />
        </div>
      </section>

      {/* Services */}
      <section id="services" className="py-24 lg:py-32 relative overflow-hidden">
        {/* Background elements */}
        <div className="absolute top-0 right-0 w-full h-full overflow-hidden pointer-events-none">
          <div className="absolute -top-1/4 -right-1/4 w-[800px] h-[800px] bg-amber-500/10 blur-[120px] rounded-full" />
          <div className="absolute bottom-0 left-1/4 w-[600px] h-[600px] bg-amber-600/5 blur-[100px] rounded-full" />
        </div>

        <div className="container mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
          <div className="flex flex-col lg:flex-row lg:items-end justify-between gap-8 mb-16 lg:mb-24">
            <div className="max-w-3xl">
              <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-amber-500/10 border border-amber-500/20 mb-6 backdrop-blur-sm">
                <Settings className="w-4 h-4 text-amber-400" />
                <span className="text-sm text-amber-300 font-bold uppercase tracking-widest">Наши услуги</span>
              </div>
              <h2 className="text-4xl sm:text-5xl lg:text-6xl font-black mb-6 tracking-tight leading-tight">
                <span className="text-white">Комплексная </span>
                <br className="hidden sm:block" />
                <span className="text-gradient">реставрация домов</span>
              </h2>
              <p className="text-gray-400 text-lg sm:text-xl font-light max-w-2xl leading-relaxed">
                Мы предлагаем полный спектр услуг от базовой шлифовки до премиального финишного покрытия, сохраняя природную красоту дерева и продлевая жизнь вашего дома на десятилетия.
              </p>
            </div>
            <div className="hidden lg:block pb-4">
              <button type="button" onClick={() => setCallbackOpen(true)} className="inline-flex items-center justify-center gap-3 px-8 py-4 rounded-2xl bg-white/5 border border-white/10 hover:bg-white/10 text-white font-bold uppercase tracking-wider transition-all hover:scale-105 active:scale-95 shadow-xl">
                Заказать выезд <ArrowRight className="w-5 h-5 text-amber-400" />
              </button>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-12 gap-6">
            {services.map((s, i) => {
              const spanClass = 
                i === 0 ? 'lg:col-span-8 md:col-span-2' :
                i === 1 ? 'lg:col-span-4 md:col-span-1' :
                i === 2 ? 'lg:col-span-4 md:col-span-1' :
                i === 3 ? 'lg:col-span-8 md:col-span-2' :
                i === 4 ? 'lg:col-span-6 md:col-span-1' :
                i === 5 ? 'lg:col-span-6 md:col-span-1' : 'lg:col-span-4 md:col-span-1';

              return (
                <div key={i} className={`group relative bg-card/40 backdrop-blur-sm border border-white/5 hover:border-amber-500/40 rounded-[2rem] overflow-hidden transition-all duration-500 hover:shadow-[0_0_40px_-10px_rgba(245,158,11,0.2)] ${spanClass}`}>
                  <div className="absolute inset-0">
                    <img src={s.img} alt={s.title} className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-1000 opacity-60" />
                    <div className="absolute inset-0 bg-gradient-to-t from-stone-950/95 via-stone-950/50 to-stone-950/20 group-hover:via-stone-950/40 transition-colors duration-500" />
                  </div>
                  <div className="relative p-8 sm:p-10 h-full flex flex-col justify-end min-h-[360px]">
                    <div className="absolute top-8 right-8 px-4 py-2 rounded-full bg-black/50 border border-white/10 backdrop-blur-md">
                      <span className="text-amber-400 text-sm font-black tracking-wider">{s.price}</span>
                    </div>
                    <div className="w-16 h-16 rounded-2xl bg-amber-500/10 border border-amber-500/20 flex items-center justify-center mb-8 backdrop-blur-md group-hover:bg-amber-500/20 transition-colors">
                      <s.icon className="w-8 h-8 text-amber-400 group-hover:scale-110 group-hover:-rotate-6 transition-transform duration-500" />
                    </div>
                    <h3 className="text-2xl sm:text-3xl font-bold text-white mb-4 tracking-tight group-hover:text-amber-300 transition-colors">{s.title}</h3>
                    <p className="text-gray-400 mb-8 text-base leading-relaxed font-light max-w-md">{s.description}</p>
                    <button type="button" onClick={() => setCallbackOpen(true)} className="inline-flex items-center gap-4 text-amber-400 hover:text-amber-300 font-bold uppercase tracking-widest text-sm w-fit group/btn">
                      <span className="relative overflow-hidden">
                        <span className="inline-block transition-transform duration-300 group-hover/btn:-translate-y-full">Узнать подробнее</span>
                        <span className="absolute left-0 top-0 inline-block transition-transform duration-300 translate-y-full group-hover/btn:translate-y-0 text-white">Узнать подробнее</span>
                      </span>
                      <div className="w-10 h-10 rounded-full bg-amber-500/10 border border-amber-500/30 flex items-center justify-center group-hover/btn:bg-amber-500 group-hover/btn:border-amber-500 group-hover/btn:text-stone-950 transition-all duration-300">
                        <ArrowRight className="w-5 h-5 group-hover/btn:-rotate-45 transition-transform duration-300" />
                      </div>
                    </button>
                  </div>
                </div>
              );
            })}
          </div>

          <div className="mt-20 lg:mt-32">
            <InlineLeadForm
              title="Онлайн-калькулятор"
              benefit="Узнайте примерную стоимость за 2 клика"
              leadType="cost"
              buttonText="Получить расчёт"
              icon={<Calculator className="w-8 h-8 text-amber-400" />}
              benefits={[
                { icon: FileCheck, title: 'Бесплатный расчёт сметы', description: 'Рассчитаем стоимость работ под ваш объект' },
                { icon: Clock, title: 'Перезвон за 30 минут', description: 'Свяжемся в течение получаса в удобное время' },
                { icon: Shield, title: 'Консультация специалиста', description: 'Ответим на вопросы по материалам и срокам' },
              ]}
            />
          </div>
        </div>
      </section>

      {/* Portfolio */}
      <section id="portfolio" className="py-20 lg:py-32 relative">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="max-w-3xl mb-16">
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-amber-500/10 border border-amber-500/20 mb-6 backdrop-blur-sm">
              <Images className="w-4 h-4 text-amber-400" />
              <span className="text-sm text-amber-300 font-bold uppercase tracking-widest">Портфолио</span>
            </div>
            <h2 className="text-3xl sm:text-4xl lg:text-5xl font-black mb-6 tracking-tight">
              <span className="text-white">Наши </span>
              <span className="text-gradient">проекты</span>
            </h2>
            <p className="text-gray-400 text-lg sm:text-xl font-light leading-relaxed">
              Оцените качество нашей работы: мы бережно восстанавливаем древесину, возвращая домам первозданный вид и надежную защиту.
            </p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {portfolioItems.map((item, i) => (
              <div key={i} onClick={() => setLightboxIndex(i)} className="group relative aspect-[4/3] rounded-2xl overflow-hidden cursor-pointer shadow-xl shadow-black/20">
                <img src={item.image} alt={item.title} className="absolute inset-0 w-full h-full object-cover group-hover:scale-110 transition-transform duration-500" />
                <div className="absolute inset-0 bg-gradient-to-t from-black/90 via-black/40 to-transparent opacity-0 group-hover:opacity-100 transition-opacity">
                  <div className="absolute bottom-0 left-0 right-0 p-6">
                    <h3 className="text-xl font-bold text-white mb-2 tracking-tight">{item.title}</h3>
                    <p className="text-gray-400 text-sm font-light uppercase tracking-widest">{item.location}, {item.year}</p>
                  </div>
                  <div className="absolute top-4 right-4 w-10 h-10 rounded-full bg-amber-500 flex items-center justify-center shadow-lg">
                    <Maximize2 className="w-5 h-5 text-white" />
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
        {lightboxIndex !== null && (
          <div className="fixed inset-0 z-[100] bg-black/95 flex flex-col" onClick={() => setLightboxIndex(null)}>
            <button className="absolute top-6 right-6 z-[110] w-12 h-12 rounded-full bg-white/10 border border-white/10 flex items-center justify-center" onClick={(e) => { e.stopPropagation(); setLightboxIndex(null); }}>
              <X className="w-6 h-6 text-white" />
            </button>
            <div className="flex-1 flex items-center justify-center p-8" onClick={(e) => e.stopPropagation()}>
              <img src={portfolioItems[lightboxIndex].image} alt={portfolioItems[lightboxIndex].title} className="max-w-full max-h-full object-contain rounded-lg shadow-2xl" />
            </div>
            <div className="p-8 bg-stone-950/80 backdrop-blur-md text-center border-t border-white/5">
              <h3 className="text-2xl font-bold text-white mb-2 tracking-tight">{portfolioItems[lightboxIndex].title}</h3>
              <p className="text-gray-400 text-sm font-light uppercase tracking-[0.2em]">{portfolioItems[lightboxIndex].location}, {portfolioItems[lightboxIndex].year}</p>
            </div>
          </div>
        )}
      </section>

      {/* Process */}
      <section id="process" className="py-24 lg:py-32 relative overflow-hidden">
        {/* Background elements */}
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-full h-full max-w-[1000px] bg-amber-500/5 blur-[120px] rounded-full pointer-events-none" />

        <div className="container mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
          <div className="max-w-7xl mx-auto mb-16 lg:mb-24">
            <div className="max-w-3xl">
              <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-amber-500/10 border border-amber-500/20 mb-6 backdrop-blur-sm">
                <Clock className="w-4 h-4 text-amber-400" />
                <span className="text-sm text-amber-300 font-bold uppercase tracking-widest">Как мы работаем</span>
              </div>
              <h2 className="text-4xl sm:text-5xl lg:text-6xl font-black mb-6 tracking-tight leading-tight">
                <span className="text-white">Этапы </span>
                <span className="text-gradient">нашей работы</span>
              </h2>
              <p className="text-gray-400 text-lg sm:text-xl font-light leading-relaxed">
                Прозрачный и отлаженный процесс от первого звонка до сдачи готового объекта.
              </p>
            </div>
          </div>

          <div className="relative grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 lg:gap-8 max-w-7xl mx-auto mb-16 lg:mb-24 pt-4">
            {/* Connecting line (Desktop) */}
            <div className="hidden lg:block absolute top-[4.75rem] left-[10%] right-[10%] h-px bg-gradient-to-r from-transparent via-amber-500/30 to-transparent pointer-events-none" />

            {processSteps.map((step, idx) => (
              <div key={step.num} className="group relative rounded-[2.5rem] border border-white/5 bg-card/40 backdrop-blur-xl p-8 hover:border-amber-500/30 hover:bg-stone-950/80 transition-all duration-500 shadow-[0_0_40px_-10px_rgba(0,0,0,0.3)] hover:shadow-[0_0_40px_-10px_rgba(245,158,11,0.15)] flex flex-col h-full overflow-hidden">
                {/* Hover Glow */}
                <div className="absolute inset-0 bg-gradient-to-br from-amber-500/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500 pointer-events-none" />
                
                {/* Large Background Number */}
                <div className="absolute -right-4 -bottom-6 text-[8rem] font-black text-white/5 group-hover:text-white/10 transition-colors select-none pointer-events-none leading-none">
                  {step.num}
                </div>
                
                {/* Header with Step Number */}
                <div className="relative z-10 flex items-center justify-between mb-8">
                  <div className="w-14 h-14 rounded-2xl bg-amber-500/10 border border-amber-500/20 flex items-center justify-center group-hover:bg-amber-500 group-hover:scale-110 group-hover:-rotate-6 transition-all duration-500 shadow-lg shadow-amber-500/5">
                    <span className="text-xl font-black text-amber-400 group-hover:text-stone-950">{step.num}</span>
                  </div>
                  {idx < processSteps.length - 1 && (
                    <div className="hidden lg:flex w-8 h-8 items-center justify-center rounded-full bg-stone-950 border border-white/10 text-gray-500 shadow-xl group-hover:text-amber-400 transition-colors">
                      <ChevronRight className="w-4 h-4" />
                    </div>
                  )}
                </div>

                <div className="relative z-10 flex-1">
                  <h3 className="text-2xl font-bold text-white mb-4 tracking-tight group-hover:text-amber-300 transition-colors">{step.title}</h3>
                  <p className="text-gray-400 text-sm leading-relaxed font-light">{step.description}</p>
                </div>
              </div>
            ))}
          </div>

          <div className="max-w-7xl mx-auto">
            <button
              type="button"
              onClick={() => setCallbackOpen(true)}
              className="group relative w-full rounded-2xl bg-stone-950/60 backdrop-blur-md border border-white/5 p-6 sm:p-8 flex flex-col md:flex-row items-center gap-6 text-left transition-all duration-300 hover:border-amber-500/30 hover:bg-stone-950/80 shadow-xl overflow-hidden"
            >
              <div className="absolute inset-0 bg-gradient-to-r from-amber-500/0 via-amber-500/5 to-amber-500/0 opacity-0 group-hover:opacity-100 transition-opacity duration-500 pointer-events-none" />
              
              <div className="relative z-10 w-16 h-16 rounded-2xl bg-amber-500/10 border border-amber-500/20 flex items-center justify-center flex-shrink-0 group-hover:scale-110 transition-transform duration-300">
                <Rocket className="w-8 h-8 text-amber-500" />
              </div>
              
              <div className="relative z-10 flex-1 min-w-0">
                <h3 className="text-xl sm:text-2xl font-black text-white mb-2 uppercase tracking-tight">Готовы преобразить ваш дом?</h3>
                <p className="text-gray-400 text-sm leading-relaxed font-light">
                  Ваш дом будет защищён на десятилетия. Шлифовка, покраска и антисептирование продлят срок службы древесины и сохранят её красоту. Оставьте заявку — сделаем замер и рассчитаем смету бесплатно.
                </p>
              </div>
              
              <div className="relative z-10 flex-shrink-0 mt-4 md:mt-0 w-full md:w-auto">
                <span className="flex items-center justify-center gap-2 px-6 py-4 rounded-xl bg-amber-600 group-hover:bg-amber-500 text-stone-950 font-black text-sm uppercase tracking-widest transition-colors shadow-lg shadow-amber-900/20 w-full">
                  Вызвать мастера <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
                </span>
              </div>
            </button>
          </div>
        </div>
      </section>

      {/* Comparison */}
      <section id="comparison" className="py-20 lg:py-28 relative overflow-hidden bg-stone-950/20">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
          <div className="max-w-5xl mx-auto mb-16">
            <div className="max-w-3xl">
              <h2 className="text-3xl sm:text-4xl lg:text-5xl font-black mb-6 tracking-tight">
                <span className="text-white">Преображение </span>
                <span className="text-gradient">вашего дома</span>
              </h2>
              <p className="text-gray-400 text-lg font-light leading-relaxed">
                Устраняем последствия времени и ошибок, возвращая дереву первозданный вид и защиту.
              </p>
            </div>
          </div>

          <div className="max-w-6xl mx-auto grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
            {/* До (Before) */}
            <div className="relative rounded-[2rem] overflow-hidden group shadow-2xl">
              <div className="absolute inset-0">
                <img src="/before.jpg" alt="Состояние до" className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-1000 grayscale opacity-40" />
                <div className="absolute inset-0 bg-stone-950/80 backdrop-blur-[8px]" />
              </div>
              <div className="relative z-10 p-8 sm:p-12 h-full flex flex-col">
                <div className="flex items-center gap-4 mb-8">
                  <div className="w-12 h-12 rounded-xl bg-stone-900/50 border border-white/10 flex items-center justify-center">
                    <XCircle className="w-5 h-5 text-red-500/70" />
                  </div>
                  <h3 className="text-xl font-bold text-white tracking-tight">Если оставить как есть</h3>
                </div>
                <div className="space-y-5 flex-1">
                  {problems.map((p, i) => (
                    <div key={i} className="flex items-start gap-4 group/item">
                      <XCircle className="w-4 h-4 text-red-500/40 shrink-0 mt-1 transition-colors group-hover/item:text-red-400" />
                      <p className="text-gray-400 text-sm leading-relaxed font-light">{p}</p>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* После (After) */}
            <div className="relative rounded-[2rem] overflow-hidden group shadow-2xl">
              <div className="absolute inset-0">
                <img src="/after.jpg" alt="После реставрации" className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-1000" />
                <div className="absolute inset-0 bg-stone-950/60 backdrop-blur-[8px]" />
                <div className="absolute inset-0 bg-gradient-to-br from-amber-500/10 to-transparent mix-blend-overlay" />
              </div>
              <div className="relative z-10 p-8 sm:p-12 h-full flex flex-col">
                <div className="flex items-center gap-4 mb-8">
                  <div className="w-12 h-12 rounded-xl bg-amber-500 flex items-center justify-center shadow-lg shadow-amber-500/20">
                    <CheckCircle2 className="w-6 h-6 text-stone-950" />
                  </div>
                  <h3 className="text-xl font-bold text-white tracking-tight">После нашей работы</h3>
                </div>
                <div className="space-y-5 flex-1">
                  {solutions.map((s, i) => (
                    <div key={i} className="flex items-start gap-4 group/item">
                      <div className="w-4 h-4 rounded-full bg-amber-500/20 flex items-center justify-center shrink-0 mt-1 transition-colors group-hover/item:bg-amber-500/40">
                        <CheckCircle2 className="w-2.5 h-2.5 text-amber-500" />
                      </div>
                      <p className="text-white text-sm font-medium leading-relaxed drop-shadow-md">{s}</p>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 max-w-6xl mx-auto">
            {comparisons.map((item, i) => (
              <div key={i} className="p-6 rounded-2xl bg-stone-950/60 backdrop-blur-xl border border-white/5 flex flex-col hover:bg-stone-900 transition-colors shadow-xl group">
                <div className="flex items-center gap-4 mb-5">
                  <div className="w-10 h-10 rounded-xl bg-stone-900 border border-white/5 flex items-center justify-center group-hover:border-amber-500/30 group-hover:bg-amber-500/5 transition-all">
                    <item.icon className="w-4 h-4 text-amber-500/60 group-hover:text-amber-400" />
                  </div>
                  <h4 className="text-xs font-bold text-white uppercase tracking-widest leading-snug">{item.aspect}</h4>
                </div>
                <div className="w-full space-y-4 pt-5 border-t border-white/5 flex-1">
                  <div className="text-[11px] text-gray-500 font-light flex items-start gap-2.5">
                    <XCircle className="w-3.5 h-3.5 text-red-500/30 shrink-0 mt-0.5" />
                    <span className="leading-relaxed">{item.before}</span>
                  </div>
                  <div className="text-[11px] text-amber-100/90 font-medium flex items-start gap-2.5">
                    <CheckCircle2 className="w-3.5 h-3.5 text-amber-500 shrink-0 mt-0.5" />
                    <span className="leading-relaxed drop-shadow-sm">{item.after}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* WhyUs */}
      <section id="whyus" className="py-20 lg:py-28 relative overflow-hidden bg-stone-950/30">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
          <div className="max-w-5xl mx-auto mb-16">
            <div className="max-w-3xl">
              <h2 className="text-3xl sm:text-4xl lg:text-5xl font-black mb-4 tracking-tight">
                <span className="text-white">Опыт, которому </span>
                <span className="text-gradient">доверяют</span>
              </h2>
              <p className="text-gray-400 text-lg font-light leading-relaxed">
                Мы создаем безупречный результат, который будет радовать вас и вашу семью долгие годы.
              </p>
            </div>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 max-w-4xl mx-auto mb-16">
            {achievements.map((a, i) => (
              <div key={i} className="group relative text-center p-6 rounded-2xl bg-card/30 border border-white/5 hover:border-amber-500/30 transition-all duration-300">
                <div className="text-3xl font-black text-amber-500 mb-2 group-hover:scale-105 transition-transform duration-300">{a.value}</div>
                <div className="text-[10px] text-gray-400 font-bold uppercase tracking-widest">{a.label}</div>
              </div>
            ))}
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-5xl mx-auto">
            {reasons.map((r, i) => (
              <div key={i} className="group p-6 sm:p-8 rounded-[1.5rem] bg-stone-950/50 border border-white/5 hover:border-amber-500/30 transition-all duration-300 flex flex-col">
                <div className="flex items-center gap-4 mb-6">
                  <div className="w-12 h-12 rounded-xl bg-amber-500/10 border border-amber-500/20 flex items-center justify-center group-hover:bg-amber-500 group-hover:scale-110 group-hover:-rotate-6 transition-all duration-300">
                    <r.icon className="w-5 h-5 text-amber-400 group-hover:text-stone-950" />
                  </div>
                  <h3 className="text-lg font-bold text-white tracking-tight group-hover:text-amber-300 transition-colors">{r.title}</h3>
                </div>
                
                <p className="text-gray-400 text-sm font-light leading-relaxed mb-6 flex-1">{r.description}</p>
                
                <div className="space-y-2 pt-4 border-t border-white/5">
                  {r.features.map((f, j) => (
                    <div key={j} className="flex items-center gap-3 text-xs text-gray-300 font-medium">
                      <BadgeCheck className="w-4 h-4 text-amber-500 shrink-0" />
                      {f}
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Quiz Instead of Calculator */}
      <QuizSection
        quizStep={quizStep}
        setQuizStep={setQuizStep}
        quizAnswers={quizAnswers}
        setQuizAnswers={setQuizAnswers}
        quizDone={quizDone}
        setQuizDone={setQuizDone}
        estimatedPrice={estimatedPrice}
        setEstimatedPrice={setEstimatedPrice}
        onRequestCallback={() => setCallbackOpen(true)}
      />

      {/* FAQ */}
      <section id="faq" className="py-20 lg:py-32 relative">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="max-w-3xl mx-auto mb-12">
            <div>
              <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-amber-500/10 border border-amber-500/20 mb-6">
                <MessageCircleQuestion className="w-4 h-4 text-amber-400" />
                <span className="text-sm text-amber-300 font-bold uppercase tracking-widest">Вопросы и ответы</span>
              </div>
              <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold mb-6 tracking-tight">
                <span className="text-white">Часто задаваемые </span>
                <span className="text-gradient">вопросы</span>
              </h2>
            </div>
          </div>
          <div className="max-w-3xl mx-auto space-y-4">
            {faqItems.map((item, i) => (
              <div key={i} className={`rounded-2xl border border-border/30 overflow-hidden transition-all ${faqOpen === i ? 'border-amber-500/30' : ''}`}>
                <button onClick={() => setFaqOpen(faqOpen === i ? null : i)} className="w-full p-6 flex items-start gap-4 text-left">
                  <div className={`w-10 h-10 rounded-lg flex items-center justify-center flex-shrink-0 ${faqOpen === i ? 'bg-amber-500/20' : 'bg-card/50'}`}>
                    <HelpCircle className={`w-5 h-5 ${faqOpen === i ? 'text-amber-400' : 'text-gray-500'}`} />
                  </div>
                  <div className="flex-1">
                    <span className="px-2 py-0.5 rounded-full bg-amber-500/10 text-amber-400 text-[10px] font-bold uppercase tracking-widest mr-2">{item.category}</span>
                    <h3 className="text-lg font-bold text-white mt-1 leading-tight">{item.question}</h3>
                  </div>
                  {faqOpen === i ? <ChevronUp className="w-5 h-5 text-amber-400" /> : <ChevronDown className="w-5 h-5 text-gray-500" />}
                </button>
                {faqOpen === i && (
                  <div className="px-6 pb-6 pl-[4.5rem]">
                    <p className="text-gray-400 text-sm leading-relaxed font-light">{item.answer}</p>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Testimonials */}
      <section id="testimonials" className="py-24 lg:py-32 relative overflow-hidden bg-stone-950/30">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8 relative">
          <div className="max-w-3xl mb-16 lg:mb-24">
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-amber-500/10 border border-amber-500/20 mb-6 backdrop-blur-sm">
              <MessageSquare className="w-4 h-4 text-amber-400" />
              <span className="text-sm text-amber-300 font-bold uppercase tracking-widest">Отзывы</span>
            </div>
            <h2 className="text-4xl sm:text-5xl lg:text-6xl font-black mb-6 tracking-tight">
              <span className="text-white">Что говорят </span>
              <span className="text-gradient">наши клиенты</span>
            </h2>
            <p className="text-gray-400 text-lg font-light max-w-2xl mx-auto">Живые отзывы о нашей работе от владельцев деревянных домов со всего Подмосковья.</p>
          </div>
          
          <div className="columns-1 md:columns-2 lg:columns-3 gap-6 space-y-6">
            {testimonials.map((t, i) => (
              <div key={i} className="break-inside-avoid p-6 rounded-[1.5rem] bg-card/40 backdrop-blur-md border border-white/5 hover:border-amber-500/30 transition-all duration-300 hover:-translate-y-1 hover:shadow-2xl hover:shadow-amber-500/5 group">
                <div className="flex justify-between items-start mb-4">
                  <div className="flex gap-1">
                    {[...Array(t.rating)].map((_, j) => (
                      <Star key={j} className="w-3.5 h-3.5 fill-amber-500 text-amber-500" />
                    ))}
                  </div>
                  <Quote className="w-6 h-6 text-amber-500/10 group-hover:text-amber-500/20 transition-colors" />
                </div>
                <p className="text-gray-300 mb-6 font-light leading-relaxed text-sm">&quot;{t.content}&quot;</p>
                <div className="flex items-center justify-between pt-4 border-t border-white/5">
                  <div className="flex items-center gap-3">
                    <div className="w-8 h-8 rounded-full bg-stone-800 flex items-center justify-center text-xs font-bold text-gray-400">
                      {t.name.charAt(0)}
                    </div>
                    <div>
                      <div className="font-bold text-white text-sm tracking-tight">{t.name}</div>
                      <div className="text-[10px] text-amber-500 font-bold uppercase tracking-widest mt-0.5">{t.role}</div>
                    </div>
                  </div>
                  <div className="text-[10px] text-gray-600 font-bold uppercase tracking-widest">{t.date}</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Contact Section */}
      <ContactSection formData={formData} setFormData={setFormData} formSent={formSent} setFormSent={setFormSent} onRequestCallback={() => setCallbackOpen(true)} />

      {/* Footer */}
      <footer className="py-16 border-t border-border/30 bg-stone-950">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-12 mb-12">
            <div>
              <div className="flex items-center gap-3 mb-6">
                <div className="w-12 h-12 rounded-xl bg-amber-500/20 flex items-center justify-center">
                  <span className="text-2xl font-bold text-amber-400">A</span>
                </div>
                <div>
                  <div className="text-xl font-bold text-white uppercase tracking-tighter leading-none">ArteMadera</div>
                  <div className="text-[10px] text-gray-500 font-bold uppercase tracking-widest mt-1">Premium Sanding</div>
                </div>
              </div>
              <p className="text-gray-400 text-sm mb-6 font-light leading-relaxed">Профессиональная шлифовка и реставрация деревянных домов в Москве и области.</p>
            </div>
            <div>
              <h4 className="text-sm font-bold text-white uppercase tracking-widest mb-6">Услуги</h4>
              <ul className="space-y-3">
                {footerServices.map((l, i) => (
                  <li key={i}>
                    <button onClick={() => scrollToSection(l.href)} className="text-gray-500 hover:text-amber-400 text-sm transition-colors font-medium">{l.label}</button>
                  </li>
                ))}
              </ul>
            </div>
            <div>
              <h4 className="text-sm font-bold text-white uppercase tracking-widest mb-6">Компания</h4>
              <ul className="space-y-3">
                {footerCompany.map((l, i) => (
                  <li key={i}>
                    <button onClick={() => scrollToSection(l.href)} className="text-gray-500 hover:text-amber-400 text-sm transition-colors font-medium">{l.label}</button>
                  </li>
                ))}
              </ul>
            </div>
            <div>
              <h4 className="text-sm font-bold text-white uppercase tracking-widest mb-6">Контакты</h4>
              <ul className="space-y-4">
                <li className="flex items-start gap-3 group">
                  <Phone className="w-4 h-4 text-amber-400 flex-shrink-0 mt-0.5 group-hover:scale-110 transition-transform" />
                  <a href={`tel:${PHONE.replace(/\D/g, '')}`} className="text-gray-400 hover:text-amber-400 text-sm font-bold">{PHONE}</a>
                </li>
                <li className="flex items-start gap-3 group">
                  <Mail className="w-4 h-4 text-amber-400 flex-shrink-0 mt-0.5 group-hover:scale-110 transition-transform" />
                  <a href={`mailto:${EMAIL}`} className="text-gray-400 hover:text-amber-400 text-sm font-medium">{EMAIL}</a>
                </li>
                <li className="flex items-start gap-3">
                  <MapPin className="w-4 h-4 text-amber-400 flex-shrink-0 mt-0.5" />
                  <span className="text-gray-400 text-sm font-light">{ADDRESS}</span>
                </li>
              </ul>
            </div>
          </div>
          <div className="pt-8 border-t border-border/30 flex flex-col sm:flex-row justify-between items-center gap-4">
            <p className="text-gray-600 text-[10px] font-bold uppercase tracking-widest">© {new Date().getFullYear()} ArteMadera. Все права защищены.</p>
            <div className="flex gap-6">
              <button className="text-gray-600 hover:text-amber-400 text-[10px] font-bold uppercase tracking-widest transition-colors">Конфиденциальность</button>
              <button className="text-gray-600 hover:text-amber-400 text-[10px] font-bold uppercase tracking-widest transition-colors">Оферта</button>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}

function QuizSideImage({ step, quizAnswers }: { step: any; quizAnswers: Record<number, string | string[]> }) {
  let src = step.stepImg ?? '/service-1.jpg';
  const answer = quizAnswers[step.id];
  if (step.options?.some((o: any) => o.img)) {
    if (step.multiple && Array.isArray(answer) && answer.length > 0) {
      const first = step.options.find((o: any) => answer.includes(o.value));
      src = first?.img ?? first?.fallback ?? src;
    } else if (!step.multiple && typeof answer === 'string') {
      const opt = step.options.find((o: any) => o.value === answer);
      src = opt?.img ?? opt?.fallback ?? src;
    } else {
      src = step.options[0]?.img ?? step.options[0]?.fallback ?? src;
    }
  }
  return (
    <div className="absolute inset-0 bg-card/30 flex items-center justify-center group overflow-hidden">
      <img src={src} alt="" className="absolute inset-0 w-full h-full object-cover group-hover:scale-105 transition-transform duration-700 opacity-80" />
      <div className="absolute inset-0 bg-gradient-to-t from-background via-transparent to-transparent" />
    </div>
  );
}

function QuizSection(props: any) {
  const { quizStep, setQuizStep, quizAnswers, setQuizAnswers, quizDone, setQuizDone, estimatedPrice, setEstimatedPrice, onRequestCallback } = props;
  const step = quizSteps[quizStep];
  const progress = ((quizStep + 1) / quizSteps.length) * 100;

  const handleAnswer = (value: string) => {
    if (step.multiple) {
      const current = (quizAnswers[step.id] as string[]) || [];
      const updated = current.includes(value) ? current.filter((v) => v !== value) : [...current, value];
      setQuizAnswers({ ...quizAnswers, [step.id]: updated });
    } else {
      setQuizAnswers({ ...quizAnswers, [step.id]: value });
    }
  };

  const next = () => {
    if (quizStep < quizSteps.length - 1) {
      setQuizStep(quizStep + 1);
    } else {
      const house = quizSteps[0].options.find((o: any) => o.value === quizAnswers[1]);
      const sizeOpt = quizSteps[1].options.find((o: any) => o.value === quizAnswers[2]);
      const services = (quizAnswers[3] as string[]) || [];
      let base = house?.price ?? 1000;
      let mult = (sizeOpt as any)?.multiplier ?? 1;
      let add = 0;
      quizSteps[2].options.forEach((o: any) => {
        if (services.includes(o.value) && typeof o.price === 'number') add += o.price;
      });
      const area = quizAnswers[2] === 'small' ? 40 : quizAnswers[2] === 'medium' ? 75 : quizAnswers[2] === 'large' ? 125 : 200;
      setEstimatedPrice(Math.round((base + add) * area * mult));
      setQuizDone(true);
    }
  };

  if (!step) return null;

  return (
    <section id="quiz" className="py-20 lg:py-32 relative overflow-hidden">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8 relative">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-12">
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-amber-500/10 border border-amber-500/20 mb-6">
              <Calculator className="w-4 h-4 text-amber-400" />
              <span className="text-sm text-amber-300 font-bold uppercase tracking-widest">Калькулятор стоимости</span>
            </div>
            <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold mb-6 tracking-tight text-white">Рассчитайте <span className="text-gradient">стоимость работ</span></h2>
          </div>
          <div className="rounded-[2rem] bg-card/50 border border-border/50 overflow-hidden shadow-2xl">
            {!quizDone ? (
              <div className="grid grid-cols-1 lg:grid-cols-[1fr_auto_420px] gap-0 min-h-[400px] lg:min-h-[500px]">
                <div className="p-8 sm:p-12 flex flex-col">
                  <div className="mb-10">
                    <div className="flex justify-between text-[10px] font-bold text-gray-500 uppercase tracking-widest mb-2">
                      <span>Вопрос {quizStep + 1} из {quizSteps.length}</span>
                      <span>{Math.round(progress)}%</span>
                    </div>
                    <div className="h-1 w-full rounded-full bg-border/50 overflow-hidden">
                      <div className="h-full bg-amber-500 rounded-full transition-all duration-500" style={{ width: `${progress}%` }} />
                    </div>
                  </div>
                  <div className="mb-10 flex-1">
                    <div className="flex items-center gap-4 mb-8">
                      <div className="w-12 h-12 rounded-xl bg-amber-500/20 flex items-center justify-center">
                        <step.icon className="w-6 h-6 text-amber-400" />
                      </div>
                      <h3 className="text-2xl font-bold text-white leading-tight tracking-tight">{step.question}</h3>
                    </div>
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                      {step.options.map((opt: any) => {
                        const active = step.multiple ? (quizAnswers[step.id] || []).includes(opt.value) : quizAnswers[step.id] === opt.value;
                        return (
                          <button
                            key={opt.value}
                            onClick={() => handleAnswer(opt.value)}
                            className={`p-5 rounded-2xl border-2 text-left transition-all flex items-center gap-4 ${active ? 'border-amber-500 bg-amber-500/10' : 'border-border/30 bg-white/5 hover:border-amber-500/30'}`}
                          >
                            <div className={`w-5 h-5 rounded-lg border-2 flex items-center justify-center flex-shrink-0 ${active ? 'border-amber-500 bg-amber-500' : 'border-gray-600'}`}>
                              {active && <CheckCircle2 className="w-3 h-3 text-white" />}
                            </div>
                            <span className="text-white font-bold text-sm tracking-tight">{opt.label}</span>
                          </button>
                        );
                      })}
                    </div>
                  </div>
                  <div className="flex justify-between pt-8 border-t border-border/30">
                    <button onClick={() => setQuizStep(Math.max(0, quizStep - 1))} disabled={quizStep === 0} className="px-6 py-2.5 rounded-xl border border-border/50 text-gray-500 hover:text-white disabled:opacity-0 font-bold text-sm transition-all uppercase tracking-widest">
                      <ChevronLeft className="w-4 h-4 inline mr-2" /> Назад
                    </button>
                    <button onClick={next} disabled={step.multiple ? (quizAnswers[step.id] || []).length === 0 : !quizAnswers[step.id]} className="px-10 py-3 rounded-xl bg-amber-600 hover:bg-amber-500 text-white font-black text-sm shadow-xl shadow-amber-900/20 transition-all disabled:opacity-50 uppercase tracking-widest">
                      {quizStep === quizSteps.length - 1 ? 'Рассчитать' : 'Далее'} <ChevronRight className="w-4 h-4 inline ml-2" />
                    </button>
                  </div>
                </div>
                <div className="hidden lg:block w-px self-stretch bg-border/30" />
                <div className="hidden lg:block relative w-[420px] shrink-0 self-stretch">
                  <QuizSideImage step={step} quizAnswers={quizAnswers} />
                </div>
              </div>
            ) : (
              <div className="text-center p-16 sm:p-24 bg-card/50">
                <div className="w-20 h-20 rounded-2xl bg-amber-500/20 flex items-center justify-center mx-auto mb-10 shadow-2xl shadow-amber-500/20">
                  <CheckCircle2 className="w-10 h-10 text-amber-400" />
                </div>
                <h3 className="text-3xl sm:text-4xl font-black text-white mb-6 uppercase tracking-tight">Ваш расчёт готов!</h3>
                <div className="text-5xl sm:text-6xl font-black text-gradient mb-8 leading-none tracking-tighter">от {estimatedPrice.toLocaleString()} ₽</div>
                <p className="text-gray-400 text-lg mb-12 max-w-md mx-auto font-light leading-relaxed">Точная стоимость после осмотра. Оставьте заявку — приедем, замерим и ответим на все вопросы.</p>
                <div className="flex flex-col sm:flex-row gap-4 justify-center">
                  <button type="button" onClick={onRequestCallback} className="inline-flex items-center justify-center gap-3 bg-amber-600 hover:bg-amber-500 text-white px-10 py-5 rounded-2xl text-lg font-black transition-all shadow-xl shadow-amber-900/20 uppercase tracking-widest">
                    <Phone className="w-6 h-6" /> Получить консультацию
                  </button>
                  <button type="button" onClick={() => { setQuizStep(0); setQuizAnswers({}); setQuizDone(false); }} className="inline-flex items-center justify-center border-2 border-border/30 text-gray-500 hover:text-white px-10 py-5 rounded-2xl text-lg font-bold transition-all uppercase tracking-widest">
                    Пройти заново
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </section>
  );
}

function CalculatorSection(props: any) {
  const { calcHouseType, setCalcHouseType, calcArea, setCalcArea, calcServices, setCalcServices, onRequestCallback } = props;
  const house = houseTypes.find((h) => h.value === calcHouseType);
  const basePrice = house?.price ?? 1200;
  const addPrice = calcServices.reduce((sum, id) => sum + (additionalServices.find((x) => x.id === id)?.price ?? 0), 0);
  const totalPerM2 = basePrice + addPrice;
  const total = totalPerM2 * calcArea;
  const discount = calcArea > 150 ? 0.1 : calcArea > 100 ? 0.05 : 0;
  const final = Math.round(total * (1 - discount));

  return (
    <section id="calculator" className="py-20 lg:py-32 relative overflow-hidden bg-white/5">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8 relative">
        <div className="max-w-5xl mx-auto">
          <div className="text-center mb-16">
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-amber-500/10 border border-amber-500/20 mb-6">
              <Calculator className="w-4 h-4 text-amber-400" />
              <span className="text-sm text-amber-300 font-bold uppercase tracking-widest">Калькулятор</span>
            </div>
            <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold mb-6 tracking-tight text-white">Точный расчёт стоимости</h2>
            <p className="text-gray-400 text-lg font-light">Выберите параметры и получите мгновенный расчёт.</p>
          </div>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <div className="p-8 rounded-[2rem] bg-card/50 border border-border/50 space-y-10">
              <div>
                <label className="text-white font-bold mb-6 block uppercase tracking-widest text-xs">1. Тип дома</label>
                <div className="grid grid-cols-2 gap-4">
                  {houseTypes.map((t) => (
                    <button
                      key={t.value}
                      onClick={() => setCalcHouseType(t.value)}
                      className={`p-5 rounded-2xl border-2 text-left transition-all ${calcHouseType === t.value ? 'border-amber-500 bg-amber-500/10' : 'border-border/30 hover:border-amber-500/30'}`}
                    >
                      <t.icon className={`w-6 h-6 mb-3 ${calcHouseType === t.value ? 'text-amber-400' : 'text-gray-500'}`} />
                      <div className="text-sm font-bold text-white tracking-tight">{t.label}</div>
                      <div className="text-[10px] text-gray-500 uppercase mt-1">от {t.price} ₽/м²</div>
                    </button>
                  ))}
                </div>
              </div>
              <div>
                <div className="flex justify-between items-end mb-6">
                  <label className="text-white font-bold uppercase tracking-widest text-xs">2. Площадь дома</label>
                  <span className="text-3xl font-black text-amber-500 leading-none">{calcArea} м²</span>
                </div>
                <input type="range" min={20} max={300} step={5} value={calcArea} onChange={(e) => setCalcArea(Number(e.target.value))} className="w-full h-2 rounded-full appearance-none bg-border/50 accent-amber-500" />
                <div className="flex justify-between text-[10px] font-bold text-gray-600 mt-2 uppercase tracking-widest"><span>20 м²</span><span>300 м²</span></div>
              </div>
              <div>
                <label className="text-white font-bold mb-6 block uppercase tracking-widest text-xs">3. Дополнительные услуги</label>
                <div className="space-y-3">
                  {additionalServices.map((s) => (
                    <button
                      key={s.id}
                      onClick={() => setCalcServices(calcServices.includes(s.id) ? calcServices.filter(x => x !== s.id) : [...calcServices, s.id])}
                      className={`w-full p-4 rounded-2xl border-2 flex items-center gap-4 transition-all ${calcServices.includes(s.id) ? 'border-amber-500 bg-amber-500/10' : 'border-border/30 hover:border-amber-500/30'}`}
                    >
                      <div className={`w-10 h-10 rounded-xl flex items-center justify-center shrink-0 ${calcServices.includes(s.id) ? 'bg-amber-500 shadow-lg shadow-amber-500/20' : 'bg-stone-900'}`}>
                        <s.icon className={`w-5 h-5 ${calcServices.includes(s.id) ? 'text-white' : 'text-gray-500'}`} />
                      </div>
                      <div className="flex-1 text-left">
                        <div className="text-sm font-bold text-white tracking-tight">{s.label}</div>
                        <div className="text-[10px] text-gray-500 uppercase">+{s.price} ₽/м²</div>
                      </div>
                      {calcServices.includes(s.id) && <CheckCircle2 className="w-5 h-5 text-amber-400" />}
                    </button>
                  ))}
                </div>
              </div>
            </div>
            <div className="p-10 rounded-[2rem] bg-gradient-to-br from-amber-600 to-amber-700 shadow-2xl shadow-amber-900/40 relative overflow-hidden flex flex-col justify-between">
              <div className="absolute top-0 right-0 w-64 h-64 bg-white/10 rounded-full blur-[80px] -translate-y-1/2 translate-x-1/2 pointer-events-none" />
              <div>
                <h3 className="text-2xl font-black text-white mb-8 uppercase tracking-widest">Итог расчёта</h3>
                <div className="space-y-4 mb-10 text-amber-100 font-medium">
                  <div className="flex justify-between text-sm"><span>Базовая шлифовка</span><span className="text-white font-bold">{basePrice} ₽/м²</span></div>
                  {calcServices.map((id) => {
                    const s = additionalServices.find((x) => x.id === id);
                    return <div key={id} className="flex justify-between text-sm"><span>{s?.label}</span><span className="text-white font-bold">+{s?.price} ₽/м²</span></div>;
                  })}
                  <div className="flex justify-between text-sm"><span>Общая площадь</span><span className="text-white font-bold">{calcArea} м²</span></div>
                  {discount > 0 && <div className="flex justify-between text-sm text-white font-black uppercase tracking-widest"><span>Скидка за объём</span><span>-{Math.round(discount * 100)}%</span></div>}
                </div>
              </div>
              <div>
                <div className="border-t border-white/20 pt-8 mb-10">
                  <div className="text-[10px] font-black text-amber-200 uppercase tracking-[0.2em] mb-2">Предварительная стоимость:</div>
                  <div className="flex items-end gap-3">
                    <div className="text-5xl sm:text-6xl font-black text-white leading-none tracking-tighter">{final.toLocaleString()} ₽</div>
                  </div>
                </div>
                <button type="button" onClick={onRequestCallback} className="w-full flex items-center justify-center gap-3 bg-stone-950 hover:bg-stone-900 text-white py-5 rounded-2xl font-black text-lg transition-all shadow-xl shadow-black/30 mb-8 uppercase tracking-widest">
                  <Phone className="w-5 h-5" /> Жду звонка
                </button>
                <ul className="text-[10px] text-amber-100/70 space-y-3 font-bold uppercase tracking-widest">
                  <li className="flex items-center gap-3"><CheckCircle2 className="w-4 h-4" /> Шлифовка всей площади</li>
                  <li className="flex items-center gap-3"><CheckCircle2 className="w-4 h-4" /> Работа и материалы</li>
                  <li className="flex items-center gap-3"><CheckCircle2 className="w-4 h-4" /> Гарантия 3 года по договору</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

function ContactSection(props: any) {
  const { formData, setFormData, formSent, setFormSent } = props;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const phoneDigits = getPhoneDigits(formData.phone);
    if (phoneDigits.length < 11) return;
    try {
      const res = await fetch(API_LEAD_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ phone: phoneDigits, type: 'contact' }),
      });
      if (res.ok) {
        setFormSent(true);
        setFormData({ ...formData, phone: '' });
        setTimeout(() => setFormSent(false), 3000);
      }
    } catch {
      setFormSent(true);
      setTimeout(() => setFormSent(false), 3000);
    }
  };

  return (
    <section id="contact" className="py-20 lg:py-32 relative">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="max-w-4xl mx-auto mb-16">
          <div className="max-w-3xl">
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-amber-500/10 border border-amber-500/20 mb-6">
              <Contact2 className="w-4 h-4 text-amber-400" />
              <span className="text-sm text-amber-300 font-bold uppercase tracking-widest">Свяжитесь с нами</span>
            </div>
            <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold mb-6 tracking-tight text-white">Получите <span className="text-gradient">бесплатную консультацию</span></h2>
            <p className="text-gray-400 text-lg font-light">Оставьте заявку — свяжемся в течение 30 минут.</p>
          </div>
        </div>
        <div className="max-w-4xl mx-auto bg-card/40 backdrop-blur-xl border border-white/5 rounded-[2.5rem] overflow-hidden shadow-2xl flex flex-col md:flex-row">
          <div className="flex-1 p-8 sm:p-12 border-b md:border-b-0 md:border-r border-white/5 bg-stone-950/50">
            <div className="w-12 h-12 rounded-2xl bg-amber-500/10 flex items-center justify-center mb-8">
              <Phone className="w-6 h-6 text-amber-500" />
            </div>
            <h3 className="text-2xl font-black text-white mb-4 tracking-tight">Нужна помощь?</h3>
            <p className="text-gray-400 text-sm font-light leading-relaxed mb-8">Задайте любой вопрос или вызовите мастера на бесплатный замер.</p>
            
            <div className="space-y-6">
              <div>
                <div className="text-[10px] text-gray-500 font-bold uppercase tracking-widest mb-1">Звоните напрямую</div>
                <a href={`tel:${PHONE.replace(/\D/g, '')}`} className="text-xl font-bold text-white hover:text-amber-400 transition-colors">{PHONE}</a>
              </div>
              <div>
                <div className="text-[10px] text-gray-500 font-bold uppercase tracking-widest mb-1">Пишите на почту</div>
                <a href={`mailto:${EMAIL}`} className="text-lg font-medium text-gray-300 hover:text-amber-400 transition-colors">{EMAIL}</a>
              </div>
            </div>
          </div>
          
          <div className="flex-1 p-8 sm:p-12 bg-amber-500/5 relative overflow-hidden">
            <div className="absolute top-0 right-0 w-64 h-64 bg-amber-500/10 blur-[80px] rounded-full pointer-events-none" />
            
            <div className="relative z-10">
              {formSent ? (
                <div className="h-full flex flex-col items-center justify-center py-12 text-center">
                  <div className="w-16 h-16 rounded-full bg-green-500/20 flex items-center justify-center mb-6">
                    <CheckCircle2 className="w-8 h-8 text-green-400" />
                  </div>
                  <h4 className="text-xl font-black text-white mb-2 uppercase tracking-widest">Заявка принята</h4>
                  <p className="text-sm text-gray-400">Мы перезвоним вам в ближайшее время.</p>
                </div>
              ) : (
                <form onSubmit={handleSubmit} className="space-y-5">
                  <div className="text-sm font-medium text-white mb-6">Оставьте номер телефона</div>
                  <div className="relative">
                    <div className="absolute left-4 top-1/2 -translate-y-1/2 w-8 h-8 rounded-full bg-white/5 flex items-center justify-center">
                      <Phone className="w-4 h-4 text-gray-400" />
                    </div>
                    <input
                      required
                      type="tel"
                      placeholder="+7 (999) 000-00-00"
                      value={formData.phone}
                      onChange={(e) => setFormData({ ...formData, phone: formatPhoneMask(e.target.value) })}
                      className="w-full pl-14 pr-4 py-4 rounded-xl bg-white/5 border border-white/10 focus:border-amber-500/50 focus:bg-white/10 transition-all focus:outline-none text-white text-base font-bold placeholder:text-gray-600 shadow-inner"
                    />
                  </div>
                  <button type="submit" className="w-full flex items-center justify-center gap-2 bg-gradient-to-r from-amber-600 to-amber-500 text-stone-950 py-4 rounded-xl font-black text-sm uppercase tracking-widest hover:scale-[1.02] transition-transform shadow-xl shadow-amber-900/20">
                    Жду звонка <Send className="w-4 h-4" />
                  </button>
                  <p className="text-center text-[10px] text-gray-500 font-light mt-4">
                    Нажимая кнопку, вы соглашаетесь с политикой конфиденциальности
                  </p>
                </form>
              )}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

function InlineLeadForm(props: any) {
  const { title, benefit, leadType, buttonText, icon, benefits } = props;
  const [phone, setPhone] = useState('');
  const [sent, setSent] = useState(false);
  const [area, setArea] = useState(75);
  const [houseType, setHouseType] = useState('srub');

  const basePrice = houseTypes.find((h) => h.value === houseType)?.price || 1200;
  const total = basePrice * area;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const digits = getPhoneDigits(phone);
    if (digits.length < 11) return;
    try {
      const res = await fetch(API_LEAD_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ phone: digits, type: leadType }),
      });
      if (res.ok) {
        setSent(true);
        setPhone('');
      }
    } catch {
      setSent(true);
    }
  };

  if (sent) {
    return (
      <div className="relative rounded-[2.5rem] bg-card/40 backdrop-blur-2xl border border-white/5 p-16 text-center overflow-hidden shadow-2xl">
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[500px] h-[500px] bg-green-500/10 blur-[100px] rounded-full pointer-events-none" />
        <div className="relative z-10 max-w-lg mx-auto">
          <div className="w-24 h-24 mx-auto bg-green-500/10 rounded-3xl flex items-center justify-center mb-8 border border-green-500/20 shadow-lg shadow-green-500/10">
            <CheckCircle2 className="w-12 h-12 text-green-400" />
          </div>
          <h4 className="text-3xl sm:text-4xl font-black text-white uppercase tracking-tight mb-4">Заявка принята</h4>
          <p className="text-gray-400 text-lg font-light leading-relaxed">
            Спасибо за обращение. Наш специалист свяжется с вами в течение получаса для обсуждения деталей.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="relative rounded-[2rem] bg-card/40 backdrop-blur-2xl border border-white/5 p-6 sm:p-8 overflow-hidden shadow-[0_0_80px_-20px_rgba(0,0,0,0.5)]">
      {/* Background glow effects */}
      <div className="absolute top-0 right-0 w-[600px] h-[600px] bg-amber-500/10 blur-[100px] rounded-full translate-x-1/3 -translate-y-1/3 pointer-events-none" />
      <div className="absolute bottom-0 left-0 w-[400px] h-[400px] bg-amber-600/5 blur-[80px] rounded-full -translate-x-1/3 translate-y-1/3 pointer-events-none" />

      <div className="relative z-10 grid grid-cols-1 lg:grid-cols-[1fr_auto_1fr] gap-8 lg:gap-10 items-center">
        {/* Left Content */}
        <div className="flex flex-col items-start text-left w-full max-w-[480px] mx-auto">
          <div className="inline-flex items-center justify-center w-12 h-12 rounded-2xl bg-amber-500/10 border border-amber-500/20 mb-5 shadow-lg shadow-amber-500/5">
            <div className="scale-75 text-amber-400">{icon}</div>
          </div>
          
          <h3 className="text-2xl sm:text-3xl lg:text-4xl font-black text-white mb-3 leading-[1.1] tracking-tight uppercase">
            {title}
          </h3>
          <p className="text-gray-400 text-sm sm:text-base font-light leading-relaxed mb-6">
            {benefit}
          </p>

          {/* Render passed benefits if available */}
          {benefits && benefits.length > 0 && (
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-x-6 gap-y-3 w-full">
              {benefits.map((b: any, i: number) => (
                <div key={i} className="flex items-start gap-3">
                  <div className="w-8 h-8 rounded-xl bg-white/5 flex items-center justify-center flex-shrink-0 border border-white/10 group-hover:border-amber-500/30 transition-colors">
                    <b.icon className="w-3.5 h-3.5 text-amber-400" />
                  </div>
                  <div className="pt-0.5">
                    <div className="text-white font-bold text-xs mb-0.5">{b.title}</div>
                    <div className="text-gray-500 text-[11px] font-light leading-snug">{b.description}</div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
        
        {/* Divider */}
        <div className="hidden lg:block w-px h-full min-h-[300px] bg-gradient-to-b from-transparent via-white/10 to-transparent" />
        
        {/* Right Form Card */}
        <div className="w-full max-w-[480px] mx-auto">
          <div className="relative z-10 space-y-6">
            <div className="space-y-5">
              {/* House Type */}
              <div>
                <label className="block text-[10px] font-bold text-amber-500 uppercase tracking-[0.2em] mb-2.5 ml-1">Материал дома</label>
                <div className="grid grid-cols-2 gap-2.5">
                  {houseTypes.map((t) => (
                    <button
                      key={t.value}
                      onClick={() => setHouseType(t.value)}
                      className={`p-3 rounded-xl border transition-all text-left flex items-center gap-2.5 ${
                        houseType === t.value 
                          ? 'bg-amber-500/20 border-amber-500 text-white shadow-[0_0_15px_-5px_rgba(245,158,11,0.3)]' 
                          : 'bg-white/5 border-white/10 text-gray-400 hover:bg-white/10 hover:text-gray-200 hover:border-white/20'
                      }`}
                    >
                      <t.icon className={`w-3.5 h-3.5 flex-shrink-0 transition-colors ${houseType === t.value ? 'text-amber-400' : 'text-gray-500'}`} />
                      <span className="text-[11px] font-bold tracking-wider uppercase">{t.label}</span>
                    </button>
                  ))}
                </div>
              </div>

              {/* Area */}
              <div>
                <div className="flex justify-between items-end mb-3 ml-1">
                  <label className="text-[10px] font-bold text-amber-500 uppercase tracking-[0.2em]">Площадь по полу</label>
                  <span className="text-xl font-black text-white">{area} м²</span>
                </div>
                <div className="relative pt-1 pb-1">
                  <input
                    type="range"
                    min={20}
                    max={300}
                    step={5}
                    value={area}
                    onChange={(e) => setArea(Number(e.target.value))}
                    className="w-full h-1.5 rounded-full appearance-none bg-white/10 accent-amber-500 outline-none hover:bg-white/20 transition-all cursor-pointer"
                  />
                </div>
                <div className="flex justify-between text-[9px] font-bold text-gray-500 mt-1.5">
                  <span>20 м²</span>
                  <span>300 м²</span>
                </div>
              </div>

              {/* Total */}
              <div className="flex items-end justify-between py-3 border-y border-white/10 my-4">
                <span className="text-xs text-gray-400 font-light">Примерная сумма:</span>
                <span className="text-2xl font-black text-amber-500 tracking-tighter">{total.toLocaleString()} ₽</span>
              </div>

              {/* Form */}
              <div>
                <form onSubmit={handleSubmit} className="space-y-3">
                  <div className="relative group">
                    <input
                      required
                      type="tel"
                      placeholder="Ваш телефон"
                      value={phone}
                      onChange={(e) => setPhone(formatPhoneMask(e.target.value))}
                      className="w-full px-4 py-3 rounded-xl bg-white/5 border border-white/10 focus:border-amber-500 focus:bg-white/10 transition-all focus:outline-none text-white text-base font-bold placeholder:text-gray-500 shadow-inner"
                    />
                    <div className="absolute -inset-1 rounded-2xl bg-amber-500/20 blur-lg opacity-0 group-focus-within:opacity-100 transition-opacity duration-500 pointer-events-none" />
                  </div>
                  
                  <button type="submit" className="relative w-full group overflow-hidden rounded-xl shadow-lg shadow-amber-900/20">
                    <div className="absolute inset-0 bg-gradient-to-r from-amber-600 to-amber-500 transition-transform duration-500 group-hover:scale-105" />
                    <div className="relative flex items-center justify-center gap-2 px-5 py-3 text-white font-black text-xs uppercase tracking-widest">
                      <span>Зафиксировать цену</span>
                      <CheckCircle2 className="w-4 h-4 group-hover:scale-110 group-hover:rotate-6 transition-all duration-300" />
                    </div>
                  </button>
                  <p className="text-center text-[9px] text-gray-500 font-light mt-3">
                    Нажимая на кнопку, вы соглашаетесь с условиями обработки данных
                  </p>
                </form>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
