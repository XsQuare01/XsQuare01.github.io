import { relation } from './readout.mjs';

// Both arrows stay in [−3, 3] on a 0.5 grid, so the chain a + b ends inside the
// ±6 plot and every drawn coordinate is a whole pixel (one step is 15px).
export const LIMITS = Object.freeze({ min: -3, max: 3, step: 0.5 });

export function initialState() {
  return { a: { x: 3, y: 1 }, b: { x: 1, y: 2 } };
}

// `+ 0` turns −0 into 0, so a value snapped from −0.1 does not print as "−0".
const snap = (v) => Math.max(LIMITS.min, Math.min(LIMITS.max, Math.round(v / LIMITS.step) * LIMITS.step)) + 0;

export function move(state, target, axis, value) {
  if (!['a', 'b'].includes(target) || !['x', 'y'].includes(axis) || !Number.isFinite(value)) return state;
  return { ...state, [target]: { ...state[target], [axis]: snap(value) } };
}

const length = (v) => Math.hypot(v.x, v.y);

export function measure({ a, b }) {
  const sum = { x: a.x + b.x, y: a.y + b.y };
  return { sum, lengths: { a: length(a), b: length(b), sum: length(sum) } };
}

// The text uses U+2212 for negatives, so the live readouts do too.
export const formatNumber = (n) => Number(n.toFixed(2)).toString().replace('-', '−');

// The ‖a‖ + ‖b‖ readout. Lengths such as √0.5 are rounded, so the sign is "≈"
// unless every number shown is exact.
export function lengthSumText(state) {
  const { lengths } = measure(state);
  const total = lengths.a + lengths.b;
  return `${formatNumber(lengths.a)} + ${formatNumber(lengths.b)} ${relation(lengths.a, lengths.b, total)} ${formatNumber(total)}`;
}

// SVG geometry shared by the static picture and the live lab: one unit is 30px,
// and model (0, 0) sits at (200, 245).
export const toSvg = ({ x, y }) => ({ x: 200 + 30 * x, y: 245 - 30 * y });
export const fromSvg = ({ x, y }) => ({ x: (x - 200) / 30, y: (245 - y) / 30 });

// The handle for b sits where b's head is once it hangs off a: the end of the
// chain, a + b. Dragging it changes b alone; dragging a carries b along.
// `grab` is the pointer's offset from the handle centre at pointerdown, kept so
// the handle does not jump under the finger.
export function dragTo(state, target, pointer, grab) {
  const p = fromSvg({ x: pointer.x - grab.x, y: pointer.y - grab.y });
  const value = target === 'a' ? p : { x: p.x - state.a.x, y: p.y - state.a.y };
  return move(move(state, target, 'x', value.x), target, 'y', value.y);
}

// Arrowheads stop short of the handle at the tip, so an arrow shorter than this
// has no room for one: the sum's 16px head, pulled 11px back, reaches 25.4px from
// the tip (test/vector-sum.test.mjs reads that from the SVG). A zero arrow has no
// direction and never gets one.
export const HEAD_MIN = 26;

const segment = (from, to) => {
  const p = toSvg(from), q = toSvg(to);
  return { x1: p.x, y1: p.y, x2: q.x, y2: q.y, head: Math.hypot(q.x - p.x, q.y - p.y) >= HEAD_MIN };
};

// Every position the live lab draws. The static SVG must equal layout(initialState()).
export function layout(state) {
  const o = { x: 0, y: 0 };
  const { sum } = measure(state);
  return {
    a: segment(o, state.a),
    b: segment(state.a, sum),
    sum: segment(o, sum),
    // The other order, b first and then a, drawn dashed: the two paths close a
    // parallelogram whose diagonal is the sum.
    bFirst: segment(o, state.b),
    aSecond: segment(state.b, sum),
    handles: { a: toSvg(state.a), b: toSvg(sum) },
  };
}
