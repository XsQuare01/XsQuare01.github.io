import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import {
  initialState, measure, move, dragTo, layout, lengthSumText, toSvg, formatNumber, LIMITS, HEAD_MIN,
} from '../src/labs/vector-sum-model.mjs';
import { pickHandle } from '../src/labs/pick-handle.mjs';

const near = (actual, expected, message) => assert.ok(Math.abs(actual - expected) < 1e-9, `${message}: ${actual} ≠ ${expected}`);
const SVG = readFileSync(new URL('../public/images/robotics-vector-projection/sum-lab.svg', import.meta.url), 'utf8');
const VALUES = [];
for (let v = LIMITS.min; v <= LIMITS.max; v += LIMITS.step) VALUES.push(v);
const VECTORS = VALUES.flatMap((x) => VALUES.map((y) => ({ x, y })));

// The pixel geometry is read off the static picture (axes at x = 200 and y = 245,
// grid lines 30px apart) rather than taken from the model's toSvg.
const PX = ({ x, y }) => ({ x: 200 + 30 * x, y: 245 - 30 * y });
test('the test geometry matches the axes and grid the picture draws', () => {
  assert.match(SVG, /<line x1="14" y1="245" x2="382" y2="245"/);
  assert.match(SVG, /<line x1="200" y1="431" x2="200" y2="61"/);
  assert.match(SVG, /M230 65V425 M20 215H380/, 'grid lines one unit from the axes');
});

test('the article example: (3, 1) + (1, 2) = (4, 3), and the lengths do not add', () => {
  const { sum, lengths } = measure(initialState());
  assert.deepEqual(sum, { x: 4, y: 3 });
  near(lengths.sum, 5, '|a + b|');
  near(lengths.a + lengths.b, Math.sqrt(10) + Math.sqrt(5), '|a| + |b|');
  assert.equal(formatNumber(lengths.a + lengths.b), '5.4');
  assert.deepEqual(measure({ a: { x: Math.sqrt(3), y: 1 }, b: { x: 0, y: 1 } }).sum, { x: Math.sqrt(3), y: 2 }, 'the two rods');
});

test('over every state, the arrows and the dashed other order close a parallelogram', () => {
  assert.equal(VECTORS.length, 13 * 13);
  for (const a of VECTORS) {
    for (const b of VECTORS) {
      const at = layout({ a, b });
      const where = `a ${a.x},${a.y} b ${b.x},${b.y}`;
      const seg = (s) => ({ from: { x: s.x1, y: s.y1 }, to: { x: s.x2, y: s.y2 } });
      const o = PX({ x: 0, y: 0 }), tipA = PX(a), tipB = PX(b), end = PX({ x: a.x + b.x, y: a.y + b.y });
      assert.deepEqual(seg(at.a), { from: o, to: tipA }, `a at ${where}`);
      assert.deepEqual(seg(at.b), { from: tipA, to: end }, `b hangs off a at ${where}`);
      assert.deepEqual(seg(at.sum), { from: o, to: end }, `sum at ${where}`);
      assert.deepEqual(seg(at.bFirst), { from: o, to: tipB }, `b first at ${where}`);
      assert.deepEqual(seg(at.aSecond), { from: tipB, to: end }, `then a ends where a then b ends at ${where}`);
      const vec = (s) => ({ x: s.x2 - s.x1, y: s.y2 - s.y1 });
      assert.deepEqual(vec(at.aSecond), vec(at.a), `opposite sides are the same vector at ${where}`);
      assert.deepEqual(vec(at.bFirst), vec(at.b), `opposite sides are the same vector at ${where}`);
    }
  }
});

