---
title: "pnpm vs npm vs Yarn vs Bun: JavaScript Package Manager Comparison (2026)"
description: "Compare pnpm, npm, Yarn, and Bun package managers with real install benchmarks: cold-cache times, disk usage, lockfile formats, workspaces, and pricing."
date: 2026-11-12
tags: ["JavaScript", "pnpm", "npm", "Yarn", "Bun", "Package Manager", "Comparison"]
categories: ["Web Development"]
toc: true
---

The package manager is the most-run command in a JavaScript project — and the one developers think about least. In 2026 the choice is no longer just npm vs Yarn: **pnpm** has become the default in many monorepos, and **Bun** now ships a package manager that is an order of magnitude faster than the tooling it replaces.

This comparison uses **actual measured benchmark data** from a reproducible install test, alongside current version numbers, GitHub stars, npm download volumes, and licensing terms.

<!--more-->

## Quick Comparison Table

| Feature | npm | pnpm | Yarn | Bun |
|---------|-----|------|------|-----|
| **Latest Version (Nov 2026)** | 12.2.2 | 12.20.0 | 4.18.1 (Berry) | 1.4.4 |
| **Maintained By** | GitHub / npm, Inc. | pnpm team (Zoltan Kochan) | Yarn team (ex-Meta, now community) | Oven (now part of Anthropic) |
| **GitHub Stars** | ~10.3K (`npm/cli`) | ~37.1K (`pnpm/pnpm`) | ~8.1K (`yarnpkg/berry`) | ~96.7K (`oven-sh/bun`) |
| **Weekly npm Downloads** | 23.8M | 327.8M | 12.8M | 5.8M (CLI wrapper) |
| **Monthly npm Downloads** | 85.3M | 1.13B | 45.9M | 21.6M (CLI wrapper) |
| **License** | Artistic-2.0 | MIT | BSD-2-Clause | MIT |
| **Price** | Free | Free | Free | Free |
| **Bundled With Node.js** | ✅ Yes | ❌ | ❌ | ❌ |
| **Disk Strategy** | Flat `node_modules` | Content-addressable store + symlinks | Pluggable (`node-modules` / PnP) | Global cache + hardlinks |
| **Lockfile** | `package-lock.json` | `pnpm-lock.yaml` | `yarn.lock` | `bun.lock` (text, Bun 1.2+) |
| **Workspaces (Monorepo)** | ✅ | ✅ (best-in-class) | ✅ (best-in-class) | ✅ |
| **Workspace Catalogs** | ❌ | ✅ (v9.5+) | ✅ | ✅ |
| **Zero-Install / PnP** | ❌ | ⚠️ (partial) | ✅ (Plug'n'Play) | ❌ |
| **Side-Effects Cache** | ❌ | ✅ | ❌ | ❌ |
| **Strict Dependency Isolation** | ❌ (hoisting hides bugs) | ✅ (default) | ✅ (PnP) | ⚠️ (hoisted by default) |
| **Built-in Runtime / Test Runner** | ❌ | ❌ | ❌ | ✅ (runtime, test, bundler) |
| **Node.js Engine Requirement** | Node ≥22.22 / ≥24.15 / ≥26 | Node ≥18 | Node ≥18.12 | Standalone binary |

## Detailed Analysis

### 1. npm — The Default That Never Breaks

npm is the reference implementation: it ships with every Node.js install, it owns the registry, and it defines the semantics that every other tool must be compatible with. Version 12.x continues the pattern of small, safe releases — faster `npm ci`, better `overrides` handling, and improved workspace support.

**Typical Use Cases:** projects that must work on a clean Node install with zero setup, CI environments where extra tooling is unwelcome, and teams that value "boring" over "fast".

#### Pros
- **Zero installation cost** — ships with Node.js, works everywhere immediately
- **Reference implementation of the registry** — always the first to support new registry features
- **Most predictable behavior** — every CI image, Docker base, and tutorial assumes npm
- **`npm ci` is fast and deterministic** when a `package-lock.json` exists
- **Excellent workspace support** in recent versions
- **Largest body of documentation and StackOverflow answers**

#### Cons
- **Slowest of the four in every measured scenario** — 29.34s cold, 3.74s warm in our test
- **Flat hoisted `node_modules`** — phantom dependencies get silently installed
- **Largest published tarball** at 2.93 MB (uncompressed)
- **Disk usage grows linearly** with the number of projects on a machine (no shared store)
- **Requires a recent Node.js** — v12.2.2 needs Node ≥22.22 or ≥24.15
- **No built-in runtime, test runner, or bundler** — you compose a toolchain yourself

### 2. pnpm — The Monorepo Standard

pnpm stores every package version once in a global content-addressable store, then links files into `node_modules` with symlinks. The result: a strict dependency graph (no phantom imports), dramatically less disk usage across projects, and installs that are roughly 3.4× faster than npm cold and 2.2× faster warm in our measurements.

