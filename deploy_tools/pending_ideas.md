# DevTools Hub 待发布文章队列（新工具对比）

> 本文件存放**尚未发布**的开发者工具对比选题。
> 每次 cron 任务自动运行：取第一个条目 → 生成中英文文章 → 提交到 content_calendar.json（status 改 published）→ 把本文件对应条目删除 → git push。
> 全部发布完后可删除本文件。

## 待发布选题

### 1. 语言工具链：Rust 工具生态对比
- **slug**: rust-toolchain-comparison
- **工具**: Cargo, Ruff, Pyright (对照), clippy, rust-analyzer
- **en_title**: Cargo vs Ruff vs Clippy vs rust-analyzer: Rust Toolchain Comparison (2026)
- **zh_title**: Cargo vs Ruff vs Clippy vs rust-analyzer：Rust 工具链对比（2026）
- **tags(en)**: ["Rust", "Cargo", "Ruff", "Clippy", "rust-analyzer", "Toolchain", "Comparison"]
- **tags(zh)**: ["Rust", "Cargo", "Ruff", "Clippy", "rust-analyzer", "工具链", "对比"]
- **category**: Web Development → 改为 "Developer Tools"
- **说明**: 对比 Rust 官方工具链（cargo/clippy/rust-analyzer）与 Python 系工具（ruff/pyright 作交叉对照）的差异，突出 Rust 工具链的编译器级检查优势。

### 2. 前端测试：Vitest vs Jest vs Playwright vs Cypress
- **slug**: frontend-testing-comparison
- **en_title**: Vitest vs Jest vs Playwright vs Cypress: Frontend Testing Comparison (2026)
- **zh_title**: Vitest vs Jest vs Playwright vs Cypress：前端测试工具对比（2026）
- **tags(en)**: ["Testing", "Vitest", "Jest", "Playwright", "Cypress", "Frontend", "Comparison"]
- **tags(zh)**: ["测试", "Vitest", "Jest", "Playwright", "Cypress", "前端", "对比"]
- **category**: Web Development

### 3. 包管理器：pnpm vs npm vs yarn vs Bun
- **slug**: package-manager-comparison
- **en_title**: pnpm vs npm vs Yarn vs Bun: JavaScript Package Manager Comparison (2026)
- **zh_title**: pnpm vs npm vs Yarn vs Bun：JS 包管理器对比（2026）
- **tags(en)**: ["JavaScript", "pnpm", "npm", "Yarn", "Bun", "Package Manager", "Comparison"]
- **tags(zh)**: ["JavaScript", "pnpm", "npm", "Yarn", "Bun", "包管理器", "对比"]
- **category**: Web Development

### 4. Python 包管理：uv vs pip vs poetry vs Rye
- **slug**: python-package-manager-comparison
- **en_title**: uv vs pip vs Poetry vs Rye: Python Package Manager Comparison (2026)
- **zh_title**: uv vs pip vs Poetry vs Rye：Python 包管理器对比（2026）
- **tags(en)**: ["Python", "uv", "pip", "Poetry", "Rye", "Package Manager", "Comparison"]
- **tags(zh)**: ["Python", "uv", "pip", "Poetry", "Rye", "包管理器", "对比"]
- **category**: Web Development

### 5. 终端工具：Warp vs iTerm2 vs Alacritty vs Ghostty vs Kitty
- **slug**: terminal-emulator-comparison
- **en_title**: Warp vs iTerm2 vs Ghostty vs Alacritty vs Kitty: Terminal Emulator Comparison (2026)
- **zh_title**: Warp vs iTerm2 vs Ghostty vs Alacritty vs Kitty：终端模拟器对比（2026）
- **tags(en)**: ["Terminal", "Warp", "iTerm2", "Ghostty", "Alacritty", "Kitty", "Comparison"]
- **tags(zh)**: ["终端", "Warp", "iTerm2", "Ghostty", "Alacritty", "Kitty", "对比"]
- **category**: Developer Tools

### 6. 代码搜索/分析：ripgrep vs fd vs fzf vs ast-grep
- **slug**: code-search-comparison
- **en_title**: ripgrep vs fd vs fzf vs ast-grep: Code Search & Analysis Tools (2026)
- **zh_title**: ripgrep vs fd vs fzf vs ast-grep：代码搜索与分析工具对比（2026）
- **tags(en)**: ["ripgrep", "fd", "fzf", "ast-grep", "CLI", "Comparison"]
- **tags(zh)**: ["ripgrep", "fd", "fzf", "ast-grep", "CLI", "对比"]
- **category**: Developer Tools

### 7. 数据库迁移工具：prisma vs alembic vs TypeORM vs SQLx
- **slug**: db-migration-comparison
- **en_title**: Prisma vs Alembic vs TypeORM vs SQLx: Database Migration & ORM Comparison (2026)
- **zh_title**: Prisma vs Alembic vs TypeORM vs SQLx：数据库迁移与 ORM 对比（2026）
- **tags(en)**: ["Database", "Prisma", "Alembic", "TypeORM", "SQLx", "ORM", "Migration", "Comparison"]
- **tags(zh)**: ["数据库", "Prisma", "Alembic", "TypeORM", "SQLx", "ORM", "迁移", "对比"]
- **category**: Databases

### 8. Web 服务器/网关：Caddy vs Nginx vs Traefik vs Envoy
- **slug**: web-server-comparison
- **en_title**: Caddy vs Nginx vs Traefik vs Envoy: Web Server & API Gateway Comparison (2026)
- **zh_title**: Caddy vs Nginx vs Traefik vs Envoy：Web 服务器与 API 网关对比（2026）
- **tags(en)**: ["Caddy", "Nginx", "Traefik", "Envoy", "Proxy", "Comparison"]
- **tags(zh)**: ["Caddy", "Nginx", "Traefik", "Envoy", "代理", "对比"]
- **category**: DevOps

### 9. 日志/可观测性：Loki vs Fluent Bit vs Vector vs OpenTelemetry
- **slug**: logging-observability-comparison
- **en_title**: Loki vs Fluent Bit vs Vector vs OpenTelemetry: Logging & Observability (2026)
- **zh_title**: Loki vs Fluent Bit vs Vector vs OpenTelemetry：日志与可观测性工具对比（2026）
- **tags(en)**: ["Logging", "Loki", "Fluent Bit", "Vector", "OpenTelemetry", "Comparison"]
- **tags(zh)**: ["日志", "Loki", "Fluent Bit", "Vector", "OpenTelemetry", "可观测性", "对比"]
- **category**: DevOps

### 10. 代码评审与静态分析：SonarQube vs CodeQL vs Semgrep vs golangci-lint
- **slug**: code-review-sast-comparison
- **en_title**: SonarQube vs CodeQL vs Semgrep vs golangci-lint: Code Review & SAST Comparison (2026)
- **zh_title**: SonarQube vs CodeQL vs Semgrep vs golangci-lint：代码评审与静态分析对比（2026）
- **tags(en)**: ["SAST", "SonarQube", "CodeQL", "Semgrep", "Security", "Comparison"]
- **tags(zh)**: ["SAST", "SonarQube", "CodeQL", "Semgrep", "安全", "静态分析", "对比"]
- **category**: DevOps
