import {
  initialState, measure, layout, setAngle, setCoord, rodGrab, dragRod, dragPoint, matrixText, combinationText,
  LIMITS, formatNumber as fmt,
} from './rotation-matrix-model.mjs';
import { pickHandle } from './pick-handle.mjs';
import { relation } from './readout.mjs';

const pair = (v) => `(${fmt(v.x)}, ${fmt(v.y)})`;
const TEXTS = ['theta', 'm11', 'm12', 'm21', 'm22', 's1', 's2', 'p1', 'p2', 'rel'];

export function mount(figure) {
  const live = figure.querySelector('.lab-live');
  const svg = live?.querySelector('svg');
  if (!svg) throw new Error('실험 SVG가 없습니다.');
  const get = (name) => {
    const element = svg.querySelector(`[data-part="${name}"]`);
    if (!element) throw new Error(`실험 요소 누락: ${name}`);
    return element;
  };
  const parts = Object.fromEntries(['grid-frame', 'frame', 'chain-x', 'chain-y', 'arrow-p', 'handle-p', 'handle-rod', ...TEXTS]
    .map((name) => [name, get(name)]));
  // data-marker keeps the arrowhead reference even when the first frame draws an
  // arrow too short for one; the plugin prefixes it along with marker-end.
  const marker = parts['arrow-p'].getAttribute('data-marker');
  let state = initialState();
  let selected = 'p';
  let drag = null;
  const id = figure.dataset.labId;
  const controls = document.createElement('div');
  controls.className = 'lab-controls';
  controls.innerHTML = `
    <div class="lab-toolbar"><span>막대의 각도와 집게 끝의 막대 좌표</span>
      <button type="button" class="lab-reset">처음으로</button></div>
    <p class="lab-input-note" id="${id}note">각도는 x축 양의 방향에서 잽니다. 반시계 방향이 양수입니다. 막대 좌표는 막대를 따라 s<sub>x</sub>, 막대 왼쪽으로 s<sub>y</sub>만큼 간 자리입니다.</p>
    <div class="lab-inputs">
      <label class="lab-wide" for="${id}theta"><span>각도 θ <output data-value="theta"></output></span><input id="${id}theta" type="range" min="${LIMITS.thetaMin}" max="${LIMITS.thetaMax}" step="${LIMITS.thetaStep}" aria-describedby="${id}note" /></label>
      <label for="${id}sx"><span>막대 좌표 s<sub>x</sub> <output data-value="sx"></output></span><input id="${id}sx" type="range" min="${LIMITS.min}" max="${LIMITS.max}" step="${LIMITS.step}" aria-describedby="${id}note" /></label>
      <label for="${id}sy"><span>막대 좌표 s<sub>y</sub> <output data-value="sy"></output></span><input id="${id}sy" type="range" min="${LIMITS.min}" max="${LIMITS.max}" step="${LIMITS.step}" aria-describedby="${id}note" /></label>
    </div>
    <dl class="lab-readouts"><div><dt>각도 (라디안)</dt><dd data-value="rad"></dd></div><div><dt>막대 좌표 (s<sub>x</sub>, s<sub>y</sub>)</dt><dd data-value="s"></dd></div><div><dt>첫째 열 e′<sub>x</sub> = (cos θ, sin θ)</dt><dd data-value="ex"></dd></div><div><dt>둘째 열 e′<sub>y</sub> = (−sin θ, cos θ)</dt><dd data-value="ey"></dd></div><div class="lab-wide"><dt>고정 좌표 p = s<sub>x</sub>e′<sub>x</sub> + s<sub>y</sub>e′<sub>y</sub></dt><dd data-value="p"></dd></div><div class="lab-wide"><dt>길이</dt><dd data-value="length"></dd></div></dl>
    <p class="lab-input-note">값은 소수 둘째 자리까지 반올림합니다.</p>
    <p class="lab-status" role="status" aria-atomic="true"></p>`;
  const status = controls.querySelector('.lab-status');
  const inputs = { theta: controls.querySelector(`#${id}theta`), x: controls.querySelector(`#${id}sx`), y: controls.querySelector(`#${id}sy`) };
  const outputs = Object.fromEntries([...controls.querySelectorAll('[data-value]')].map((el) => [el.dataset.value, el]));
  const attrs = (node, values) => Object.entries(values).forEach(([k, v]) => node.setAttribute(k, String(v)));
  const render = () => {
    const v = measure(state);
    const at = layout(state);
    const m = matrixText(state);
    attrs(parts['grid-frame'], { transform: at.turn });
    attrs(parts.frame, { transform: at.turn });
    attrs(parts['chain-x'], at.chainX);
    attrs(parts['chain-y'], at.chainY);
    attrs(parts['arrow-p'], { x2: at.arrow.x2, y2: at.arrow.y2 });
    if (at.arrow.head) parts['arrow-p'].setAttribute('marker-end', marker);
    else parts['arrow-p'].removeAttribute('marker-end');
    attrs(parts['handle-p'], { transform: `translate(${at.handleP.x} ${at.handleP.y})` });
    for (const key of ['p', 'rod']) parts[`handle-${key}`].classList.toggle('is-selected', drag !== null && key === selected);
    const texts = {
      theta: `θ = ${fmt(state.theta)}°`,
      m11: m.m[0][0], m12: m.m[0][1], m21: m.m[1][0], m22: m.m[1][1],
      s1: m.s[0], s2: m.s[1], p1: m.p[0], p2: m.p[1], rel: m.rel,
    };
    for (const name of TEXTS) parts[name].textContent = texts[name];
    inputs.theta.value = state.theta;
    inputs.x.value = state.s.x;
    inputs.y.value = state.s.y;
    outputs.theta.textContent = `${fmt(state.theta)}°`;
    outputs.sx.textContent = fmt(state.s.x);
    outputs.sy.textContent = fmt(state.s.y);
    outputs.rad.textContent = `${fmt(v.rad)} rad`;
    outputs.s.textContent = pair(state.s);
    outputs.ex.textContent = pair(v.ex);
    outputs.ey.textContent = pair(v.ey);
    outputs.p.textContent = combinationText(state);
    outputs.length.textContent = `‖p‖ = ‖s‖ ${relation(v.length)} ${fmt(v.length)}`;
    // Every rounded pair is marked ≈, the same rule as the readout equations.
    const near = (u) => `${relation(u.x, u.y)} ${pair(u)}`;
    const summary = `θ = ${fmt(state.theta)}°. 막대 좌표 ${pair(state.s)}, 고정 좌표 ${near(v.p)}. 첫째 열 ${near(v.ex)}, 둘째 열 ${near(v.ey)}.`;
    svg.setAttribute('aria-label', summary);
    return summary;
  };
  const announce = () => { status.textContent = render(); };
  inputs.theta.addEventListener('input', () => { state = setAngle(state, Number(inputs.theta.value)); render(); });
  for (const axis of ['x', 'y']) {
    inputs[axis].addEventListener('input', () => { state = setCoord(state, axis, Number(inputs[axis].value)); render(); });
  }
  for (const input of Object.values(inputs)) input.addEventListener('change', announce);
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
    const { handles } = layout(state);
    const key = pickHandle(handles, position, selected);
    if (!key) return;
    selected = key;
    drag = key === 'rod'
      ? { pointer: event.pointerId, offset: rodGrab(state, position) }
      : { pointer: event.pointerId, x: position.x - handles[key].x, y: position.y - handles[key].y };
    svg.setPointerCapture(event.pointerId); render(); event.preventDefault();
  });
  svg.addEventListener('pointermove', (event) => {
    if (!drag || event.pointerId !== drag.pointer) return;
    const position = pointerPosition(event);
    if (!position) return;
    state = selected === 'rod' ? dragRod(state, position, drag.offset) : dragPoint(state, position, drag);
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
