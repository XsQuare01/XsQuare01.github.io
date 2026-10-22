import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import {
  initialState, measure, toRod, setAngle, setCoord, setCoords, rodGrab, dragRod, dragPoint, layout,
  matrixText, combinationText, formatNumber, LIMITS, ROD, HEAD_MIN,
} from '../src/labs/rotation-matrix-model.mjs';
import { pickHandle } from '../src/labs/pick-handle.mjs';

const near = (actual, expected, message, tol = 1e-9) => assert.ok(Math.abs(actual - expected) < tol, `${message}: ${actual} ≠ ${expected}`);
const SVG = readFileSync(new URL('../public/images/robotics-rotation-matrix/rotation-lab.svg', import.meta.url), 'utf8');
const ANGLES = [];
for (let t = LIMITS.thetaMin; t <= LIMITS.thetaMax; t += LIMITS.thetaStep) ANGLES.push(t);
const VALUES = [];
for (let v = LIMITS.min; v <= LIMITS.max; v += LIMITS.step) VALUES.push(v);
const POINTS = VALUES.flatMap((x) => VALUES.map((y) => ({ x, y })));
const rad = (deg) => (deg * Math.PI) / 180;

// The pixel geometry is read off the static picture (fixed axes through (210, 250),
// ticks 40px apart) rather than taken from the model's toSvg.
const PX = ({ x, y }) => ({ x: 210 + 40 * x, y: 250 - 40 * y });
test('the test geometry matches the axes, ticks and rod axes the picture draws', () => {
  assert.match(SVG, /<line x1="30" y1="250" x2="390" y2="250"/);
  assert.match(SVG, /<line x1="210" y1="70" x2="210" y2="430"/);
  assert.match(SVG, /M170 246V254 M206 290H214 M250 246V254/, 'ticks one unit either side of O');
  assert.match(SVG, /<line x1="210" y1="250" x2="250" y2="250" stroke="#fbbf24" stroke-width="4"/, 'e′x is one unit along the rod');
  assert.match(SVG, /<line x1="210" y1="250" x2="210" y2="210" stroke="#4ade80" stroke-width="4"/, 'e′y is one unit to its left');
});

// What SVG's rotate(a cx cy) does to a point: the rotation matrix [cos a, −sin a;
// sin a, cos a] about (cx, cy), in screen coordinates where y points down.
const ROTATE = /^rotate\((-?[\d.]+) (-?[\d.]+) (-?[\d.]+)\)$/;
function turned(transform, point) {
  const m = transform.match(ROTATE);
  assert.ok(m, `transform ${transform}`);
  const [a, cx, cy] = m.slice(1).map(Number);
  const c = Math.cos(rad(a)), s = Math.sin(rad(a));
  const dx = point.x - cx, dy = point.y - cy;
  return { x: cx + dx * c - dy * s, y: cy + dx * s + dy * c };
}

test('the article examples: (3, 1) turns to (1, 3) when cos θ = 0.6, and to (−1, 3) at 90°', () => {
  const theta0 = (Math.atan2(4, 3) * 180) / Math.PI;
  const at0 = measure({ theta: theta0, s: { x: 3, y: 1 } });
  near(at0.ex.x, 0.6, 'cos θ'); near(at0.ex.y, 0.8, 'sin θ');
  near(at0.ey.x, -0.8, '−sin θ'); near(at0.ey.y, 0.6, 'cos θ');
  near(at0.p.x, 1, 'p x'); near(at0.p.y, 3, 'p y');
  const back = toRod(theta0, { x: 1, y: 3 });
  near(back.x, 3, 'back along the rod'); near(back.y, 1, 'back to its left');
  const q = measure({ theta: 90, s: { x: 3, y: 1 } });
  near(q.p.x, -1, '90° x'); near(q.p.y, 3, '90° y');
  const still = measure({ theta: 0, s: { x: 3, y: 1 } });
  assert.deepEqual(still.p, { x: 3, y: 1 }, 'θ = 0 leaves the point alone');
  // The addition formula, with α the angle of (3, 1): (1, 3)/√10 is at α + θ0.
  const alpha = Math.atan2(1, 3);
  near(Math.cos(alpha + rad(theta0)), 1 / Math.sqrt(10), 'cos(α + θ)');
  near(Math.sin(alpha + rad(theta0)), 3 / Math.sqrt(10), 'sin(α + θ)');
});

