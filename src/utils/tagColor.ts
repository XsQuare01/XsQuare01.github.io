const TAG_COLORS = [
  { bg: 'rgba(56, 189, 248, 0.15)', border: 'rgba(56, 189, 248, 0.5)', text: '#38bdf8' },   // sky
  { bg: 'rgba(167, 139, 250, 0.15)', border: 'rgba(167, 139, 250, 0.5)', text: '#a78bfa' }, // purple
  { bg: 'rgba(52, 211, 153, 0.15)', border: 'rgba(52, 211, 153, 0.5)', text: '#34d399' },   // emerald
  { bg: 'rgba(251, 191, 36, 0.15)', border: 'rgba(251, 191, 36, 0.5)', text: '#fbbf24' },   // amber
  { bg: 'rgba(244, 114, 182, 0.15)', border: 'rgba(244, 114, 182, 0.5)', text: '#f472b6' }, // pink
  { bg: 'rgba(249, 115, 22, 0.15)', border: 'rgba(249, 115, 22, 0.5)', text: '#fb923c' },   // orange
];

export function getTagColor(tag: string) {
  let hash = 0;
  for (let i = 0; i < tag.length; i++) {
    hash = (hash * 31 + tag.charCodeAt(i)) % TAG_COLORS.length;
  }
  return TAG_COLORS[Math.abs(hash)];
}

export function tagStyle(tag: string): string {
  const c = getTagColor(tag);
  return `background:${c.bg};border-color:${c.border};color:${c.text};`;
}
