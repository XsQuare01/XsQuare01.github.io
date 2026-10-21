import { relation } from './readout.mjs';

// a stays in [−3, 3] so that |a| ≤ 3√2 ≈ 4.24: the foot F of the perpendicular is
// never farther from O than a's tip, so it stays inside the ±4.5 plot. The
// direction point D may go to ±4; only its direction matters.
export const LIMITS = Object.freeze({ min: -3, max: 3, dirMin: -4, dirMax: 4, step: 0.5 });
export const PLOT = 4.5;

// D = (3, 4) gives u = (0.6, 0.8) exactly. The direction is taken from a grid
// point rather than an angle input for this reason: whole degrees never reach
// the 53.13° of (3, 4).
export function initialState() {
  return { a: { x: 1, y: 3 }, d: { x: 3, y: 4 } };
}

const RANGE = { a: [LIMITS.min, LIMITS.max], d: [LIMITS.dirMin, LIMITS.dirMax] };
// `+ 0` turns −0 into 0, so a value snapped from −0.1 does not print as "−0".
const snap = (value, [min, max]) => Math.max(min, Math.min(max, Math.round(value / LIMITS.step) * LIMITS.step)) + 0;

// One coordinate at a time, as the range inputs and their arrow keys change it.
export function move(state, target, axis, value) {
  if (!RANGE[target] || !['x', 'y'].includes(axis) || !Number.isFinite(value)) return state;
  const moved = { ...state[target], [axis]: snap(value, RANGE[target]) };
  // D at the origin names no direction. A step that lands there goes one grid
  // point further the same way, so the arrow keys carry D across 0 instead of
  // sticking at ±0.5.
  if (target === 'd' && moved.x === 0 && moved.y === 0) {
    const way = Math.sign(value - state.d[axis]);
    if (way === 0) return state;
    moved[axis] = way * LIMITS.step;
  }
  return { ...state, [target]: moved };
}

// Both coordinates at once, as a drag sets them. Applying x and then y would
// refuse a diagonal move such as (0.5, 0) → (0, 0.5) that only passes the origin.
// Dropping D on the origin itself is refused: there is no direction to keep.
export function moveTo(state, target, point) {
  if (!RANGE[target] || !Number.isFinite(point.x) || !Number.isFinite(point.y)) return state;
  const moved = { x: snap(point.x, RANGE[target]), y: snap(point.y, RANGE[target]) };
  if (target === 'd' && moved.x === 0 && moved.y === 0) return state;
  return { ...state, [target]: moved };
}

export function measure({ a, d }) {
  const dl = Math.hypot(d.x, d.y);
  const u = { x: d.x / dl, y: d.y / dl };
  const s = a.x * u.x + a.y * u.y;
  const proj = { x: s * u.x, y: s * u.y };
  const rest = { x: a.x - proj.x, y: a.y - proj.y };
  const al = Math.hypot(a.x, a.y);
  // The angle between a and u, as a size in [0°, 180°]: its sign does not change
  // cos φ. A zero vector has no direction, so it has no angle either.
  const cross = u.x * a.y - u.y * a.x;
  const phi = al > 0 ? (Math.atan2(Math.abs(cross), s) * 180) / Math.PI : null;
  return { u, s, proj, rest, lengths: { a: al, rest: Math.hypot(rest.x, rest.y) }, phi };
}

// The text uses U+2212 for negatives, so the live readouts do too.
export const formatNumber = (n) => Number(n.toFixed(2)).toString().replace('-', '−');
// A negative factor reads better in parentheses: 1 × (−0.6).
const factor = (n) => { const text = formatNumber(n); return text.startsWith('−') ? `(${text})` : text; };

// The two readouts that compute a · u. u is usually rounded (D = (1, 2) gives
// 0.447…), so each sign is "≈" unless every number shown is exact.
export function dotText(state) {
  const { u, s } = measure(state);
  const { a } = state;
  return `${factor(a.x)} × ${factor(u.x)} + ${factor(a.y)} × ${factor(u.y)} ${relation(a.x, a.y, u.x, u.y, s)} ${formatNumber(s)}`;
}

export function cosText(state) {
  const { lengths, phi, s } = measure(state);
  if (phi === null) return '0 (a의 방향을 정할 수 없음)';
  return `${formatNumber(lengths.a)} × cos ${formatNumber(phi)}° ${relation(lengths.a, phi, s)} ${formatNumber(s)}`;
}

