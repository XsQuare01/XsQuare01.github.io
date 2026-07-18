// 강조 단 하나 (#43) — 태그·배지는 모두 잉크블루 단색으로 통일한다.
// 색은 테마 토큰(--accent)을 참조해 라이트/다크에 자동 적응한다.
const TAG_STYLE = {
  bg: 'var(--accent-dim)',
  border: 'color-mix(in srgb, var(--accent) 32%, transparent)',
  text: 'var(--accent)',
};

export function getTagColor(_tag: string) {
  return TAG_STYLE;
}

export function tagStyle(_tag: string): string {
  return `background:${TAG_STYLE.bg};border-color:${TAG_STYLE.border};color:${TAG_STYLE.text};`;
}
