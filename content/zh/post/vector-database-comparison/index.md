---
title: "Pinecone vs Qdrant vs Weaviate vs Milvus：向量数据库对比（2026）"
description: "对比 Pinecone、Qdrant、Weaviate 和 Milvus 四大向量数据库在 RAG 与语义搜索场景的表现。功能、价格、性能基准与选型建议。"
date: 2026-11-17
tags: ["向量数据库", "Pinecone", "Qdrant", "Weaviate", "Milvus", "RAG", "AI", "对比"]
categories: ["数据库"]
toc: true
---

RAG、语义搜索和推荐系统的底座都是同一个东西：一个能存储数千万乃至数十亿高维向量、并在毫秒内回答"什么与这个最相似"的数据库。2026 年，这个领域已经收敛到四个正经选项：**Pinecone**（纯托管的先行者）、**Qdrant**（Rust 性能主力）、**Weaviate**（AI 模块丰富的通才）、**Milvus**（分布式规模之王）。

本文基于当前版本号、GitHub Star 数、官方定价页和公开基准测试数据，帮你选出合适的那一个。

<!--more-->

## 快速对比表

| 特性 | Pinecone | Qdrant | Weaviate | Milvus |
|------|----------|--------|----------|--------|
| **最新版本（2026 年 11 月）** | n/a（托管服务，API 优先） | 1.20.1 | 1.40.4 | 3.0.0 |
| **维护方** | Pinecone Inc.（YC W21） | Qdrant Inc. | Weaviate Inc. | Zilliz / LF AI & Foundation |
| **实现语言** | 专有 | Rust | Go | Go |
| **GitHub Stars** | n/a（核心不开源） | ~35.4K | ~16.9K | ~46.6K |
| **开源协议** | 专有 | Apache-2.0 | BSD-3-Clause | Apache-2.0 |
| **可自托管** | ❌ 否 | ✅ 单二进制 / Docker | ✅ Docker / Helm | ✅（多组件） |
| **索引类型** | HNSW + 量化 | HNSW + 标量/乘积/二进制量化 | HNSW、flat + 旋转量化（RQ） | HNSW、IVF、DiskANN、GPU 索引 |
| **混合搜索（关键词 + 向量）** | ✅ | ✅（稀疏向量） | ✅（内置 BM25） | ✅（BM25 → 稀疏向量，v2.5+） |
| **内置向量模型 / AI 模块** | ✅（云推理） | ✅（云推理） | ✅（50+ 向量化模块、生成式搜索） | ❌（自带模型管线） |
| **多租户** | Namespaces | 基于 payload（快、内置） | 一等公民 tenant（每租户一个 shard） | 数据库 + 分区 |
| **设计规模** | 无服务器架构，自动扩缩 | 无共享架构集群 | 云原生集群 | 分布式、存算分离（十亿级向量） |
| **最高 SLA** | 99.95% | 99.95%（Premium，多 AZ） | 99.95%（Premium 独占） | 99.95%（Enterprise） |
| **HIPAA 合规** | ✅（$190/月附加，或 Enterprise 含） | ❌ | ✅（独占部署） | ❌ |
| **免费额度** | 2 GB + 100 万读单元/月 | 0.5 vCPU / 1 GB 内存 / 4 GB 磁盘 | 10 万对象、1 GB 内存、10 GB 磁盘 | 5 GB + 250 万 vCU/月 |
| **付费入门** | Builder $20/月（固定价） | ~$26/月（最小 Standard 集群） | Flex 从 $45/月起 | $4/百万 vCU，无最低消费（存储 $0.04/GB/月） |

## 详细分析

### 1. Pinecone —— 零运维的托管先行者

Pinecone 开创了向量数据库这个品类，也是四者中**唯一纯托管**的一家——没有可自托管的开源内核。全部运行在无服务器架构上：你只管写入向量，分片、扩缩容和索引优化都由 Pinecone 在幕后完成。2026 年 5–9 月修订后的价格体系共四档：免费 Starter、固定价 $20/月的 Builder、最低 $50/月的 Standard 和最低 $500/月的 Enterprise。注意**读操作的价格是写的 3–4 倍**（Standard 档读单元 $16–18/百万，写单元 $4–4.5/百万），读多写少的工作负载要仔细算账。

**典型场景：** 想完全跳过基础设施的团队、追求"开箱即用"的 RAG 产品、需要 HIPAA 或私网端点但不想自己跑集群的公司。

