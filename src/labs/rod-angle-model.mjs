// θ runs over (−180°, 180°], the representative range this lab and the article use
// for a direction (30°, 390° and −330° are one direction). Math.atan2 itself returns
// radians in [−π, π], so fromTip converts to degrees and wrap() turns −180° into
// 180°. The slider therefore starts at −179.
export const LIMITS = Object.freeze({
  thetaMin: -179, thetaMax: 180, thetaStep: 1,
  lengthMin: 0.5, lengthMax: 3, lengthStep: 0.25,
});

// θ is in degrees: the inputs and readouts show degrees, and radians are derived.
export function initialState() {
  return { theta: 30, length: 2 };
}

// An angle outside the range names the same direction as one inside it, so it is
// wrapped rather than clamped: 500° is 140°, and −180° is 180°.
const wrap = (deg) => {
  const v = (((deg + 180) % 360) + 360) % 360 - 180;
  return v === -180 ? 180 : v;
};

export function setAngle(state, value) {
  if (!Number.isFinite(value)) return state;
  return { ...state, theta: wrap(Math.round(value / LIMITS.thetaStep) * LIMITS.thetaStep) };
}

export function setLength(state, value) {
  if (!Number.isFinite(value)) return state;
  const snapped = Math.round(value / LIMITS.lengthStep) * LIMITS.lengthStep;
  return { ...state, length: Math.max(LIMITS.lengthMin, Math.min(LIMITS.lengthMax, snapped)) };
}

export function measure({ theta, length }) {
  const rad = (theta * Math.PI) / 180;
  const cos = Math.cos(rad), sin = Math.sin(rad);
  return { rad, cos, sin, x: length * cos, y: length * sin };
}

// Dragging the tip: the angle comes back from atan2, which keeps the quadrant that
// y/x alone loses, and the length from the distance to the origin. The origin has
// no angle, so a drag onto it keeps the current one.
export function fromTip(state, point) {
  if (!Number.isFinite(point.x) || !Number.isFinite(point.y)) return state;
  const r = Math.hypot(point.x, point.y);
  const angled = r > 1e-9 ? setAngle(state, (Math.atan2(point.y, point.x) * 180) / Math.PI) : state;
  return setLength(angled, r);
}

// `grab` is the pointer's offset from the tip at pointerdown, kept so the tip does
// not jump under the finger.
export function dragTip(state, pointer, grab) {
  return fromTip(state, fromSvg({ x: pointer.x - grab.x, y: pointer.y - grab.y }));
}

// The text uses U+2212 for negatives, so the live readouts do too.
export const formatNumber = (n) => Number(n.toFixed(2)).toString().replace('-', '−');

// SVG geometry shared by the static picture and the live lab: one unit is 60px,
// and model (0, 0) sits at (200, 250).
export const toSvg = ({ x, y }) => ({ x: 200 + 60 * x, y: 250 - 60 * y });
export const fromSvg = ({ x, y }) => ({ x: (x - 200) / 60, y: (250 - y) / 60 });

const r1 = (v) => Math.round(v * 10) / 10;
const ARC_RADIUS = 36;
// Labels stay between the title and the legend row.
const BOUNDS = { x1: 4, y1: 44, x2: 396, y2: 440 };
const P_SIZE = { w: 16, h: 18 }, THETA_SIZE = { w: 12, h: 15 };
// The θ arc is too small to name below this angle; the readouts still show θ.
const THETA_LABEL_MIN = 20;

const box = (cx, cy, { w, h }) => ({ x1: cx - w / 2, y1: cy - h / 2, x2: cx + w / 2, y2: cy + h / 2 });
const textBox = (x, baseline, w, h, anchor) => {
  const x1 = anchor === 'middle' ? x - w / 2 : anchor === 'end' ? x - w : x;
  return { x1, y1: baseline - h, x2: x1 + w, y2: baseline };
};
const overlaps = (a, b, pad) => a.x1 < b.x2 + pad && b.x1 < a.x2 + pad && a.y1 < b.y2 + pad && b.y1 < a.y2 + pad;

// Fixed text in the figure: tick numbers, axis letters and O.
export const FIXED_TEXT = Object.freeze([
  ...[-3, -2, -1, 1, 2, 3].map((n) => textBox(200 + 60 * n, 275, n < 0 ? 22 : 12, 15, 'middle')),
  ...[-3, -2, -1, 1, 2, 3].map((n) => textBox(187, 257 - 60 * n, n < 0 ? 22 : 12, 15, 'end')),
  textBox(386, 257, 12, 16, 'start'), textBox(207, 60, 12, 16, 'start'), textBox(187, 240, 17, 17, 'end'),
]);

