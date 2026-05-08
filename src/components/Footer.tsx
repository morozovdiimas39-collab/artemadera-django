import { Link } from 'react-router-dom';
import { Phone, Mail, MapPin, Instagram, Facebook, Youtube } from 'lucide-react';

const PHONE = '+7 (495) 005-01-45';
const EMAIL = 'info@artemadera.ru';
const ADDRESS = 'Москва, ВДНХ, ул. Ярославская';

export default function Footer() {
  const scrollToSection = (href: string) => {
    const el = document.querySelector(href);
    if (el) el.scrollIntoView({ behavior: 'smooth' });
  };

  const footerServices = [
    { label: 'Шлифовка срубов', href: '#services' },
    { label: 'Консьержная шлифовка', href: '#services' },
    { label: 'Покраска и пропитка', href: '#services' },
    { label: 'Антисептирование', href: '#services' },
    { label: 'Ремонт швов', href: '#services' },
  ];

  const footerCompany = [
    { label: 'О нас', href: '#whyus' },
    { label: 'Работы', href: '#portfolio' },
    { label: 'Отзывы', href: '#testimonials' },
    { label: 'Контакты', href: '#contact' },
  ];

  return (
    <footer className="bg-stone-950 border-t border-white/5 pt-24 pb-12">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-12 mb-20">
          <div>
            <Link to="/" className="flex items-center gap-3 mb-8 group">
              <div className="w-12 h-12 rounded-xl bg-amber-500/20 border border-amber-500/30 flex items-center justify-center group-hover:bg-amber-500/30 transition-colors">
                <span className="text-2xl font-bold text-amber-400">A</span>
              </div>
              <div className="flex flex-col">
                <span className="text-2xl font-black text-white leading-none tracking-tighter">ARTEMADERA</span>
                <span className="text-[10px] font-bold text-amber-500/50 uppercase tracking-widest leading-none mt-1.5">Premium Sanding</span>
              </div>
            </Link>
            <p className="text-gray-500 text-sm leading-relaxed mb-8 max-w-xs font-light">
              Профессиональная шлифовка и реставрация деревянных домов в Москве и области. Возвращаем природную красоту дерева и защищаем ваш дом на десятилетия.
            </p>
            <div className="flex gap-4">
              <a href="#" className="w-10 h-10 rounded-xl bg-white/5 border border-white/10 flex items-center justify-center text-gray-400 hover:text-amber-400 hover:border-amber-500/50 transition-all">
                <Instagram className="w-5 h-5" />
              </a>
              <a href="#" className="w-10 h-10 rounded-xl bg-white/5 border border-white/10 flex items-center justify-center text-gray-400 hover:text-amber-400 hover:border-amber-500/50 transition-all">
                <Facebook className="w-5 h-5" />
              </a>
              <a href="#" className="w-10 h-10 rounded-xl bg-white/5 border border-white/10 flex items-center justify-center text-gray-400 hover:text-amber-400 hover:border-amber-500/50 transition-all">
                <Youtube className="w-5 h-5" />
              </a>
            </div>
          </div>

          <div>
            <h4 className="text-sm font-bold text-white uppercase tracking-[0.2em] mb-8">Услуги</h4>
            <ul className="space-y-4">
              {footerServices.map((l, i) => (
                <li key={i}>
                  <button onClick={() => scrollToSection(l.href)} className="text-gray-500 hover:text-amber-400 text-sm transition-colors font-medium">{l.label}</button>
                </li>
              ))}
            </ul>
          </div>

          <div>
            <h4 className="text-sm font-bold text-white uppercase tracking-[0.2em] mb-8">Компания</h4>
            <ul className="space-y-4">
              {footerCompany.map((l, i) => (
                <li key={i}>
                  <button onClick={() => scrollToSection(l.href)} className="text-gray-500 hover:text-amber-400 text-sm transition-colors font-medium">{l.label}</button>
                </li>
              ))}
            </ul>
          </div>

          <div>
            <h4 className="text-sm font-bold text-white uppercase tracking-[0.2em] mb-8">Контакты</h4>
            <ul className="space-y-6">
              <li>
                <a href={`tel:${PHONE.replace(/\D/g, '')}`} className="flex items-start gap-4 group">
                  <div className="w-10 h-10 rounded-xl bg-amber-500/10 border border-amber-500/20 flex items-center justify-center shrink-0 group-hover:bg-amber-500 group-hover:text-white transition-all">
                    <Phone className="w-5 h-5 text-amber-500 group-hover:text-white transition-colors" />
                  </div>
                  <div className="flex flex-col">
                    <span className="text-white font-bold text-lg leading-none">{PHONE}</span>
                    <span className="text-xs text-gray-500 mt-1.5 font-bold uppercase tracking-widest">Звонок бесплатный</span>
                  </div>
                </a>
              </li>
              <li>
                <div className="flex items-start gap-4">
                  <div className="w-10 h-10 rounded-xl bg-white/5 border border-white/10 flex items-center justify-center shrink-0">
                    <Mail className="w-5 h-5 text-gray-400" />
                  </div>
                  <div className="flex flex-col">
                    <span className="text-gray-300 font-medium">{EMAIL}</span>
                    <span className="text-xs text-gray-600 mt-1 uppercase font-bold tracking-widest">Напишите нам</span>
                  </div>
                </div>
              </li>
              <li>
                <div className="flex items-start gap-4">
                  <div className="w-10 h-10 rounded-xl bg-white/5 border border-white/10 flex items-center justify-center shrink-0">
                    <MapPin className="w-5 h-5 text-gray-400" />
                  </div>
                  <div className="flex flex-col">
                    <span className="text-gray-300 font-medium">{ADDRESS}</span>
                    <span className="text-xs text-gray-600 mt-1 uppercase font-bold tracking-widest">Приезжайте в гости</span>
                  </div>
                </div>
              </li>
            </ul>
          </div>
        </div>

        <div className="pt-12 border-t border-white/5 flex flex-col md:flex-row justify-between items-center gap-6">
          <p className="text-gray-600 text-xs font-bold uppercase tracking-widest">
            © {new Date().getFullYear()} ARTEMADERA. ВСЕ ПРАВА ЗАЩИЩЕНЫ.
          </p>
          <div className="flex gap-8">
            <button className="text-gray-600 hover:text-amber-500 text-xs font-bold uppercase tracking-widest transition-colors">Конфиденциальность</button>
            <button className="text-gray-600 hover:text-amber-500 text-xs font-bold uppercase tracking-widest transition-colors">Оферта</button>
          </div>
        </div>
      </div>
    </footer>
  );
}
