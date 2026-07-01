export type Difficulty = '입문' | '초급' | '중급' | '고급' | '심화';

const STARS: Record<Difficulty, string> = {
  입문: '★☆☆☆☆',
  초급: '★★☆☆☆',
  중급: '★★★☆☆',
  고급: '★★★★☆',
  심화: '★★★★★',
};

// 난이도 라벨을 별 5개 표기로 변환 (예: '중급' → '★★★☆☆')
export function difficultyStars(difficulty: Difficulty): string {
  return STARS[difficulty];
}
