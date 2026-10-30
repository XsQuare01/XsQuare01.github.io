import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import {
  initialState, measure, setAngle, grab, dragTo, layout, distanceText, LIMITS, ARC1, ARC2, EXTENSION, STILL_RADIUS,
} from '../src/labs/arm-forward-model.mjs';
import { pickHandle } from '../src/labs/pick-handle.mjs';

const near = (actual, expected, message, tol = 1e-9) => assert.ok(Math.abs(actual - expected) < tol, `${message}: ${actual} ≠ ${expected}`);
const SVG = readFileSync(new URL('../public/images/robotics-two-link-arm/forward-lab.svg', import.meta.url), 'utf8');
const ANGLES = [];
for (let t = LIMITS.thetaMin; t <= LIMITS.thetaMax; t += LIMITS.step) ANGLES.push(t);
const rad = (d) => (d * Math.PI) / 180;
// The difference of two directions in degrees, brought into (−180°, 180°].
const turn = (d) => { const v = (((d + 180) % 360) + 360) % 360 - 180; return v === -180 ? 180 : v; };

// The pixel geometry is read off the static picture (axes through (210, 250), ticks
// 50px apart) rather than taken from the model's toSvg.
const PX = ({ x, y }) => ({ x: 210 + 50 * x, y: 250 - 50 * y });
test('the test geometry matches the axes and ticks the picture draws', () => {
  assert.match(SVG, /<line x1="35" y1="250" x2="385" y2="250"/);
  assert.match(SVG, /<line x1="210" y1="75" x2="210" y2="425"/);
  assert.match(SVG, /M160 246V254 M206 300H214 M260 246V254/, 'ticks one unit either side of O');
});

test('the article example: (30°, 60°) puts the tip at (√3, 2), straight above the elbow', () => {
  const v = measure(initialState());
  near(v.elbow.x, Math.sqrt(3), 'E x'); near(v.elbow.y, 1, 'E y');
  near(v.tip.x, Math.sqrt(3), 'P x'); near(v.tip.y, 2, 'P y');
  assert.equal(v.heading2, 90, 'the second link points along θ1 + θ2');
  near(v.d2, 7, '‖P‖²');
  assert.equal(distanceText(initialState()), '5 + 4 × 0.5 = 7');
  assert.equal(distanceText({ theta1: 0, theta2: 120 }), '5 + 4 × (−0.5) = 3');
  assert.equal(distanceText({ theta1: 0, theta2: 45 }), '5 + 4 × 0.71 ≈ 7.83');
  const folded = measure({ theta1: 0, theta2: 180 });
  near(folded.tip.x, 1, 'folded tip'); near(folded.d, 1, 'folded distance');
});

// The angle of a drawn segment in model terms (counterclockwise from +x), read from
// its SVG end points, where y points down.
const direction = (s) => (Math.atan2(-(s.y2 - s.y1), s.x2 - s.x1) * 180) / Math.PI;
const length = (s) => Math.hypot(s.x2 - s.x1, s.y2 - s.y1);
// An arc path "Mx yAr r 0 0 f x y": its two end points and sweep flag.
const ARC = /^M(-?[\d.]+) (-?[\d.]+)A([\d.]+) \3 0 0 ([01]) (-?[\d.]+) (-?[\d.]+)$/;