#### 优点
- **真正的零运维**——没有版本升级、没有扩缩容决策、没有索引调优，无服务器架构全部托管
- **上手最快**——一个 API key 就能拥有生产级向量库
- **安全合规栈成熟**——RBAC、SSO、BYOC、私网端点、客户自管密钥（CMEK）、HIPAA（附加或 Enterprise）
- **Standard 档含 3 周试用 + $300 额度**
- **专用读节点（Dedicated Read Nodes）** 支撑高 QPS 读场景
- **对象存储导入**仅 $0.25/GB

#### 缺点
- **不可自托管、无源代码**——无法逃离锁定，同等硬件下单价是四者中最高的
- **大规模时托管成本最高**——社区 1 亿向量基准中，Pinecone 每百万查询 $0.42，约为 Qdrant/Milvus/Weaviate 的 2–4 倍
- **没有 Weaviate 那种内置向量模型模块**——向量由 Pinecone 的推理服务生成（单独计费）
- **免费/Builder 档可选区域有限**（Starter 仅限 us-east-1）
- **Builder 档超额直接阻断读取**（429）而非按量计费——生产应用可能直接"答不上话"

### 2. Qdrant —— Rust 性能主力

Qdrant 用 Rust 编写，是可自托管向量数据库中公认的**性能标杆**。1.20.1（2026 年 11 月 13 日发布）刚落地，带来更快的 HNSW 图构建（PiPNN）和安全补丁；项目每 6–8 周发布一个次版本。它的差异化特性是**在高选择率（过滤掉 99% 向量）下依然快速的 payload 过滤**、完整的量化套件（标量、乘积、二进制、1-bit）以及基于 payload 的内置多租户——数千个租户共用一个索引也便宜。Qdrant Cloud 免费档（0.5 vCPU / 1 GB 内存 / 4 GB 磁盘）大约能撑住 768 维的 100 万向量；付费集群按 vCPU/内存/磁盘小时计费，官方不公布单价（需用计算器估算）。

**典型场景：** 过滤 + 召回 + 延迟都必须收紧的自托管或混合部署、多租户 SaaS 平台、今天想在 Docker 里跑 Apache-2.0 内核、将来升级到托管服务的团队。

#### 优点
- **完整数据库中延迟–吞吐平衡最佳**——独立学术研究（arXiv 2608.12812）测得 Qdrant 中位延迟最低（SIFT1M 上 4.55 ms P50），单线程 QPS 最高（216）
- **开源 + 托管同一套内核**——Apache-2.0 跑 Docker，或花钱让 Qdrant Cloud 替你跑
- **过滤性能最强**——即使排除 99% 的向量，payload 过滤依然很快
- **内置多租户**——一个索引、多租户、每租户独立分片
- **云版支持 GPU 加速索引**（AWS）
- **发布勤快**——截至 2026 年 11 月，近 90 天 4 个版本；~35.4K Star

#### 缺点
- **云定价不透明**——无公开的每 vCPU/每 GB 单价，预算只能靠计算器，不如包月对手好估
- **没有 Weaviate 那种 50+ 个内置向量化模块**——向量要自己算
- **免费集群闲置 1 周自动挂起**、4 周删除
- **没有像 Pinecone/Weaviate 那样的 HIPAA/合规档位**
- **高维时内存占用可观**——按 Qdrant 自己的计算器，1536 维不量化时约 9.2 GiB/百万向量

### 3. Weaviate —— AI 模块丰富的通才

Weaviate（当前线为 1.40，最新补丁 1.40.4）是四者中最"AI 原生"的：内置 **50+ 个向量化模块**（OpenAI、Cohere、Google、Voyage、Hugging Face 等）、BM25 + 向量的混合搜索（融合排序）、查询时生成式搜索（LLM 一步），以及**一等公民多租户**——每个 tenant 独占一个 shard，可动态启停。1.32–1.40 的发布线大幅压缩内存：HNSW 连接压缩、旋转量化（RQ-1/4/8）、shard 副本迁移。Weaviate Cloud 在 2026 年 9 月修订了价格表（新增 RQ-4 计价、修正备份费率）：Flex 从 $45/月起，Premium 共享档约 $400/月起，独占档走销售、最高 99.95% SLA 并支持 HIPAA。

**典型场景：** 想让数据库顺带完成 embedding 与 rerank 的团队、需要按客户隔离知识库的多租户 SaaS、在意 GraphQL 风格 API 和知识图谱交叉引用的项目。

