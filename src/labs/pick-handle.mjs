// Handles can overlap (a zero arrow puts two on one spot), and the handle drawn last
// would always win the pointer. Pick the handle nearest the pointer instead; on a
// tie keep the one already selected, so a choice made in the select box survives.
// `reach` is the radius of the invisible hit circle drawn around each handle.
export function pickHandle(handles, pointer, selected, reach = 27) {
  let best = null;
  let bestDistance = Infinity;
  for (const [key, at] of Object.entries(handles)) {
    const distance = Math.hypot(pointer.x - at.x, pointer.y - at.y);
    if (distance > reach) continue;
    const tie = Math.abs(distance - bestDistance) < 1e-9;
    if (distance < bestDistance && !tie) { best = key; bestDistance = distance; }
    else if (tie && key === selected) best = key;
  }
  return best;
}
