import assert from "node:assert/strict";
import { test } from "node:test";

import { isFixtureRequestUrl } from "../../playwright.config.js";

test("allows the exact loopback fixture origin", () => {
  const origin = "http://127.0.0.1:4173";

  assert.equal(isFixtureRequestUrl(`${origin}/scenario`, origin), true);
});

test("rejects requests outside the exact loopback fixture origin", () => {
  const origin = "http://127.0.0.1:4173";

  assert.equal(isFixtureRequestUrl("https://provider.invalid/jobs", origin), false);
  assert.equal(isFixtureRequestUrl("http://127.0.0.1:4174/", origin), false);
  assert.equal(isFixtureRequestUrl("https://127.0.0.1:4173/", origin), false);
  assert.equal(isFixtureRequestUrl("http://user@127.0.0.1:4173/", origin), false);
  assert.equal(isFixtureRequestUrl(`${origin}/`, "https://provider.invalid"), false);
  assert.equal(isFixtureRequestUrl("not a URL", origin), false);
});
