export interface Category {
  slug: string;
  label: string;
  icon: string;
  description: string;
}

export const categories: Category[] = [
  {
    slug: 'cryptography',
    label: '암호학',
    icon: '🔐',
    description: '오토마타, 튜링 머신 등 계산 이론의 수학적 기반을 다룹니다.\n암호학적 프로토콜과 복잡도 이론의 응용까지 탐구합니다.',
  },
  { slug: 'game-dev',     label: '게임 개발', icon: '🎮', description: '게임 설계 패턴과 구현 경험' },
  { slug: 'web-dev',      label: '웹 개발',  icon: '🌐', description: '프론트엔드, 백엔드, 인프라 경험' },
];

export function getCategoryLabel(slug: string): string {
  return categories.find((c) => c.slug === slug)?.label ?? slug;
}