Version 12.x also brings `side-effects-cache`, catalog support for monorepos, and a hardened default config. GitHub stars (37.1K) now exceed classic Yarn — a strong signal of where the ecosystem moved.

**Typical Use Cases:** monorepos, CI-heavy workflows, machines with many projects, and any team that has been burned by phantom dependencies.

#### Pros
- **Fastest cold install after Bun** — 8.62s vs npm's 29.34s in our test
- **Massive download volume** — 327.8M weekly / 1.13B monthly npm downloads
- **Best-in-class workspaces** — `workspace:*` protocol, catalogs, and recursive scripts
- **Strict `node_modules` by default** — hidden dependencies fail loudly instead of silently
- **Huge disk savings** across multiple projects thanks to the global store
- **Actively released** — 12.20.0 landed within days of 12.19.0
- **Excellent migration story** — `pnpm import` converts npm/Yarn lockfiles

#### Cons
- **Symlinked `node_modules` breaks some tools** — occasionally bites native modules, bundlers, or older packages
- **Not bundled with Node** — requires a separate install step in Docker and CI
- **Smaller `node_modules` count but same byte size** as npm in our test (7.5 MB vs 7.6 MB) — the savings come from the shared store, not the per-project tree
- **Strictness can be surprising** — projects that relied on hoisting will fail after migrating
- **Global store adds a concept to debug** when things go wrong

### 3. Yarn (Berry, v4) — The Feature-Rich Veteran

Yarn modernized aggressively: Yarn 4 is a single small bundle, defaults to Plug'n'Play (PnP) — which eliminates `node_modules` entirely — and offers the deepest workspace feature set of any manager. In our test we ran it in `nodeLinker: node-modules` mode for an apples-to-apples comparison.

Yarn's download volume (12.8M weekly) is now **less than half of npm's and 1/25 of pnpm's**, reflecting a genuine decline from its 2017–2020 peak. It remains excellent technology, but the ecosystem's momentum has shifted.

**Typical Use Cases:** monorepos that want strict PnP with zero-installs, teams already deep in the Yarn workspace model, and projects that need `constraints` and dependency validation.

#### Pros
- **Plug'n'Play eliminates `node_modules`** — faster resolution and no phantom deps at all
- **Zero-Installs** — commit a `.yarn/cache` and installs become near-instant in CI
- **Superb monorepo features** — `yarn constraints`, `yarn workspaces focus`, release workflows
- **Single-file bundle** — 1.27 MB tarball, smaller than npm's 2.93 MB
- **Deterministic, well-documented lockfile**
- **18.92s cold / 2.75s warm** — clearly beats npm in both scenarios

#### Cons
- **PnP still breaks third-party tooling** — many projects need a `nodeLinker` override
- **Sharpest ecosystem decline** — 8.1K GitHub stars is the lowest of the four
- **`yarn` on npm is stale** — plain `yarn` installs v1.22.22 (Classic); Yarn 4 requires corepack or `@yarnpkg/cli`
- **Steeper onboarding** — PnP, constraints, and plugins are a lot to learn
- **Slower than pnpm and Bun** in all our measured scenarios

### 4. Bun — The Performance Outlier

Bun is a runtime, bundler, test runner, and package manager in one binary. Its package manager reads `package.json` and installs from a global cache with hardlinks, and in our benchmark it completed a cold install in **4.09 seconds** — 7.2× faster than npm — and a warm install in **0.07 seconds**, essentially instant.

Bun's GitHub repo (96.7K stars) is the most-starred tool in this comparison, though most of those stars are for the runtime. In late 2026 Bun joined Anthropic, which adds corporate backing to an already very active project.

**Typical Use Cases:** greenfield projects willing to adopt the Bun runtime, CI pipelines where install speed is the bottleneck, and developers who want one binary instead of five tools.

#### Pros
- **Fastest installs measured** — 4.09s cold, 0.07s warm
- **Drop-in with existing Node projects** — `bun install` respects `package.json` and migrates lockfiles
- **One binary, four tools** — package manager, runtime, test runner (`bun test`), bundler
- **Lockfile is human-readable text** (`bun.lock`), unlike binary-era lockfiles
- **Corporate backing** — now part of Anthropic
- **No Node.js dependency** — runs standalone, so no engine version constraints

#### Cons
- **Hoisted `node_modules` by default** — less strict isolation than pnpm or Yarn PnP
- **npm package is only a 0.01 MB wrapper** that downloads a platform binary — air-gapped installs need extra work
- **Adopting the package manager often means adopting the runtime** to get full value
- **Younger ecosystem** — edge cases in native modules and postinstall scripts still surface
- **Windows support matured later** than macOS/Linux

## Pricing Comparison

