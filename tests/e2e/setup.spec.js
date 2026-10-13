import assert from "node:assert/strict";
import { createServer } from "node:http";

import { expect, test } from "@playwright/test";

import { isFixtureRequestUrl } from "../../playwright.config.js";

/** @type {import("node:http").Server | undefined} */
let fixtureServer;
let fixtureOrigin = "";

test.beforeAll(async () => {
  const server = createServer((request, response) => {
    if (request.url !== "/") {
      response.writeHead(404);
      response.end();
      return;
    }

    response.writeHead(200, { "content-type": "text/html; charset=utf-8" });
    response.end(`<!doctype html>
      <html lang="en">
        <head><meta charset="utf-8"><title>Offline fixture</title></head>
        <body>
          <h1>Synthetic offline fixture</h1>
          <output data-status="provider">pending</output>
          <script>
            fetch("https://provider.invalid/jobs")
              .then(() => { document.querySelector('[data-status="provider"]').textContent = "unexpected"; })
              .catch(() => { document.querySelector('[data-status="provider"]').textContent = "blocked"; });
          </script>
        </body>
      </html>`);
  });
  fixtureServer = server;

  /** @type {Promise<void>} */
  const listening = new Promise((resolve, reject) => {
    server.once("error", reject);
    server.listen(0, "127.0.0.1", () => resolve());
  });
  await listening;

  const address = server.address();
  if (address === null || typeof address === "string") {
    throw new Error("The loopback fixture server did not receive a TCP port");
  }
  fixtureOrigin = `http://127.0.0.1:${address.port}`;
});

test.afterAll(async () => {
  if (fixtureServer?.listening) {
    const server = fixtureServer;
    /** @type {Promise<void>} */
    const serverClosed = new Promise((resolve, reject) => {
      server.close((error) => {
        if (error) {
          reject(error);
          return;
        }
        resolve();
      });
    });
    await serverClosed;
  }
});

test("runs a disposable loopback fixture and blocks an external request", async ({
  page,
}) => {
  /** @type {string[]} */
  const deniedRequests = [];

  await page.route("**/*", async (route) => {
    const requestUrl = route.request().url();
    if (isFixtureRequestUrl(requestUrl, fixtureOrigin)) {
      await route.continue();
      return;
    }
    deniedRequests.push(requestUrl);
    await route.abort();
  });

  await page.goto(fixtureOrigin);
  await expect(
    page.getByRole("heading", { name: "Synthetic offline fixture" }),
  ).toBeVisible();
  await expect(page.locator('[data-status="provider"]')).toHaveText("blocked");
  assert.deepEqual(deniedRequests, ["https://provider.invalid/jobs"]);
});
