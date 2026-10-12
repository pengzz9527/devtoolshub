---
title: "📊 DuckDB 实战笔记｜2026-09-24：MERGE INTO — 增量更新数据的一站式方案"
description: "每天一个 DuckDB 实战技巧。今天教你用 MERGE INTO 一条 SQL 搞定 UPSERT：新增用户插入、已有用户更新、删掉不存在的用户——告别五十行 Python 比对代码。"
date: 2026-09-24
tags: ["DuckDB", "MERGE INTO", "UPSERT", "增量更新", "ETL", "SQL", "实战"]
categories: ["DuckDB 实战笔记"]
toc: false
---

# 📊 DuckDB 实战笔记 ｜ 2026-09-24

> 每天一个 DuckDB 实战技巧，让你立刻能用。

---

## 🔥 今日话题：MERGE INTO — 增量更新数据的一站式方案

你有没有遇到过这种场景：

> 每天从上游拿到一份新的用户数据，需要把新增用户插入、已有用户更新、删掉不存在的用户。用 Python 写？先查现有数据、再比对差异、然后分别执行 INSERT/UPDATE/DELETE……代码五十行起步，还容易漏边界情况。

**这是 ETL 中最常见的「Upsert」需求。**

传统做法要三张表来回 JOIN，逻辑复杂、容易出错。DuckDB 用一条 `MERGE INTO` 语句搞定所有操作——插入、更新、删除一步到位。

---

## 📋 场景一：基础 UPSERT — 新记录插入、已有记录更新

假设你每天收到一张用户快照表 `daily_users`，需要根据主键 `user_id` 更新到 `users` 表：

```sql
-- 创建目标表（初始状态）
CREATE TABLE users AS SELECT * FROM (VALUES
    (1, 'Alice', 'alice@email.com', '2024-01-01'),
    (2, 'Bob',   'bob@email.com',   '2024-01-01'),
    (3, 'Carol', 'carol@email.com', '2024-01-01')
) t(user_id, name, email, updated_at);

-- 模拟今天的新数据
CREATE TABLE daily_users AS SELECT * FROM (VALUES
    (2, 'Bob_Jr', 'bob_new@email.com', '2024-09-24'),  -- 已存在，需更新
    (4, 'Dave',   'dave@email.com',  '2024-09-24'),    -- 新用户，需插入
    (1, 'Alice',  'alice_v2@email.com', '2024-09-24')  -- 已存在，需更新
) t(user_id, name, email, updated_at);
```

**一条 MERGE INTO 搞定：**

```sql
MERGE INTO users AS target
USING daily_users AS source
ON target.user_id = source.user_id
WHEN MATCHED THEN
    UPDATE SET
        name       = source.name,
        email      = source.email,
        updated_at = source.updated_at
WHEN NOT MATCHED THEN
    INSERT (user_id, name, email, updated_at)
    VALUES (source.user_id, source.name, source.email, source.updated_at);

-- 查看结果
SELECT * FROM users ORDER BY user_id;
```

**结果解读：**
- user_id=2（Bob → Bob_Jr）和 user_id=1（Alice 邮箱变更）被**更新**
- user_id=4（Dave）被**插入**
- 原来有的 user_id=3（Carol）保持不变（如果没有 DELETE 子句）

---

## 📋 场景二：带条件过滤的更新

不是所有字段都要无条件覆盖。比如只想在"name 发生变化"时才更新：

```sql
MERGE INTO users AS target
USING daily_users AS source
ON target.user_id = source.user_id
WHEN MATCHED AND target.name <> source.name THEN
    UPDATE SET
        name       = source.name,
        updated_at = source.updated_at
WHEN NOT MATCHED THEN
    INSERT (user_id, name, email, updated_at)
    VALUES (source.user_id, source.name, source.email, source.updated_at);
```

`AND target.name <> source.name` 就是**条件过滤器**，只有满足条件的行才会触发 UPDATE，避免无意义的写入。

---

## 📋 场景三：全量同步 + 软删除

实际业务中，上游数据可能删除了某些用户。用 `DELETE` 子句实现**反向删除**：

