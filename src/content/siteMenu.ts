export type MenuLink = { label: string; to: string };
export type MenuGroup = { title: string; links: MenuLink[] };

export const TOP_INFO_LINKS: MenuLink[] = [
  { label: 'О нас', to: '/o-kompanii' },
  { label: 'Блог', to: '/blog' },
  { label: 'Портфолио', to: '/portfolio' },
  { label: 'Цены', to: '/ceny' },
  { label: 'Отзывы', to: '/otzyvy' },
  { label: 'Контакты', to: '/kontakty' },
];

export const MENU_GROUPS: MenuGroup[] = [
  {
    title: 'Отделочные работы',
    links: [
      { label: 'Шлифовка срубов', to: '/otdelka/shlifovka/sruba' },
      { label: 'Шлифовка оцилиндрованного бревна', to: '/otdelka/shlifovka/ocilindrovannogo-brevna' },
      { label: 'Шлифовка дома из бруса', to: '/otdelka/shlifovka/brusa' },
      { label: 'Шлифовка лафета', to: '/otdelka/shlifovka/lafeta' },
      { label: 'Покраска', to: '/pokraska' },
      { label: 'Теплый шов', to: '/teplyy-shov' },
      { label: 'Конопатка', to: '/otdelka/konopatka' },
      { label: 'Отделка стен', to: '/otdelka/sten' },
      { label: 'Отделка пола', to: '/otdelka/pola' },
    ],
  },
  {
    title: 'Обсада',
    links: [
      { label: 'Обсада / Окосячка', to: '/obsada' },
      { label: 'Окна', to: '/obsada/okna' },
      { label: 'Двери', to: '/obsada/dveri' },
    ],
  },
  {
    title: 'Другие разделы',
    links: [
      { label: 'Крыши', to: '/kryshi' },
      { label: 'Инженерия', to: '/injeneriya' },
      { label: 'Беседки', to: '/proizvodstvo/besedki' },
      { label: 'Фальшбалки', to: '/proizvodstvo/falshbalki' },
      { label: 'Плинтусы', to: '/proizvodstvo/plintusy' },
    ],
  },
];

export const ALL_MENU_LINKS: MenuLink[] = [...TOP_INFO_LINKS, ...MENU_GROUPS.flatMap((g) => g.links)];
