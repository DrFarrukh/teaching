import { cp, mkdir, rm } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const project = resolve(here, "..");
const dist = resolve(project, "dist");

await rm(dist, { recursive: true, force: true });
await mkdir(dist, { recursive: true });

for (const item of ["index.html", "lecture.css", "vendor", "public"]) {
  await cp(resolve(project, item), resolve(dist, item), { recursive: true });
}

console.log(`Built static deck in ${dist}`);
