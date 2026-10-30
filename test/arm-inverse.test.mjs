import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import {
  initialState, measure, setCoord, setTarget, dragTo, layout, cosText, poseText, LIMITS,
} from '../src/labs/arm-inverse-model.mjs';
import { forward } from '../src/labs/two-link.mjs';

const near = (actual, expected, message, tol = 1e-9) => assert.ok(Math.abs(actual - expected) < tol, `${message}: ${actual} ≠ ${expected}`);
const SVG = readFileSync(new URL('../public/images/robotics-two-link-arm/inverse-lab.svg', import.meta.url), 'utf8');
const VALUES = [];
for (let v = LIMITS.min; v <= LIMITS.max; v += LIMITS.step) VALUES.push(v);
const TARGETS = VALUES.flatMap((x) => VALUES.map((y) => ({ x, y })));

// The pixel geometry is read off the static picture rather than the model's toSvg:
// axes through (210, 250), the ring's circles of radius 150 and 50 about O.
const PX = ({ x, y }) => ({ x: 210 + 50 * x, y: 250 - 50 * y });
test('the test geometry matches the axes and the ring the picture draws', () => {
  assert.match(SVG, /<line x1="35" y1="250" x2="385" y2="250"/);
  assert.match(SVG, /<line x1="210" y1="75" x2="210" y2="425"/);
  assert.match(SVG, /<circle cx="210" cy="250" r="150" fill="none"/, 'the outer edge, L1 + L2 = 3');
  assert.match(SVG, /<circle cx="210" cy="250" r="50" fill="none"/, 'the inner edge, L1 − L2 = 1');
});

test('the article examples: two postures for (2, 1), one on each edge, none outside', () => {
  const [a, b] = measure(initialState()).poses;
  assert.equal(measure(initialState()).poses.length, 2);
  near(a.theta1, 0, '① θ1'); near(a.theta2, 90, '① θ2');
  near(a.elbow.x, 2, '① E x'); near(a.elbow.y, 0, '① E y');
  near(b.theta1, (2 * Math.atan2(1, 2) * 180) / Math.PI, '② θ1'); near(b.theta2, -90, '② θ2');
  near(b.elbow.x, 1.2, '② E x'); near(b.elbow.y, 1.6, '② E y');
  near(Math.cos((b.theta1 * Math.PI) / 180), 0.6, '② cos θ1');
  const one = (target) => { const p = measure({ target }).poses; assert.equal(p.length, 1, `one posture at ${target.x},${target.y}`); return p[0]; };
  const outer = one({ x: 3, y: 0 }); near(outer.theta1, 0, 'stretched θ1'); near(outer.theta2, 0, 'stretched θ2');
  const inner = one({ x: 1, y: 0 }); near(inner.theta1, 0, 'folded θ1'); near(inner.theta2, 180, 'folded θ2');
  const left = one({ x: -3, y: 0 }); near(left.theta1, 180, 'stretched left θ1'); near(left.theta2, 0, 'stretched left θ2');
  for (const target of [{ x: 3, y: 1 }, { x: 0.5, y: 0 }, { x: 0, y: 0 }]) assert.equal(measure({ target }).poses.length, 0, `${target.x},${target.y} is out of reach`);
  assert.equal(cosText(initialState()), '(5 − 5) / 4 = 0');
  assert.equal(poseText(a), '(θ1, θ2) = (0°, 90°)');
  assert.equal(poseText(b), '(θ1, θ2) ≈ (53.13°, −90°)');
});

// Reflection across the line through O along unit u: 2(v · u)u − v.
const mirror = (v, u) => { const k = 2 * (v.x * u.x + v.y * u.y); return { x: k * u.x - v.x, y: k * u.y - v.y }; };

