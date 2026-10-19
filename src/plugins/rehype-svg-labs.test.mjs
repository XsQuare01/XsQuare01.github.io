import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, mkdirSync, writeFileSync, rmSync } from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { rehypeSvgLabs } from './rehype-svg-labs.mjs';

const sample = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" data-lab="point-vector"><defs><marker id="arrow"/></defs><path marker-end="url(#arrow)"/><text>그림</text></svg>';
const figure = (src = '/images/test-lab.svg') => ({ type: 'element', tagName: 'figure', properties: { className: ['post-figure'] }, children: [
  { type: 'element', tagName: 'img', properties: { src, alt: 'A와 "B" <비교>' } },
  { type: 'element', tagName: 'figcaption', children: [{ type: 'text', value: '설명' }] },
] });
function fixture(t, source = sample) {
  const dir = mkdtempSync(path.join(os.tmpdir(), 'svg-lab-test-'));
  mkdirSync(path.join(dir, 'images'));
  writeFileSync(path.join(dir, 'images/test-lab.svg'), source);
  t.after(() => rmSync(dir, { recursive: true, force: true }));
  return dir;
}

test('keeps the caption and static image, and initially hides the live copy', (t) => {
  const fig = figure();
  rehypeSvgLabs({ publicDir: fixture(t) })({ children: [fig] });
  assert.deepEqual(fig.properties.className, ['post-figure', 'svg-lab']);
  assert.equal(fig.children[0].tagName, 'img');
  assert.equal(fig.children[1].properties.hidden, true);
  assert.equal(fig.children[2].tagName, 'figcaption');
  assert.match(fig.children[1].children[0].value, /aria-label="A와 &quot;B&quot; &lt;비교>"/);
});

test('repeated instances get distinct IDs and matching marker references', (t) => {
  const first = figure(), second = figure();
  rehypeSvgLabs({ publicDir: fixture(t) })({ children: [first, second] });
  assert.notEqual(first.properties['data-lab-id'], second.properties['data-lab-id']);
  for (const fig of [first, second]) {
    const raw = fig.children[1].children[0].value;
    const marker = raw.match(/id="([^"]+)"/)[1];
    assert.ok(raw.includes(`url(#${marker})`));
  }
});

test('missing, remote, traversal, and ordinary image paths stay static', (t) => {
  const plugin = rehypeSvgLabs({ publicDir: fixture(t) });
  for (const src of ['/images/absent-lab.svg', 'https://example.com/test-lab.svg', '/images/../test-lab.svg', '/images/%2e%2e/test-lab.svg', '/images/test-steps.svg']) {
    const fig = figure(src); const before = structuredClone(fig);
    plugin({ children: [fig] });
    assert.deepEqual(fig, before);
  }
});

test('unknown labs, active content, and unsupported ID syntax retain fallback', (t) => {
  for (const source of [sample.replace('point-vector', 'unknown'), sample.replace('</svg>', '<script>alert(1)</script></svg>'), sample.replace('id="arrow"', "id='arrow'"), '<svg data-lab="point-vector">']) {
    const fig = figure(), before = structuredClone(fig);
    rehypeSvgLabs({ publicDir: fixture(t, source) })({ children: [fig] });
    assert.deepEqual(fig, before);
  }
});