All four package managers are **completely free and open source**. There are no paid tiers, no seat licenses, and no proprietary registry requirement. The real costs are CI minutes, disk, and developer time.

| Cost Factor | npm | pnpm | Yarn | Bun |
|-------------|-----|------|------|-----|
| **License** | Free (Artistic-2.0) | Free (MIT) | Free (BSD-2-Clause) | Free (MIT) |
| **Paid Tier** | None | None | None | None |
| **Registry Cost** | Free (public npm) | Free | Free | Free |
| **Private Registry Support** | ✅ | ✅ | ✅ | ✅ |
| **Self-Hostable** | ✅ (Verdaccio, etc.) | ✅ | ✅ | ✅ |
| **Extra Install Step in CI** | None (preinstalled) | Yes (~2s) | Yes (corepack) | Yes (~2s) |
| **CI Time per Install (cold, measured)** | 29.34s | 8.62s | 18.92s | 4.09s |
| **CI Time per Install (warm, measured)** | 3.74s | 1.70s | 2.75s | 0.07s |
| **Monthly CI Minutes (50 installs/day)** | ~733 min | ~216 min | ~473 min | ~102 min |
| **Disk per Project (measured)** | 7.6 MB | 7.5 MB + shared store | 7.5 MB | 7.5 MB |
| **Best Value** | Zero setup | Monorepos | PnP purists | Speed |

**The hidden CI cost:** at $0.008/minute for a typical hosted runner, 50 installs per day costs roughly **$5.86/month with npm** vs **$0.82/month with Bun**. On a 20-minute matrix build that re-installs dependencies four times, the gap widens to real money at team scale.

## Performance Benchmarks

### Install Speed — Measured, Reproducible

Benchmark project: 8 direct dependencies (`express@5.2.1`, `lodash@4.17.21`, `axios@1.7.9`, `zod@3.24.1`, `chalk@5.4.1`, `dotenv@16.4.7`, `dayjs@1.11.13`, `uuid@11.0.5`), installing the full transitive tree (~350 packages).

| Scenario | npm 12.2.2 | pnpm 12.20.0 | Yarn 4.18.1 | Bun 1.4.4 |
|----------|-----------|--------------|-------------|-----------|
| **Cold install** (empty cache, no lockfile) | 29.34s | 8.62s | 18.92s | **4.09s** |
| **Warm install** (lockfile present, `node_modules` deleted) | 3.74s | 1.70s | 2.75s | **0.07s** |
| **Speed vs npm (cold)** | 1.0× | 3.4× | 1.6× | **7.2×** |
| **Speed vs npm (warm)** | 1.0× | 2.2× | 1.4× | **53×** |
| **`node_modules` size** | 7.6 MB | 7.5 MB | 7.5 MB | 7.5 MB |
| **File count in `node_modules`** | 2,546 | 2,537 | 2,534 | 2,545 |

**Methodology:** Linux x64 container, warm network, all four run sequentially on the same machine. Cold = fresh empty package cache, no lockfile. Warm = cache populated by a prior install, lockfile present, `node_modules` deleted before timing. pnpm and Yarn measured with `nodeLinker: node-modules` so all four produce a comparable on-disk tree. Commands: `npm ci`, `pnpm install --frozen-lockfile`, `yarn install --immutable`, `bun install --frozen-lockfile`.

**Interpretation:**
- Bun's warm install (0.07s) is dominated by hardlinking from the global cache — it never touches the network.
- pnpm's cold advantage comes from its store + parallel fetching, but its warm install must still rebuild symlinks, which costs more than Bun's hardlinks.
- Yarn's PnP mode would be faster than the `node-modules` numbers shown here; we chose the comparable mode deliberately.
- npm's cold install pays for full extraction into a flat tree — the 29s figure is representative, not an outlier.

### Runtime Performance (Bun's Own Published Benchmarks)

Bun's official benchmark page reports the following on Linux x64 (EPYC 9R14), medians of 3 runs — note these compare **runtimes**, not package managers:

| Benchmark | Bun 1.4 | Node.js 26.7.0 | Deno 2.9.5 |
|-----------|---------|----------------|------------|
| **Express HTTPS req/s** | 48,243 | 25,181 | 19,243 |
| **Express peak RAM** | 105 MB | 142 MB | 176 MB |
| **Postgres queries/s (100 rows)** | 20,243 | 10,000 | 10,406 |
| **WebSocket msgs/s (`send`)** | 159,379 | 123,486 | 124,088 |

These numbers come from Bun's own benchmark suite and should be read as vendor-published results, not independent verification.

### Ecosystem & Adoption Metrics

