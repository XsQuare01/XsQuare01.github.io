import test from 'node:test';
import assert from 'node:assert/strict';
import { initialState, measure, move, formatNumber } from '../src/labs/point-vector-model.mjs';

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
