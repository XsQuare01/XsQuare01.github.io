import { test } from 'node:test';
import assert from 'node:assert/strict';
import { rehypeSvgSteps } from './rehype-svg-steps.mjs';

// 테스트 파일은 package.json의 "test:js"에 경로를 직접 나열해 등록한다(글롭이 아니다).
// 글롭으로 걸어 두면 패턴이 하나도 안 맞을 때도 "tests 0, pass 0, fail 0"으로 조용히
// 종료 코드 0을 내기 때문이다 — 테스트가 하나도 안 돈 걸 성공으로 오인할 수 있다.
// 그러니 이 파일 옆에 새 *.test.mjs를 추가하면 "test:js" 스크립트에도 그 경로를 손으로 더해야 한다.

// rehypeFigureCaption이 만들어 둔 모양을 그대로 흉내낸다: figure.post-figure > (img, figcaption).
// wrapper div는 없다 — Astro는 rehype-raw를 사용자 rehype 플러그인 뒤에 돌리므로, 마크다운의
// raw HTML div는 이 단계에서 아직 파싱되지 않은 'raw' 문자열 노드다(className을 볼 수 없다).
// 그래서 이 플러그인은 대상을 wrapper 클래스가 아니라 파일명 규약(-steps.svg)으로 찾는다.
function tree(src, alt = '설명 문장') {
  return {
    type: 'root',
    children: [{
      type: 'element', tagName: 'figure', properties: { className: ['post-figure'] },
      children: [
        { type: 'element', tagName: 'img', properties: { src, alt }, children: [] },
        { type: 'element', tagName: 'figcaption', properties: {}, children: [{ type: 'text', value: alt }] },
      ],
    }],
  };
}

const run = (t) => { rehypeSvgSteps({ publicDir: 'test/fixtures' })(t); return t; };
const figure = (t) => t.children[0];
const classes = (fig) => fig.properties.className || [];

test('data-step이 있는 -steps.svg는 인라인 svg로 교체되고 figure는 svg-steps 클래스를 얻는다', () => {
  const fig = figure(run(tree('/ok-steps.svg')));
  const [first, second] = fig.children;
  assert.equal(first.tagName, 'svg');
  assert.equal(second.tagName, 'figcaption', 'figcaption은 그대로 남는다');
  assert.ok(classes(fig).includes('svg-steps'), 'figure가 svg-steps 클래스를 얻는다');
  const groups = first.children.filter((c) => c.tagName === 'g');
  assert.equal(groups.length, 2);
  assert.equal(groups[0].properties['data-step'], '1');
  assert.equal(groups[0].properties['data-step-label'], '첫 점을 놓는다');
});

test('alt는 접근 가능한 이름(role/aria-label)으로 옮겨진다', () => {
  const fig = figure(run(tree('/ok-steps.svg')));
  const svg = fig.children[0];
  assert.equal(svg.properties.role, 'img');
  assert.equal(svg.properties['aria-label'], '설명 문장');
});

test('data-step이 없는 -steps.svg는 img로 남고 figure는 클래스를 얻지 않는다', () => {
  const fig = figure(run(tree('/plain-steps.svg')));
  const svg = fig.children[0];
  assert.equal(svg.tagName, 'img', 'data-step이 없으면 교체하지 않는다');
  assert.ok(!classes(fig).includes('svg-steps'));
});

test('파일이 없으면 img로 남고 빌드를 깨지 않는다', () => {
  const fig = figure(run(tree('/does-not-exist-steps.svg')));
  const svg = fig.children[0];
  assert.equal(svg.tagName, 'img');
  assert.ok(!classes(fig).includes('svg-steps'));
});

test('src가 -steps.svg로 끝나지 않으면 건드리지 않는다(파일 내용이 유효해도)', () => {
  const fig = figure(run(tree('/other.svg')));
  const svg = fig.children[0];
  assert.equal(svg.tagName, 'img', '파일명 규약이 아니면 data-step 유무와 무관하게 무시한다');
  assert.ok(!classes(fig).includes('svg-steps'));
});

test('주석 안에 남은 data-step 초안은 단계로 세지 않는다', () => {
  const fig = figure(run(tree('/commented-steps.svg')));
  const svg = fig.children[0];
  assert.equal(svg.tagName, 'svg');
  const groups = svg.children.filter((c) => c.tagName === 'g');
  assert.equal(groups.length, 1, '주석 속 data-step="9"는 세지 않고 실제 그룹 하나만 남는다');
  assert.equal(groups[0].properties['data-step'], '1');
});

// data-step-label 값 안에 리터럴 '>'가 있으면 quote-unaware하게 [^>]*로 여는 태그를
// 훑을 때 그 '>'에서 태그가 잘려 나갔다(라벨이 빈 문자열이 되고 나머지가 stray text로
// <g> 안에 끼어들었다). 이제는 quote-aware하게 훑으므로 라벨이 그대로 살아야 한다 —
// 그래서 이 케이스는 "안전하게 거부"가 아니라 "정확히 파싱"을 골랐다: 값 안의 '>'는
// 합법적인 XML이고, 저작자가 라벨에 비교 연산자를 쓰지 못하게 막을 이유가 없다.
test("data-step-label 값 안의 리터럴 '>'는 태그를 자르지 않고 라벨로 그대로 파싱된다", () => {
  const fig = figure(run(tree('/gt-label-steps.svg')));
  const svg = fig.children[0];
  assert.equal(svg.tagName, 'svg', '거부하지 않고 인라인 svg로 교체된다');
  const groups = svg.children.filter((c) => c.tagName === 'g');
  assert.equal(groups.length, 2);
  assert.equal(groups[1].properties['data-step-label'], '외적 > 0', "'>' 이후가 잘리지 않는다");
  // stray text가 없어야 한다: 두 번째 그룹의 유일한 자식은 body를 감싼 raw 노드 하나뿐
  assert.equal(groups[1].children.length, 1);
});

// data-step="1a"처럼 값이 숫자가 아니면 groupRe가 그 <g>를 그룹으로 뽑아내지 못한다.
// 실제 data-step 속성 등장 횟수(2)와 뽑힌 그룹 수(1)가 어긋나므로, 잘못된 결과를
// 조용히 내보내는 대신 null을 돌려줘 호출자가 원래의 <img>로 되돌아가야 한다.
test('data-step 값이 숫자가 아니면 개수가 어긋나 img로 거부된다', () => {
  const fig = figure(run(tree('/malformed-step-steps.svg')));
  const svg = fig.children[0];
  assert.equal(svg.tagName, 'img', '개수 불일치로 안전하게 거부한다');
  assert.ok(!classes(fig).includes('svg-steps'));
});
