// Must list the same labs as LABS in src/plugins/rehype-svg-labs.mjs; a lab missing
// here stays a static picture without any error. test/lab-loader.test.mjs compares them.
export const LAB_MODULES = {
  'point-vector': () => import('./point-vector.js'),
  'rod-angle': () => import('./rod-angle.js'),
  'vector-sum': () => import('./vector-sum.js'),
  'vector-projection': () => import('./vector-projection.js'),
  'rotation-matrix': () => import('./rotation-matrix.js'),
};
const modules = LAB_MODULES;

// `registry` is injectable so tests can exercise the fallback paths without a DOM.
export async function initLabs(root = document, registry = modules) {
  for (const figure of root.querySelectorAll('.svg-lab[data-lab]')) {
    if (figure.classList.contains('is-live')) continue;
    const load = registry[figure.dataset.lab];
    if (!load) continue;
    try {
      const { mount } = await load();
      mount(figure);
    } catch (error) {
      // A failed import or initialization must not hide the readable static image.
      figure.classList.remove('is-live');
      const live = figure.querySelector('.lab-live');
      if (live) live.hidden = true;
      console.warn('실험을 불러오지 못해 기본 그림을 표시합니다.', error);
    }
  }
}