#### 优点
- **默认配置召回率最佳**——独立 arXiv 研究中，SIFT1M 上默认设置即 >99% recall@K，为所有被测数据库最高
- **内置 AI 工具链最丰富**——向量化、重排、生成式搜索都是一等模块，不是外挂
- **多租户机制独有**——每租户一个 shard、动态启停，四者中独一无二
- **托管定价最可预测**——按维度 + 按 GiB 计价，Flex 档 $45 保底清晰
- **BSD-3 协议**——四者中最宽松，无专利授予歧义
- **HNSW 快照 + RQ 压缩**——存量数据无需重建索引即可显著降内存

#### 缺点
- **单线程延迟高于 Qdrant/Milvus 之外**——同研究中 ~87–88 QPS，对比 Qdrant 的 216（召回与速度互有取舍）
- **运维包袱偏重**——Go + gRPC 集群；从 1.27 到 1.40 的升级会弃用旧客户端，必须跟进版本
- **开源双雄中 Star 数最低**——~16.9K，对比 Qdrant ~35.4K、Milvus ~46.6K
- **免费档偏紧**（10 万对象、1 个集合）——原型期很容易超
- **Premium 独占档价格不公开**——需走销售

### 4. Milvus —— 分布式规模之王

Milvus 是本对比中 Star 数最高的项目（~46.6K），也是四者中**唯一从第一天就为十亿级向量设计**的：全分布式架构、存算分离、分层存储（热数据在内存、冷数据在对象存储）、DiskANN 磁盘索引和 GPU 索引。3.0.0（2026 年 7 月 29 日）新增**外部集合**——对 lakehouse 文件（Parquet）原地建索引，并支持在线增删 schema 列。自 2.5 起原生支持全文搜索（BM25 转稀疏向量）。托管路径是 Zilliz Cloud：免费档 5 GB + 250 万 vCU，Serverless $4/百万 vCU、存储 $0.04/GB/月（2026 年 1 月统一降价 87%），Dedicated 集群 Enterprise 档约 $197/月起。

**典型场景：** 大规模生产级检索（十亿级向量）、多模态搜索、希望把向量搜索嵌进现有对象存储架构的数据工程团队。

#### 优点
- **大规模经过验证**——四者中唯一有 1 亿–10 亿+ 向量公开战绩的引擎（如 Zilliz 的 VectorDBBench XLarge 用例）
- **大规模时每查询成本最低之一**——$0.04/GB/月存储 + $4/百万 vCU 计算，大而不常查的索引成本极低；社区 1 亿基准中 Milvus 为 $0.21/百万查询
- **存算分离 + 分层存储**——冷数据放 S3 类对象存储并按其计价
- **lakehouse 集成（3.0）**——对象存储里的 Parquet 原地建索引，无需拷贝
- **索引菜单最全**——HNSW、IVF、DiskANN、GPU 索引、稀疏（BM25）
- **项目活跃**——3.0 于 2026 年 7 月发布；~46.6K Star

#### 缺点
- **自托管最难**——6+ 个微服务（proxy、query node、index node、etcd、MinIO、Pulsar/Kafka），没有 Qdrant/Weaviate 那种"Docker 一条命令"的体验
- **无内置向量模块**——embedding 管线要自己搭
- **运维人才池较小**——熟悉 Milvus 内部机制的工程师少于 Postgres 或 Qdrant
- **托管入门（Enterprise $197/月起）高于 Qdrant/Weaviate 入门价**（中等规模工作负载时）
- **社区基准中召回/吞吐均衡不是最佳**——1 亿测试中 0.988 召回 @ 4,600 QPS，QPS 低于 Weaviate，召回低于 Qdrant

## 价格对比

四者都有实质性的免费档；但托管付费档的计费维度完全不同，预算差异也在这里拉开。

