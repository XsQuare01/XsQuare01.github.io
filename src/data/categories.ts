export interface Category {
  slug: string;
  label: string;
  icon: string;
  /** 카테고리 목록 카드에 쓰는 짧은 소개 */
  description: string;
  /**
   * 주제를 실제 개념 이름으로 서술한 문장. 홈의 주제 소개, 카테고리 허브의 메타 설명,
   * llms.txt가 모두 이 하나를 쓴다. 같은 말을 세 군데에 따로 적으면 반드시 어긋난다.
   * 아직 글이 없는 카테고리는 비워 둔다.
   */
  intro?: string;
  /**
   * 이 카테고리를 대표하는 글. 배열 순서가 곧 읽기 권장 순서다.
   * llms.txt는 이 목록을 본문에 싣고 나머지는 Optional로 내린다.
   */
  featured?: string[];
}

/**
 * 사이트 전체를 대표하는 글. 홈 상단 「추천 글」과 llms.txt의 「먼저 읽을 글」이
 * 같은 목록을 쓴다. 사람에게 먼저 권하는 글과 기계에게 먼저 권하는 글이 다를 이유가 없다.
 */
export const HOME_FEATURED = ['rsa', 'algo-orientation'];

export const categories: Category[] = [
  {
    slug: 'theory',
    label: '계산 이론',
    icon: '🧮',
    description: '오토마타, 튜링 머신, 복잡도 클래스 등 계산 이론의 수학적 기반을 다룹니다.',
    intro:
      '유한 오토마타에서 튜링 기계까지 계산 모델을 차례로 쌓아 올리고, 결정 가능성과 복잡도 클래스로 「풀 수 있는 문제」의 경계를 그립니다. 집합의 농도처럼 그 경계를 떠받치는 수학도 함께 다룹니다.',
    featured: ['problem-and-solution', 'dfa', 'turing-machine', 'classes'],
  },
  {
    slug: 'cryptography',
    label: '암호학',
    icon: '🔐',
    description: '정수론, 암호학적 프로토콜, 계산 복잡도의 응용을 탐구합니다.\n계산 이론 시리즈를 먼저 읽기를 권장합니다.',
    intro:
      '나눗셈 정리와 합동식, 페르마 소정리와 중국인의 나머지 정리에서 시작해 RSA·ElGamal·Diffie-Hellman을 직접 구성합니다. 해시와 전자 서명, 영지식 증명까지 이어집니다.',
    featured: ['gcd', 'modular', 'rsa', 'diffie-hellman', 'zero-knowledge'],
  },
  {
    slug: 'algorithm',
    label: '알고리즘',
    icon: '📊',
    description: '자료구조와 알고리즘 설계 및 분석을 다룹니다.',
    intro:
      '분할 정복·그리디·동적 계획법을 설계 전략으로 묶어 정리합니다. 정렬과 선택, 최단 경로와 최소 신장 트리, 가장 가까운 점 쌍과 볼록 껍질을 왜 그 방법이 옳은지까지 증명합니다.',
    featured: ['algo-orientation', 'divide-and-conquer', 'greedy', 'dp-1', 'convex-hull-1'],
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