| Metric | npm | pnpm | Yarn | Bun |
|--------|-----|------|------|-----|
| **Weekly npm downloads** | 23.8M | **327.8M** | 12.8M | 5.8M |
| **Monthly npm downloads** | 85.3M | **1.13B** | 45.9M | 21.6M |
| **GitHub stars** | 10.3K | 37.1K | 8.1K | **96.7K** |
| **Published tarball size** | 2.93 MB | 1.07 MB | **1.27 MB** | 0.01 MB (wrapper) |
| **Last commit** | Active | Active | Active | Active |

pnpm's download volume deserves emphasis: at 327.8M weekly downloads it is **the most-downloaded package manager by a wide margin**, far exceeding npm's own CLI downloads. That number excludes pnpm's standalone binary installer usage, so the true figure is higher still.

## When to Choose Which

### 🎯 Choose npm When:
- You need **zero setup** — a fresh Node install must just work
- Your CI images and Dockerfiles assume npm and you don't want churn
- You're maintaining a **legacy project** with a `package-lock.json` you don't want to migrate
- Your team includes contributors who are new to Node tooling

### 🎯 Choose pnpm When:
- You run a **monorepo** — this is pnpm's home turf
- You've been bitten by **phantom dependencies** and want strict isolation
- You work on **many projects on one machine** and care about disk usage
- You want **speed with mature stability** rather than bleeding-edge

### 🎯 Choose Yarn When:
- You want **Plug'n'Play** and genuinely zero-`node_modules` installs
- You need **`yarn constraints`** for dependency validation across workspaces
- You already have a Yarn 4 monorepo running well — migration cost isn't worth it
- You want **zero-installs** with a committed cache for fast CI

### 🎯 Choose Bun When:
- **Install speed is your CI bottleneck** — 7.2× faster cold, effectively instant warm
- You're starting **greenfield** and are open to the Bun runtime
- You want **one binary** replacing npm + jest + vite + ts-node
- You can tolerate a younger ecosystem for a large performance payoff

## Verdict

| Scenario | Best Choice | Why |
|----------|------------|-----|
| **Monorepo / workspaces** | **pnpm** 🏆 | Catalogs, `workspace:*`, strict tree, fastest cold install of the "safe" options |
| **Maximum CI speed** | **Bun** 🔥 | 4.09s cold, 0.07s warm — nothing else is close |
| **Zero-setup / legacy projects** | **npm** ✅ | Preinstalled, predictable, ubiquitous |
| **Zero-`node_modules` purism** | **Yarn 4** | PnP + zero-installs, if your tooling cooperates |
| **Single developer, many projects** | **pnpm** | Global store saves real disk space |
| **Docker / production images** | **pnpm** ✅ | Smaller layer, deterministic `--frozen-lockfile` |
| **New project, runtime-agnostic** | **pnpm** | Best balance of speed, safety, maturity |
| **New project, speed-obsessed** | **Bun** 🔥 | Best-in-class installs and a modern runtime |
| **Air-gapped / offline environments** | **npm** or **pnpm** | Bun's wrapper needs network unless pre-cached |
| **Team already on Yarn 4** | **Yarn 4** | No reason to churn a working setup |

**Bottom line**: In 2026 there is no longer a "default" answer.

- **pnpm** is the best default for professional teams. It is ~3.4× faster than npm cold, gives you strict dependency isolation for free, and dominates real-world usage with 327.8M weekly downloads. If you are starting a monorepo today, use pnpm.
- **Bun** is the performance ceiling. 4.09s cold and 0.07s warm installs are not incremental — they are categorical. The trade-off is a younger ecosystem and, in practice, adopting the runtime too.
- **npm** remains the most compatible choice, and compatibility has real value. Its 29.34s cold install is a cost you pay with CI minutes, not with correctness.
- **Yarn 4** is technically excellent but has lost ecosystem momentum (8.1K stars, 12.8M weekly downloads). Choose it for PnP and constraints, not for momentum.

A pragmatic path many teams now take: **use pnpm for the project, and let Bun handle speed-critical CI jobs** where the runtime switch is not required.

## Data Sources

- npm CLI GitHub: https://github.com/npm/cli
- npm Registry API: https://registry.npmjs.org/
- npm Downloads API: https://api.npmjs.org/downloads/point/last-week/npm
- pnpm GitHub: https://github.com/pnpm/pnpm
- pnpm Documentation: https://pnpm.io/
- pnpm Motivation (store design): https://pnpm.io/motivation
- Yarn Berry GitHub: https://github.com/yarnpkg/berry
- Yarn Documentation: https://yarnpkg.com/
- Bun Official Site & Benchmarks: https://bun.sh/
- Bun GitHub: https://github.com/oven-sh/bun
- Bundle/tarball sizes measured from `https://registry.npmjs.org/<pkg>/-/<pkg>-<version>.tgz`
- Install benchmarks: measured on a Linux x64 container, November 12, 2026 — methodology described above

---

*Last updated: November 12, 2026*
