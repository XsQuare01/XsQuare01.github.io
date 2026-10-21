import { initialState, measure, layout, setAngle, setLength, dragTip, LIMITS, formatNumber as fmt } from './rod-angle-model.mjs';

const pair = (x, y) => `(${fmt(x)}, ${fmt(y)})`;

export function mount(figure) {
  const live = figure.querySelector('.lab-live');
  const svg = live?.querySelector('svg');
  if (!svg) throw new Error('실험 SVG가 없습니다.');
  const get = (name) => {
    const element = svg.querySelector(`[data-part="${name}"]`);
    if (!element) throw new Error(`실험 요소 누락: ${name}`);
    return element;
  };
  const parts = Object.fromEntries(['rod', 'x-part', 'y-part', 'arc', 'unit-dot', 'p', 'label-p', 'label-theta', 'summary']
    .map((name) => [name, get(name)]));
  let state = initialState();
  let drag = null;
  const id = figure.dataset.labId;
  const controls = document.createElement('div');
  controls.className = 'lab-controls';
  controls.innerHTML = `
    <div class="lab-toolbar"><span>막대의 각도와 길이</span>
      <button type="button" class="lab-reset">처음으로</button></div>
    <p class="lab-input-note" id="${id}note">각도는 x축 양의 방향에서 잽니다. 반시계 방향이 양수입니다.</p>
    <div class="lab-inputs">
      <label for="${id}theta"><span>각도 θ <output data-value="theta"></output></span><input id="${id}theta" type="range" min="${LIMITS.thetaMin}" max="${LIMITS.thetaMax}" step="${LIMITS.thetaStep}" aria-describedby="${id}note" /></label>
      <label for="${id}length"><span>길이 L <output data-value="length"></output></span><input id="${id}length" type="range" min="${LIMITS.lengthMin}" max="${LIMITS.lengthMax}" step="${LIMITS.lengthStep}" /></label>
    </div>
    <dl class="lab-readouts"><div><dt>각도 (라디안)</dt><dd data-value="rad"></dd></div><div><dt>끝점 (x, y)</dt><dd data-value="tip"></dd></div><div><dt>cos θ</dt><dd data-value="cos"></dd></div><div><dt>sin θ</dt><dd data-value="sin"></dd></div></dl>
    <p class="lab-input-note">값은 소수 둘째 자리까지 반올림합니다.</p>
    <p class="lab-status" role="status" aria-atomic="true"></p>`;
  const status = controls.querySelector('.lab-status');
  const inputs = { theta: controls.querySelector(`#${id}theta`), length: controls.querySelector(`#${id}length`) };
  const outputs = Object.fromEntries([...controls.querySelectorAll('[data-value]')].map((el) => [el.dataset.value, el]));
  const attrs = (node, values) => Object.entries(values).forEach(([k, v]) => node.setAttribute(k, String(v)));
  const render = () => {
    const v = measure(state);
    const at = layout(state);
    attrs(parts.rod, { x2: at.tip.x, y2: at.tip.y });
    attrs(parts['x-part'], { x2: at.tip.x });
    attrs(parts['y-part'], { x1: at.tip.x, x2: at.tip.x, y2: at.tip.y });
    attrs(parts.p, { transform: `translate(${at.tip.x} ${at.tip.y})` });
    attrs(parts['unit-dot'], { cx: at.unit.x, cy: at.unit.y });
    attrs(parts.arc, { d: at.arc });
    attrs(parts['label-p'], at.labels.p);
    // The model hides θ when the arc is too small to name or no spot is clear;
    // the readouts below always show the angle.
    const { visible, ...thetaLabel } = at.labels.theta;
    attrs(parts['label-theta'], { ...thetaLabel, visibility: visible ? 'visible' : 'hidden' });
    inputs.theta.value = state.theta;
    inputs.length.value = state.length;
    outputs.theta.textContent = `${fmt(state.theta)}°`;
    outputs.length.textContent = fmt(state.length);
    outputs.rad.textContent = `${fmt(v.rad)} rad`;
    outputs.tip.textContent = pair(v.x, v.y);
    outputs.cos.textContent = fmt(v.cos);
    outputs.sin.textContent = fmt(v.sin);
    const summary = `θ = ${fmt(state.theta)}°(${fmt(v.rad)} 라디안), L = ${fmt(state.length)}. 끝점 ${pair(v.x, v.y)}, cos θ = ${fmt(v.cos)}, sin θ = ${fmt(v.sin)}.`;
    svg.setAttribute('aria-label', summary);
    parts.summary.textContent = `θ = ${fmt(state.theta)}° · 끝점 ${pair(v.x, v.y)}`;
    return summary;
  };
  const announce = () => { status.textContent = render(); };
  inputs.theta.addEventListener('input', () => { state = setAngle(state, Number(inputs.theta.value)); render(); });
  inputs.length.addEventListener('input', () => { state = setLength(state, Number(inputs.length.value)); render(); });
  for (const input of Object.values(inputs)) input.addEventListener('change', announce);
  controls.querySelector('button').addEventListener('click', () => { state = initialState(); announce(); });
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
    const { tip } = layout(state);
    drag = { pointer: event.pointerId, x: position.x - tip.x, y: position.y - tip.y };
    parts.p.classList.add('is-selected');
    svg.setPointerCapture(event.pointerId); event.preventDefault();
  });
  svg.addEventListener('pointermove', (event) => {
    if (!drag || event.pointerId !== drag.pointer) return;
    const position = pointerPosition(event);
    if (!position) return;
    state = dragTip(state, position, drag);
    render();
  });
  const end = (event) => {
    if (!drag || event.pointerId !== drag.pointer) return;
    const pointer = drag.pointer; drag = null;
    parts.p.classList.remove('is-selected');
    if (svg.hasPointerCapture(pointer)) svg.releasePointerCapture(pointer);
    announce();
  };
  svg.addEventListener('pointerup', end);
  svg.addEventListener('pointercancel', end);
  svg.addEventListener('lostpointercapture', end);
  // Browsers read touch-action from the outer <svg>, not from its children, so a
  // touch that starts on the tip must cancel page panning here (see SVG_LABS.md).
  svg.addEventListener('touchstart', (event) => {
    if (event.target.closest?.('[data-point]')) event.preventDefault();
  }, { passive: false });
  live.append(controls);
  render();
  live.hidden = false;
  figure.classList.add('is-live');
}
