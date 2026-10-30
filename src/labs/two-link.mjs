// The planar two-link arm of the robotics-two-link-arm post: the shoulder at O, a
// first link of length L1 to the elbow E, a second link of length L2 to the tip P.
// θ1 is measured from the x-axis, θ2 from the direction of the first link; both in
// degrees, counterclockwise positive.
export const L1 = 2;
export const L2 = 1;

export const rad = (deg) => (deg * Math.PI) / 180;
export const deg = (r) => (r * 180) / Math.PI;

// An angle outside (−180°, 180°] names the same direction as one inside it, so it is
// wrapped rather than clamped: 500° is 140°, and −180° is 180°.
export function wrap(d) {
  const v = (((d + 180) % 360) + 360) % 360 - 180;
  return (v === -180 ? 180 : v) + 0;
}

// Forward kinematics: the elbow is L1 along θ1, and the second link points along
// θ1 + θ2 once the first link's turn is added to its own.
export function forward(theta1, theta2) {
  const a = { x: L1 * Math.cos(rad(theta1)), y: L1 * Math.sin(rad(theta1)) };
  const b = { x: L2 * Math.cos(rad(theta1 + theta2)), y: L2 * Math.sin(rad(theta1 + theta2)) };
  return { elbow: a, link2: b, tip: { x: a.x + b.x, y: a.y + b.y } };
}

// Inverse kinematics as far as the post takes it: how many postures put the tip on
// the target, and which. The distance d fixes cos θ2 = (d² − L1² − L2²) / (2 L1 L2);
// inside the ring there are two θ2 of opposite sign, on its edge one, outside none.
// Each θ2 has one θ1: the one that turns the tip's rod coordinates s onto the target.
// With L1 ≠ L2 the target O is never reached, so d = 0 needs no case of its own.
export function postures(target) {
  const d2 = target.x * target.x + target.y * target.y;
  const c = (d2 - L1 * L1 - L2 * L2) / (2 * L1 * L2);
  if (c > 1 + 1e-12 || c < -1 - 1e-12) return [];
  const t2 = deg(Math.acos(Math.max(-1, Math.min(1, c))));
  const both = Math.abs(Math.abs(c) - 1) < 1e-12 ? [t2] : [t2, -t2];
  return both.map((theta2) => {
    const s = { x: L1 + L2 * Math.cos(rad(theta2)), y: L2 * Math.sin(rad(theta2)) };
    const theta1 = wrap(deg(Math.atan2(target.y, target.x) - Math.atan2(s.y, s.x)));
    return { theta1, theta2: wrap(theta2), ...forward(theta1, theta2) };
  });
}

// The text uses U+2212 for negatives, so the live readouts do too.
export const formatNumber = (n) => Number(n.toFixed(2)).toString().replace('-', '−');

// SVG geometry shared by both arm labs: one unit is 50px, and model (0, 0) sits at
// (210, 250), leaving room for tick numbers on the left.
export const UNIT = 50;
export const O = Object.freeze({ x: 210, y: 250 });
export const toSvg = ({ x, y }) => ({ x: O.x + UNIT * x, y: O.y - UNIT * y });
export const fromSvg = ({ x, y }) => ({ x: (x - O.x) / UNIT, y: (O.y - y) / UNIT });
