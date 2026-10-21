import { initialState, measure, move, dragTo, layout, dotText, cosText, LIMITS, formatNumber as fmt } from './vector-projection-model.mjs';
import { pickHandle } from './pick-handle.mjs';
import { relation } from './readout.mjs';

const pair = (v) => `(${fmt(v.x)}, ${fmt(v.y)})`;
const NAMES = { a: '화살표 a의 성분', d: '방향 점 D의 좌표' };
const RANGES = { a: [LIMITS.min, LIMITS.max], d: [LIMITS.dirMin, LIMITS.dirMax] };

export function mount(figure) {
  const live = figure.querySelector('.lab-live');
  const svg = live?.querySelector('svg');
  if (!svg) throw new Error('실험 SVG가 없습니다.');
  const get = (name) => {
    const element = svg.querySelector(`[data-part="${name}"]`);
    if (!element) throw new Error(`실험 요소 누락: ${name}`);
    return element;
  };
  const parts = Object.fromEntries(['ell', 'shadow', 'rest', 'right-angle', 'a', 'u', 'foot', 'handle-a', 'handle-d', 'summary']
    .map((name) => [name, get(name)]));
  // data-marker keeps the arrowhead reference even when the first frame draws an
  // arrow too short for one; the plugin prefixes it along with marker-end.
  const marker = parts.a.getAttribute('data-marker');
  let state = initialState();
  let selected = 'a';
  let drag = null;
  const id = figure.dataset.labId;
  const controls = document.createElement('div');
  controls.className = 'lab-controls';
  controls.innerHTML = `
    <div class="lab-toolbar"><label for="${id}target">움직일 대상</label>
      <select id="${id}target"><option value="a">a (파란 점)</option><option value="d">방향 점 D (흰 마름모)</option></select>
      <button type="button" class="lab-reset">처음으로</button></div>
    <p class="lab-input-note" id="${id}note"></p>
    <div class="lab-inputs">
      <label for="${id}x"><span>x <output data-value="x"></output></span><input id="${id}x" type="range" step="${LIMITS.step}" aria-describedby="${id}note" /></label>
      <label for="${id}y"><span>y <output data-value="y"></output></span><input id="${id}y" type="range" step="${LIMITS.step}" aria-describedby="${id}note" /></label>
    </div>
    <dl class="lab-readouts"><div><dt>a</dt><dd data-value="a"></dd></div><div><dt>u = D / ‖D‖</dt><dd data-value="u"></dd></div><div><dt>a · u</dt><dd data-value="dot"></dd></div><div><dt>‖a‖ cos φ</dt><dd data-value="cos"></dd></div><div><dt>정사영 (a · u) u</dt><dd data-value="proj"></dd></div><div><dt>나머지 a − (a · u) u</dt><dd data-value="rest"></dd></div></dl>
    <p class="lab-input-note">값은 소수 둘째 자리까지 반올림합니다.</p>
    <p class="lab-status" role="status" aria-atomic="true"></p>`;
  const targetSelect = controls.querySelector('select');
  const note = controls.querySelector(`#${id}note`);
  const status = controls.querySelector('.lab-status');
  const inputs = { x: controls.querySelector(`#${id}x`), y: controls.querySelector(`#${id}y`) };
  const outputs = Object.fromEntries([...controls.querySelectorAll('[data-value]')].map((el) => [el.dataset.value, el]));
  const attrs = (node, values) => Object.entries(values).forEach(([k, v]) => node.setAttribute(k, String(v)));
  const render = () => {
    const v = measure(state);
    const at = layout(state);
    attrs(parts.ell, { x1: at.ell.from.x, y1: at.ell.from.y, x2: at.ell.to.x, y2: at.ell.to.y });
    attrs(parts.shadow, { x2: at.foot.x, y2: at.foot.y });
    attrs(parts.rest, { x1: at.foot.x, y1: at.foot.y, x2: at.a.x, y2: at.a.y });
    attrs(parts['right-angle'], { d: at.rightAngle });
    attrs(parts.a, { x2: at.a.x, y2: at.a.y });
    if (at.a.head) parts.a.setAttribute('marker-end', marker);
    else parts.a.removeAttribute('marker-end');
    attrs(parts.u, { x1: at.u.from.x, y1: at.u.from.y, x2: at.u.to.x, y2: at.u.to.y });
    attrs(parts.foot, { cx: at.foot.x, cy: at.foot.y });
    attrs(parts['handle-a'], { transform: `translate(${at.a.x} ${at.a.y})` });
    attrs(parts['handle-d'], { transform: `translate(${at.d.x} ${at.d.y})` });
    for (const key of ['a', 'd']) parts[`handle-${key}`].classList.toggle('is-selected', key === selected);
    for (const axis of ['x', 'y']) {
      [inputs[axis].min, inputs[axis].max] = RANGES[selected];
      inputs[axis].value = state[selected][axis];
      outputs[axis].textContent = fmt(state[selected][axis]);
      inputs[axis].setAttribute('aria-label', `${NAMES[selected]} ${axis}`);
    }
    note.textContent = selected === 'a'
      ? '화살표 a의 성분입니다. 한 칸의 길이는 1입니다.'
      : '방향 점 D의 좌표입니다. 방향만 쓰므로 D를 원점에 둘 수는 없습니다.';
    outputs.a.textContent = pair(state.a);
    outputs.u.textContent = pair(v.u);
    outputs.dot.textContent = dotText(state);
    outputs.cos.textContent = cosText(state);
    outputs.proj.textContent = pair(v.proj);
    outputs.rest.textContent = `${pair(v.rest)}, 길이 ${fmt(v.lengths.rest)}`;
    const sign = relation(v.s);
    const summary = `a ${pair(state.a)}, u ${pair(v.u)}. a · u ${sign} ${fmt(v.s)}, 정사영 ${pair(v.proj)}, 나머지 ${pair(v.rest)}.`;
    svg.setAttribute('aria-label', summary);
    parts.summary.textContent = `a · u ${sign} ${fmt(v.s)}, 정사영 ${pair(v.proj)}`;
    return summary;
  };
  const announce = () => { status.textContent = render(); };
  targetSelect.addEventListener('change', () => { selected = targetSelect.value; render(); });
  for (const axis of ['x', 'y']) {
    inputs[axis].addEventListener('input', () => { state = move(state, selected, axis, Number(inputs[axis].value)); render(); });
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
    if (event.button !== 0 || drag || !event.target.closest('[data-point]')) return;
    const position = pointerPosition(event);
    if (!position) return;
    const at = layout(state);
    const handles = { a: at.a, d: at.d };
    const key = pickHandle(handles, position, selected);
    if (!key) return;
    selected = key; targetSelect.value = selected;
    drag = { pointer: event.pointerId, x: position.x - handles[key].x, y: position.y - handles[key].y };
    svg.setPointerCapture(event.pointerId); render(); event.preventDefault();
  });
  svg.addEventListener('pointermove', (event) => {
    if (!drag || event.pointerId !== drag.pointer) return;
    const position = pointerPosition(event);
    if (!position) return;
    state = dragTo(state, selected, position, drag);
    render();
  });
  const end = (event) => {
    if (!drag || event.pointerId !== drag.pointer) return;
    const pointer = drag.pointer; drag = null;
    if (svg.hasPointerCapture(pointer)) svg.releasePointerCapture(pointer);
    announce();
  };
  svg.addEventListener('pointerup', end);
  svg.addEventListener('pointercancel', end);
  svg.addEventListener('lostpointercapture', end);
  // Browsers read touch-action from the outer <svg>, not from its children, so a
  // touch that starts on a handle must cancel page panning here (see SVG_LABS.md).
  svg.addEventListener('touchstart', (event) => {
    if (event.target.closest?.('[data-point]')) event.preventDefault();
  }, { passive: false });
  live.append(controls);
  render();
  live.hidden = false;
  figure.classList.add('is-live');
}
