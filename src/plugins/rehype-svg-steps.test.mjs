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
