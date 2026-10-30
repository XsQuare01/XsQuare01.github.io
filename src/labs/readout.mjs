// The live readouts round to two decimals. An equation keeps "=" only when no
// number in it was rounded, so it still holds for a reader who checks it by hand;
// otherwise it reads "≈". The values themselves are never bent to fit.
export const isExact = (n) => Math.abs(n * 100 - Math.round(n * 100)) < 1e-6;
export const relation = (...values) => (values.every(isExact) ? '=' : '≈');
// A value standing alone in a readout cell (a pair of coordinates, a distance) is
// marked "≈" only when rounded; an exact one stands bare, since "= 1" on its own
// reads oddly. `text` is the value as shown, `values` the numbers in it.
export const approx = (text, ...values) => (relation(...values) === '=' ? text : `≈ ${text}`);