// SVG geometry shared by the static picture and the live lab: one unit is 40px,
// and model (0, 0) sits at (200, 250).
export const UNIT = 40;
export const toSvg = ({ x, y }) => ({ x: 200 + UNIT * x, y: 250 - UNIT * y });
export const fromSvg = ({ x, y }) => ({ x: (x - 200) / UNIT, y: (250 - y) / UNIT });

// `grab` is the pointer's offset from the handle centre at pointerdown, kept so
// the handle does not jump under the finger.
export function dragTo(state, target, pointer, grab) {
  return moveTo(state, target, fromSvg({ x: pointer.x - grab.x, y: pointer.y - grab.y }));
}

const r1 = (v) => Math.round(v * 10) / 10 + 0;
const svgPoint = (v) => { const p = toSvg(v); return { x: r1(p.x), y: r1(p.y) }; };
// The right-angle mark is 9px and a's handle at the far end of the remainder has
// radius 8, so a remainder shorter than this would hide the mark under the handle.
export const RIGHT_ANGLE_MIN = 18;
// a's arrowhead stops short of the handle at its tip, so a shorter arrow has no
// room for one. A zero arrow has no direction and never gets one.
export const HEAD_MIN = 24;
const MARK = 9;
// u is drawn as a free arrow 16px beside the line, so it does not sit on the
// shadow, which runs along the same line from O.
const U_OFFSET = 16;
// The O label: text anchored at its right end, up and left of the origin. With 6px
// of margin for u's arrowhead.
export const O_LABEL = Object.freeze({ x1: 172, y1: 225, x2: 188, y2: 241 });
const LABEL_MARGIN = 6;
const crossesLabel = ({ from, to }) => {
  for (let i = 0; i <= 40; i++) {
    const x = from.x + ((to.x - from.x) * i) / 40, y = from.y + ((to.y - from.y) * i) / 40;
    if (x > O_LABEL.x1 - LABEL_MARGIN && x < O_LABEL.x2 + LABEL_MARGIN && y > O_LABEL.y1 - LABEL_MARGIN && y < O_LABEL.y2 + LABEL_MARGIN) return true;
  }
  return false;
};

// Every position the live lab draws. The static SVG must equal layout(initialState()).
export function layout(state) {
  const { u, s, proj, rest, lengths } = measure(state);
  const o = toSvg({ x: 0, y: 0 });
  // The line through O along u, cut where it leaves the ±PLOT square.
  const reach = Math.min(...[u.x, u.y].filter((c) => Math.abs(c) > 1e-12).map((c) => PLOT / Math.abs(c)));
  const foot = svgPoint(proj);
  let rightAngle = '';
  if (lengths.rest * UNIT >= RIGHT_ANGLE_MIN) {
    // One leg runs along the line back toward O, the other up the remainder; SVG
    // y points down, so the model's y components flip sign.
    // A tolerance keeps rounding noise in s from flipping the leg when F is at O.
    const along = s > 1e-9 ? -1 : 1;
    const e1 = { x: along * u.x * MARK, y: -along * u.y * MARK };
    const e2 = { x: (rest.x / lengths.rest) * MARK, y: (-rest.y / lengths.rest) * MARK };
    const p = (k1, k2) => `${r1(foot.x + k1 * e1.x + k2 * e2.x)} ${r1(foot.y + k1 * e1.y + k2 * e2.y)}`;
    rightAngle = `M${p(1, 0)}L${p(1, 1)}L${p(0, 1)}`;
  }
  // The right-hand normal of u is (u.y, −u.x); SVG y points down, so it is (u.y, u.x)
  // here. u takes the right-hand side unless that crosses the O label.
  const uArrow = (side) => {
    const from = { x: r1(o.x + side * U_OFFSET * u.y), y: r1(o.y + side * U_OFFSET * u.x) };
    return { from, to: { x: r1(from.x + UNIT * u.x), y: r1(from.y - UNIT * u.y) } };
  };
  const right = uArrow(1);
  return {
    ell: { from: svgPoint({ x: -reach * u.x, y: -reach * u.y }), to: svgPoint({ x: reach * u.x, y: reach * u.y }) },
    u: crossesLabel(right) ? uArrow(-1) : right,
    a: { ...toSvg(state.a), head: lengths.a * UNIT >= HEAD_MIN },
    d: toSvg(state.d),
    foot,
    o,
    rightAngle,
  };
}