test('over every state, the turned group draws P at s_x e′x + s_y e′y, inside the plot', () => {
  let checked = 0;
  for (const theta of ANGLES) {
    const c = Math.cos(rad(theta)), sn = Math.sin(rad(theta));
    for (const s of POINTS) {
      const state = { theta, s };
      const at = layout(state);
      const where = `θ ${theta} s ${s.x},${s.y}`;
      const expected = PX({ x: s.x * c - s.y * sn, y: s.x * sn + s.y * c });
      const drawn = turned(at.turn, at.handleP);
      near(drawn.x, expected.x, `P x at ${where}`, 1e-6);
      near(drawn.y, expected.y, `P y at ${where}`, 1e-6);
      // The chain runs from O along the rod by s_x, then to its left by s_y, and the
      // arrow ends where the chain does, all in rod coordinates before the turn.
      assert.deepEqual([at.chainX.x1, at.chainX.y1, at.chainX.x2, at.chainX.y2], [210, 250, PX(s).x, 250], `chain x at ${where}`);
      assert.deepEqual([at.chainY.x1, at.chainY.y1, at.chainY.x2, at.chainY.y2], [PX(s).x, 250, PX(s).x, PX(s).y], `chain y at ${where}`);
      assert.deepEqual([at.arrow.x2, at.arrow.y2], [PX(s).x, PX(s).y], `arrow at ${where}`);
      // The handle used for picking is where P is drawn.
      near(at.handles.p.x, drawn.x, `picked P x at ${where}`, 0.051);
      near(at.handles.p.y, drawn.y, `picked P y at ${where}`, 0.051);
      // P's dot (radius 8) and the rod end's diamond (radius 9) stay inside the frame.
      assert.ok(drawn.x - 8 >= 30 && drawn.x + 8 <= 390 && drawn.y - 8 >= 70 && drawn.y + 8 <= 430, `P leaves the plot at ${where}`);
      const { p, length } = measure(state);
      near(Math.hypot(p.x, p.y), length, `length kept at ${where}`);
      const back = toRod(theta, p);
      near(back.x, s.x, `rod x back at ${where}`); near(back.y, s.y, `rod y back at ${where}`);
      const units = Math.hypot(s.x, s.y);
      if (units === 0) assert.equal(at.arrow.head, false, `zero arrow has a head at ${where}`);
      if (units >= 1) assert.equal(at.arrow.head, true, `long arrow lost its head at ${where}`);
      checked++;
    }
    const atRod = layout({ theta, s: { x: 0, y: 0 } });
    const rodEnd = turned(atRod.turn, PX({ x: ROD, y: 0 }));
    near(rodEnd.x, PX({ x: ROD * c, y: ROD * sn }).x, `rod end x at θ ${theta}`, 1e-6);
    near(rodEnd.y, PX({ x: ROD * c, y: ROD * sn }).y, `rod end y at θ ${theta}`, 1e-6);
    // The handle used for picking is where the rod end is drawn.
    near(atRod.handles.rod.x, rodEnd.x, `picked rod end x at θ ${theta}`, 0.051);
    near(atRod.handles.rod.y, rodEnd.y, `picked rod end y at θ ${theta}`, 0.051);
    assert.ok(rodEnd.x - 9 >= 30 && rodEnd.x + 9 <= 390 && rodEnd.y - 9 >= 70 && rodEnd.y + 9 <= 430, `rod end leaves the plot at θ ${theta}`);
  }
  assert.equal(checked, 360 * 13 * 13);
});

