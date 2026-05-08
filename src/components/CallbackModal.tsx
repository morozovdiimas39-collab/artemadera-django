import { useState } from 'react';
import { Phone, X, CheckCircle2 } from 'lucide-react';
import { API_LEAD_URL, formatPhoneMask, getPhoneDigits } from '../lib/phone';

type Props = { open: boolean; onClose: () => void };

export default function CallbackModal({ open, onClose }: Props) {
  const [phone, setPhone] = useState('');
  const [loading, setLoading] = useState(false);
  const [sent, setSent] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const digits = getPhoneDigits(phone);
    if (digits.length < 11) return;
    setLoading(true);
    try {
      const res = await fetch(API_LEAD_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ phone: digits, type: 'callback' }),
      });
      if (res.ok) {
        setSent(true);
        setPhone('');
        setTimeout(() => { setSent(false); onClose(); }, 2500);
      }
    } catch {
      setSent(true);
      setTimeout(() => { setSent(false); }, 2500);
    } finally {
      setLoading(false);
    }
  };

  if (!open) return null;

  return (
    <div className="fixed inset-0 z-[60] flex items-start justify-center p-4 sm:items-center sm:p-0">
      <div className="absolute inset-0 bg-black/80 backdrop-blur-sm" onClick={onClose} aria-hidden />
      <div className="relative w-full max-w-md rounded-2xl border-2 border-amber-500/40 bg-amber-500/10 shadow-xl shadow-amber-900/20" onClick={(e) => e.stopPropagation()}>
        <button type="button" onClick={onClose} className="absolute top-4 right-4 w-10 h-10 rounded-xl bg-white/10 border border-amber-500/30 flex items-center justify-center text-gray-300 hover:text-white hover:border-amber-500/50 transition-colors" aria-label="Закрыть">
          <X className="w-5 h-5" />
        </button>
        <div className="p-6 pt-12 sm:p-8">
          <div className="flex items-center gap-4 mb-4">
            <div className="w-14 h-14 rounded-xl bg-amber-500/20 flex items-center justify-center">
              <Phone className="w-7 h-7 text-amber-400" />
            </div>
            <div>
              <h3 className="text-2xl sm:text-3xl font-bold text-white">Позвоните сейчас</h3>
              <p className="text-amber-200/90 text-base font-medium mt-1">Бесплатный замер и расчёт за 30 минут. Оставьте номер — перезвоним.</p>
            </div>
          </div>
          {sent ? (
            <div className="py-8 text-center">
              <div className="w-16 h-16 rounded-full bg-green-500/30 flex items-center justify-center mx-auto mb-4">
                <CheckCircle2 className="w-8 h-8 text-green-400" />
              </div>
              <h4 className="text-xl font-bold text-white mb-2">Заявка принята</h4>
              <p className="text-amber-200/90">Мы перезвоним в ближайшее время.</p>
            </div>
          ) : (
            <form onSubmit={handleSubmit} className="space-y-4 mt-6">
              <label htmlFor="callback-phone" className="sr-only">Телефон</label>
              <input
                id="callback-phone"
                type="tel"
                placeholder="+7 (999) 999-99-99"
                value={phone}
                onChange={(e) => setPhone(formatPhoneMask(e.target.value))}
                className="w-full px-4 py-4 rounded-xl bg-background/80 border-2 border-amber-500/30 focus:border-amber-500 focus:outline-none text-white placeholder:text-gray-500 text-base"
              />
              <button
                type="submit"
                disabled={loading || getPhoneDigits(phone).length < 11}
                className="w-full flex items-center justify-center gap-2 bg-amber-600 hover:bg-amber-500 disabled:opacity-50 disabled:pointer-events-none text-white py-4 rounded-xl font-bold text-lg transition-colors"
              >
                <Phone className="w-5 h-5" /> {loading ? 'Отправка...' : 'Жду звонка'}
              </button>
              <p className="text-xs text-amber-200/70 text-center">Нажимая кнопку, вы соглашаетесь с политикой конфиденциальности</p>
            </form>
          )}
        </div>
      </div>
    </div>
  );
}
