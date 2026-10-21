import { initialState, measure, move, dragTo, layout, lengthSumText, LIMITS, formatNumber as fmt } from './vector-sum-model.mjs';
import { pickHandle } from './pick-handle.mjs';

const pair = (v) => `(${fmt(v.x)}, ${fmt(v.y)})`;
const NAMES = { a: '화살표 a', b: '화살표 b' };

export function mount(figure) {
  const live = figure.querySelector('.lab-live');
  const svg = live?.querySelector('svg');
  if (!svg) throw new Error('실험 SVG가 없습니다.');
  const get = (name) => {
    const element = svg.querySelector(`[data-part="${name}"]`);
    if (!element) throw new Error(`실험 요소 누락: ${name}`);
    return element;
  };
  const parts = Object.fromEntries(['a', 'b', 'sum', 'b-first', 'a-second', 'handle-a', 'handle-b', 'summary']
    .map((name) => [name, get(name)]));
  // data-marker keeps the arrowhead reference even when the first frame draws an
  // arrow too short for one; the plugin prefixes it along with marker-end.
  const markers = Object.fromEntries(['a', 'b', 'sum'].map((key) => [key, parts[key].getAttribute('data-marker')]));
  let state = initialState();
  let selected = 'a';
  let drag = null;
  const id = figure.dataset.labId;
  const controls = document.createElement('div');
  controls.className = 'lab-controls';
  controls.innerHTML = `
    <div class="lab-toolbar"><label for="${id}target">바꿀 화살표</label>
      <select id="${id}target"><option value="a">a (파란 점)</option><option value="b">b (보라 마름모)</option></select>
      <button type="button" class="lab-reset">처음으로</button></div>
    <p class="lab-input-note" id="${id}note">고른 화살표의 성분입니다. 한 칸의 길이는 1입니다.</p>
    <div class="lab-inputs">
      <label for="${id}x"><span>x 성분 <output data-value="x"></output></span><input id="${id}x" type="range" min="${LIMITS.min}" max="${LIMITS.max}" step="${LIMITS.step}" aria-describedby="${id}note" /></label>
      <label for="${id}y"><span>y 성분 <output data-value="y"></output></span><input id="${id}y" type="range" min="${LIMITS.min}" max="${LIMITS.max}" step="${LIMITS.step}" aria-describedby="${id}note" /></label>
    </div>
    <dl class="lab-readouts"><div><dt>a</dt><dd data-value="a"></dd></div><div><dt>b</dt><dd data-value="b"></dd></div><div><dt>a + b</dt><dd data-value="sum"></dd></div><div><dt>‖a‖ + ‖b‖</dt><dd data-value="lengths"></dd></div><div><dt>‖a + b‖</dt><dd data-value="sum-length"></dd></div></dl>
    <p class="lab-input-note">길이는 소수 둘째 자리까지 반올림합니다.</p>
    <p class="lab-status" role="status" aria-atomic="true"></p>`;
  const targetSelect = controls.querySelector('select');
  const status = controls.querySelector('.lab-status');
  const inputs = { x: controls.querySelector(`#${id}x`), y: controls.querySelector(`#${id}y`) };
  const outputs = Object.fromEntries([...controls.querySelectorAll('[data-value]')].map((el) => [el.dataset.value, el]));
  const attrs = (node, values) => Object.entries(values).forEach(([k, v]) => node.setAttribute(k, String(v)));
  const line = (node, { x1, y1, x2, y2 }) => attrs(node, { x1, y1, x2, y2 });
  const render = () => {
    const { sum, lengths } = measure(state);
    const at = layout(state);
    for (const [key, segment] of [['a', at.a], ['b', at.b], ['sum', at.sum]]) {
      line(parts[key], segment);
      if (segment.head) parts[key].setAttribute('marker-end', markers[key]);
      else parts[key].removeAttribute('marker-end');
    }
    line(parts['b-first'], at.bFirst);
    line(parts['a-second'], at.aSecond);
    for (const key of ['a', 'b']) {
      attrs(parts[`handle-${key}`], { transform: `translate(${at.handles[key].x} ${at.handles[key].y})` });
      parts[`handle-${key}`].classList.toggle('is-selected', key === selected);
    }
    for (const axis of ['x', 'y']) {
      inputs[axis].value = state[selected][axis];
      outputs[axis].textContent = fmt(state[selected][axis]);
      inputs[axis].setAttribute('aria-label', `${NAMES[selected]}의 ${axis} 성분`);
    }
    outputs.a.textContent = pair(state.a);
    outputs.b.textContent = pair(state.b);
    outputs.sum.textContent = pair(sum);
    outputs.lengths.textContent = lengthSumText(state);
    outputs['sum-length'].textContent = fmt(lengths.sum);
    const summary = `a ${pair(state.a)}, b ${pair(state.b)}. a + b ${pair(sum)}, 길이 ${fmt(lengths.sum)}. 두 길이의 합은 ${fmt(lengths.a + lengths.b)}.`;
    svg.setAttribute('aria-label', summary);
    parts.summary.textContent = `a + b = ${pair(sum)}, 길이 ${fmt(lengths.sum)}`;
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
    const { handles } = layout(state);
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