// A reader can check a displayed equation by hand, so "=" must hold for the numbers
// as shown. Whether a number was rounded is judged from the true value here, not
// from the model's own test for exactness.
const shown = (text) => Number(text.replace(/−/g, '-').replace(/[()]/g, ''));
const NEG_ZERO = /(^|[^\d.])−0(?![\d.])/;
test('the readouts say = only when every number shown is exact', () => {
  assert.deepEqual(matrixText(initialState()), { m: [['0.87', '−0.5'], ['0.5', '0.87']], s: ['3', '1'], p: ['2.1', '2.37'], rel: '≈' });
  assert.equal(combinationText(initialState()), '3 × (0.87, 0.5) + 1 × (−0.5, 0.87) ≈ (2.1, 2.37)');
  assert.equal(combinationText({ theta: 90, s: { x: 3, y: 1 } }), '3 × (0, 1) + 1 × (−1, 0) = (−1, 3)');
  assert.equal(combinationText({ theta: 180, s: { x: -2.5, y: 0.5 } }), '(−2.5) × (−1, 0) + 0.5 × (0, −1) = (2.5, −0.5)');
  assert.equal(matrixText({ theta: 60, s: { x: 2, y: 0 } }).rel, '≈', 'sin 60° is rounded even though s_y = 0 hides it');
  for (const theta of ANGLES) {
    const c = Math.cos(rad(theta)), sn = Math.sin(rad(theta));
    for (const s of POINTS) {
      const where = `θ ${theta} s ${s.x},${s.y}`;
      const m = matrixText({ theta, s });
      const [m11, m12, m21, m22] = m.m.flat().map(shown);
      const [s1, s2] = m.s.map(shown), [p1, p2] = m.p.map(shown);
      const truth = [c, -sn, sn, c, s.x, s.y, s.x * c - s.y * sn, s.x * sn + s.y * c];
      const errors = [m11, m12, m21, m22, s1, s2, p1, p2].map((v, i) => Math.abs(v - truth[i]));
      assert.ok(errors.every((e) => e <= 0.005 + 1e-9), `a number shown off by more than rounding at ${where}`);
      const rounded = errors.some((e) => e > 1e-9);
      if (m.rel === '=') {
        assert.ok(!rounded, `rounded numbers joined by = at ${where}`);
        near(m11 * s1 + m12 * s2, p1, `shown row 1 at ${where}`); near(m21 * s1 + m22 * s2, p2, `shown row 2 at ${where}`);
      } else assert.ok(rounded, `exact numbers joined by ≈ at ${where}`);
      const line = combinationText({ theta, s });
      const n = line.match(/^(\S+) × \((\S+), (\S+)\) \+ (\S+) × \((\S+), (\S+)\) ([=≈]) \((\S+), (\S+)\)$/);
      assert.ok(n, `readout shape at ${where}: ${line}`);
      assert.equal(n[7], m.rel, `the two readouts agree at ${where}`);
      if (n[7] === '=') {
        const [a, ex, ey, b, fx, fy, px, py] = [1, 2, 3, 4, 5, 6, 8, 9].map((i) => shown(n[i]));
        near(a * ex + b * fx, px, `shown columns x at ${where}`); near(a * ey + b * fy, py, `shown columns y at ${where}`);
      }
      assert.ok(![line, ...m.m.flat(), ...m.p].some((t) => NEG_ZERO.test(t)), `negative zero at ${where}`);
    }
  }
});

test('the angle wraps into (−180°, 180°] and the rod coordinates snap to the 0.5 grid', () => {
  const state = initialState();
  assert.equal(setAngle(state, 500).theta, 140);
  assert.equal(setAngle(state, -180).theta, 180);
  assert.equal(setAngle(state, -179.6).theta, 180);
  assert.equal(setAngle(state, 89.6).theta, 90);
  assert.ok(Object.is(setAngle(state, -0.2).theta, 0), 'no negative zero');
  assert.equal(setAngle(state, NaN), state);
  assert.equal(setCoord(state, 'x', 2.2).s.x, 2);
  assert.equal(setCoord(state, 'y', 2.3).s.y, 2.5);
  assert.equal(setCoord(state, 'x', 9).s.x, 3);
  assert.equal(setCoord(state, 'y', -9).s.y, -3);
  assert.ok(Object.is(setCoord(state, 'y', -0.1).s.y, 0), 'no negative zero');
  assert.equal(setCoord(state, 'z', 1), state);
  assert.equal(setCoord(state, 'x', NaN), state);
  assert.deepEqual(setCoords(state, { x: -0.2, y: 3.4 }).s, { x: 0, y: 3 });
  assert.ok(Object.is(setCoords(state, { x: -0.2, y: 1 }).s.x, 0), 'no negative zero');
  assert.equal(setCoords(state, { x: 1, y: NaN }), state);
  assert.equal(formatNumber(-0.001), '0');
});

