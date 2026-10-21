import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import {
  initialState, measure, move, moveTo, dragTo, layout, toSvg, formatNumber, LIMITS, PLOT, UNIT, HEAD_MIN,
} from '../src/labs/vector-projection-model.mjs';

const near = (actual, expected, message, eps = 1e-9) => assert.ok(Math.abs(actual - expected) < eps, `${message}: ${actual} ≠ ${expected}`);
const SVG = readFileSync(new URL('../public/images/robotics-vector-projection/projection-lab.svg', import.meta.url), 'utf8');
const grid = (min, max) => { const out = []; for (let v = min; v <= max; v += LIMITS.step) out.push(v); return out; };
const pairs = (values) => values.flatMap((x) => values.map((y) => ({ x, y })));
const A_VALUES = pairs(grid(LIMITS.min, LIMITS.max));
const D_VALUES = pairs(grid(LIMITS.dirMin, LIMITS.dirMax)).filter((d) => d.x !== 0 || d.y !== 0);

test('the article example: (1, 3) onto (0.6, 0.8)', () => {
  const v = measure(initialState());
  near(v.u.x, 0.6, 'u x'); near(v.u.y, 0.8, 'u y');
  near(v.s, 3, 'a · u');
  near(v.proj.x, 1.8, 'F x'); near(v.proj.y, 2.4, 'F y');
  near(v.rest.x, -0.8, 'rest x'); near(v.rest.y, 0.6, 'rest y');
  near(v.lengths.rest, 1, '|rest|');
  near(v.lengths.a ** 2, 10, '|a|²');
  near(v.phi, (Math.acos(3 / Math.sqrt(10)) * 180) / Math.PI, 'φ');
  assert.equal(formatNumber(v.phi), '18.43');
});

test('the perpendicular and the negative examples', () => {
  const d = { x: 3, y: 4 };
  near(measure({ a: { x: -4, y: 3 }, d }).s, 0, '(−4, 3) · u');
  near(measure({ a: { x: -4, y: 3 }, d }).phi, 90, 'perpendicular');
  near(measure({ a: { x: -3, y: 1 }, d }).s, -1, '(−3, 1) · u');
  near(measure({ a: { x: 2, y: 5 }, d: { x: 1, y: 0 } }).s, 2, 'onto e_x the shadow is the x component');
  near(measure({ a: { x: 2, y: 5 }, d: { x: 0, y: 1 } }).s, 5, 'onto e_y it is the y component');
  assert.equal(measure({ a: { x: 0, y: 0 }, d }).phi, null, 'a zero vector has no angle');
});

test('inputs snap and clamp, and the arrow keys carry D across the origin', () => {
  const state = initialState();
  assert.equal(move(state, 'a', 'x', 9).a.x, 3);
  assert.equal(move(state, 'd', 'x', -9).d.x, -4);
  assert.equal(move(state, 'a', 'y', 1.3).a.y, 1.5);
  assert.ok(Object.is(move(state, 'a', 'x', -0.1).a.x, 0), 'no negative zero');
  assert.equal(move(state, 'x', 'x', 1), state);
  assert.equal(move(state, 'a', 'x', Infinity), state);
  const onAxis = move(state, 'd', 'x', 0);
  assert.deepEqual(onAxis.d, { x: 0, y: 4 });
  // A step from 0.5 down to 0 would put D on the origin; it lands on −0.5 instead.
  let d = { ...state, d: { x: 0, y: 0.5 } };
  d = move(d, 'd', 'y', 0);
  assert.deepEqual(d.d, { x: 0, y: -0.5 });
  assert.deepEqual(move(d, 'd', 'y', 0).d, { x: 0, y: 0.5 }, 'and back up across it');
  assert.deepEqual(move({ ...state, d: { x: 0.5, y: 0 } }, 'd', 'x', 0).d, { x: -0.5, y: 0 });
});

