export interface Category {
  slug: string;
  label: string;
  icon: string;
  description: string;
}

export const categories: Category[] = [
  { slug: 'math',      label: '수학',     icon: '∑',  description: '알고리즘과 암호학의 기초가 되는 수리적 개념들' },
  { slug: 'algorithm', label: '알고리즘', icon: '⚙️', description: '문제 해결과 자료구조, 복잡도 분석' },
  { slug: 'game-dev',  label: '게임 개발', icon: '🎮', description: '게임 설계 패턴과 구현 경험' },
  { slug: 'web-dev',   label: '웹 개발',  icon: '🌐', description: '프론트엔드, 백엔드, 인프라 경험' },
];

export function getCategoryLabel(slug: string): string {
  return categories.find((c) => c.slug === slug)?.label ?? slug;
}
