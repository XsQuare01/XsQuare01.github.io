export const LIMITS = Object.freeze({ min: -1, max: 6, originMin: -1, originMax: 3, step: 0.25 });

export function initialState() {
  return { a: { x: 1, y: 1 }, b: { x: 4, y: 5 }, o: { x: 0, y: 0 } };
}

export function measure({ a, b, o }) {
  const delta = { x: b.x - a.x, y: b.y - a.y };
  return {
    a: { x: a.x - o.x, y: a.y - o.y },
    b: { x: b.x - o.x, y: b.y - o.y },
    delta, distance: Math.hypot(delta.x, delta.y),
  };
}

export function move(state, target, axis, value) {
  if (!['a', 'b', 'o'].includes(target) || !['x', 'y'].includes(axis) || !Number.isFinite(value)) return state;
  const min = target === 'o' ? LIMITS.originMin : LIMITS.min;
  const max = target === 'o' ? LIMITS.originMax : LIMITS.max;
  const next = Math.max(min, Math.min(max, Math.round(value / LIMITS.step) * LIMITS.step));
  return { ...state, [target]: { ...state[target], [axis]: next } };
}

// The text uses U+2212 for negatives, so the live readouts do too.
export const formatNumber = (n) => Number(n.toFixed(2)).toString().replace('-', '−');

// SVG geometry shared by the static picture and the live lab: one unit is 40px,
// and model (0, 0) sits at (70, 350).
export const toSvg = ({ x, y }) => ({ x: 70 + 40 * x, y: 350 - 40 * y });
export const fromSvg = ({ x, y }) => ({ x: (x - 70) / 40, y: (350 - y) / 40 });

// `grab` is the pointer's offset from the handle centre at pointerdown, kept so
// the handle does not jump under the finger.
export function dragTo(state, target, pointer, grab) {
  const p = fromSvg({ x: pointer.x - grab.x, y: pointer.y - grab.y });
  return move(move(state, target, 'x', p.x), target, 'y', p.y);
}

const LABEL_GAP = 24;
const clamp = (v, lo, hi) => Math.max(lo, Math.min(hi, v));

// A's label sits behind the arrow and B's beyond its head, so neither lies on the
// arrow and close points push their labels apart. A zero vector has no direction,
// so its labels split along a fixed diagonal. O's label takes the empty slot where
// the y-axis tick 0 would be, away from the two −1 ticks at the corner.
export function labelPositions(state) {
  const { delta, distance } = measure(state);
  const u = distance > 0 ? { x: delta.x / distance, y: delta.y / distance } : { x: Math.SQRT1_2, y: Math.SQRT1_2 };
  const at = (point, sign) => {
    const c = toSvg(point);
    return {
      x: clamp(Math.round(c.x + sign * LABEL_GAP * u.x), 16, 384),
      y: clamp(Math.round(c.y - sign * LABEL_GAP * u.y + 8), 70, 410),
    };
  };
  const o = toSvg(state.o);
  return { a: at(state.a, -1), b: at(state.b, 1), o: { x: o.x - 13, y: o.y - 10 } };
}