test('over every state, the drawn arm is the article’s formula and stays in the plot', () => {
  let checked = 0;
  for (const theta1 of ANGLES) {
    for (const theta2 of ANGLES) {
      const at = layout({ theta1, theta2 });
      const where = `(${theta1}°, ${theta2}°)`;
      const elbow = PX({ x: 2 * Math.cos(rad(theta1)), y: 2 * Math.sin(rad(theta1)) });
      const tip = PX({ x: 2 * Math.cos(rad(theta1)) + Math.cos(rad(theta1 + theta2)), y: 2 * Math.sin(rad(theta1)) + Math.sin(rad(theta1 + theta2)) });
      assert.deepEqual([at.link1.x1, at.link1.y1], [210, 250], `link 1 starts at O ${where}`);
      near(at.link1.x2, elbow.x, `E x ${where}`, 0.051); near(at.link1.y2, elbow.y, `E y ${where}`, 0.051);
      assert.deepEqual([at.link2.x1, at.link2.y1], [at.link1.x2, at.link1.y2], `link 2 starts at E ${where}`);
      near(at.link2.x2, tip.x, `P x ${where}`, 0.051); near(at.link2.y2, tip.y, `P y ${where}`, 0.051);
      assert.deepEqual([at.reach.x2, at.reach.y2], [at.link2.x2, at.link2.y2], `a + b ends at P ${where}`);
      // The handles a reader grabs sit where the formula puts E and P.
      near(at.handles.elbow.x, elbow.x, `E handle x ${where}`, 0.051); near(at.handles.elbow.y, elbow.y, `E handle y ${where}`, 0.051);
      near(at.handles.tip.x, tip.x, `P handle x ${where}`, 0.051); near(at.handles.tip.y, tip.y, `P handle y ${where}`, 0.051);
      near(length(at.link1), 100, `link 1 is L1 long ${where}`, 0.15);
      near(length(at.link2), 50, `link 2 is L2 long ${where}`, 0.15);
      near(turn(direction(at.link2) - direction(at.link1) - theta2), 0, `θ2 is the turn from link 1 to link 2 ${where}`, 0.2);
      near(turn(direction(at.extension) - direction(at.link1)), 0, `the extension carries on along link 1 ${where}`, 0.2);
      near(length(at.extension), EXTENSION, `extension length ${where}`, 0.15);
      // Each arc runs from the reference direction to the link and turns the right way.
      for (const [d, c, r, from, by] of [[at.arc1, { x: 210, y: 250 }, ARC1, 0, theta1], [at.arc2, at.handles.elbow, ARC2, theta1, theta2]]) {
        if (by === 0) { assert.equal(d, '', `no arc for a zero angle ${where}`); continue; }
        const m = d.match(ARC);
        assert.ok(m, `arc shape ${where}: ${d}`);
        const [sx, sy, rr, flag, ex, ey] = [m[1], m[2], m[3], m[4], m[5], m[6]].map(Number);
        assert.equal(rr, r);
        near(turn(direction({ x1: c.x, y1: c.y, x2: sx, y2: sy }) - from), 0, `arc start ${where}`, 0.3);
        near(turn(direction({ x1: c.x, y1: c.y, x2: ex, y2: ey }) - from - by), 0, `arc end ${where}`, 0.3);
        // 180° is the representative of a half turn, so it sweeps counterclockwise.
        assert.equal(flag, by > 0 ? 0 : 1, `arc sweep ${where}`);
      }
      // E's dot (radius 8) and P's diamond (radius 10) stay inside the frame.
      for (const [h, r] of [[at.handles.elbow, 8], [at.handles.tip, 10]]) {
        assert.ok(h.x - r >= 35 && h.x + r <= 385 && h.y - r >= 75 && h.y + r <= 425, `handle leaves the plot ${where}`);
      }
      near(measure({ theta1, theta2 }).d2, 5 + 4 * Math.cos(rad(theta2)), `‖P‖² depends on θ2 alone ${where}`, 1e-9);
      checked++;
    }
  }
  assert.equal(checked, 360 * 360);
});

// A reader can check a displayed equation by hand, so "=" must hold for the numbers
// as shown. Whether a number was rounded is judged from the true value here.
const shown = (text) => Number(text.replace(/−/g, '-').replace(/[()]/g, ''));
test('the distance readout says = only when the numbers shown are exact', () => {
  for (const theta2 of ANGLES) {
    const text = distanceText({ theta1: 0, theta2 });
    const m = text.match(/^5 \+ 4 × (\S+) ([=≈]) (\S+)$/);
    assert.ok(m, `readout shape at θ2 ${theta2}: ${text}`);
    const [c, d2] = [shown(m[1]), shown(m[3])];
    const truth = [Math.cos(rad(theta2)), 5 + 4 * Math.cos(rad(theta2))];
    const errors = [c - truth[0], d2 - truth[1]].map(Math.abs);
    assert.ok(errors.every((e) => e <= 0.005 + 1e-9), `a number shown off by more than rounding at θ2 ${theta2}`);
    if (m[2] === '=') { assert.ok(errors.every((e) => e < 1e-9), `rounded numbers joined by = at θ2 ${theta2}`); near(5 + 4 * c, d2, 'shown numbers add up'); }
    else assert.ok(errors.some((e) => e > 1e-9), `exact numbers joined by ≈ at θ2 ${theta2}`);
    assert.ok(!/(^|[^\d.])−0(?![\d.])/.test(text), `negative zero at θ2 ${theta2}`);
  }
});

test('both joint angles wrap into (−180°, 180°] in whole degrees', () => {
  const state = initialState();
  assert.equal(setAngle(state, 'theta1', 500).theta1, 140);
  assert.equal(setAngle(state, 'theta2', -180).theta2, 180);
  assert.equal(setAngle(state, 'theta2', -179.6).theta2, 180);
  assert.equal(setAngle(state, 'theta1', 89.6).theta1, 90);
  assert.ok(Object.is(setAngle(state, 'theta1', -0.2).theta1, 0), 'no negative zero');
  assert.equal(setAngle(state, 'theta3', 10), state);
  assert.equal(setAngle(state, 'theta1', NaN), state);
});