test('a drag sets both coordinates at once and refuses only the origin itself', () => {
  const state = { ...initialState(), d: { x: 0.5, y: 0 } };
  assert.deepEqual(moveTo(state, 'd', { x: 0, y: 0.5 }).d, { x: 0, y: 0.5 }, 'a diagonal past the origin is not refused');
  assert.equal(moveTo(state, 'd', { x: 0.1, y: -0.1 }), state, 'dropping D on the origin keeps the old direction');
  const grab = { x: -4, y: 6 };
  const at = layout(state);
  assert.deepEqual(dragTo(state, 'd', { x: at.d.x + grab.x, y: at.d.y + grab.y }, grab), state, 'grabbing alone moves nothing');
  const target = toSvg({ x: -2, y: 0.5 });
  assert.deepEqual(dragTo(state, 'a', { x: target.x + grab.x, y: target.y + grab.y }, grab).a, { x: -2, y: 0.5 });
  assert.deepEqual(dragTo(state, 'd', toSvg({ x: 0, y: 0.5 }), { x: 0, y: 0 }).d, { x: 0, y: 0.5 }, 'the drag itself moves diagonally past the origin');
});

test('over every state, a = s u + r with r ⟂ u, and F is the closest point of the line', () => {
  let checked = 0;
  for (const d of D_VALUES) {
    for (const a of A_VALUES) {
      const v = measure({ a, d });
      const where = `a ${a.x},${a.y} D ${d.x},${d.y}`;
      near(Math.hypot(v.u.x, v.u.y), 1, `|u| at ${where}`);
      near(v.u.x * d.y - v.u.y * d.x, 0, `u along D at ${where}`);
      assert.ok(v.u.x * d.x + v.u.y * d.y > 0, `u points toward D at ${where}`);
      near(v.proj.x + v.rest.x, a.x, `a x at ${where}`); near(v.proj.y + v.rest.y, a.y, `a y at ${where}`);
      near(v.rest.x * v.u.x + v.rest.y * v.u.y, 0, `r · u at ${where}`);
      near(v.lengths.a ** 2, v.s ** 2 + v.lengths.rest ** 2, `Pythagoras at ${where}`, 1e-9);
      if (v.phi === null) assert.deepEqual(a, { x: 0, y: 0 }, `φ is missing only for a zero a at ${where}`);
      else {
        assert.ok(v.phi >= 0 && v.phi <= 180, `φ is a size in [0°, 180°] at ${where}`);
        near(v.lengths.a * Math.cos((v.phi * Math.PI) / 180), v.s, `|a| cos φ at ${where}`, 1e-9);
      }
      // Moving along the line away from F only adds (s − t)² to the squared distance.
      for (const dt of [-1, -0.25, 0.25, 1]) {
        const t = v.s + dt;
        const gap = (a.x - t * v.u.x) ** 2 + (a.y - t * v.u.y) ** 2;
        near(gap - v.lengths.rest ** 2, dt * dt, `closest point at ${where}`, 1e-9);
      }
      checked++;
    }
  }
  assert.equal(checked, 13 * 13 * (17 * 17 - 1));
});

// Independent of the model: pixel geometry read off the picture (origin at
// (200, 250), 40px a unit), and text boxes for the O label and the tick numbers
// as the static SVG places them (approximate glyph boxes at font size 18–20).
const PX = ({ x, y }) => ({ x: 200 + 40 * x, y: 250 - 40 * y });
const O = PX({ x: 0, y: 0 });
const TEXT = [
  { name: 'O', x1: 174, x2: 188, y1: 226, y2: 240 },
  ...[-4, -2, 2, 4].map((n) => ({ name: `x tick ${n}`, x1: PX({ x: n, y: 0 }).x - 11, x2: PX({ x: n, y: 0 }).x + 11, y1: 258, y2: 272 })),
  ...[-4, -2, 2, 4].map((n) => ({ name: `y tick ${n}`, x1: 166, x2: 188, y1: PX({ x: 0, y: n }).y - 8, y2: PX({ x: 0, y: n }).y + 6 })),
];
const PLOT_BOX = { x1: 20, x2: 380, y1: 70, y2: 430 };
const inside = ({ x, y }) => x >= PLOT_BOX.x1 && x <= PLOT_BOX.x2 && y >= PLOT_BOX.y1 && y <= PLOT_BOX.y2;
const sub = (p, q) => ({ x: p.x - q.x, y: p.y - q.y });
const dot = (p, q) => p.x * q.x + p.y * q.y;
const cross = (p, q) => p.x * q.y - p.y * q.x;
const len = (p) => Math.hypot(p.x, p.y);
const markPoints = (d) => [...d.matchAll(/-?[\d.]+ -?[\d.]+/g)].map((m) => { const [x, y] = m[0].split(' ').map(Number); return { x, y }; });

