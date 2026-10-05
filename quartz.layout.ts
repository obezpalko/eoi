import { PageLayout, SharedLayout } from "./quartz/cfg"
import * as Component from "./quartz/components"
import { FileTrieNode } from "./quartz/util/fileTrie"

// Explorer order: folders first, sorted by folder name so the 10-, 20-, ...
// prefixes decide the order even when a folder note gives the folder another
// title; notes sorted by title. Serialised to the browser, so keep it
// self-contained (no helpers or named inner functions: the bundler wraps
// those in a __name() call that doesn't exist client-side).
const explorerSortFn = (a: FileTrieNode, b: FileTrieNode) => {
  if (a.isFolder !== b.isFolder) return a.isFolder ? -1 : 1
  const keyA = a.isFolder ? a.slugSegment : a.displayName
  const keyB = b.isFolder ? b.slugSegment : b.displayName
  return keyA.localeCompare(keyB, undefined, { numeric: true, sensitivity: "base" })
}

// components shared across all pages
export const sharedPageComponents: SharedLayout = {
  head: Component.Head(),
  header: [],
  afterBody: [],
  footer: Component.Footer({
    links: {
      GitHub: "https://github.com/jackyzha0/quartz",
      "Discord Community": "https://discord.gg/cRFFHYye7t",
    },
  }),
}

// components for pages that display a single page (e.g. a single note)
export const defaultContentPageLayout: PageLayout = {
  beforeBody: [
    Component.ConditionalRender({
      component: Component.Breadcrumbs(),
      condition: (page) => page.fileData.slug !== "index",
    }),
    Component.ArticleTitle(),
    Component.ContentMeta(),
    Component.TagList(),
  ],
  left: [
    Component.PageTitle(),
    Component.MobileOnly(Component.Spacer()),
    Component.Flex({
      components: [
        {
          Component: Component.Search(),
          grow: true,
        },
        { Component: Component.Darkmode() },
        { Component: Component.ReaderMode() },
      ],
    }),
    Component.Explorer({ sortFn: explorerSortFn }),
  ],
  right: [
    // Component.Graph(),
    Component.DesktopOnly(Component.TableOfContents()),
    Component.Backlinks(),
  ],
}

// components for pages that display lists of pages  (e.g. tags or folders)
export const defaultListPageLayout: PageLayout = {
  beforeBody: [Component.Breadcrumbs(), Component.ArticleTitle(), Component.ContentMeta()],
  left: [
    Component.PageTitle(),
    Component.MobileOnly(Component.Spacer()),
    Component.Flex({
      components: [
        {
          Component: Component.Search(),
          grow: true,
        },
        { Component: Component.Darkmode() },
      ],
    }),
    Component.Explorer({ sortFn: explorerSortFn }),
  ],
  right: [],
}