// A reader can check a displayed equation by hand, so "=" must hold for the numbers
// as shown. Whether a number was rounded is judged from the true value here, not
// from the model's own test for exactness.
const shown = (text) => Number(text.replace('−', '-').replace(/[()]/g, ''));
test('the length readout says = only when the numbers shown add up exactly', () => {
  assert.equal(lengthSumText({ a: { x: 0.5, y: 0.5 }, b: { x: 0.5, y: 0.5 } }), '0.71 + 0.71 ≈ 1.41');
  assert.equal(lengthSumText(initialState()), '3.16 + 2.24 ≈ 5.4');
  assert.equal(lengthSumText({ a: { x: 3, y: 0 }, b: { x: 0, y: 2 } }), '3 + 2 = 5');
  for (const a of VECTORS) {
    for (const b of VECTORS) {
      const m = lengthSumText({ a, b }).match(/^(\S+) \+ (\S+) ([=≈]) (\S+)$/);
      assert.ok(m, 'readout shape');
      const [x, y, z] = [m[1], m[2], m[4]].map(shown);
      const truth = [Math.hypot(a.x, a.y), Math.hypot(b.x, b.y)];
      const rounded = [x - truth[0], y - truth[1], z - truth[0] - truth[1]].some((e) => Math.abs(e) > 1e-9);
      if (m[3] === '=') { assert.ok(!rounded, `rounded numbers joined by = at a ${a.x},${a.y} b ${b.x},${b.y}`); near(x + y, z, 'shown numbers add up'); }
      else assert.ok(rounded, `exact numbers joined by ≈ at a ${a.x},${a.y} b ${b.x},${b.y}`);
    }
  }
});

test('inputs snap to the 0.5 grid and stay in [−3, 3]', () => {
  const state = initialState();
  assert.equal(move(state, 'a', 'x', 2.2).a.x, 2);
  assert.equal(move(state, 'b', 'y', 2.3).b.y, 2.5);
  assert.equal(move(state, 'a', 'x', 9).a.x, 3);
  assert.equal(move(state, 'b', 'x', -9).b.x, -3);
  assert.ok(Object.is(move(state, 'a', 'y', -0.1).a.y, 0), 'no negative zero');
  assert.equal(move(state, 'c', 'x', 1), state);
  assert.equal(move(state, 'a', 'z', 1), state);
  assert.equal(move(state, 'a', 'x', NaN), state);
});

test('dragging a carries b along; dragging the chain end changes b alone', () => {
  const state = initialState();
  const grab = { x: 5, y: -3 };
  const at = layout(state).handles;
  assert.deepEqual(dragTo(state, 'a', { x: at.a.x + grab.x, y: at.a.y + grab.y }, grab), state, 'grabbing alone moves nothing');
  const moved = dragTo(state, 'a', { x: toSvg({ x: 1, y: 1 }).x + grab.x, y: toSvg({ x: 1, y: 1 }).y + grab.y }, grab);
  assert.deepEqual(moved, { a: { x: 1, y: 1 }, b: { x: 1, y: 2 } });
  assert.deepEqual(layout(moved).handles.b, PX({ x: 2, y: 3 }), 'the b handle rides on the new chain end');
  const back = dragTo(state, 'b', toSvg({ x: 0, y: 0 }), { x: 0, y: 0 });
  assert.deepEqual(back, { a: { x: 3, y: 1 }, b: { x: -3, y: -1 } }, 'pulling the end to O makes b = −a');
  assert.equal(layout(back).sum.head, false, 'a zero sum has no head');
});

test('a press goes to the nearest handle, and a tie keeps the selected one', () => {
  const handles = { a: { x: 100, y: 100 }, b: { x: 110, y: 100 } };
  assert.equal(pickHandle(handles, { x: 108, y: 100 }, 'a'), 'b', 'nearest wins over drawing order');
  assert.equal(pickHandle(handles, { x: 101, y: 100 }, 'b'), 'a');
  assert.equal(pickHandle({ a: { x: 5, y: 5 }, b: { x: 5, y: 5 } }, { x: 6, y: 6 }, 'a'), 'a', 'stacked handles keep the selection');
  assert.equal(pickHandle({ a: { x: 5, y: 5 }, b: { x: 5, y: 5 } }, { x: 6, y: 6 }, 'b'), 'b');
  assert.equal(pickHandle(handles, { x: 200, y: 200 }, 'a'), null, 'outside every hit circle');
});

