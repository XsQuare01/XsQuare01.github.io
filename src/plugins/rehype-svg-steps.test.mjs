import { test } from 'node:test';
import assert from 'node:assert/strict';
import { rehypeSvgSteps } from './rehype-svg-steps.mjs';

// 테스트 파일은 package.json의 "test:js"에 경로를 직접 나열해 등록한다(글롭이 아니다).
// 글롭으로 걸어 두면 패턴이 하나도 안 맞을 때도 "tests 0, pass 0, fail 0"으로 조용히
// 종료 코드 0을 내기 때문이다 — 테스트가 하나도 안 돈 걸 성공으로 오인할 수 있다.
// 그러니 이 파일 옆에 새 *.test.mjs를 추가하면 "test:js" 스크립트에도 그 경로를 손으로 더해야 한다.

// 이 테스트가 이 플러그인을 확인하는 주된 수단인 이유가 하나 더 있다. 플러그인만 고치고
// npm run build를 돌리면 Astro가 이전 렌더 결과를 캐시에서 그대로 쓴다 — 글 파일의 digest가
// 안 바뀌었으므로 다시 렌더할 이유가 없다고 보기 때문이다. 그래서 dist를 열어 봐도 예전
// 출력이 보이고, 초록인 빌드가 확인처럼 보인다. dist로 확인하려면 대상 글의 내용을 한 글자라도
// 바꿔 digest를 흔들어야 한다(CI는 캐시 없이 돌므로 영향받지 않는다).

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

// 인라인되면 SVG 내부 id가 페이지 전역 이름이 된다. 아래 여섯 개는 그 id를 파일 경로에서
// 만든 접두어로 격리하는 동작을 붙잡는다. 접두어의 근거가 문서 순서가 아니라 경로이므로,
// 기대값을 파일명에서 그대로 읽을 수 있다(/marker-steps.svg → marker-steps-).
const restOf = (svg) => svg.children[0].value;
const bodyOf = (svg, step) => svg.children[step].children[0].value;

test('id와 그 참조에 파일 경로에서 만든 접두어가 붙는다', () => {
  const svg = figure(run(tree('/marker-steps.svg'))).children[0];
  assert.match(restOf(svg), /<marker id="marker-steps-tip"/, '정의에 접두어가 붙는다');
  assert.doesNotMatch(restOf(svg), /id="tip"/, '접두어 없는 정의가 남지 않는다');
  assert.match(bodyOf(svg, 2), /marker-end="url\(#marker-steps-tip\)"/, '단계 안의 참조도 따라간다');
});

// 이 동작이 필요한 이유가 정확히 이 상황이다. 두 파일이 각자 <marker id="tip">을 정의하면
// 인라인 후 url(#tip)이 문서 순서상 첫 정의로 해석되어 둘째 도식의 화살촉이 바뀐다.
test('같은 id를 쓰는 도식 둘이 한 페이지에 있어도 이름이 갈린다', () => {
  const t = tree('/marker-steps.svg');
  t.children.push(tree('/marker2-steps.svg').children[0]);
  run(t);
  const ids = t.children.map((fig) => restOf(fig.children[0]).match(/id="([^"]+)"/)[1]);
  assert.deepEqual(ids, ['marker-steps-tip', 'marker2-steps-tip']);
});

test('href·xlink:href·aria-describedby도 함께 재작성된다', () => {
  const svg = figure(run(tree('/refs-steps.svg'))).children[0];
  assert.match(restOf(svg), /<text id="refs-steps-lbl"/);
  assert.match(restOf(svg), /<desc id="refs-steps-note"/);
  assert.match(bodyOf(svg, 1), /<use href="#refs-steps-lbl"/);
  assert.match(bodyOf(svg, 1), /xlink:href="#refs-steps-lbl"/);
  assert.match(bodyOf(svg, 1), /aria-describedby="refs-steps-note"/);
});

// 접두어를 붙이면 깨지는 두 경우. 바깥 URL의 fragment는 이 도식의 id가 아니고, 정의되지
// 않은 id를 가리키는 참조는 도식 밖의 무언가를 가리키려던 것일 수 있다. 둘 다 그대로 둔다.
test('바깥 URL의 fragment와 정의 없는 참조는 건드리지 않는다', () => {
  const svg = figure(run(tree('/refs-steps.svg'))).children[0];
  assert.match(bodyOf(svg, 2), /href="https:\/\/example\.com\/#lbl"/);
  assert.match(bodyOf(svg, 2), /url\(#absent\)/);
});

// 겹따옴표 규약을 어긴 id는 재작성 대상에서 빠지므로 접두어 없이 페이지에 나간다.
// 조용히 충돌할 수 있는 결과를 내보내는 대신 개수 검사로 잡아 img로 되돌아간다.
test('홑따옴표 id는 개수가 어긋나 img로 거부된다', () => {
  const fig = figure(run(tree('/quoted-id-steps.svg')));
  assert.equal(fig.children[0].tagName, 'img');
  assert.ok(!classes(fig).includes('svg-steps'));
});

// url( #tip )처럼 우리 세 패턴이 못 잡는 참조 형태. 정의만 접두어를 얻고 참조는 남으면
// 화살촉이 사라진 선이 나가므로, 결과를 다시 읽어 확인하고 거부한다.
test('접두어를 붙이지 못한 참조가 남으면 img로 거부된다', () => {
  const fig = figure(run(tree('/spaced-ref-steps.svg')));
  assert.equal(fig.children[0].tagName, 'img');
  assert.ok(!classes(fig).includes('svg-steps'));
});

test('파일명이 숫자로 시작해도 id로 쓸 수 있는 접두어를 만든다', () => {
  const svg = figure(run(tree('/9-digit-steps.svg'))).children[0];
  assert.match(restOf(svg), /id="svg-9-digit-steps-tip"/, 'XML Name은 숫자로 시작할 수 없다');
  assert.match(bodyOf(svg, 1), /url\(#svg-9-digit-steps-tip\)/);
});

// 이 저장소의 도식은 id를 arr·arr-red처럼 짓는다 — 한쪽이 다른 쪽의 앞부분이다.
// 재작성 패턴이 뒤끝을 닫아 두지 않으면 짧은 id 차례에 긴 참조가 잘려 나간다.
test('한 id가 다른 id의 앞부분이어도 참조가 어긋나지 않는다', () => {
  const svg = figure(run(tree('/nested-id-steps.svg'))).children[0];
  assert.match(restOf(svg), /id="nested-id-steps-arr"/);
  assert.match(restOf(svg), /id="nested-id-steps-arr-red"/);
  assert.match(bodyOf(svg, 1), /marker-end="url\(#nested-id-steps-arr\)"/);
  assert.match(bodyOf(svg, 2), /marker-end="url\(#nested-id-steps-arr-red\)"/);
});
