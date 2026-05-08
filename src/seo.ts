type SeoPayload = {
  title: string;
  description: string;
  path?: string;
  image?: string;
};

const SITE_NAME = 'ArteMadera';
const DEFAULT_IMAGE = '/og-image.svg';

function upsertMeta(attr: 'name' | 'property', key: string, content: string) {
  let meta = document.querySelector(`meta[${attr}="${key}"]`);
  if (!meta) {
    meta = document.createElement('meta');
    meta.setAttribute(attr, key);
    document.head.appendChild(meta);
  }
  meta.setAttribute('content', content);
}

function upsertCanonical(url: string) {
  let link = document.querySelector('link[rel="canonical"]');
  if (!link) {
    link = document.createElement('link');
    link.setAttribute('rel', 'canonical');
    document.head.appendChild(link);
  }
  link.setAttribute('href', url);
}

export function applySeo({ title, description, path = '/', image = DEFAULT_IMAGE }: SeoPayload) {
  const origin = window.location.origin;
  const canonicalUrl = new URL(path, origin).toString();
  const imageUrl = new URL(image, origin).toString();

  document.title = title;
  upsertMeta('name', 'description', description);
  upsertMeta('property', 'og:type', 'website');
  upsertMeta('property', 'og:site_name', SITE_NAME);
  upsertMeta('property', 'og:title', title);
  upsertMeta('property', 'og:description', description);
  upsertMeta('property', 'og:url', canonicalUrl);
  upsertMeta('property', 'og:image', imageUrl);
  upsertMeta('name', 'twitter:card', 'summary_large_image');
  upsertMeta('name', 'twitter:title', title);
  upsertMeta('name', 'twitter:description', description);
  upsertMeta('name', 'twitter:image', imageUrl);
  upsertCanonical(canonicalUrl);
}
