# 📊 DuckDB 实战笔记 ｜ 2026-09-17

> 每天一个 DuckDB 实战技巧，让你立刻能用。

---

## 🔥 今日话题：去重与排名 — 一条 SQL 解决重复数据与 TopN 查询

**核心技巧：ROW_NUMBER() 分组排名 + QUALIFY 一步过滤**

```sql
-- 创建示例订单表
CREATE TABLE orders AS SELECT * FROM (VALUES
    ('2024-01-01', 'Alice', 'Electronics', 299.99),
    ('2024-01-02', 'Alice', 'Books', 15.99),
    ('2024-01-01', 'Alice', 'Electronics', 299.99),
    ('2024-01-03', 'Bob', 'Clothing', 59.99),
    ('2024-01-01', 'Bob', 'Electronics', 499.99),
    ('2024-01-02', 'Bob', 'Books', 22.50)
) t(order_date, customer, category, amount);
```

**原理：用 ROW_NUMBER() 按分组标记顺序，再筛选 rn=1 即得去重记录；DuckDB 支持 `QUALIFY` 子句，可直接对窗口函数结果过滤，省掉一层 CTE。**

适用场景：
- 📌 用户表去重（保留最新一条记录）
- 📌 找出每个客户的 Top 3 消费品类
- 📌 异常订单检测（同一订单重复提交）
- 📌 报表中展示各区域销售额前 N 名

---

### 🎯 场景 1：用户去重 — 保留最新一笔订单

**问题**：订单表有重复录入，想获取每个客户的最新一笔订单信息。

```sql
SELECT order_date, customer, category, amount
FROM orders
QUALIFY ROW_NUMBER() OVER (
    PARTITION BY customer
    ORDER BY order_date DESC
) = 1
ORDER BY customer;
```

**结果解读**：每行是不同客户的最新订单，Alice 最新在 1月2日，Bob 最新在 1月3日。重复的 Alice 1月1日记录已被过滤。

> 💡 不用 `QUALIFY` 也可以，等价写法是套一层 CTE 再 `WHERE rn = 1`，但 `QUALIFY` 更简洁。

---

### 🎯 场景 2：每个客户的消费 Top 3 品类

**问题**：运营需要知道每个客户消费金额最高的品类排名，用于精准营销。

```sql
SELECT customer, category, total_spend
FROM (
    SELECT customer, category,
           SUM(amount) AS total_spend,
           ROW_NUMBER() OVER (
               PARTITION BY customer
               ORDER BY SUM(amount) DESC
           ) AS rank
    FROM orders
    GROUP BY customer, category
)
WHERE rank <= 3
ORDER BY customer, rank;
```

**业务价值**：直接得到每个客户的消费偏好排名，可结合用户画像做个性化推荐。

> ⚠️ 注意：窗口函数不能直接写在 `WHERE` 里，这里必须先聚合再开窗，所以套一层子查询是必要的。

---

### 🎯 场景 3：检测重复订单（同一用户同金额同日期）

**问题**：支付系统可能出现重复回调，需要识别并提交审核。

```sql
SELECT customer, order_date, category, amount, COUNT(*) AS dup_count
FROM orders
GROUP BY customer, order_date, category, amount
HAVING COUNT(*) > 1
ORDER BY dup_count DESC;
```

**结果解读**：返回所有重复行，`dup_count` 表示重复次数。此结果可直接导出给财务团队核对。

---

### 💡 进阶技巧：RANK vs DENSE_RANK vs ROW_NUMBER

```sql
-- 三者对比（以场景2为例）
WITH compared AS (
    SELECT customer, category, SUM(amount) AS total,
           ROW_NUMBER() OVER (PARTITION BY customer ORDER BY SUM(amount) DESC) AS rn,
           RANK()       OVER (PARTITION BY customer ORDER BY SUM(amount) DESC) AS rk,
           DENSE_RANK() OVER (PARTITION BY customer ORDER BY SUM(amount) DESC) AS drk
    FROM orders
    GROUP BY customer, category
)
SELECT customer, category, total, rn, rk, drk
FROM compared
ORDER BY customer, rn;
```

| 函数 | 并列处理 | 后续排名 |
|------|---------|---------|
| `ROW_NUMBER()` | 强制唯一序号 | 无间隔 |
| `RANK()` | 同名次，下一个跳号 | 有间隔 |
| `DENSE_RANK()` | 同名次，下一个连续 | 无间隔 |

体育比赛排名用 `RANK()`，连续编号用 `DENSE_RANK()`，严格去重取 TOP N 用 `ROW_NUMBER()`。

---

## 📌 总结

去重和排名是数据分析中最常见的两个需求，`ROW_NUMBER()` 配合 `PARTITION BY` 可以优雅地同时解决两者，再加上 DuckDB 的 `QUALIFY` 子句能少写一层 CTE。记住区分三个排名函数的差异，选对函数可以避免隐藏的逻辑 bug。

**行动建议**：打开 DuckDB，用今天的 orders 表跑一遍三个场景的 SQL，然后把 customer 换成你自己的业务字段试一次。实践一次胜过读十遍！

📌 收藏笔记，下次遇到直接参考。
🔍 [duckdblab.org](https://duckdblab.org) 系统学习 DuckDB。
