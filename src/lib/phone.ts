export const API_LEAD_URL = import.meta.env.VITE_API_LEAD_URL ?? '/api/lead';

export function formatPhoneMask(value: string): string {
  const digits = value.replace(/\D/g, '');
  const d = digits.startsWith('7') || digits.startsWith('8') ? digits.slice(1) : digits;
  const s = d.slice(0, 10);
  if (s.length === 0) return '';
  if (s.length <= 3) return `+7 (${s}`;
  if (s.length <= 6) return `+7 (${s.slice(0, 3)}) ${s.slice(3)}`;
  return `+7 (${s.slice(0, 3)}) ${s.slice(3, 6)}-${s.slice(6, 8)}-${s.slice(8, 10)}`;
}

export function getPhoneDigits(masked: string): string {
  const digits = masked.replace(/\D/g, '');
  if (digits.startsWith('8')) return '7' + digits.slice(1, 11);
  if (digits.startsWith('7')) return digits.slice(0, 11);
  return '7' + digits.slice(0, 10);
}
