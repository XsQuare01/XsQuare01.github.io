import {
  initialState, measure, layout, setCoord, dragTo, cosText, poseText, LIMITS, formatNumber as fmt,
} from './arm-inverse-model.mjs';
import { approx } from './readout.mjs';

const pair = (v) => `(${fmt(v.x)}, ${fmt(v.y)})`;
const near = (v) => approx(pair(v), v.x, v.y);
const nearNumber = (n) => approx(fmt(n), n);
// The target turns red where no posture reaches it (red marks failure in the palette).
const COLOURS = { reachable: '#e2e8f0', unreachable: '#f87171' };

export function mount(figure) {
  const live = figure.querySelector('.lab-live');
  const svg = live?.querySelector('svg');
  if (!svg) throw new Error('실험 SVG가 없습니다.');
  const get = (name) => {
    const element = svg.querySelector(`[data-part="${name}"]`);
    if (!element) throw new Error(`실험 요소 누락: ${name}`);
    return element;
  };
  const names = ['handle-target', 'target-ring', 'target-dot', 'summary'];
  for (const n of [1, 2]) names.push(`arm${n}`, `arm${n}-link1`, `arm${n}-link2`, `arm${n}-elbow`);
  const parts = Object.fromEntries(names.map((name) => [name, get(name)]));
  let state = initialState();
  let drag = null;
  const id = figure.dataset.labId;
  const controls = document.createElement('div');
  controls.className = 'lab-controls';
  controls.innerHTML = `
    <div class="lab-toolbar"><span>목표점 T</span>
      <button type="button" class="lab-reset">처음으로</button></div>
    <p class="lab-input-note" id="${id}note">목표점의 좌표입니다. 한 칸의 길이는 1이고, 링크 길이는 L<sub>1</sub> = 2, L<sub>2</sub> = 1입니다.</p>
    <div class="lab-inputs">
      <label for="${id}x"><span>x <output data-value="x"></output></span><input id="${id}x" type="range" min="${LIMITS.min}" max="${LIMITS.max}" step="${LIMITS.step}" aria-describedby="${id}note" /></label>
      <label for="${id}y"><span>y <output data-value="y"></output></span><input id="${id}y" type="range" min="${LIMITS.min}" max="${LIMITS.max}" step="${LIMITS.step}" aria-describedby="${id}note" /></label>
    </div>
    <dl class="lab-readouts"><div><dt>거리 d = ‖T‖</dt><dd data-value="d"></dd></div><div><dt>자세의 수</dt><dd data-value="count"></dd></div><div class="lab-wide"><dt>c = (d² − L<sub>1</sub>² − L<sub>2</sub>²) / (2L<sub>1</sub>L<sub>2</sub>), 닿으려면 cos θ<sub>2</sub> = c</dt><dd data-value="cos"></dd></div><div class="lab-wide"><dt>자세 ① (실선)</dt><dd data-value="pose1"></dd></div><div class="lab-wide"><dt>자세 ② (점선)</dt><dd data-value="pose2"></dd></div></dl>
    <p class="lab-input-note">값은 소수 둘째 자리까지 반올림합니다.</p>
    <p class="lab-status" role="status" aria-atomic="true"></p>`;
  const status = controls.querySelector('.lab-status');
  const inputs = { x: controls.querySelector(`#${id}x`), y: controls.querySelector(`#${id}y`) };
  const outputs = Object.fromEntries([...controls.querySelectorAll('[data-value]')].map((el) => [el.dataset.value, el]));
  const attrs = (node, values) => Object.entries(values).forEach(([k, v]) => node.setAttribute(k, String(v)));
  const describe = (pose) => (pose ? `${poseText(pose)}, 팔꿈치 ${near(pose.elbow)}` : '없음');
  const render = () => {
    const v = measure(state);
    const at = layout(state);
    attrs(parts['handle-target'], { transform: `translate(${at.target.x} ${at.target.y})` });
    const colour = at.reachable ? COLOURS.reachable : COLOURS.unreachable;
    attrs(parts['target-ring'], { stroke: colour });
    attrs(parts['target-dot'], { fill: colour });
    parts['handle-target'].classList.toggle('is-selected', drag !== null);
    at.arms.forEach((arm, i) => {
      const n = i + 1;
      attrs(parts[`arm${n}`], { visibility: arm.visible ? 'visible' : 'hidden' });
      attrs(parts[`arm${n}-link1`], arm.link1);
      attrs(parts[`arm${n}-link2`], arm.link2);
      attrs(parts[`arm${n}-elbow`], { cx: arm.elbow.x, cy: arm.elbow.y });
    });
    for (const axis of ['x', 'y']) {
      inputs[axis].value = state.target[axis];
      outputs[axis].textContent = fmt(state.target[axis]);
    }
    outputs.d.textContent = nearNumber(v.d);
    outputs.count.textContent = `${v.poses.length}${v.poses.length ? '' : ' (닿지 않음)'}`;
    // Outside the ring no angle has this cosine, which is why the target is out of reach.
    outputs.cos.textContent = `${cosText(state)}${v.poses.length ? '' : ' (|c| > 1이라 그런 θ2가 없다)'}`;
    outputs.pose1.textContent = describe(v.poses[0]);
    outputs.pose2.textContent = describe(v.poses[1]);
    const summary = `목표점 ${pair(state.target)}, 거리 ${nearNumber(v.d)}. 자세 ${v.poses.length}개.`
      + v.poses.map((pose, i) => ` 자세 ${i + 1}: ${describe(pose)}.`).join('');
    svg.setAttribute('aria-label', summary);
    parts.summary.textContent = v.poses.length ? `자세 ${v.poses.length}개` : '닿지 않음';
    return summary;
  };
  const announce = () => { status.textContent = render(); };
  for (const axis of ['x', 'y']) {
    inputs[axis].addEventListener('input', () => { state = setCoord(state, axis, Number(inputs[axis].value)); render(); });
    inputs[axis].addEventListener('change', announce);
  }
  // A reset in the middle of a drag ends the drag too (see arm-forward.js).
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
    const { target } = layout(state);
    drag = { pointer: event.pointerId, x: position.x - target.x, y: position.y - target.y };
    svg.setPointerCapture(event.pointerId); render(); event.preventDefault();
  });
  svg.addEventListener('pointermove', (event) => {
    if (!drag || event.pointerId !== drag.pointer) return;
    const position = pointerPosition(event);
    if (!position) return;
    state = dragTo(state, position, drag);
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
  // touch that starts on the target must cancel page panning here (see SVG_LABS.md).
  svg.addEventListener('touchstart', (event) => {
    if (event.target.closest?.('[data-point]')) event.preventDefault();
  }, { passive: false });
  live.append(controls);
  render();
  live.hidden = false;
  figure.classList.add('is-live');
}
