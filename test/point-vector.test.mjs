import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { initialState, measure, move, formatNumber, toSvg, fromSvg, dragTo, labelPositions } from '../src/labs/point-vector-model.mjs';

const LAB_SVG = readFileSync(new URL('../public/images/robotics-points-vectors/displacement-lab.svg', import.meta.url), 'utf8');
const tagOf = (part) => {
  const tag = LAB_SVG.match(new RegExp(`<[^>]*data-part="${part}"[^>]*>`))?.[0];
  assert.ok(tag, `data-part="${part}" is missing`);
  return tag;
};
const attr = (tag, name) => Number(tag.match(new RegExp(`\\s${name}="([^"]+)"`))[1]);
const sub = (p, q) => ({ x: p.x - q.x, y: p.y - q.y });
const dot = (p, q) => p.x * q.x + p.y * q.y;

test('the article example and translated coordinates agree', () => {
  const state = initialState();
  assert.deepEqual(measure(state), { a: { x: 1, y: 1 }, b: { x: 4, y: 5 }, delta: { x: 3, y: 4 }, distance: 5 });
  const moved = move(move(state, 'o', 'x', 1), 'o', 'y', 2);
  assert.deepEqual(measure(moved), { a: { x: 0, y: -1 }, b: { x: 3, y: 3 }, delta: { x: 3, y: 4 }, distance: 5 });
  assert.deepEqual(moved.a, state.a);
  assert.deepEqual(moved.b, state.b);
  assert.deepEqual(state.o, { x: 0, y: 0 }, 'updates must not mutate the baseline');
});

test('origin translation preserves displacement and distance for many positions', () => {
  for (let ax = -1; ax <= 6; ax++) for (let bx = -1; bx <= 6; bx++) {
    const state = { a: { x: ax, y: bx }, b: { x: bx, y: ax }, o: { x: 0, y: 0 } };
    const before = measure(state);
    for (let ox = -1; ox <= 3; ox += 0.25) {
      const after = measure({ ...state, o: { x: ox, y: -ox } });
      assert.deepEqual(after.delta, before.delta);
      assert.equal(after.distance, before.distance);
      assert.equal(after.b.x - after.a.x, before.delta.x);
      assert.equal(after.b.y - after.a.y, before.delta.y);
    }
  }
});

test('reversing endpoints reverses direction, and coincident points have zero length', () => {
  const state = initialState();
  assert.deepEqual(measure({ ...state, a: state.b, b: state.a }).delta, { x: -3, y: -4 });
  assert.equal(measure({ ...state, a: state.b, b: state.a }).distance, 5);
  assert.deepEqual(measure({ ...state, b: state.a }).delta, { x: 0, y: 0 });
  assert.equal(measure({ ...state, b: state.a }).distance, 0);
});

test('input constraints prevent off-plot and nonfinite states', () => {
  const state = initialState();
  assert.equal(move(state, 'a', 'x', Infinity), state);
  assert.equal(move(state, 'a', 'x', NaN), state);
  assert.equal(move(state, 'unknown', 'x', 0), state);
  assert.equal(move(state, 'a', 'x', 100).a.x, 6);
  assert.equal(move(state, 'a', 'y', -100).a.y, -1);
  assert.equal(move(state, 'o', 'x', 100).o.x, 3);
  assert.equal(move(state, 'a', 'x', 1.37).a.x, 1.25);
  assert.equal(formatNumber(-0), '0');
});

test('negatives use the minus sign the article uses', () => {
  assert.equal(formatNumber(-1), '−1');
  assert.equal(formatNumber(-0.25), '−0.25');
  assert.equal(formatNumber(4.85), '4.85');
});

// The static SVG is what readers without JavaScript and printed copies get, so it
// must be exactly the lab's first frame.
test('the static picture is the first frame of the live lab', () => {
  const state = initialState();
  const labels = labelPositions(state);
  for (const key of ['a', 'b', 'o']) {
    const c = toSvg(state[key]);
    assert.ok(tagOf(key).includes(`transform="translate(${c.x} ${c.y})"`), `point ${key}`);
    const label = tagOf(`label-${key}`);
    assert.deepEqual({ x: attr(label, 'x'), y: attr(label, 'y') }, labels[key], `label-${key}`);
  }
  assert.match(LAB_SVG, /data-part="summary"[^>]*>변위 \(3, 4\) · 거리 5</);
});

test('labels sit behind A and beyond B, so neither lies on the arrow', () => {
  const cases = [
    [{ x: 1, y: 1 }, { x: 4, y: 5 }], [{ x: 4, y: 5 }, { x: 1, y: 1 }],
    [{ x: 2, y: 2 }, { x: 2.25, y: 2 }], [{ x: 0, y: 3 }, { x: 5, y: 3 }], [{ x: 3, y: 0 }, { x: 3, y: 4 }],
  ];
  for (const [a, b] of cases) {
    const labels = labelPositions({ a, b, o: { x: 0, y: 0 } });
    const A = toSvg(a), B = toSvg(b), arrow = sub(B, A);
    // Undo the 8px baseline shift to compare the label centre with the point.
    const centre = (p) => ({ x: p.x, y: p.y - 8 });
    assert.ok(dot(sub(centre(labels.a), A), arrow) < 0, `A label for ${JSON.stringify([a, b])}`);
    assert.ok(dot(sub(centre(labels.b), B), arrow) > 0, `B label for ${JSON.stringify([a, b])}`);
  }
  const zero = labelPositions({ a: { x: 2, y: 2 }, b: { x: 2, y: 2 }, o: { x: 0, y: 0 } });
  assert.notDeepEqual(zero.a, zero.b, 'coincident points still get separate labels');
  for (const corner of [{ x: -1, y: -1 }, { x: 6, y: 6 }]) {
    const { a, b } = labelPositions({ a: corner, b: { x: 2, y: 2 }, o: { x: 0, y: 0 } });
    for (const p of [a, b]) assert.ok(p.x >= 16 && p.x <= 384 && p.y >= 70 && p.y <= 410, 'labels stay inside the figure');
  }
});

test('dragging keeps the grab offset and snaps to the input step', () => {
  const state = initialState();
  const grab = { x: 5, y: -3 }; // the pointer landed 5px right of and 3px above A's centre
  const start = toSvg(state.a);
  const at = (dx, dy) => ({ x: start.x + grab.x + dx, y: start.y + grab.y + dy });
  assert.deepEqual(dragTo(state, 'a', at(0, 0), grab).a, state.a, 'grabbing alone does not move the point');
  assert.deepEqual(dragTo(state, 'a', at(40, -80), grab).a, { x: 2, y: 3 });
  assert.deepEqual(dragTo(state, 'a', at(11, 0), grab).a, { x: 1.25, y: 1 }, '11px is 0.275, which snaps to 0.25');
  assert.deepEqual(dragTo(state, 'a', { x: 1e4, y: -1e4 }, grab).a, { x: 6, y: 6 });
  assert.deepEqual(dragTo(state, 'o', toSvg({ x: 1, y: 2 }), { x: 0, y: 0 }).o, { x: 1, y: 2 });
  assert.deepEqual(fromSvg(toSvg({ x: -1, y: 2.5 })), { x: -1, y: 2.5 });
});

test('the reset baseline is a fresh copy each time', () => {
  const first = initialState();
  first.a.x = 3;
  assert.deepEqual(initialState().a, { x: 1, y: 1 });
});