test('dragging the rod end turns the rod; dragging P moves it on the turned grid', () => {
  const state = initialState();
  const grab = { x: 4, y: -3 };
  const at = layout(state).handles;
  const hold = (h) => ({ x: h.x + grab.x, y: h.y + grab.y });
  // The rod end is held by an angle, so an off-centre grab stays put as the rod turns.
  // This press is 20px across the rod from its end, about 7° ahead of it.
  const press = { x: at.rod.x - 10, y: at.rod.y - 17 };
  const offset = rodGrab(state, press);
  assert.deepEqual(dragRod(state, press, offset), state, 'grabbing the rod end alone turns nothing');
  const swing = (deg) => {
    const r = Math.hypot(press.x - 210, press.y - 250), a = Math.atan2(250 - press.y, press.x - 210) + rad(deg);
    return { x: 210 + r * Math.cos(a), y: 250 - r * Math.sin(a) };
  };
  assert.equal(dragRod(state, swing(100), offset).theta, 130, 'the rod follows the pointer round O by the same angle');
  assert.equal(dragRod(state, swing(170), offset).theta, -160, 'and wraps past 180°');
  assert.equal(dragRod(state, PX({ x: 0, y: 2 }), rodGrab(state, at.rod)).theta, 90, 'straight up is 90° for a centred grab');
  assert.equal(dragRod(state, PX({ x: -1, y: -1 }), rodGrab(state, at.rod)).theta, -135);
  assert.equal(dragRod(state, PX({ x: 0, y: 0 }), offset), state, 'a pointer on O has no direction');
  assert.deepEqual(dragPoint(state, hold(at.p), grab), state, 'grabbing P alone moves nothing');
  // At 30°, rod coordinates (1, 2) sit at 1 e′x + 2 e′y in fixed coordinates.
  const c = Math.cos(rad(30)), sn = Math.sin(rad(30));
  const target = PX({ x: 1 * c - 2 * sn, y: 1 * sn + 2 * c });
  assert.deepEqual(dragPoint(state, hold({ x: target.x + 3, y: target.y - 2 }), grab).s, { x: 1, y: 2 }, 'snapped on the turned grid');
  assert.deepEqual(dragPoint(state, hold(PX({ x: -9, y: 9 })), grab).s, { x: -3, y: 3 }, 'clamped to the rod coordinates’ range');
  assert.equal(dragPoint(state, hold(target), grab).theta, 30, 'moving P keeps the angle');
});

test('a press goes to the nearer handle when P sits close to the rod end', () => {
  const state = { theta: 0, s: { x: 3, y: 0 } };
  const { handles } = layout(state);
  assert.deepEqual(handles, { rod: PX({ x: 4, y: 0 }), p: PX({ x: 3, y: 0 }) });
  assert.equal(pickHandle(handles, { x: handles.p.x + 22, y: handles.p.y }, 'p'), 'rod');
  assert.equal(pickHandle(handles, { x: handles.p.x + 18, y: handles.p.y }, 'rod'), 'p');
});

// How far an arrowhead reaches back from the line's end: refX in a 10-unit viewBox
// scaled to markerWidth pixels.
const MARKERS = Object.fromEntries([...SVG.matchAll(/<marker id="([^"]+)"[^>]*refX="([\d.]+)"[^>]*markerWidth="(\d+)"/g)]
  .map((m) => [m[1], { back: (Number(m[2]) * Number(m[3])) / 10, tipBack: ((Number(m[2]) - 9) * Number(m[3])) / 10 }]));