test('dragging E turns the whole arm about O; dragging P turns the second link about E', () => {
  const state = initialState();
  const { handles } = layout(state);
  // A press 12px across link 1 from E and one 10px across link 2 from P.
  const pressE = { x: handles.elbow.x - 6, y: handles.elbow.y - 10 };
  const pressP = { x: handles.tip.x - 10, y: handles.tip.y };
  const offE = grab(state, 'elbow', pressE), offP = grab(state, 'tip', pressP);
  assert.deepEqual(dragTo(state, 'elbow', pressE, offE), state, 'grabbing E alone turns nothing');
  assert.deepEqual(dragTo(state, 'tip', pressP, offP), state, 'grabbing P alone turns nothing');
  const about = (p, c, deg) => {
    const r = Math.hypot(p.x - c.x, p.y - c.y), a = Math.atan2(c.y - p.y, p.x - c.x) + rad(deg);
    return { x: c.x + r * Math.cos(a), y: c.y - r * Math.sin(a) };
  };
  const turnedArm = dragTo(state, 'elbow', about(pressE, { x: 210, y: 250 }, 100), offE);
  assert.deepEqual(turnedArm, { theta1: 130, theta2: 60 }, 'E swings the arm; θ2 rides along');
  assert.deepEqual(dragTo(state, 'elbow', about(pressE, { x: 210, y: 250 }, 170), offE), { theta1: -160, theta2: 60 }, 'and wraps past 180°');
  assert.deepEqual(dragTo(state, 'tip', about(pressP, handles.elbow, -90), offP), { theta1: 30, theta2: -30 }, 'P turns the second link only');
  assert.deepEqual(dragTo(state, 'elbow', { x: 210, y: 250 }, offE), state, 'a pointer on O has no direction');
  assert.deepEqual(dragTo(state, 'tip', PX(measure(state).elbow), offP), state, 'a pointer on E has no direction');
  // Near a centre each pixel swings the direction wildly, so a few pixels away it
  // still keeps the angle; once clear of it the drag turns the link again.
  const e = PX(measure(state).elbow);
  assert.deepEqual(dragTo(state, 'tip', { x: e.x + STILL_RADIUS - 1, y: e.y }, offP), state, 'just off E keeps θ2');
  assert.deepEqual(dragTo(state, 'elbow', { x: 210, y: 250 - (STILL_RADIUS - 1) }, offE), state, 'just off O keeps θ1');
  assert.notDeepEqual(dragTo(state, 'tip', { x: e.x + STILL_RADIUS + 1, y: e.y }, offP), state, 'clear of E the drag turns again');
  assert.equal(dragTo(state, 'shoulder', pressE, 0), state);
});

test('a press goes to the nearer handle when the arm folds back', () => {
  const { handles } = layout({ theta1: 0, theta2: 180 });
  assert.deepEqual(handles, { elbow: PX({ x: 2, y: 0 }), tip: PX({ x: 1, y: 0 }) });
  assert.equal(pickHandle(handles, { x: handles.tip.x + 30, y: handles.tip.y }, 'tip'), 'elbow');
  assert.equal(pickHandle(handles, { x: handles.tip.x + 20, y: handles.tip.y }, 'elbow'), 'tip');
});

// How far an arrowhead reaches back from the line's end: refX in a 10-unit viewBox
// scaled to markerWidth pixels.
const MARKERS = Object.fromEntries([...SVG.matchAll(/<marker id="([^"]+)"[^>]*refX="([\d.]+)"[^>]*markerWidth="(\d+)"/g)]
  .map((m) => [m[1], { back: (Number(m[2]) * Number(m[3])) / 10, tipBack: ((Number(m[2]) - 9) * Number(m[3])) / 10 }]));

test('the link heads fit on the links and stop short of the handles', () => {
  assert.deepEqual(Object.keys(MARKERS).sort(), ['rta-l-a', 'rta-l-b']);
  assert.ok(MARKERS['rta-l-a'].back <= 100 && MARKERS['rta-l-b'].back <= 50, 'heads longer than the links');
  assert.ok(MARKERS['rta-l-a'].tipBack >= 8, 'the first head clears E’s 8px dot');
  assert.ok(MARKERS['rta-l-b'].tipBack >= 10, 'the second head clears P’s 10px diamond');
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
  for (const part of ['link1', 'link2', 'reach', 'extension']) {
    for (const name of ['x1', 'y1', 'x2', 'y2']) assert.equal(attr(tag(part), name), String(at[part][name]), `${part} ${name}`);
  }
  assert.equal(attr(tag('arc1'), 'd'), at.arc1);
  assert.equal(attr(tag('arc2'), 'd'), at.arc2);
  for (const key of ['elbow', 'tip']) assert.equal(attr(tag(`handle-${key}`), 'transform'), `translate(${at.handles[key].x} ${at.handles[key].y})`);
  assert.match(SVG, /data-part="summary"[^>]*>손끝 P ≈ \(1\.73, 2\)</);
});
