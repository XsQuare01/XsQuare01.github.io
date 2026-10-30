import { L1, L2, postures, formatNumber, UNIT, O, toSvg, fromSvg } from './two-link.mjs';
import { relation } from './readout.mjs';

export { formatNumber, UNIT, O, toSvg, fromSvg };
// The target moves on a 0.5 grid in [−3, 3]², which shows every case: inside, on
// either edge, in the hole and beyond the ring (the corners). Going further out
// would put the target over the tick numbers left of the plot.
export const LIMITS = Object.freeze({ min: -3, max: 3, step: 0.5 });

// (2, 1) has d² = 5 and cos θ2 = 0: the postures (0°, 90°) and (53.13°, −90°).
export function initialState() {
  return { target: { x: 2, y: 1 } };
}

// `+ 0` turns −0 into 0, so a value snapped from −0.1 does not print as "−0".
const snap = (value) => Math.max(LIMITS.min, Math.min(LIMITS.max, Math.round(value / LIMITS.step) * LIMITS.step)) + 0;

export function setCoord(state, axis, value) {
  if (!['x', 'y'].includes(axis) || !Number.isFinite(value)) return state;
  return { ...state, target: { ...state.target, [axis]: snap(value) } };
}

export function setTarget(state, point) {
  if (!Number.isFinite(point.x) || !Number.isFinite(point.y)) return state;
  return { ...state, target: { x: snap(point.x), y: snap(point.y) } };
}

export function measure({ target }) {
  const d2 = target.x * target.x + target.y * target.y;
  const c = (d2 - L1 * L1 - L2 * L2) / (2 * L1 * L2);
  return { d2, d: Math.sqrt(d2), c, poses: postures(target) };
}

// c = (d² − 5) / 4 with the numbers of this arm, the value cos θ2 must take. Grid
// targets make d² exact; the quotient often needs more than two decimals, and then
// the sign is "≈". Outside the ring |c| > 1 and no θ2 has it.
export function cosText(state) {
  const { d2, c } = measure(state);
  return `(${formatNumber(d2)} − ${L1 * L1 + L2 * L2}) / ${2 * L1 * L2} ${relation(d2, c)} ${formatNumber(c)}`;
}

// One posture's joint angles, marked ≈ when either is rounded.
export function poseText(pose) {
  return `(θ1, θ2) ${relation(pose.theta1, pose.theta2)} (${formatNumber(pose.theta1)}°, ${formatNumber(pose.theta2)}°)`;
}

// `grab` is the pointer's offset from the target's centre at pointerdown, kept so
// the target does not jump under the finger.
export function dragTo(state, pointer, grab) {
  return setTarget(state, fromSvg({ x: pointer.x - grab.x, y: pointer.y - grab.y }));
}

const r1 = (v) => Math.round(v * 10) / 10 + 0;
const point = (v) => { const p = toSvg(v); return { x: r1(p.x), y: r1(p.y) }; };

// Every position the live lab draws. The static SVG must equal layout(initialState()).
// Posture ① has θ2 > 0 (or the one posture on an edge) and is drawn solid; ② is
// dashed. Arms that do not exist are hidden, not removed, so the parts stay put.
export function layout(state) {
  const { poses } = measure(state);
  const o = toSvg({ x: 0, y: 0 });
  const t = point(state.target);
  const arm = (pose) => {
    if (!pose) return { visible: false, link1: { x1: o.x, y1: o.y, x2: o.x, y2: o.y }, link2: { x1: o.x, y1: o.y, x2: o.x, y2: o.y }, elbow: { x: o.x, y: o.y } };
    const e = point(pose.elbow);
    return { visible: true, link1: { x1: o.x, y1: o.y, x2: e.x, y2: e.y }, link2: { x1: e.x, y1: e.y, x2: t.x, y2: t.y }, elbow: e };
  };
  return { target: t, reachable: poses.length > 0, arms: [arm(poses[0]), arm(poses[1])] };
}
