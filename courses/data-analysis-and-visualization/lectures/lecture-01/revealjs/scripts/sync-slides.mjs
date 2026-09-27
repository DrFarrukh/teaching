import { cp, mkdir, readFile, rm, writeFile } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const project = resolve(here, "..");
const lecture = resolve(project, "..");
const publicDir = resolve(project, "public");

const source = await readFile(resolve(lecture, "slides.md"), "utf8");
const withoutMarpHeader = source.replace(/^---\r?\n[\s\S]*?\r?\n---\r?\n/, "");
const revealMarkdown = withoutMarpHeader.replaceAll("](outputs/", "](public/outputs/");

await mkdir(publicDir, { recursive: true });
await writeFile(resolve(publicDir, "slides.md"), revealMarkdown.trimStart(), "utf8");

const targetOutputs = resolve(publicDir, "outputs");
await rm(targetOutputs, { recursive: true, force: true });
await cp(resolve(lecture, "outputs"), targetOutputs, { recursive: true });

console.log("Synced slides.md and figures.");