| 成本项 | Pinecone | Qdrant Cloud | Weaviate Cloud | Zilliz Cloud（Milvus） |
|--------|----------|--------------|----------------|--------------------------|
| **免费档** | 2 GB、100 万读单元、AWS us-east-1 | 0.5 vCPU / 1 GB 内存 / 4 GB 磁盘（~768 维 100 万向量） | 10 万对象、1 GB 内存、10 GB 磁盘 | 5 GB 存储、250 万 vCU、5 个集合 |
| **付费入门** | Builder $20/月固定（硬性配额） | ~$26/月（最小 Standard 集群） | Flex 从 $45/月起 | $4/百万 vCU，无最低消费 |
| **中型生产** | Standard 最低 $50/月起 | $68–103/月（1–3 节点、~50–100 万向量） | Flex/Premium 共享约 $400/月起 | Enterprise 约 $197/月起（Dedicated） |
| **顶级** | Enterprise 最低 $500/月起、99.95% SLA | Premium，最低消费，最高 99.95% 多 AZ | Premium 独占，99.95%、HIPAA | Business Critical / BYOC（走销售） |
| **存储费率** | $0.33/GB/月 | 按小时（随 vCPU/内存/磁盘） | 从 $0.12/GiB（Flex） | **$0.04/GB/月**（AWS/Azure/GCP 统一） |
| **读/查询计费** | $16–18/百万读单元 | 含在集群费用中 | 含（按维度 + 存储模型） | 每次查询负载 6+ vCU |
| **写计费** | $4–4.5/百万写单元 | 含在集群费用中 | 含 | 每 KB 插入 0.25 vCU |
| **出口流量** | 含 100 GB，超出 $0.10/GB | n/a | 免费（促销期） | n/a |
| **HIPAA** | $190/月附加（Standard）/ Enterprise 含 | ❌ | ✅（独占部署） | ❌ |
| **自托管成本** | ❌ 不可行 | $0（Apache-2.0）+ 自有基础设施 | $0（BSD-3）+ 自有基础设施 | $0（Apache-2.0）+ 基础设施 + 运维人力 |

**成本直觉：** 读重的 RAG 应用每月约 1 亿次查询时，Pinecone 单读单元账单（$160–180）就可能超过 Qdrant/Weaviate 整个集群的费用；写多、查少的大型索引，Zilliz Cloud 的计费结构（按 KB 计写、空闲计算免费）在结构上最便宜；自托管 Qdrant 的边际成本最低，但运维人力才是真正的开销。

## 性能基准

三个公开来源，覆盖范围各不相同。所有数据均为方向性参考而非绝对结论——硬件、量化设置和工作负载组合对结果的影响最大。

### 社区基准：1 亿向量、1536 维、HNSW

来自 2026 年社区基准（jhondados/vector-database-benchmark），四家托管服务使用相同数据规模：

| 数据库 | Recall@10 | QPS | P99 延迟 | 每百万查询成本 |
|--------|-----------|-----|----------|----------------|
| **Qdrant** | **0.991** | 4,200 | 12 ms | **$0.18** |
| Weaviate | 0.989 | **5,100** | **9 ms** | $0.24 |
| Milvus | 0.988 | 4,600 | 11 ms | $0.21 |
| Pinecone | 0.985 | 3,800 | 14 ms | $0.42 |

解读：召回差距很小（<0.7%）；**Qdrant 每查询成本最低**，Weaviate P99 最快，Pinecone 最贵；不在本阵容中的 pgvector 以 $0.08 依然便宜得多。

### 独立学术研究（arXiv 2608.12812）

2026 年 7 月的一项研究对七个系统（FAISS、Qdrant、Milvus、Weaviate、Chroma、pgvector、LanceDB）在六个数据集（最多 400 万向量）上测了 15 项质量/延迟/吞吐/资源指标。单线程 SIFT1M 结果：

| 系统 | SIFT1M QPS（单线程） | 亮点 |
|------|----------------------|------|
| FAISS（进程内库） | 866 | 无数据库特性（无持久化/过滤） |
| **Qdrant** | **216** | 完整数据库中 P50 最低：4.55 ms |
| pgvector | 154 | SQL 集成、ACID |
| Chroma | 133 | 面向 RAG 原型 |
| Weaviate | ~88 | **默认召回最高（>99%）** |
| Milvus | ~87 | 高维召回最佳（GIST1M 960 维：0.971） |
| LanceDB | 53 | 建索引速度比 Weaviate 快 11 倍 |

**结论：** FAISS 裸吞吐第一，但它是库不是数据库；完整数据库中 Qdrant 速度领先、Weaviate 默认精度领先、Milvus 在高维与分布式规模上领先。没有系统在所有指标上全面胜出——研究的选型建议是"均衡生产选 Qdrant，高维/大规模选 Milvus"。

### Zilliz 的 VectorDBBench（厂商赞助，2026 年 6 月更新）

VectorDBBench 由 Zilliz（Milvus 母公司）维护——结果宜按"对厂商有利"来读。标准用例覆盖到 LAION-100M。其中 Medium 用例（Cohere，1M × 768 维，无过滤），Milvus 在 16 vCPU/64 GB + HNSW 上以 **2,098 QPS、100% 召回**得分领先同档硬件的 Pinecone 与 pgVector。自 2026 年 6 月起，该套件还纳入**全文（BM25）搜索**基准——四家数据库如今均已支持。

