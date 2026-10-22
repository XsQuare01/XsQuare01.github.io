import { relation } from './readout.mjs';

// θ runs over (−180°, 180°] as in the rod-angle lab. s stays in [−3, 3] so that
// |p| = |s| ≤ 3√2 ≈ 4.24 keeps the point inside the ±4.5 plot; the rod is 4 long.
export const LIMITS = Object.freeze({
  thetaMin: -179, thetaMax: 180, thetaStep: 1,
  min: -3, max: 3, step: 0.5,
});
export const PLOT = 4.5;
export const ROD = 4;

// The gripper sits 3 along the rod and 1 to its left. Whole degrees never reach the
// 53.13° at which (3, 1) lands on (1, 3), so the lab starts at the 30° of the
// rod-angle lab instead.
export function initialState() {
  return { theta: 30, s: { x: 3, y: 1 } };
}

// An angle outside the range names the same direction as one inside it, so it is
// wrapped rather than clamped: 500° is 140°, and −180° is 180°.
const wrap = (deg) => {
  const v = (((deg + 180) % 360) + 360) % 360 - 180;
  return v === -180 ? 180 : v;
};
// `+ 0` turns −0 into 0, so a value snapped from −0.1 does not print as "−0".
const snap = (value) => Math.max(LIMITS.min, Math.min(LIMITS.max, Math.round(value / LIMITS.step) * LIMITS.step)) + 0;

export function setAngle(state, value) {
  if (!Number.isFinite(value)) return state;
  return { ...state, theta: wrap(Math.round(value / LIMITS.thetaStep) * LIMITS.thetaStep) + 0 };
}

// One coordinate at a time, as the range inputs change it.
export function setCoord(state, axis, value) {
  if (!['x', 'y'].includes(axis) || !Number.isFinite(value)) return state;
  return { ...state, s: { ...state.s, [axis]: snap(value) } };
}

// Both coordinates at once, as a drag sets them.
export function setCoords(state, point) {
  if (!Number.isFinite(point.x) || !Number.isFinite(point.y)) return state;
  return { ...state, s: { x: snap(point.x), y: snap(point.y) } };
}

// The turned axes are the two columns of R(θ), and the turned point adds them up
// s_x and s_y times.
export function measure({ theta, s }) {
  const rad = (theta * Math.PI) / 180;
  const c = Math.cos(rad), sn = Math.sin(rad);
  const ex = { x: c, y: sn }, ey = { x: -sn, y: c };
  const p = { x: s.x * ex.x + s.y * ey.x, y: s.x * ex.y + s.y * ey.y };
  return { rad, ex, ey, p, length: Math.hypot(s.x, s.y) };
}

// Back from fixed to rod coordinates: the turned axes are perpendicular unit vectors,
// so each rod coordinate is the dot product with one of them.
export function toRod(theta, point) {
  const { ex, ey } = measure({ theta, s: { x: 0, y: 0 } });
  return { x: point.x * ex.x + point.y * ex.y, y: point.x * ey.x + point.y * ey.y };
}

// The text uses U+2212 for negatives, so the live readouts do too.
export const formatNumber = (n) => Number(n.toFixed(2)).toString().replace('-', '−');
// A negative factor reads better in parentheses: 1 × (−0.5, 0.87).
const factor = (n) => { const text = formatNumber(n); return text.startsWith('−') ? `(${text})` : text; };
const pair = (v) => `(${formatNumber(v.x)}, ${formatNumber(v.y)})`;

// Every number the equation shows: R(θ)'s entries, s and p. cos θ and sin θ are
// usually rounded, so the sign is "≈" unless every one of them is exact.
const sign = (state) => {
  const { ex, p } = measure(state);
  return relation(ex.x, ex.y, state.s.x, state.s.y, p.x, p.y);
};