test('the picture geometry the tests assume is the one drawn', () => {
  assert.match(SVG, /<line x1="14" y1="250" x2="382" y2="250"/);
  assert.match(SVG, /<line x1="200" y1="436" x2="200" y2="64"/);
  assert.match(SVG, /<text x="188" y="240"[^>]*text-anchor="end">O</);
  assert.match(SVG, /M240 70V430 M20 210H380/, 'grid lines one unit from the axes');
});

test('over every state, the drawing stays in the plot and each mark sits where it should', () => {
  let marks = 0;
  for (const d of D_VALUES) {
    for (const a of A_VALUES) {
      const at = layout({ a, d });
      const where = `a ${a.x},${a.y} D ${d.x},${d.y}`;
      const A = PX(a), D = PX(d), dir = sub(D, O);
      const unitDir = { x: dir.x / len(dir), y: dir.y / len(dir) };
      for (const point of [at.foot, at.a, at.d, at.u.from, at.u.to, at.ell.from, at.ell.to]) {
        assert.ok(inside(point), `outside the plot at ${where}`);
        // Coordinates are written to the SVG with at most one decimal.
        for (const c of [point.x, point.y]) assert.ok(Math.abs(c * 10 - Math.round(c * 10)) < 1e-6, `${c} at ${where}`);
      }
      // ℓ passes through O and D and ends on the edge of the ±PLOT square.
      for (const end of [at.ell.from, at.ell.to]) {
        near(cross(sub(end, O), dir), 0, `line end off the line at ${where}`, 0.1 * len(dir));
        const m = sub(end, O);
        near(Math.max(Math.abs(m.x), Math.abs(m.y)), PLOT * UNIT, `line end not at the edge at ${where}`, 0.2);
      }
      // F is the foot of the perpendicular from A: on ℓ, with A − F perpendicular to ℓ.
      near(cross(sub(at.foot, O), unitDir), 0, `F off the line at ${where}`, 0.1);
      near(dot(sub(A, at.foot), unitDir), 0, `A − F not perpendicular at ${where}`, 0.1);
      // u: one unit long, parallel to ℓ and pointing at D, 16px to one side of it,
      // and clear of the O label and the tick numbers.
      const uVec = sub(at.u.to, at.u.from);
      near(len(uVec), UNIT, `u length at ${where}`, 0.2);
      near(cross(uVec, unitDir), 0, `u not parallel at ${where}`, 0.2);
      assert.ok(dot(uVec, unitDir) > 0, `u points away from D at ${where}`);
      near(Math.abs(cross(sub(at.u.from, O), unitDir)), 16, `u not 16px from ℓ at ${where}`, 0.2);
      for (let i = 0; i <= 40; i++) {
        const p = { x: at.u.from.x + (uVec.x * i) / 40, y: at.u.from.y + (uVec.y * i) / 40 };
        for (const t of TEXT) assert.ok(!(p.x > t.x1 && p.x < t.x2 && p.y > t.y1 && p.y < t.y2), `u crosses ${t.name} at ${where}`);
      }
      // a's arrowhead: never on a zero arrow, always on one a unit or longer.
      const aUnits = Math.hypot(a.x, a.y);
      if (aUnits === 0) assert.equal(at.a.head, false, `zero a has a head at ${where}`);
      if (aUnits >= 1) assert.equal(at.a.head, true, `long a lost its head at ${where}`);
      // The right-angle mark: two 9px legs from F, one along ℓ toward O and one up
      // the remainder toward A, and clear of a's 8px handle.
      const rest = len(sub(A, at.foot));
      if (rest >= 40) assert.notEqual(at.rightAngle, '', `a long remainder lost its mark at ${where}`);
      if (at.rightAngle === '') continue;
      marks++;
      const [p1, p2, p3] = markPoints(at.rightAngle);
      const leg1 = sub(p1, at.foot), leg3 = sub(p3, at.foot);
      near(len(leg1), 9, `leg along ℓ at ${where}`, 0.2);
      near(len(leg3), 9, `leg along r at ${where}`, 0.2);
      near(cross(leg1, unitDir), 0, `leg not along ℓ at ${where}`, 0.2);
      if (len(sub(at.foot, O)) > 1) assert.ok(dot(leg1, sub(O, at.foot)) > 0, `leg points away from O at ${where}`);
      assert.ok(dot(leg3, sub(A, at.foot)) > 0 && Math.abs(cross(leg3, sub(A, at.foot))) < 0.2 * rest, `leg not toward A at ${where}`);
      near(p2.x, p1.x + leg3.x, `corner x at ${where}`, 0.2); near(p2.y, p1.y + leg3.y, `corner y at ${where}`, 0.2);
      for (const p of [p1, p2, p3]) assert.ok(inside(p), `mark outside the plot at ${where}`);
      for (const p of [p2, p3]) assert.ok(len(sub(p, A)) >= 8, `mark under a's handle at ${where}`);
    }
  }
  assert.ok(marks > 30000, `only ${marks} states drew a mark`);
});