## 选型场景

### 🎯 选 Pinecone：
- 想要**零基础设施**、账单只有一行
- 需要 **HIPAA、私网端点或 BYOC** 但不想自己跑集群
- 读负载不重；优先上线速度而非成本

### 🎯 选 Qdrant：
- 想要**开源 + 最佳过滤 + 延迟表现**
- 运营**多租户 SaaS**，需要便宜快速的 payload 租户隔离
- 今天 Docker 自托管、将来迁托管（同一套引擎）

### 🎯 选 Weaviate：
- 想让数据库**顺带做 embedding、重排甚至生成答案**（模块）
- 需要**按客户隔离租户**并动态启停
- **定价可预测**比极限延迟更重要

### 🎯 选 Milvus：
- 路线图上写着**数亿+ 向量**或多模态数据
- 已有**对象存储 / lakehouse**，希望原地建索引（3.0 外部集合）
- 能运行（或付费运行）**分布式系统**，想要分层存储的经济性

## 结论

| 场景 | 最佳选择 | 原因 |
|------|----------|------|
| **零运维、最快起步** | **Pinecone** 🔥 | 无需思考集群，全程无服务器 |
| **自托管默认项** | **Qdrant** 🏆 | 单二进制、Apache-2.0、完整数据库中延迟/QPS 平衡最佳 |
| **多租户 SaaS** | **Qdrant** 或 **Weaviate** | Qdrant 胜在 payload 租户速度；Weaviate 胜在 shard 租户隔离 |
| **内置向量 + 生成式搜索** | **Weaviate** | 50+ 模块、混合融合、默认召回最高 |
| **十亿级 / 多模态** | **Milvus** | 唯一可信的分布式架构 + 分层存储 |
| **lakehouse 集成** | **Milvus 3.0** | 对象存储中的 Parquet 原地建索引 |
| **又大又冷的索引最省钱** | **Zilliz Cloud** | 存储 $0.04/GB/月、空闲计算免费 |
| **HIPAA 合规搜索** | **Pinecone** 或 **Weaviate 独占** | 两者都有公开的合规路径 |
| **预算极紧、已在用 Postgres** | **pgvector**（本阵容之外） | 社区基准中 $0.08/百万查询 |

**总结：** 2026 年对大多数团队来说，实际候选是 **自托管选 Qdrant、全托管选 Pinecone**——它们夹住运维光谱的两端，而实际召回质量几乎相同（社区 1 亿向量基准中 0.985–0.991）。想让数据库兼任 embedding 与检索管线时选 **Weaviate**；路线图上的"scale"指的是**十亿向量**或**PB 级对象存储**时选 **Milvus**。

真正决定选择的往往不是数据库本身，而是你的**运维容忍度**（托管 vs 自托管）、**租户模型**（是否按客户隔离）和**计费维度**（按查询如 Pinecone、按资源如 Qdrant/Weaviate、按用量如 Zilliz）。选一个匹配你流量形状的计费维度，再用各家免费档实测验证。

## 参考资料

- Qdrant GitHub：https://github.com/qdrant/qdrant （v1.20.1，~35.4K stars，2026 年 11 月）
- Qdrant Cloud 定价：https://qdrant.tech/pricing
- Qdrant Cloud 免费/标准档说明：https://qdrant.tech/documentation/cloud/create-cluster
- Weaviate GitHub：https://github.com/weaviate/weaviate （v1.40.4，~16.9K stars，2026 年 11 月）
- Weaviate 版本说明：https://docs.weaviate.io/weaviate/release-notes
- Weaviate Cloud 定价（2026 年 9 月更新）：https://weaviate.io/pricing
- Milvus GitHub：https://github.com/milvus-io/milvus （3.0.0，~46.6K stars，2026 年 11 月）
- Zilliz Cloud 定价：https://zilliz.com/pricing
- Pinecone 定价与成本模型：https://www.pinecone.io/pricing、https://docs.pinecone.io/guides/cost/understand-cost
- VectorDBBench（Zilliz，含 2026 年 6 月全文搜索更新）：https://github.com/zilliztech/VectorDBBench
- 社区 1 亿向量基准：https://github.com/jhondados/vector-database-benchmark
- 学术 ANN 基准研究：https://arxiv.org/abs/2608.12812

---

*最后更新：2026年11月17日*
