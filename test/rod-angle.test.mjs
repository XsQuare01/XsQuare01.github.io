import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import {
  initialState, measure, setAngle, setLength, fromTip, dragTip, layout, toSvg, fromSvg, formatNumber, LIMITS, FIXED_TEXT,
} from '../src/labs/rod-angle-model.mjs';

const near = (actual, expected, message) => assert.ok(Math.abs(actual - expected) < 1e-9, `${message}: ${actual} ≠ ${expected}`);
const SVG = readFileSync(new URL('../public/images/robotics-sine-cosine/rod-lab.svg', import.meta.url), 'utf8');

test('the article examples land where the text says', () => {
  const at = (theta, length) => measure({ theta, length });
  near(at(30, 1).x, Math.sqrt(3) / 2, 'cos 30°'); near(at(30, 1).y, 0.5, 'sin 30°');
  near(at(30, 2).x, Math.sqrt(3), '2 cos 30°'); near(at(30, 2).y, 1, '2 sin 30°');
  near(at(120, 2).x, -1, '2 cos 120°'); near(at(120, 2).y, Math.sqrt(3), '2 sin 120°');
  near(at(-30, 2).x, Math.sqrt(3), '2 cos −30°'); near(at(-30, 2).y, -1, '2 sin −30°');
  near(at(30, 2).rad, Math.PI / 6, '30° in radians');
});

test('every angle puts the length-1 tip on the unit circle, and length L scales it', () => {
  for (let theta = LIMITS.thetaMin; theta <= LIMITS.thetaMax; theta++) {
    const { cos, sin } = measure({ theta, length: 1 });
    near(cos * cos + sin * sin, 1, `cos² + sin² at ${theta}°`);
    const { x, y } = measure({ theta, length: 2.5 });
    near(Math.hypot(x, y), 2.5, `length at ${theta}°`);
  }
});

test('signs follow the quadrant', () => {
  const sign = (theta) => { const { x, y } = measure({ theta, length: 2 }); return [Math.sign(x), Math.sign(y)]; };
  assert.deepEqual(sign(45), [1, 1]);
  assert.deepEqual(sign(135), [-1, 1]);
  assert.deepEqual(sign(-135), [-1, -1]);
  assert.deepEqual(sign(-45), [1, -1]);
});

test('the tip gives back length and angle, with the quadrant y/x alone would lose', () => {
  const state = initialState();
  assert.deepEqual(fromTip(state, { x: 1.5, y: 2 }), { theta: 53, length: 2.5 });
  assert.deepEqual(fromTip(state, { x: -1.5, y: -2 }), { theta: -127, length: 2.5 }, 'same y/x, opposite direction');
  assert.deepEqual(fromTip(state, { x: 0, y: 0 }), { theta: state.theta, length: LIMITS.lengthMin }, 'the origin has no angle');
  assert.deepEqual(fromTip(state, { x: 30, y: 0 }), { theta: 0, length: LIMITS.lengthMax });
  assert.equal(fromTip(state, { x: -2, y: -0.01 }).theta, 180, 'just below the negative x-axis rounds to 180°, never −180°');
  assert.equal(fromTip(state, { x: NaN, y: 1 }), state);
});

test('angles stay in (−180°, 180°] and lengths snap into range', () => {
  const state = initialState();
  assert.equal(setAngle(state, 30.4).theta, 30);
  assert.equal(setAngle(state, -180).theta, 180, '−180° and 180° are one direction');
  assert.equal(setAngle(state, 500).theta, 140, 'wrapped, not clamped');
  assert.equal(setAngle(state, -500).theta, -140);
  assert.equal(setAngle(state, -0.2).theta, 0);
  assert.ok(Object.is(setAngle(state, -0.2).theta, 0), 'no negative zero');
  assert.equal(setLength(state, 1.1).length, 1);
  assert.equal(setLength(state, 0).length, 0.5);
  assert.equal(setLength(state, 9).length, 3);
  assert.equal(setAngle(state, Infinity), state);
  assert.equal(formatNumber(-1.732), '−1.73');
  assert.equal(formatNumber(2 * Math.sin(Math.PI / 6)), '1', 'floating noise rounds away');
  assert.equal(formatNumber(Math.cos(Math.PI / 2)), '0');
});

test('dragging keeps the grab offset', () => {
  const state = initialState();
  const grab = { x: 4, y: -6 };
  const start = layout(state).tip;
  assert.deepEqual(dragTip(state, { x: start.x + grab.x, y: start.y + grab.y }, grab), state, 'grabbing alone does not move the tip');
  const target = toSvg({ x: 0, y: 1.5 });
  assert.deepEqual(dragTip(state, { x: target.x + grab.x, y: target.y + grab.y }, grab), { theta: 90, length: 1.5 });
  assert.deepEqual(fromSvg(toSvg({ x: -2, y: 0.5 })), { x: -2, y: 0.5 });
});