test('over every target, the postures are counted, drawn and mirrored as the article says', () => {
  for (const target of TARGETS) {
    const where = `T ${target.x},${target.y}`;
    const d2 = target.x * target.x + target.y * target.y;
    // Independent of the model: the ring is 1 ≤ d² ≤ 9, its edges hold one posture.
    const expected = d2 < 1 || d2 > 9 ? 0 : d2 === 1 || d2 === 9 ? 1 : 2;
    const { poses } = measure({ target });
    assert.equal(poses.length, expected, `posture count at ${where}`);
    const at = layout({ target });
    assert.equal(at.reachable, expected > 0, `target colour at ${where}`);
    assert.deepEqual(at.target, PX(target), `target drawn at ${where}`);
    at.arms.forEach((arm, i) => assert.equal(arm.visible, i < expected, `arm ${i + 1} visibility at ${where}`));
    poses.forEach((pose, i) => {
      const reached = forward(pose.theta1, pose.theta2).tip;
      near(reached.x, target.x, `posture ${i + 1} reaches x at ${where}`); near(reached.y, target.y, `posture ${i + 1} reaches y at ${where}`);
      assert.ok(pose.theta1 > -180 && pose.theta1 <= 180 && pose.theta2 > -180 && pose.theta2 <= 180, `angles in range at ${where}`);
      // The drawn elbow is L1 from O and L2 from the target, in pixels.
      const arm = at.arms[i];
      near(Math.hypot(arm.elbow.x - 210, arm.elbow.y - 250), 100, `elbow ${i + 1} from O at ${where}`, 0.15);
      near(Math.hypot(arm.elbow.x - at.target.x, arm.elbow.y - at.target.y), 50, `elbow ${i + 1} from T at ${where}`, 0.15);
      assert.deepEqual([arm.link1.x2, arm.link1.y2, arm.link2.x1, arm.link2.y1, arm.link2.x2, arm.link2.y2],
        [arm.elbow.x, arm.elbow.y, arm.elbow.x, arm.elbow.y, at.target.x, at.target.y], `arm ${i + 1} joins O, E and T at ${where}`);
    });
    // Read off the drawing: which way each drawn arm bends at the elbow (the cross
    // product of link 1 and link 2 with y turned up), as a sine of the bend angle.
    const bend = (arm) => {
      const u = { x: arm.link1.x2 - arm.link1.x1, y: -(arm.link1.y2 - arm.link1.y1) };
      const w = { x: arm.link2.x2 - arm.link2.x1, y: -(arm.link2.y2 - arm.link2.y1) };
      return (u.x * w.y - u.y * w.x) / (Math.hypot(u.x, u.y) * Math.hypot(w.x, w.y));
    };
    if (expected === 2) {
      assert.ok(poses[0].theta2 > 0 && poses[1].theta2 < 0, `① turns counterclockwise, ② clockwise at ${where}`);
      assert.ok(bend(at.arms[0]) > 0.01 && bend(at.arms[1]) < -0.01, `drawn ① bends counterclockwise, ② clockwise at ${where}`);
      // The two drawn elbows are different points, mirrored across the line OT in pixels.
      const [e1, e2] = at.arms.map((a) => ({ x: a.elbow.x - 210, y: a.elbow.y - 250 }));
      assert.ok(Math.hypot(e1.x - e2.x, e1.y - e2.y) > 1, `two distinct elbows drawn at ${where}`);
      const t = { x: at.target.x - 210, y: at.target.y - 250 }, tl = Math.hypot(t.x, t.y);
      const m = mirror(e1, { x: t.x / tl, y: t.y / tl });
      near(m.x, e2.x, `drawn elbows mirrored x at ${where}`, 0.2); near(m.y, e2.y, `drawn elbows mirrored y at ${where}`, 0.2);
    }
    if (expected === 1) {
      assert.ok(poses[0].theta2 === 0 || poses[0].theta2 === 180, `the edge posture is stretched or folded at ${where}`);
      assert.ok(Math.abs(bend(at.arms[0])) < 0.01, `the drawn edge posture is straight or folded at ${where}`);
    }
  }
});

