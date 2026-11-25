// News-image entry (Node 22, standard library only): draw the poster with the
// bundled Python script, then place the finished image at the output path the
// grader reads. The drawing itself is deterministic and offline, so running
// this twice writes identical bytes.
//
// Local run:  mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { spawnSync } from "node:child_process";
import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const built = join(here, "entry.png");

const run = spawnSync("python3", [join(here, "draw_poster.py"), built], {
  cwd: here,
  stdio: "inherit",
});
if (run.status !== 0) {
  throw new Error(`draw_poster.py exited with status ${run.status}`);
}

mkdirSync(outDir, { recursive: true });
copyFileSync(built, join(outDir, "entry.png"));
