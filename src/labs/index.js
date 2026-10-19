const modules = { 'point-vector': () => import('./point-vector.js') };

export async function initLabs(root = document) {
  for (const figure of root.querySelectorAll('.svg-lab[data-lab]')) {
    if (figure.classList.contains('is-live')) continue;
    const load = modules[figure.dataset.lab];
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