// How far an arrowhead reaches back from the line's end: refX in a 10-unit viewBox
// scaled to markerWidth pixels.
const MARKERS = Object.fromEntries([...SVG.matchAll(/<marker id="([^"]+)"[^>]*refX="([\d.]+)"[^>]*markerWidth="(\d+)"/g)]
  .map((m) => [m[1], { back: (Number(m[2]) * Number(m[3])) / 10, tipBack: ((Number(m[2]) - 9) * Number(m[3])) / 10 }]));

test('every arrowhead fits on the shortest arrow that gets one, and stops short of its handle', () => {
  assert.deepEqual(Object.keys(MARKERS).sort(), ['rvp-l-a', 'rvp-l-b', 'rvp-l-s']);
  for (const [id, m] of Object.entries(MARKERS)) {
    assert.ok(m.back <= HEAD_MIN, `${id} reaches ${m.back}px back, beyond HEAD_MIN ${HEAD_MIN}`);
  }
  assert.ok(MARKERS['rvp-l-a'].tipBack >= 8, 'a’s head clears the 8px blue dot');
  assert.ok(MARKERS['rvp-l-b'].tipBack >= 10 && MARKERS['rvp-l-s'].tipBack >= 10, 'b and the sum clear the 10px diamond');
});

const INSIDE = { x1: 20, x2: 380, y1: 65, y2: 425 };

test('over every state, the drawing stays in the plot and arrowheads follow the arrow length', () => {
  let checked = 0;
  for (const a of VECTORS) {
    for (const b of VECTORS) {
      const at = layout({ a, b });
      for (const key of ['a', 'b', 'sum', 'bFirst', 'aSecond']) {
        const s = at[key];
        for (const [x, y] of [[s.x1, s.y1], [s.x2, s.y2]]) {
          assert.ok(x >= INSIDE.x1 && x <= INSIDE.x2 && y >= INSIDE.y1 && y <= INSIDE.y2, `${key} leaves the plot`);
        }
      }
      // Zero arrows have no direction; arrows a unit or longer always show one.
      const units = { a: Math.hypot(a.x, a.y), b: Math.hypot(b.x, b.y), sum: Math.hypot(a.x + b.x, a.y + b.y) };
      for (const key of ['a', 'b', 'sum']) {
        if (units[key] === 0) assert.equal(at[key].head, false, `${key} zero arrow has a head`);
        if (units[key] >= 1) assert.equal(at[key].head, true, `${key} long arrow lost its head`);
      }
      checked++;
    }
  }
  assert.equal(checked, 13 ** 4);
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
  for (const [part, key] of [['a', 'a'], ['b', 'b'], ['sum', 'sum'], ['b-first', 'bFirst'], ['a-second', 'aSecond']]) {
    const t = tag(part);
    for (const name of ['x1', 'y1', 'x2', 'y2']) assert.equal(attr(t, name), String(at[key][name]), `${part} ${name}`);
  }
  for (const part of ['a', 'b', 'sum']) {
    // The runtime takes the arrowhead from data-marker, so each arrow carries it.
    assert.match(attr(tag(part), 'data-marker') ?? '', /^url\(#rvp-l-[abs]\)$/, `${part} data-marker`);
    assert.equal(attr(tag(part), 'marker-end'), at[part].head ? attr(tag(part), 'data-marker') : undefined, `${part} head`);
  }
  for (const key of ['a', 'b']) {
    assert.equal(attr(tag(`handle-${key}`), 'transform'), `translate(${at.handles[key].x} ${at.handles[key].y})`);
  }
  assert.match(SVG, /data-part="summary"[^>]*>a \+ b = \(4, 3\), 길이 5</);
});