test('P’s arrowhead fits on the shortest arrow that gets one and clears P’s dot', () => {
  assert.deepEqual(Object.keys(MARKERS).sort(), ['rrm-l-p', 'rrm-l-x', 'rrm-l-y']);
  assert.ok(MARKERS['rrm-l-p'].back <= HEAD_MIN, `reaches ${MARKERS['rrm-l-p'].back}px back, beyond HEAD_MIN ${HEAD_MIN}`);
  assert.ok(MARKERS['rrm-l-p'].tipBack >= 8, 'the head clears the 8px dot');
  // The two shortest arrows: half a unit (20px) is shorter than the pulled-back head
  // and gets none; √0.5 of a unit (28px) is the shortest that must keep one.
  assert.ok(MARKERS['rrm-l-p'].back > 20, 'a 20px arrow has no room for the head');
  assert.ok(MARKERS['rrm-l-p'].back <= 40 * Math.SQRT1_2, 'a 28px arrow has room for it');
  assert.equal(layout({ theta: 0, s: { x: 0.5, y: 0 } }).arrow.head, false);
  assert.equal(layout({ theta: 0, s: { x: 0.5, y: 0.5 } }).arrow.head, true);
  // e′x and e′y are always one unit (40px) long, so their heads always fit.
  for (const id of ['rrm-l-x', 'rrm-l-y']) assert.ok(MARKERS[id].back <= 40, `${id} head longer than the axis`);
});

// The static SVG is what readers without JavaScript and printed copies get, so it
// must be exactly the lab's first frame.
test('the static picture is the first frame of the live lab', () => {
  const tag = (part) => {
    const found = SVG.match(new RegExp(`<[^>]*data-part="${part}"[^>]*>`))?.[0];
    assert.ok(found, `data-part="${part}" is missing`);
    return found;
  };
  const attr = (t, name) => t.match(new RegExp(`\\s${name}="([^"]*)"`))?.[1];
  const text = (part) => SVG.match(new RegExp(`data-part="${part}"[^>]*>([^<]*)<`))?.[1];
  const state = initialState();
  const at = layout(state);
  const m = matrixText(state);
  for (const part of ['frame', 'grid-frame']) assert.equal(attr(tag(part), 'transform'), at.turn, `${part} turn`);
  for (const [part, key] of [['chain-x', 'chainX'], ['chain-y', 'chainY']]) {
    for (const name of ['x1', 'y1', 'x2', 'y2']) assert.equal(attr(tag(part), name), String(at[key][name]), `${part} ${name}`);
  }
  assert.equal(attr(tag('arrow-p'), 'x2'), String(at.arrow.x2));
  assert.equal(attr(tag('arrow-p'), 'y2'), String(at.arrow.y2));
  // The runtime takes the arrowhead from data-marker, so the arrow carries it.
  assert.equal(attr(tag('arrow-p'), 'data-marker'), 'url(#rrm-l-p)');
  assert.equal(attr(tag('arrow-p'), 'marker-end'), at.arrow.head ? 'url(#rrm-l-p)' : undefined);
  assert.equal(attr(tag('handle-p'), 'transform'), `translate(${at.handleP.x} ${at.handleP.y})`);
  assert.equal(attr(tag('handle-rod'), 'transform'), `translate(${PX({ x: ROD, y: 0 }).x} 250)`);
  assert.equal(text('theta'), 'θ = 30°');
  assert.deepEqual([text('m11'), text('m12'), text('m21'), text('m22')], m.m.flat());
  assert.deepEqual([text('s1'), text('s2'), text('p1'), text('p2'), text('rel')], [...m.s, ...m.p, m.rel]);
  // The first column is drawn in e′x's amber and the second in e′y's green.
  for (const part of ['m11', 'm21']) assert.equal(attr(tag(part), 'fill'), '#fbbf24', `${part} colour`);
  for (const part of ['m12', 'm22']) assert.equal(attr(tag(part), 'fill'), '#4ade80', `${part} colour`);
});