function crosses(b, [a, c]) {
  const steps = Math.max(1, Math.ceil(Math.hypot(c.x - a.x, c.y - a.y)));
  for (let i = 0; i <= steps; i++) {
    const x = a.x + ((c.x - a.x) * i) / steps, y = a.y + ((c.y - a.y) * i) / steps;
    if (x > b.x1 - 1 && x < b.x2 + 1 && y > b.y1 - 1 && y < b.y2 + 1) return true;
  }
  return false;
}

// A label spot is usable when it stays in bounds and touches no fixed text, no dot,
// no drawn segment and no label already placed.
function clear(b, { dots, segments, placed }) {
  if (b.x1 < BOUNDS.x1 || b.x2 > BOUNDS.x2 || b.y1 < BOUNDS.y1 || b.y2 > BOUNDS.y2) return false;
  if ([...FIXED_TEXT, ...placed].some((t) => overlaps(b, t, 2))) return false;
  if (dots.some((d) => overlaps(b, d, 2))) return false;
  return !segments.some((s) => crosses(b, s));
}

// Every position the live lab draws. The static SVG must equal layout(initialState()).
export function layout(state) {
  const { cos, sin, x, y } = measure(state);
  const o = toSvg({ x: 0, y: 0 });
  const p = toSvg({ x, y });
  const tip = { x: r1(p.x), y: r1(p.y) };
  const u = toSvg({ x: cos, y: sin });
  const unit = { x: r1(u.x), y: r1(u.y) };
  const arcEnd = { x: r1(o.x + ARC_RADIUS * cos), y: r1(o.y - ARC_RADIUS * sin) };
  const scene = {
    dots: [box(tip.x, tip.y, { w: 20, h: 20 }), box(unit.x, unit.y, { w: 10, h: 10 })],
    segments: [[o, tip], [o, { x: tip.x, y: o.y }], [{ x: tip.x, y: o.y }, tip]],
    placed: [],
  };

  // θ names the arc from outside it, halfway between the axis and the rod.
  const half = ((state.theta / 2) * Math.PI) / 180;
  const thetaCentre = { x: Math.round(o.x + 46 * Math.cos(half)), y: Math.round(o.y - 46 * Math.sin(half)) };
  const thetaBox = box(thetaCentre.x, thetaCentre.y, THETA_SIZE);
  const thetaVisible = Math.abs(state.theta) >= THETA_LABEL_MIN && clear(thetaBox, scene);
  if (thetaVisible) scene.placed.push(thetaBox);

  // P goes beyond the tip along the rod when it can, then beside the tip, then
  // anywhere around it, taking the first spot that is clear. Near the origin the
  // ticks, the unit dot and the short parts crowd the close ring, so two wider
  // rings follow.
  const ring = (r) => [[r, 0], [-r, 0], [0, -r], [0, r], [0.7 * r, -0.7 * r], [-0.7 * r, -0.7 * r], [0.7 * r, 0.7 * r], [-0.7 * r, 0.7 * r]];
  const around = [[24 * cos, -24 * sin], [24 * sin, 24 * cos], [-24 * sin, -24 * cos], ...ring(26), ...ring(36), ...ring(46)];
  const spots = around.map(([dx, dy]) => ({ x: Math.round(tip.x + dx), y: Math.round(tip.y + dy) }));
  const pCentre = spots.find((c) => clear(box(c.x, c.y, P_SIZE), scene)) ?? spots[0];

  return {
    tip,
    unit,
    // Positive θ turns counterclockwise, which is sweep 0 once y points down.
    arc: state.theta === 0 ? '' : `M${o.x + ARC_RADIUS} ${o.y}A${ARC_RADIUS} ${ARC_RADIUS} 0 0 ${state.theta > 0 ? 0 : 1} ${arcEnd.x} ${arcEnd.y}`,
    // Label x/y are text positions: centre x, and the baseline a little below centre.
    labels: {
      p: { x: pCentre.x, y: Math.round(pCentre.y + P_SIZE.h / 2) },
      theta: { x: thetaCentre.x, y: Math.round(thetaCentre.y + THETA_SIZE.h / 2), visible: thetaVisible },
    },
  };
}
