import { initialState, measure, move, dragTo, labelPositions, toSvg, LIMITS, formatNumber as fmt } from './point-vector-model.mjs';

const NS = 'http://www.w3.org/2000/svg';
const px = (x) => toSvg({ x, y: 0 }).x;
const py = (y) => toSvg({ x: 0, y }).y;
const pair = (v) => `(${fmt(v.x)}, ${fmt(v.y)})`;

export function mount(figure) {
  const live = figure.querySelector('.lab-live');
  const svg = live?.querySelector('svg');
  if (!svg) throw new Error('실험 SVG가 없습니다.');
  const get = (name) => {
    const element = svg.querySelector(`[data-part="${name}"]`);
    if (!element) throw new Error(`실험 요소 누락: ${name}`);
    return element;
  };
  const parts = Object.fromEntries(['grid', 'x-axis', 'y-axis', 'x-label', 'y-label', 'vector', 'a', 'b', 'o', 'label-a', 'label-b', 'label-o', 'summary']
    .map((name) => [name, get(name)]));
  const marker = parts.vector.getAttribute('marker-end');
  let state = initialState();
  let selected = 'a';
  let drag = null;
  const id = figure.dataset.labId;
  const controls = document.createElement('div');
  controls.className = 'lab-controls';
  controls.innerHTML = `
    <div class="lab-toolbar"><label for="${id}target">움직일 대상</label>
      <select id="${id}target"><option value="a">점 A</option><option value="b">점 B</option><option value="o">원점 O</option></select>
      <button type="button" class="lab-reset">처음으로</button></div>
    <p class="lab-input-note" id="${id}note"></p>
    <div class="lab-inputs">
      <label for="${id}x"><span>x <output data-value="x"></output></span><input id="${id}x" type="range" step="0.25" aria-describedby="${id}note" /></label>
      <label for="${id}y"><span>y <output data-value="y"></output></span><input id="${id}y" type="range" step="0.25" aria-describedby="${id}note" /></label>
    </div>
    <dl class="lab-readouts"><div><dt>점 A의 좌표</dt><dd data-value="a"></dd></div><div><dt>점 B의 좌표</dt><dd data-value="b"></dd></div><div><dt>변위 B − A</dt><dd data-value="delta"></dd></div><div><dt>두 점 사이 거리</dt><dd data-value="distance"></dd></div></dl>
    <p class="lab-input-note">거리값은 소수 둘째 자리까지 반올림합니다.</p>
    <p class="lab-status" role="status" aria-atomic="true"></p>`;
  const targetSelect = controls.querySelector('select');
  const note = controls.querySelector('.lab-input-note');
  const status = controls.querySelector('.lab-status');
  const inputs = { x: controls.querySelector(`#${id}x`), y: controls.querySelector(`#${id}y`) };
  const outputs = Object.fromEntries([...controls.querySelectorAll('[data-value]')].map((el) => [el.dataset.value, el]));
  const attrs = (node, values) => Object.entries(values).forEach(([k, v]) => node.setAttribute(k, String(v)));
  const drawGrid = () => {
    const fragment = document.createDocumentFragment();
    const line = (values, major = false) => {
      const el = document.createElementNS(NS, 'line');
      attrs(el, { ...values, stroke: major ? '#64748b' : '#475569', 'stroke-width': 1 });
      fragment.append(el);
    };
    const tick = (text, x, y, anchor) => {
      const el = document.createElementNS(NS, 'text');
      attrs(el, { x, y, fill: '#94a3b8', stroke: 'none', 'font-size': 20, 'text-anchor': anchor });
      el.textContent = fmt(text);
      fragment.append(el);
    };
    for (let n = -7; n <= 7; n++) {
      const x = state.o.x + n, y = state.o.y + n;
      if (x >= -1 && x <= 6) {
        line({ x1: px(x), x2: px(x), y1: py(6), y2: py(-1) });
        if (n !== 0) tick(n, px(x), Math.min(py(state.o.y) + 25, 410), 'middle');
      }
      if (y >= -1 && y <= 6) {
        line({ x1: px(-1), x2: px(6), y1: py(y), y2: py(y) });
        if (n !== 0) tick(n, px(state.o.x) - 13, py(y) + 7, 'end');
      }
    }
    parts.grid.replaceChildren(fragment);
  };
  const render = () => {
    const values = measure(state);
    drawGrid();
    attrs(parts['x-axis'], { y1: py(state.o.y), y2: py(state.o.y) });
    attrs(parts['y-axis'], { x1: px(state.o.x), x2: px(state.o.x) });
    attrs(parts['x-label'], { y: py(state.o.y) + 7 });
    attrs(parts['y-label'], { x: px(state.o.x) - 7 });
    const labels = labelPositions(state);
    for (const key of ['a', 'b', 'o']) {
      attrs(parts[key], { transform: `translate(${px(state[key].x)} ${py(state[key].y)})` });
      parts[key].classList.toggle('is-selected', key === selected);
      attrs(parts[`label-${key}`], labels[key]);
    }
    attrs(parts.vector, { x1: px(state.a.x), y1: py(state.a.y), x2: px(state.b.x), y2: py(state.b.y) });
    if (values.distance === 0) parts.vector.removeAttribute('marker-end');
    else parts.vector.setAttribute('marker-end', marker);
    for (const axis of ['x', 'y']) {
      const origin = selected === 'o';
      inputs[axis].min = origin ? LIMITS.originMin : LIMITS.min - state.o[axis];
      inputs[axis].max = origin ? LIMITS.originMax : LIMITS.max - state.o[axis];
      const value = state[selected][axis] - (origin ? 0 : state.o[axis]);
      inputs[axis].value = value;
      outputs[axis].textContent = fmt(value);
      inputs[axis].setAttribute('aria-label', `${origin ? '원점 O의 이동량' : `점 ${selected.toUpperCase()}의 좌표`} ${axis}`);
    }
    note.textContent = selected === 'o' ? '처음 원점에서의 이동량입니다. 두 점은 제자리에 있습니다.' : '현재 원점 O에서 읽은 좌표입니다. 한 칸의 길이는 1입니다.';
    outputs.a.textContent = pair(values.a);
    outputs.b.textContent = pair(values.b);
    outputs.delta.textContent = pair(values.delta);
    outputs.distance.textContent = fmt(values.distance) + (values.distance === 0 ? ' · 방향 없음' : '');
    const summary = `A ${pair(values.a)}, B ${pair(values.b)}. 변위 ${pair(values.delta)}, 거리 ${fmt(values.distance)}${values.distance === 0 ? '. 영벡터는 방향이 정해지지 않습니다' : ''}.`;
    svg.setAttribute('aria-label', summary);
    parts.summary.textContent = `변위 ${pair(values.delta)} · 거리 ${fmt(values.distance)}`;
    return summary;
  };
  const announce = () => { status.textContent = render(); };
  targetSelect.addEventListener('change', () => { selected = targetSelect.value; render(); });
  for (const axis of ['x', 'y']) {
    inputs[axis].addEventListener('input', () => {
      state = move(state, selected, axis, Number(inputs[axis].value) + (selected === 'o' ? 0 : state.o[axis]));
      render();
    });
    inputs[axis].addEventListener('change', announce);
  }
  controls.querySelector('button').addEventListener('click', () => {
    state = initialState(); selected = 'a'; targetSelect.value = selected; announce();
  });
  const pointerPosition = (event) => {
    const matrix = svg.getScreenCTM();
    if (!matrix) return null;
    return new DOMPoint(event.clientX, event.clientY).matrixTransform(matrix.inverse());
  };
  svg.addEventListener('pointerdown', (event) => {
    if (event.button !== 0 || drag) return;
    const handle = event.target.closest('[data-point]');
    const position = pointerPosition(event);
    if (!handle || !position) return;
    selected = handle.dataset.point; targetSelect.value = selected;
    drag = { pointer: event.pointerId, x: position.x - px(state[selected].x), y: position.y - py(state[selected].y) };
    svg.setPointerCapture(event.pointerId); render(); event.preventDefault();
  });
  svg.addEventListener('pointermove', (event) => {
    if (!drag || event.pointerId !== drag.pointer) return;
    const p = pointerPosition(event);
    if (!p) return;
    state = dragTo(state, selected, p, drag);
    render();
  });
  // Browsers read touch-action from the outer <svg>, not from its children, so the
  // CSS on [data-point] alone lets the page pan and cancel the drag on touch screens.
  // Blocking the default only for touches that start on a handle keeps page
  // scrolling for the rest of the figure.
  svg.addEventListener('touchstart', (event) => {
    if (event.target.closest?.('[data-point]')) event.preventDefault();
  }, { passive: false });
  const end = (event) => {
    if (!drag || event.pointerId !== drag.pointer) return;
    const pointer = drag.pointer; drag = null;
    if (svg.hasPointerCapture(pointer)) svg.releasePointerCapture(pointer);
    announce();
  };
  svg.addEventListener('pointerup', end);
  svg.addEventListener('pointercancel', end);
  svg.addEventListener('lostpointercapture', end);
  live.append(controls);
  render();
  live.hidden = false;
  figure.classList.add('is-live');
}
