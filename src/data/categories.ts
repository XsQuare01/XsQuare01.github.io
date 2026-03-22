export interface Category {
  slug: string;
  label: string;
  icon: string;
  description: string;
}

export const categories: Category[] = [
  {
    slug: 'theory',
    label: '계산 이론',
    icon: '🧮',
    description: '오토마타, 튜링 머신, 복잡도 클래스 등 계산 이론의 수학적 기반을 다룹니다.',
  },
  {
    slug: 'cryptography',
    label: '암호학',
    icon: '🔐',
    description: '정수론, 암호학적 프로토콜, 계산 복잡도의 응용을 탐구합니다.\n계산 이론 시리즈를 먼저 읽기를 권장합니다.',
  },
  {
    slug: 'algorithm',
    label: '알고리즘',
    icon: '📊',
    description: '자료구조와 알고리즘 설계 및 분석을 다룹니다.',
  },
  {
    slug: 'os',
    label: '운영체제',
    icon: '⚙️',
    description: '프로세스, 메모리, 파일 시스템 등 운영체제의 핵심 개념을 다룹니다.',
  },
  {
    slug: 'unity',
    label: 'Unity',
    icon: '🎮',
    description: 'Unity 기반 클라이언트 개발, UI/UX, 구조 설계 경험을 기록합니다.',
  },
  {
    slug: 'web-dev',
    label: '웹 개발',
    icon: '🌐',
    description: '프론트엔드, 백엔드, 인프라 경험을 기록합니다.',
  },
];

export function getCategoryLabel(slug: string): string {
  return categories.find((c) => c.slug === slug)?.label ?? slug;
}
