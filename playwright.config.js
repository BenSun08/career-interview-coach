import { defineConfig } from "@playwright/test";

/**
 * @param {string} requestUrl
 * @param {string} fixtureOrigin
 * @returns {boolean}
 */
export function isFixtureRequestUrl(requestUrl, fixtureOrigin) {
  try {
    const request = new URL(requestUrl);
    const fixture = new URL(fixtureOrigin);
    const isLoopback = ["127.0.0.1", "localhost", "[::1]"].includes(
      fixture.hostname,
    );

    return (
      isLoopback &&
      fixture.protocol === "http:" &&
      request.protocol === "http:" &&
      request.username === "" &&
      request.password === "" &&
      request.origin === fixture.origin
    );
  } catch {
    return false;
  }
}

export default defineConfig({
  testDir: "./tests/e2e",
  testMatch: "**/*.spec.js",
  fullyParallel: false,
  retries: 0,
  workers: 1,
  timeout: 10_000,
  reporter: "list",
  use: {
    browserName: "chromium",
    serviceWorkers: "block",
  },
});
