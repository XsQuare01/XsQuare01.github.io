import {
  initialState, measure, layout, setAngle, grab, dragTo, distanceText, LIMITS, formatNumber as fmt,
} from './arm-forward-model.mjs';
import { pickHandle } from './pick-handle.mjs';
import { approx } from './readout.mjs';

const pair = (v) => `(${fmt(v.x)}, ${fmt(v.y)})`;
const near = (v) => approx(pair(v), v.x, v.y);
const nearNumber = (n) => approx(fmt(n), n);

export function mount(figure) {
  const live = figure.querySelector('.lab-live');
  const svg = live?.querySelector('svg');
  if (!svg) throw new Error('실험 SVG가 없습니다.');
  const get = (name) => {
    const element = svg.querySelector(`[data-part="${name}"]`);
    if (!element) throw new Error(`실험 요소 누락: ${name}`);
    return element;
  };
  const parts = Object.fromEntries(['link1', 'link2', 'reach', 'extension', 'arc1', 'arc2', 'handle-elbow', 'handle-tip', 'summary']
    .map((name) => [name, get(name)]));
  let state = initialState();
  let selected = 'tip';
  let drag = null;
  const id = figure.dataset.labId;
  const controls = document.createElement('div');
  controls.className = 'lab-controls';
  controls.innerHTML = `
    <div class="lab-toolbar"><span>두 관절의 각도</span>
      <button type="button" class="lab-reset">처음으로</button></div>
    <p class="lab-input-note" id="${id}note">θ<sub>1</sub>은 x축에서, θ<sub>2</sub>는 첫 링크의 방향(점선)에서 잽니다. 반시계 방향이 양수입니다.</p>
    <div class="lab-inputs">
      <label for="${id}t1"><span>θ<sub>1</sub> <output data-value="t1"></output></span><input id="${id}t1" type="range" min="${LIMITS.thetaMin}" max="${LIMITS.thetaMax}" step="${LIMITS.step}" aria-describedby="${id}note" /></label>
      <label for="${id}t2"><span>θ<sub>2</sub> <output data-value="t2"></output></span><input id="${id}t2" type="range" min="${LIMITS.thetaMin}" max="${LIMITS.thetaMax}" step="${LIMITS.step}" aria-describedby="${id}note" /></label>
    </div>
    <dl class="lab-readouts"><div><dt>팔꿈치 E</dt><dd data-value="elbow"></dd></div><div><dt>손끝 P</dt><dd data-value="tip"></dd></div><div><dt>둘째 링크의 방향 θ<sub>1</sub> + θ<sub>2</sub></dt><dd data-value="heading"></dd></div><div><dt>‖P‖</dt><dd data-value="d"></dd></div><div class="lab-wide"><dt>‖P‖² = L<sub>1</sub>² + L<sub>2</sub>² + 2L<sub>1</sub>L<sub>2</sub> cos θ<sub>2</sub></dt><dd data-value="d2"></dd></div></dl>
    <p class="lab-input-note">값은 소수 둘째 자리까지 반올림합니다.</p>
    <p class="lab-status" role="status" aria-atomic="true"></p>`;
  const status = controls.querySelector('.lab-status');
  const inputs = { theta1: controls.querySelector(`#${id}t1`), theta2: controls.querySelector(`#${id}t2`) };
  const outputs = Object.fromEntries([...controls.querySelectorAll('[data-value]')].map((el) => [el.dataset.value, el]));
  const attrs = (node, values) => Object.entries(values).forEach(([k, v]) => node.setAttribute(k, String(v)));
  const render = () => {
    const v = measure(state);
    const at = layout(state);
    for (const key of ['link1', 'link2', 'reach', 'extension']) attrs(parts[key], at[key]);
    attrs(parts.arc1, { d: at.arc1 });
    attrs(parts.arc2, { d: at.arc2 });
    attrs(parts['handle-elbow'], { transform: `translate(${at.handles.elbow.x} ${at.handles.elbow.y})` });
    attrs(parts['handle-tip'], { transform: `translate(${at.handles.tip.x} ${at.handles.tip.y})` });
    for (const key of ['elbow', 'tip']) parts[`handle-${key}`].classList.toggle('is-selected', drag !== null && key === selected);
    inputs.theta1.value = state.theta1;
    inputs.theta2.value = state.theta2;
    outputs.t1.textContent = `${fmt(state.theta1)}°`;
    outputs.t2.textContent = `${fmt(state.theta2)}°`;
    outputs.elbow.textContent = near(v.elbow);
    outputs.tip.textContent = near(v.tip);
    outputs.heading.textContent = `${fmt(v.heading2)}°`;
    outputs.d.textContent = nearNumber(v.d);
    outputs.d2.textContent = distanceText(state);
    const summary = `θ1 = ${fmt(state.theta1)}°, θ2 = ${fmt(state.theta2)}°. 팔꿈치 ${near(v.elbow)}, 손끝 ${near(v.tip)}.`;
    svg.setAttribute('aria-label', summary);
    parts.summary.textContent = `손끝 P ${near(v.tip)}`;
    return summary;
  };
  const announce = () => { status.textContent = render(); };
  for (const key of ['theta1', 'theta2']) {
    inputs[key].addEventListener('input', () => { state = setAngle(state, key, Number(inputs[key].value)); render(); });
    inputs[key].addEventListener('change', announce);
  }
  // A reset in the middle of a drag (another finger, or Enter) ends the drag too, so
  // the next pointermove cannot carry the old grab into the fresh state.
  controls.querySelector('button').addEventListener('click', () => {
    if (drag) {
      if (svg.hasPointerCapture(drag.pointer)) svg.releasePointerCapture(drag.pointer);
      drag = null;
    }
    state = initialState(); announce();
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
    const key = pickHandle(layout(state).handles, position, selected);
    if (!key) return;
    selected = key;
    drag = { pointer: event.pointerId, offset: grab(state, key, position) };
    svg.setPointerCapture(event.pointerId); render(); event.preventDefault();
  });
  svg.addEventListener('pointermove', (event) => {
    if (!drag || event.pointerId !== drag.pointer) return;
    const position = pointerPosition(event);
    if (!position) return;
    state = dragTo(state, selected, position, drag.offset);
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