```sql
MERGE INTO users AS target
USING daily_users AS source
ON target.user_id = source.user_id
WHEN MATCHED THEN
    UPDATE SET
        name       = source.name,
        email      = source.email,
        updated_at = source.updated_at
WHEN NOT MATCHED THEN
    INSERT (user_id, name, email, updated_at)
    VALUES (source.user_id, source.name, source.email, source.updated_at)
WHEN NOT MATCHED BY SOURCE AND target.is_deleted = FALSE THEN
    UPDATE SET is_deleted = TRUE, updated_at = DATE '2024-09-24';
```

**逻辑拆解：**
- `MATCHED` → 存在即更新
- `NOT MATCHED`（源中有、目标中没有）→ 插入
- `NOT MATCHED BY SOURCE`（目标中有、源中没有）→ 标记删除（软删）

> 💡 软删除比物理删除更安全——数据还在，只是标记为失效，随时可以恢复。

---

## 📋 场景四：处理并发冲突 — ON CONFLICT 风格

如果你更熟悉 PostgreSQL 语法，DuckDB 也支持另一种写法：

```sql
INSERT INTO users (user_id, name, email, updated_at)
SELECT user_id, name, email, updated_at
FROM daily_users
ON CONFLICT (user_id) DO UPDATE SET
    name       = excluded.name,
    email      = excluded.email,
    updated_at = excluded.updated_at;
```

`excluded` 是 DuckDB 内置的伪表，代表被拒绝插入的行数据。这种写法简洁，适合**只有插入和更新、不需要删除**的场景。

---

## 💡 MERGE INTO vs 传统三表 JOIN

| 方式 | 代码行数 | 出错风险 | 可读性 |
|------|---------|---------|--------|
| 传统做法：SELECT + INSERT + UPDATE + DELETE | 20-40 行 | 高（边界 case 多） | 差 |
| DuckDB MERGE INTO | 5-10 行 | 低（原子操作） | 好 |
| INSERT ... ON CONFLICT | 3-5 行 | 低 | 最好 |

**核心优势：**
1. **原子性** — MERGE 是一个事务，要么全部成功，要么全部回滚
2. **简洁** — 一行语句替代多步操作
3. **性能** — DuckDB 内部优化了匹配逻辑，比手动写 JOIN 快得多

---

## ⚠️ 常见陷阱

**1. 别忘记 ON 条件中的索引**
如果 `user_id` 没有索引，MERGE 会对全表做嵌套循环匹配，数据量大时极慢。建个主键或索引：
```sql
ALTER TABLE users ADD PRIMARY KEY (user_id);
```

**2. MATCHED BY SOURCE 的坑**
`NOT MATCHED BY SOURCE` 会匹配目标表中所有源表没有的行。如果你只想删除「软删标志为 false」的行，记得加过滤条件，否则会误删历史归档数据。

**3. 更新字段的来源选择**
当新旧数据都有值时，决定用哪个来源很关键：
- 用 `source.col` → 新数据优先（适合增量同步）
- 用 `COALESCE(source.col, target.col)` → 新数据为空时才用旧的（适合部分更新）

```sql
-- 智能更新：只在源数据有值时才覆盖
WHEN MATCHED THEN
    UPDATE SET
        name       = COALESCE(source.name, target.name),
        email      = COALESCE(source.email, target.email),
        updated_at = source.updated_at;
```

---

## 📌 总结

| 技能 | 一句话总结 |
|------|-----------|
| MERGE INTO 基础 | ON 条件匹配 → MATCHED 更新 → NOT MATCHED 插入 |
| 条件过滤更新 | `WHEN MATCHED AND 条件 THEN` 精准控制更新范围 |
| 反向删除 | `WHEN NOT MATCHED BY SOURCE` 处理删除逻辑 |
| ON CONFLICT 简写 | INSERT...ON CONFLICT 适合纯 Upsert 场景 |
| COALESCE 智能更新 | 新数据为空时保留旧值，避免脏数据覆盖 |

**一条 MERGE INTO，替代五十行 Python 比对代码。** 增量同步的场景里，它是最高效的解决方案。

**行动建议**：打开 DuckDB，用今天的 users 表跑一遍三种场景，然后把 user_id 换成你业务表的主键试一次。试试加上 COALESCE 的智能更新逻辑，看看效果！

📌 收藏笔记，下次做数据同步时直接参考。
🔍 [duckdblab.org](https://duckdblab.org) 系统学习 DuckDB。
