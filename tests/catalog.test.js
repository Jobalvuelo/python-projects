import assert from 'node:assert/strict';
import { experiences } from '../public/src/experiences.js';

assert.deepEqual(Object.keys(experiences), ['garden', 'surf', 'reset']);
for (const [key, experience] of Object.entries(experiences)) {
  assert.ok(experience.name, `${key} needs a name`);
  assert.deepEqual(Object.keys(experience.durations), ['3', '5', '7']);
  for (const duration of Object.values(experience.durations)) assert.ok(duration.includes.length >= 8, `${key} duration is incomplete`);
}
console.log('All 3 vibes and 9 package combinations are complete.');
