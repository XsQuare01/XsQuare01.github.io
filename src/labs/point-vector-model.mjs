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

export const formatNumber = (n) => Number(n.toFixed(2)).toString();