test('a’s arrowhead fits on the shortest arrow that gets one, and stops short of the handle', () => {
  const m = SVG.match(/<marker id="rvp-p-a"[^>]*refX="([\d.]+)"[^>]*markerWidth="(\d+)"/);
  assert.ok(m, 'marker rvp-p-a');
  const [refX, width] = [Number(m[1]), Number(m[2])];
  assert.ok((refX * width) / 10 <= HEAD_MIN, 'the head reaches past the tail of the shortest headed arrow');
  assert.ok(((refX - 9) * width) / 10 >= 8, 'the head tip stops outside the 8px blue dot');
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
  const at = layout(initialState());
  const expect = {
    ell: { x1: at.ell.from.x, y1: at.ell.from.y, x2: at.ell.to.x, y2: at.ell.to.y },
    shadow: { x1: at.o.x, y1: at.o.y, x2: at.foot.x, y2: at.foot.y },
    rest: { x1: at.foot.x, y1: at.foot.y, x2: at.a.x, y2: at.a.y },
    a: { x1: at.o.x, y1: at.o.y, x2: at.a.x, y2: at.a.y },
    u: { x1: at.u.from.x, y1: at.u.from.y, x2: at.u.to.x, y2: at.u.to.y },
    foot: { cx: at.foot.x, cy: at.foot.y },
  };
  for (const [part, values] of Object.entries(expect)) {
    for (const [name, value] of Object.entries(values)) assert.equal(attr(tag(part), name), String(value), `${part} ${name}`);
  }
  assert.equal(attr(tag('right-angle'), 'd'), at.rightAngle);
  // The runtime takes the arrowhead from data-marker, so the arrow carries it.
  assert.equal(attr(tag('a'), 'data-marker'), 'url(#rvp-p-a)');
  assert.equal(attr(tag('a'), 'marker-end'), at.a.head ? 'url(#rvp-p-a)' : undefined);
  assert.equal(attr(tag('handle-a'), 'transform'), `translate(${at.a.x} ${at.a.y})`);
  assert.equal(attr(tag('handle-d'), 'transform'), `translate(${at.d.x} ${at.d.y})`);
  assert.match(SVG, /data-part="summary"[^>]*>a · u = 3, 정사영 \(1\.8, 2\.4\)</);
});
