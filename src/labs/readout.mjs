// The live readouts round to two decimals. An equation keeps "=" only when no
// number in it was rounded, so it still holds for a reader who checks it by hand;
// otherwise it reads "≈". The values themselves are never bent to fit.
export const isExact = (n) => Math.abs(n * 100 - Math.round(n * 100)) < 1e-6;
export const relation = (...values) => (values.every(isExact) ? '=' : '≈');