// The obstacle model inside layout() is what is being tested, so the boxes and the
// segment test here are written independently of it. Text boxes are approximate
// (cap height, Arial-like widths); the model pads them by 2px on top of this.
const P_BOX = (l) => ({ x1: l.x - 8, x2: l.x + 8, y1: l.y - 18, y2: l.y });
const THETA_BOX = (l) => ({ x1: l.x - 6, x2: l.x + 6, y1: l.y - 15, y2: l.y });
const hit = (a, b) => a.x1 < b.x2 && b.x1 < a.x2 && a.y1 < b.y2 && b.y1 < a.y2;
const touchesCircle = (b, c, r) => {
  const dx = Math.max(b.x1 - c.x, 0, c.x - b.x2), dy = Math.max(b.y1 - c.y, 0, c.y - b.y2);
  return dx * dx + dy * dy < r * r;
};
function cutsSegment(b, a, c) {
  for (let t = 0; t <= 1; t += 1 / 400) {
    const x = a.x + (c.x - a.x) * t, y = a.y + (c.y - a.y) * t;
    if (x > b.x1 && x < b.x2 && y > b.y1 && y < b.y2) return true;
  }
  return false;
}

test('over every state, visible labels touch no tick, axis letter, dot, segment or each other', () => {
  const o = toSvg({ x: 0, y: 0 });
  let checked = 0;
  for (let theta = LIMITS.thetaMin; theta <= LIMITS.thetaMax; theta++) {
    for (let length = LIMITS.lengthMin; length <= LIMITS.lengthMax; length += LIMITS.lengthStep) {
      const { tip, unit, labels } = layout({ theta, length });
      const where = `${theta}°, L=${length}`;
      const foot = { x: tip.x, y: o.y };
      const boxes = [['P', P_BOX(labels.p)]];
      if (labels.theta.visible) boxes.push(['θ', THETA_BOX(labels.theta)]);
      for (const [name, b] of boxes) {
        assert.ok(b.x1 >= 0 && b.x2 <= 400 && b.y1 >= 40 && b.y2 <= 444, `${name} leaves the plot at ${where}`);
        for (const t of FIXED_TEXT) assert.ok(!hit(b, t), `${name} covers fixed text at ${where}`);
        assert.ok(!touchesCircle(b, tip, 9), `${name} covers the tip at ${where}`);
        assert.ok(!touchesCircle(b, unit, 4), `${name} covers the unit dot at ${where}`);
        for (const [a, c] of [[o, tip], [o, foot], [foot, tip]]) assert.ok(!cutsSegment(b, a, c), `${name} lies on a segment at ${where}`);
      }
      if (boxes.length === 2) assert.ok(!hit(boxes[0][1], boxes[1][1]), `P and θ overlap at ${where}`);
      if (Math.abs(theta) < 20) assert.equal(labels.theta.visible, false, `θ shown on a tiny arc at ${where}`);
      checked++;
    }
  }
  assert.equal(checked, 360 * 11);
});

test('the fixed text the layout avoids is the text the static picture draws', () => {
  const drawn = new Set([...SVG.matchAll(/<text x="([\d.]+)" y="([\d.]+)"/g)].map((m) => `${m[1]},${m[2]}`));
  for (const t of FIXED_TEXT) {
    const anchors = [t.x1, (t.x1 + t.x2) / 2, t.x2].map((x) => `${x},${t.y2}`);
    assert.ok(anchors.some((a) => drawn.has(a)), `no drawn text at the obstacle ${JSON.stringify(t)}`);
  }
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
  assert.equal(attr(tag('rod'), 'x2'), String(at.tip.x));
  assert.equal(attr(tag('rod'), 'y2'), String(at.tip.y));
  assert.equal(attr(tag('x-part'), 'x2'), String(at.tip.x));
  assert.equal(attr(tag('y-part'), 'x1'), String(at.tip.x));
  assert.equal(attr(tag('y-part'), 'x2'), String(at.tip.x));
  assert.equal(attr(tag('y-part'), 'y2'), String(at.tip.y));
  assert.equal(attr(tag('p'), 'transform'), `translate(${at.tip.x} ${at.tip.y})`);
  assert.equal(attr(tag('unit-dot'), 'cx'), String(at.unit.x));
  assert.equal(attr(tag('unit-dot'), 'cy'), String(at.unit.y));
  assert.equal(attr(tag('arc'), 'd'), at.arc);
  for (const key of ['p', 'theta']) {
    const t = tag(`label-${key}`);
    assert.deepEqual({ x: Number(attr(t, 'x')), y: Number(attr(t, 'y')) }, { x: at.labels[key].x, y: at.labels[key].y }, `label-${key}`);
  }
  assert.equal(attr(tag('label-theta'), 'visibility'), at.labels.theta.visible ? 'visible' : 'hidden');
  assert.match(SVG, /data-part="summary"[^>]*>θ = 30° · 끝점 \(1\.73, 1\)</);
});
