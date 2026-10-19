import test from 'node:test';
import assert from 'node:assert/strict';
import { initLabs } from '../src/labs/index.js';

// The loader only touches classList, dataset and `.lab-live`'s `hidden`, so a stub
// with those three is enough. It does not model layout, events or rendering.
function stubFigure(lab = 'point-vector') {
  const classes = new Set(['svg-lab']);
  const live = { hidden: true };
  return {
    dataset: { lab },
    classList: { add: (c) => classes.add(c), remove: (c) => classes.delete(c), contains: (c) => classes.has(c) },
    querySelector: (selector) => (selector === '.lab-live' ? live : null),
    live, classes,
  };
}
const page = (...figures) => ({ querySelectorAll: () => figures });
const showLive = (figure) => { figure.live.hidden = false; figure.classList.add('is-live'); };
const isStatic = (figure) => figure.live.hidden && !figure.classes.has('is-live');

test('a mounted lab goes live once and is not mounted twice', async () => {
  const figure = stubFigure();
  const mounted = [];
  const registry = { 'point-vector': async () => ({ mount: (f) => { mounted.push(f); showLive(f); } }) };
  await initLabs(page(figure), registry);
  await initLabs(page(figure), registry);
  assert.equal(mounted.length, 1);
  assert.ok(!figure.live.hidden && figure.classes.has('is-live'));
});

test('an unregistered lab keeps the static picture', async () => {
  const figure = stubFigure('unknown');
  await initLabs(page(figure), {});
  assert.ok(isStatic(figure));
});

test('a failed import keeps the static picture', async (t) => {
  const warn = t.mock.method(console, 'warn', () => {});
  const figure = stubFigure();
  await initLabs(page(figure), { 'point-vector': async () => { throw new Error('network'); } });
  assert.ok(isStatic(figure));
  assert.equal(warn.mock.callCount(), 1);
});

test('a mount that fails after showing the live copy is rolled back', async (t) => {
  t.mock.method(console, 'warn', () => {});
  const figure = stubFigure();
  const registry = { 'point-vector': async () => ({ mount: (f) => { showLive(f); throw new Error('missing part'); } }) };
  await initLabs(page(figure), registry);
  assert.ok(isStatic(figure));
});

test('one failing lab does not stop the next one', async (t) => {
  t.mock.method(console, 'warn', () => {});
  const broken = stubFigure('broken'), working = stubFigure();
  const registry = {
    broken: async () => ({ mount: () => { throw new Error('boom'); } }),
    'point-vector': async () => ({ mount: showLive }),
  };
  await initLabs(page(broken, working), registry);
  assert.ok(isStatic(broken));
  assert.ok(working.classes.has('is-live'));
});
