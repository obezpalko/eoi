import { FilePath, QUARTZ, joinSegments } from "../../util/path"
import { QuartzEmitterPlugin } from "../types"
import fs from "fs"
import { glob } from "../../util/glob"
import { dirname } from "path"

export const Static: QuartzEmitterPlugin = () => ({
  name: "Static",
  async *emit({ argv, cfg }) {
    // Copy files from quartz/static to output/static
    const staticPath = joinSegments(QUARTZ, "static")
    const fps = await glob("**", staticPath, cfg.configuration.ignorePatterns)
    const outputStaticPath = joinSegments(argv.output, "static")
    await fs.promises.mkdir(outputStaticPath, { recursive: true })
    for (const fp of fps) {
      const src = joinSegments(staticPath, fp) as FilePath
      const dest = joinSegments(outputStaticPath, fp) as FilePath
      await fs.promises.mkdir(dirname(dest), { recursive: true })
      await fs.promises.copyFile(src, dest)
      yield dest
    }

    // Copy files from quartz/root to output/
    const rootPath = joinSegments(QUARTZ, "root")
    if (fs.existsSync(rootPath)) {
      const r_fps = await glob("**", rootPath, cfg.configuration.ignorePatterns)
      for (const fp of r_fps) {
        const src = joinSegments(rootPath, fp) as FilePath
        const dest = joinSegments(argv.output, fp) as FilePath
        await fs.promises.mkdir(dirname(dest), { recursive: true })
        await fs.promises.copyFile(src, dest)
        yield dest
      }
    }
  },
  async *partialEmit() { },
})
