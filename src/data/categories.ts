export interface Category {
  slug: string;
  label: string;
  icon: string;
}

export const categories: Category[] = [
  { slug: 'math',      label: '수학',     icon: '∑' },
  { slug: 'algorithm', label: '알고리즘', icon: '⚙️' },
  { slug: 'game-dev',  label: '게임 개발', icon: '🎮' },
  { slug: 'web-dev',   label: '웹 개발',  icon: '🌐' },
];

export function getCategoryLabel(slug: string): string {
  return categories.find((c) => c.slug === slug)?.label ?? slug;
}
