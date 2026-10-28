import { L1, L2, rad, deg, wrap, forward, formatNumber, UNIT, O, toSvg, fromSvg } from './two-link.mjs';
import { relation } from './readout.mjs';

export { formatNumber, UNIT, O, toSvg, fromSvg };
// Both joints take whole degrees over (−180°, 180°], as in the rod-angle lab.
export const LIMITS = Object.freeze({ thetaMin: -179, thetaMax: 180, step: 1 });

// θ1 = 30°, θ2 = 60° puts the tip at (√3, 2): the two rods of the vector post, the
// second one pointing straight up, which is 60° from the first.
export function initialState() {
  return { theta1: 30, theta2: 60 };
}

export function setAngle(state, key, value) {
  if (!['theta1', 'theta2'].includes(key) || !Number.isFinite(value)) return state;
  return { ...state, [key]: wrap(Math.round(value)) };
}

export function measure({ theta1, theta2 }) {
  const f = forward(theta1, theta2);
  const cos2 = Math.cos(rad(theta2));
  const d2 = f.tip.x * f.tip.x + f.tip.y * f.tip.y;
  return { ...f, heading2: wrap(theta1 + theta2), cos2, d2, d: Math.sqrt(d2) };
}

// A negative factor reads better in parentheses: 4 × (−0.5).
const factor = (n) => { const text = formatNumber(n); return text.startsWith('−') ? `(${text})` : text; };

// ‖P‖² = L1² + L2² + 2 L1 L2 cos θ2 with the numbers of this arm. cos θ2 is usually
// rounded, so the sign is "≈" unless it and the result are exact.
export function distanceText(state) {
  const { cos2, d2 } = measure(state);
  return `${L1 * L1 + L2 * L2} + ${2 * L1 * L2} × ${factor(cos2)} ${relation(cos2, d2)} ${formatNumber(d2)}`;
}

// Close to the centre the pointer's direction swings wildly with each pixel, so
// within this many pixels of it a drag keeps the current angle.
export const STILL_RADIUS = 6;

// The pointer's direction from `centre` (model coordinates) in degrees, or null
// near the centre, where it has no steady direction.
function heading(pointer, centre) {
  const at = fromSvg(pointer);
  const dx = at.x - centre.x, dy = at.y - centre.y;
  if (!Number.isFinite(dx) || !Number.isFinite(dy) || Math.hypot(dx, dy) * UNIT < STILL_RADIUS) return null;
  return deg(Math.atan2(dy, dx));
}

// Both handles turn about a centre (E about O, P about E), so a pixel offset would
// drift around the finger. Each grab is kept as an angle instead: how far the link
// points past the pointer's direction at pointerdown.
export function grab(state, key, pointer) {
  const { elbow } = measure(state);
  const h = key === 'elbow' ? heading(pointer, { x: 0, y: 0 }) : heading(pointer, elbow);
  if (h === null) return 0;
  return (key === 'elbow' ? state.theta1 : state.theta1 + state.theta2) - h;
}

// Dragging the elbow turns the whole arm about O; dragging the tip turns only the
// second link about E, so θ2 is its new direction less θ1.
export function dragTo(state, key, pointer, offset) {
  if (key === 'elbow') {
    const h = heading(pointer, { x: 0, y: 0 });
    return h === null ? state : setAngle(state, 'theta1', h + offset);
  }
  if (key !== 'tip') return state;
  const h = heading(pointer, measure(state).elbow);
  return h === null ? state : setAngle(state, 'theta2', h + offset - state.theta1);
}

const r1 = (v) => Math.round(v * 10) / 10 + 0;
const point = (v) => { const p = toSvg(v); return { x: r1(p.x), y: r1(p.y) }; };
export const ARC1 = 30, ARC2 = 22, EXTENSION = 40;

// An arc of radius r about c from direction `from` turning by `turn` degrees. SVG y
// points down, so a counterclockwise turn is sweep 0. No turn, no arc.
function arc(c, r, from, turn) {
  if (turn === 0) return '';
  const end = from + turn;
  const p = (a) => `${r1(c.x + r * Math.cos(rad(a)))} ${r1(c.y - r * Math.sin(rad(a)))}`;
  return `M${p(from)}A${r} ${r} 0 0 ${turn > 0 ? 0 : 1} ${p(end)}`;
}

// Every position the live lab draws. The static SVG must equal layout(initialState()).
export function layout(state) {
  const { elbow, tip } = measure(state);
  const o = toSvg({ x: 0, y: 0 });
  const e = point(elbow), p = point(tip);
  const ext = { x: r1(e.x + EXTENSION * Math.cos(rad(state.theta1))), y: r1(e.y - EXTENSION * Math.sin(rad(state.theta1))) };
  return {
    link1: { x1: o.x, y1: o.y, x2: e.x, y2: e.y },
    link2: { x1: e.x, y1: e.y, x2: p.x, y2: p.y },
    reach: { x1: o.x, y1: o.y, x2: p.x, y2: p.y },
    extension: { x1: e.x, y1: e.y, x2: ext.x, y2: ext.y },
    arc1: arc(o, ARC1, 0, state.theta1),
    arc2: arc(e, ARC2, state.theta1, state.theta2),
    handles: { elbow: e, tip: p },
  };
}