// The matrix equation drawn under the plot: rows of R(θ), then s, then p.
export function matrixText(state) {
  const { ex, ey, p } = measure(state);
  const f = formatNumber;
  return {
    m: [[f(ex.x), f(ey.x)], [f(ex.y), f(ey.y)]],
    s: [f(state.s.x), f(state.s.y)],
    p: [f(p.x), f(p.y)],
    rel: sign(state),
  };
}

// The column reading of the same product, as a readout line.
export function combinationText(state) {
  const { ex, ey, p } = measure(state);
  return `${factor(state.s.x)} × ${pair(ex)} + ${factor(state.s.y)} × ${pair(ey)} ${sign(state)} ${pair(p)}`;
}

// SVG geometry shared by the static picture and the live lab: one unit is 40px,
// and model (0, 0) sits at (210, 250), leaving room for tick numbers on the left.
export const UNIT = 40;
export const O = Object.freeze({ x: 210, y: 250 });
export const toSvg = ({ x, y }) => ({ x: O.x + UNIT * x, y: O.y - UNIT * y });
export const fromSvg = ({ x, y }) => ({ x: (x - O.x) / UNIT, y: (O.y - y) / UNIT });

// `grab` is the pointer's offset from P's centre at pointerdown, kept so P does not
// jump under the finger.
const aim = (pointer, grab) => fromSvg({ x: pointer.x - grab.x, y: pointer.y - grab.y });
// The pointer's direction from O in degrees, or null at O, which has none.
const heading = (pointer) => {
  const at = fromSvg(pointer);
  if (!Number.isFinite(at.x) || !Number.isFinite(at.y) || Math.hypot(at.x, at.y) < 1e-9) return null;
  return (Math.atan2(at.y, at.x) * 180) / Math.PI;
};

// The rod end turns, so a fixed pixel offset would drift around the finger. The
// grab is kept as an angle instead: how far the rod is turned past the pointer's
// direction at pointerdown.
export function rodGrab(state, pointer) {
  const h = heading(pointer);
  return h === null ? 0 : state.theta - h;
}

// Dragging the rod end turns the rod with the pointer. A pointer on O has no
// direction, so the current angle stays.
export function dragRod(state, pointer, offset) {
  const h = heading(pointer);
  return h === null ? state : setAngle(state, h + offset);
}

// Dragging P moves it on the turned grid: the pointer is read in rod coordinates
// and snapped to the half-unit steps of s, half a cell of the drawn rod grid.
export function dragPoint(state, pointer, grab) {
  return setCoords(state, toRod(state.theta, aim(pointer, grab)));
}

const r1 = (v) => Math.round(v * 10) / 10 + 0;
// P's arrowhead stops short of the handle at its tip, so a shorter arrow has no
// room for one. A zero arrow has no direction and never gets one.
export const HEAD_MIN = 24;

// Every position the live lab draws. The rod, its grid, its two axes, the chain and
// both handles are drawn in rod coordinates inside one group, and only that group
// turns: `rotate(−θ)` about O, since SVG angles run clockwise. The static SVG must
// equal layout(initialState()).
export function layout(state) {
  const { s } = state;
  const { p, ex } = measure(state);
  const local = toSvg(s);
  const bend = toSvg({ x: s.x, y: 0 });
  const rodEnd = toSvg({ x: ROD * ex.x, y: ROD * ex.y }), tip = toSvg(p);
  return {
    turn: `rotate(${-state.theta + 0} ${O.x} ${O.y})`,
    chainX: { x1: O.x, y1: O.y, x2: bend.x, y2: bend.y },
    chainY: { x1: bend.x, y1: bend.y, x2: local.x, y2: local.y },
    arrow: { x2: local.x, y2: local.y, head: Math.hypot(s.x, s.y) * UNIT >= HEAD_MIN },
    handleP: local,
    // Where the two handles appear once the group is turned, for picking.
    handles: {
      rod: { x: r1(rodEnd.x), y: r1(rodEnd.y) },
      p: { x: r1(tip.x), y: r1(tip.y) },
    },
  };
}
