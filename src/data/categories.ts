export interface Category {
  slug: string;
  label: string;
}

export const categories: Category[] = [
  { slug: 'math',      label: '수학' },
  { slug: 'algorithm', label: '알고리즘' },
  { slug: 'game-dev',  label: '게임 개발' },
  { slug: 'web-dev',   label: '웹 개발' },
];

export function getCategoryLabel(slug: string): string {
  return categories.find((c) => c.slug === slug)?.label ?? slug;
}
