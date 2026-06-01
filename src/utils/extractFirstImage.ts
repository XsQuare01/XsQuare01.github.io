export function extractFirstImage(markdown: string): string | null {
  const match = markdown.match(/!\[[^\]]*\]\(([^)\s]+)/);
  return match ? match[1] : null;
}

export function absoluteImageUrl(src: string, siteOrigin: string): string {
  if (/^https?:\/\//i.test(src)) return src;
  const origin = siteOrigin.replace(/\/$/, '');
  const path = src.startsWith('/') ? src : `/${src}`;
  return `${origin}${path}`;
}
