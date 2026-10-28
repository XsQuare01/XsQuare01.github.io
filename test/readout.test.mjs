import test from 'node:test';
import assert from 'node:assert/strict';
import { isExact, relation, approx } from '../src/labs/readout.mjs';

test('a number is exact when two decimals show it whole', () => {
  assert.ok(isExact(0.5) && isExact(-1.25) && isExact(Math.sin(Math.PI / 6)), 'sin 30° is 0.5 up to float noise');
  assert.ok(!isExact(Math.SQRT1_2) && !isExact(1 / 3) && !isExact(0.125));
  assert.equal(relation(3, 0.5, -2), '=');
  assert.equal(relation(3, Math.SQRT2), '≈');
});

test('a value alone in a readout cell carries ≈ only when rounded', () => {
  assert.equal(approx('(2, 0)', 2, 0), '(2, 0)');
  assert.equal(approx('(1.73, 1)', Math.sqrt(3), 1), '≈ (1.73, 1)');
  assert.equal(approx('3', 3), '3');
  assert.equal(approx('2.24', Math.sqrt(5)), '≈ 2.24');
});
