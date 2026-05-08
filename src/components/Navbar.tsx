import { useState, useEffect } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { Phone, Menu, X, ChevronDown } from 'lucide-react';
import { ARTEMADERA_PAGES } from '../content/artemaderaStructure';

const PHONE = '+7 (495) 005-01-45';

type NavbarProps = {
  scrolled?: boolean;
  mobileMenuOpen?: boolean;
  setMobileMenuOpen?: (v: boolean) => void;
  onCallback: () => void;
  transparent?: boolean;
};

export default function Navbar({ scrolled, mobileMenuOpen, setMobileMenuOpen, onCallback, transparent }: NavbarProps) {
  const [localMobileOpen, setLocalMobileOpen] = useState(false);
  const [servicesDropdownOpen, setServicesDropdownOpen] = useState(false);
  const isMobileOpen = mobileMenuOpen !== undefined ? mobileMenuOpen : localMobileOpen;
  const setIsMobileOpen = setMobileMenuOpen || setLocalMobileOpen;
  
  const { pathname } = useLocation();
  const navigate = useNavigate();

  const scrollToSection = (href: string) => {
    setIsMobileOpen(false);
    if (href.startsWith('#')) {
      if (pathname !== '/') {
        navigate('/' + href);
      } else {
        const el = document.querySelector(href);
        if (el) el.scrollIntoView({ behavior: 'smooth' });
      }
    } else {
      navigate(href);
    }
  };

  const navLinks = [
    { label: 'Калькулятор', href: '#quiz' },
    { label: 'Этапы', href: '#process' },
    { label: 'До/После', href: '#comparison' },
    { label: 'Почему мы', href: '#whyus' },
    { label: 'Работы', href: '#recent-projects' },
    { label: 'FAQ', href: '#faq' },
    { label: 'Контакты', href: '#contact' },
  ];

  const serviceCategories = ['Отделочные работы', 'Обсада', 'Крыши', 'Инженерия', 'Производство'];

  return (
    <>
      <nav className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${scrolled ? 'bg-stone-950/90 backdrop-blur-xl border-b border-white/5 py-3' : transparent ? 'bg-transparent py-5' : 'bg-stone-950/90 backdrop-blur-xl border-b border-white/5 py-3'}`}>
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between">
            <Link to="/" className="flex items-center gap-3 group">
              <div className="w-10 h-10 rounded-xl bg-amber-500/20 border border-amber-500/30 flex items-center justify-center group-hover:bg-amber-500/30 transition-colors">
                <span className="text-xl font-bold text-amber-400">A</span>
              </div>
              <div className="flex flex-col">
                <span className="text-xl font-black text-white leading-none tracking-tighter">ARTEMADERA</span>
                <span className="text-[10px] font-bold text-amber-500/50 uppercase tracking-widest leading-none mt-1">Premium Sanding</span>
              </div>
            </Link>

            <div className="hidden xl:flex items-center gap-1 relative">
              <div 
                className="relative"
                onMouseEnter={() => setServicesDropdownOpen(true)}
                onMouseLeave={() => setServicesDropdownOpen(false)}
              >
                <button className="px-4 py-2 text-sm font-bold text-gray-400 hover:text-white transition-colors rounded-xl hover:bg-white/5 flex items-center gap-1">
                  Услуги <ChevronDown className={`w-4 h-4 transition-transform duration-300 ${servicesDropdownOpen ? 'rotate-180 text-amber-400' : ''}`} />
                </button>
                {/* Mega Menu Dropdown */}
                <div className={`absolute top-full left-0 pt-4 transition-all duration-300 origin-top ${servicesDropdownOpen ? 'opacity-100 scale-y-100' : 'opacity-0 scale-y-0 pointer-events-none'}`}>
                  <div className="bg-stone-950/95 backdrop-blur-2xl border border-white/10 rounded-2xl shadow-2xl p-6 w-[800px] flex gap-8">
                    <div className="flex-1 grid grid-cols-2 gap-x-8 gap-y-6">
                      {serviceCategories.map(cat => {
                        const catPages = ARTEMADERA_PAGES.filter(p => p.category === cat);
                        if (!catPages.length) return null;
                        return (
                          <div key={cat}>
                            <h4 className="text-amber-500 text-xs font-black uppercase tracking-widest mb-3 border-b border-white/5 pb-2">{cat}</h4>
                            <div className="flex flex-col gap-2">
                              {catPages.map(p => (
                                <Link key={p.path} to={p.path} className="text-sm text-gray-300 hover:text-white hover:text-amber-200 transition-colors block">
                                  {p.title}
                                </Link>
                              ))}
                            </div>
                          </div>
                        );
                      })}
                    </div>
                  </div>
                </div>
              </div>

              {navLinks.map((link, i) => (
                <button key={i} onClick={() => scrollToSection(link.href)} className="px-4 py-2 text-sm font-bold text-gray-400 hover:text-white transition-colors rounded-xl hover:bg-white/5">{link.label}</button>
              ))}
            </div>

            <div className="flex items-center gap-3">
              <button onClick={onCallback} className="hidden sm:flex items-center gap-2 px-6 py-2.5 rounded-xl bg-amber-600 hover:bg-amber-500 text-white text-sm font-bold transition-all shadow-lg shadow-amber-900/20">
                <Phone className="w-4 h-4" /> Позвонить
              </button>
              <button onClick={() => setIsMobileOpen(!isMobileOpen)} className="xl:hidden w-10 h-10 rounded-xl bg-white/5 border border-white/10 flex items-center justify-center">
                {isMobileOpen ? <X className="w-5 h-5 text-gray-400" /> : <Menu className="w-5 h-5 text-gray-400" />}
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Mobile Menu */}
      <div className={`fixed inset-0 z-40 xl:hidden transition-all duration-500 ${isMobileOpen ? 'opacity-100 pointer-events-auto' : 'opacity-0 pointer-events-none'}`}>
        <div className="absolute inset-0 bg-stone-950/95 backdrop-blur-xl" onClick={() => setIsMobileOpen(false)} />
        <div className={`absolute top-24 left-4 right-4 bottom-4 bg-stone-900 border border-white/10 rounded-3xl p-8 transition-all duration-500 overflow-y-auto ${isMobileOpen ? 'translate-y-0 opacity-100' : '-translate-y-10 opacity-0'}`}>
          <div className="flex flex-col gap-2">
            <div className="mb-4">
              <h4 className="text-amber-500 text-xs font-black uppercase tracking-widest mb-3 border-b border-white/5 pb-2">Услуги</h4>
              <div className="flex flex-col gap-3 pl-4">
                {ARTEMADERA_PAGES.filter(p => serviceCategories.includes(p.category)).map(p => (
                  <Link key={p.path} to={p.path} onClick={() => setIsMobileOpen(false)} className="text-lg font-bold text-gray-300 hover:text-white hover:text-amber-200 transition-all">{p.title}</Link>
                ))}
              </div>
            </div>
            
            <h4 className="text-amber-500 text-xs font-black uppercase tracking-widest mb-3 border-b border-white/5 pb-2 mt-4">Навигация</h4>
            {navLinks.map((link, i) => (
              <button key={i} onClick={() => scrollToSection(link.href)} className="w-full py-2 text-left text-xl font-bold text-gray-300 hover:text-white hover:bg-white/5 rounded-2xl transition-all">{link.label}</button>
            ))}
            <div className="mt-6 pt-6 border-t border-white/5">
              <button onClick={() => { onCallback(); setIsMobileOpen(false); }} className="w-full flex items-center justify-center gap-3 py-5 rounded-2xl bg-amber-600 text-white font-bold text-lg">
                <Phone className="w-5 h-5" /> Оставить заявку
              </button>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}
