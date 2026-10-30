import { readFileSync, realpathSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { prefixIds } from './rehype-svg-steps.mjs';

const PUBLIC = fileURLToPath(new URL('../../public/', import.meta.url));
// The runtime registry (LAB_MODULES in src/labs/index.js) must list the same labs.
export const LABS = new Set(['point-vector', 'rod-angle', 'vector-sum', 'vector-projection', 'rotation-matrix', 'arm-forward', 'arm-inverse']);
const escapeAttr = (s) => s.replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/</g, '&lt;');

// Trusted, repository-authored SVGs only. This is an authoring convention, not an
// arbitrary SVG sanitizer. Unknown/unsupported files retain the original image.
export function rehypeSvgLabs({ publicDir = PUBLIC } = {}) {
  return (tree) => {
    let instance = 0;
    const walk = (node) => {
      if (!node.children) return;
      if (node.tagName === 'figure') {
        node.children = node.children.flatMap((img) => {
          const src = img.properties?.src;
          if (img.tagName !== 'img' || typeof src !== 'string' ||
              !/^\/images\/[a-zA-Z0-9/_-]+-lab\.svg$/.test(src)) return [img];
          let source;
          try {
            const root = realpathSync(publicDir);
            const file = realpathSync(path.join(root, src.slice(1)));
            const relative = path.relative(root, file);
            if (relative.startsWith('..') || path.isAbsolute(relative)) return [img];
            source = readFileSync(file, 'utf8').replace(/<!--[\s\S]*?-->/g, '').trim();
          } catch { return [img]; }
          const opening = source.match(/^<svg\b[^>]*>/);
          const lab = opening?.[0].match(/\bdata-lab="([a-z-]+)"/)?.[1];
          if (!LABS.has(lab) || !source.endsWith('</svg>') ||
              /<(?:script|style|foreignObject)\b|\son\w+\s*=|\sstyle\s*=/i.test(source)) return [img];
          const prefix = `lab-${src.replace(/[^a-zA-Z0-9]+/g, '-')}-${++instance}-`;
          const labeled = opening[0].replace(/\s(?:role|aria-label)="[^"]*"/g, '')
            .replace(/>$/, ` role="img" aria-label="${escapeAttr(String(img.properties.alt || ''))}">`);
          const svg = prefixIds(labeled + source.slice(opening[0].length), prefix);
          if (!svg) return [img];
          node.properties ||= {};
          const classes = node.properties.className || [];
          node.properties.className = [...(Array.isArray(classes) ? classes : classes.split(' ')), 'svg-lab'];
          node.properties['data-lab'] = lab;
          node.properties['data-lab-id'] = prefix;
          img.properties.className = ['lab-static'];
          // Load the small print fallback even if initialization hides it before
          // a lazy image reaches the viewport.
          img.properties.loading = 'eager';
          // The original img is also the print fallback, even after an experiment.
          return [img, {
            type: 'element', tagName: 'div', properties: { className: ['lab-live'], hidden: true },
            children: [{ type: 'raw', value: svg }],
          }];
        });
      }
      node.children.forEach(walk);
    };
    walk(tree);
  };
}