// A reader can check a displayed equation by hand, so "=" must hold for the numbers
// as shown. Whether a number was rounded is judged from the true value here.
const shown = (text) => Number(text.replace(/−/g, '-').replace(/[()°]/g, ''));
const NEG_ZERO = /(^|[^\d.])−0(?![\d.])/;
test('the readouts say = only when every number shown is exact', () => {
  for (const target of TARGETS) {
    const where = `T ${target.x},${target.y}`;
    const text = cosText({ target });
    const m = text.match(/^\((\S+) − 5\) \/ 4 ([=≈]) (\S+)$/);
    assert.ok(m, `cos readout shape at ${where}: ${text}`);
    const d2 = target.x * target.x + target.y * target.y;
    const errors = [shown(m[1]) - d2, shown(m[3]) - (d2 - 5) / 4].map(Math.abs);
    assert.ok(errors.every((e) => e <= 0.005 + 1e-9), `a number shown off by more than rounding at ${where}`);
    if (m[2] === '=') { assert.ok(errors.every((e) => e < 1e-9), `rounded numbers joined by = at ${where}`); near((shown(m[1]) - 5) / 4, shown(m[3]), 'shown numbers divide out'); }
    else assert.ok(errors.some((e) => e > 1e-9), `exact numbers joined by ≈ at ${where}`);
    for (const pose of measure({ target }).poses) {
      const p = poseText(pose).match(/^\(θ1, θ2\) ([=≈]) \((\S+), (\S+)\)$/);
      assert.ok(p, `pose readout shape at ${where}`);
      const pe = [shown(p[2]) - pose.theta1, shown(p[3]) - pose.theta2].map(Math.abs);
      assert.ok(pe.every((e) => e <= 0.005 + 1e-9), `an angle shown off by more than rounding at ${where}`);
      assert.equal(p[1] === '=', pe.every((e) => e < 1e-9), `pose sign at ${where}`);
      assert.ok(!NEG_ZERO.test(p[0]), `negative zero at ${where}`);
    }
    assert.ok(!NEG_ZERO.test(text), `negative zero at ${where}`);
  }
});

test('the target snaps to the 0.5 grid and stays in [−3, 3]', () => {
  const state = initialState();
  assert.equal(setCoord(state, 'x', 2.2).target.x, 2);
  assert.equal(setCoord(state, 'y', 2.3).target.y, 2.5);
  assert.equal(setCoord(state, 'x', 9).target.x, 3);
  assert.equal(setCoord(state, 'y', -9).target.y, -3);
  assert.ok(Object.is(setCoord(state, 'y', -0.1).target.y, 0), 'no negative zero');
  assert.equal(setCoord(state, 'z', 1), state);
  assert.equal(setCoord(state, 'x', NaN), state);
  assert.deepEqual(setTarget(state, { x: -0.2, y: 3.4 }).target, { x: 0, y: 3 });
  // The range still reaches every case: inside, both edges, the hole, beyond the ring.
  const counts = new Set(TARGETS.map((target) => measure({ target }).poses.length));
  assert.deepEqual([...counts].sort(), [0, 1, 2]);
  assert.ok(TARGETS.some((t) => t.x * t.x + t.y * t.y > 9) && TARGETS.some((t) => t.x * t.x + t.y * t.y < 1));
  assert.equal(setTarget(state, { x: 1, y: NaN }), state);
});

test('dragging the target keeps the grab offset and snaps to the grid', () => {
  const state = initialState();
  const grab = { x: 5, y: -4 };
  const t = layout(state).target;
  assert.deepEqual(dragTo(state, { x: t.x + grab.x, y: t.y + grab.y }, grab), state, 'grabbing alone moves nothing');
  const to = PX({ x: -1.4, y: 2.6 });
  assert.deepEqual(dragTo(state, { x: to.x + grab.x, y: to.y + grab.y }, grab).target, { x: -1.5, y: 2.5 });
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
  at.arms.forEach((arm, i) => {
    const n = i + 1;
    assert.equal(attr(tag(`arm${n}`), 'visibility'), arm.visible ? 'visible' : 'hidden');
    for (const link of ['link1', 'link2']) {
      for (const name of ['x1', 'y1', 'x2', 'y2']) assert.equal(attr(tag(`arm${n}-${link}`), name), String(arm[link][name]), `arm ${n} ${link} ${name}`);
    }
    assert.equal(attr(tag(`arm${n}-elbow`), 'cx'), String(arm.elbow.x));
    assert.equal(attr(tag(`arm${n}-elbow`), 'cy'), String(arm.elbow.y));
  });
  assert.equal(attr(tag('handle-target'), 'transform'), `translate(${at.target.x} ${at.target.y})`);
  assert.equal(attr(tag('target-ring'), 'stroke'), at.reachable ? '#e2e8f0' : '#f87171');
  assert.match(SVG, /data-part="summary"[^>]*>자세 2개</);
});
