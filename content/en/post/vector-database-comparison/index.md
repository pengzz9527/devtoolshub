---
title: "Pinecone vs Qdrant vs Weaviate vs Milvus: Vector Database Comparison (2026)"
description: "Compare Pinecone, Qdrant, Weaviate, and Milvus for RAG and semantic search. Features, pricing, performance benchmarks, and which vector database to choose in 2026."
date: 2026-11-17
tags: ["Vector Database", "Pinecone", "Qdrant", "Weaviate", "Milvus", "RAG", "AI", "Comparison"]
categories: ["Databases"]
toc: true
---

RAG, semantic search, and recommendation systems all have the same foundation: a database that can hold millions of high-dimensional vectors and answer "what is closest to this?" in milliseconds. In 2026 the field has settled around four serious options: **Pinecone** (the managed-only pioneer), **Qdrant** (the Rust workhorse), **Weaviate** (the AI-module-rich generalist), and **Milvus** (the distributed scale king).

This comparison uses current version numbers, GitHub stars, official pricing pages, and published benchmark results to help you pick the right one.

<!--more-->

## Quick Comparison Table

| Feature | Pinecone | Qdrant | Weaviate | Milvus |
|---------|----------|--------|----------|--------|
| **Latest Version (Nov 2026)** | n/a (managed, API-first) | 1.20.1 | 1.40.4 | 3.0.0 |
| **Maintained By** | Pinecone Inc. (YC W21) | Qdrant Inc. | Weaviate Inc. | Zilliz / LF AI & Foundation |
| **Implementation** | Proprietary | Rust | Go | Go |
| **GitHub Stars** | n/a (no public core repo) | ~35.4K | ~16.9K | ~46.6K |
| **License** | Proprietary | Apache-2.0 | BSD-3-Clause | Apache-2.0 |
| **Self-Hostable** | ❌ No | ✅ Single binary / Docker | ✅ Docker / Helm | ✅ (multi-component) |
| **Index Types** | HNSW + quantization | HNSW + scalar/product/binary quantization | HNSW, flat + rotational quantization (RQ) | HNSW, IVF, DiskANN, GPU indexes |
| **Hybrid Search (keyword + vector)** | ✅ | ✅ (sparse vectors) | ✅ (built-in BM25) | ✅ (BM25 → sparse, v2.5+) |
| **Built-in Embedding / AI Modules** | ✅ (cloud inference) | ✅ (cloud inference) | ✅ (50+ vectorizer modules, generative search) | ❌ (bring your own) |
| **Multi-Tenancy** | Namespaces | Payload-based (fast, built-in) | First-class tenants (shard-per-tenant) | Databases + partitions |
| **Design Scale** | Serverless, auto-scaled | Shared-nothing clusters | Cloud-native clusters | Distributed, storage-compute separation (billion+ vectors) |
| **Uptime SLA (top tier)** | 99.95% | 99.95% (Premium, multi-AZ) | 99.95% (Premium dedicated) | 99.95% (Enterprise) |
| **HIPAA** | ✅ ($190/mo add-on, or in Enterprise) | ❌ | ✅ (dedicated) | ❌ |
| **Free Tier** | 2 GB + 1M read units/mo | 0.5 vCPU / 1 GB RAM / 4 GB disk | 100K objects, 1 GB RAM, 10 GB disk | 5 GB + 2.5M vCUs/mo |
| **Paid Entry Point** | Builder $20/mo flat | ~$26/mo (smallest Standard cluster) | Flex from $45/mo | $4/M vCUs, no minimum (storage $0.04/GB/mo) |

## Detailed Analysis

### 1. Pinecone — The Zero-Ops Managed Pioneered by YC

Pinecone built the category and remains the only one of the four that is **managed-only** — there is no open-source core to self-host. Everything runs on a serverless architecture: you push vectors, and Pinecone handles sharding, scaling, and index optimization behind the scenes. The 2026 price book (revised May–September 2026) now has four tiers: free Starter, a flat $20/mo Builder, Standard with a $50/mo minimum, and Enterprise with a $500/mo minimum. Reads cost 3–4× more than writes ($16–18 vs $4–4.50 per million units on Standard), so read-heavy workloads need careful budgeting.

**Typical Use Cases:** teams that want to skip all infrastructure, RAG products where "it just works" beats cost optimization, and companies needing HIPAA or private endpoints without running their own cluster.

#### Pros
- **True zero-ops** — no version upgrades, no scaling decisions, no index tuning; serverless architecture handles all of it
- **Fastest time-to-value** — one API key and you have a production-grade vector store
- **Mature security/compliance stack** — RBAC, SSO, BYOC, private endpoints, CMEK, HIPAA (add-on or Enterprise)
- **3-week trial with $300 credits** on Standard
- **Dedicated Read Nodes** for high-QPS read workloads
- **Import from object storage** at $0.25/GB

#### Cons
- **No self-hosting, no source code** — you cannot escape lock-in, and per-unit rates are the highest of the four for equivalent hardware
- **Highest managed cost at scale** — in a community 100M-vector benchmark, Pinecone's $0.42 per million queries was ~2–4× the cost of Qdrant, Milvus, and Weaviate
- **No built-in embedding models** in the same way Weaviate ships them; embeddings come from Pinecone's inference service (metered separately)
- **Region selection is limited on free/Builder tiers** (us-east-1 on Starter)
- **Builder plan blocks reads at quota** (429) instead of billing overages — a production app can literally stop answering

### 2. Qdrant — The Rust Performance Workhorse

Qdrant is written in Rust and is the performance reference among self-hostable vector databases. Version 1.20.1 (November 13, 2026) just landed with faster HNSW graph building (PiPNN) and security patches; the project ships minor releases every ~6–8 weeks. Its distinguishing features are **payload filtering that stays fast under high selectivity**, a full quantization suite (scalar, product, binary, 1-bit), and built-in multi-tenancy via payload so thousands of tenants share one index cheaply. The Qdrant Cloud free tier (0.5 vCPU / 1 GB RAM / 4 GB disk) is enough for ~1M vectors at 768 dimensions; paid clusters are billed hourly for vCPU/RAM/disk with no published per-unit rates (you price via their calculator).

**Typical Use Cases:** self-hosted or hybrid deployments where filtering + recall + latency must all be tight, multi-tenant SaaS platforms, and teams that want an open-source core they can run in Docker today and graduate to managed later.

#### Pros
- **Best latency–throughput balance of the full databases** — an independent academic study (arXiv 2608.12812) found Qdrant with the best median latency (4.55 ms P50 on SIFT1M) and highest single-threaded QPS (216) among full database systems
- **Open source + managed, same codebase** — run Apache-2.0 in Docker, or pay Qdrant Cloud to not run it
- **Strongest filtering performance** — payload filters remain fast even when 99% of vectors are excluded
- **Built-in multi-tenancy** — one index, many tenants, with per-tenant sharding
- **GPU-accelerated indexing** in Qdrant Cloud (AWS)
- **Honest, frequent releases** — four releases in the last 90 days as of November 2026; ~35.4K GitHub stars

#### Cons
- **Cloud pricing is opaque** — no published per-vCPU/per-GB rates; you must use the calculator, which makes budgeting harder than flat-fee rivals
- **No built-in vectorization modules** like Weaviate's 50+ embedding integrations — you compute embeddings yourself
- **Free tier auto-suspends after 1 week unused** and deletes after 4 weeks
- **No HIPAA/compliance tier** published the way Pinecone and Weaviate offer
- **Memory-hungry at very high dimensions** — RAM grows ~9.2 GiB per million 1536-dim vectors unquantized per Qdrant's own calculator

### 3. Weaviate — The AI-Module Generalist

Weaviate (v1.40 is the current line, with 1.40.4 the latest patch) is the most "AI-native" of the four: it ships **50+ vectorization modules** (OpenAI, Cohere, Google, Voyage, Hugging Face…), hybrid BM25 + vector search with fusion, generative search (an LLM step at query time), and first-class **multi-tenancy where each tenant gets its own shard** — you can enable/disable tenants dynamically. The 1.32–1.40 release line focused heavily on memory: compressed HNSW connections, rotational quantization (RQ-1/4/8), and shard-replica movement. Weaviate Cloud revised its price book in September 2026 (new RQ-4 pricing, corrected backup rates): Flex starts at $45/mo, Premium shared from ~$400/mo, dedicated via sales with up to 99.95% SLA and HIPAA.

**Typical Use Cases:** teams that want the database to also do embeddings and reranking, multi-tenant SaaS search (e.g. per-customer knowledge bases), and projects where a GraphQL-style API and knowledge-graph cross-references matter.

#### Pros
- **Best out-of-the-box recall** — the independent arXiv study measured >99% recall@K on SIFT1M with default settings, highest of all databases tested
- **Richest built-in AI tooling** — vectorizers, rerankers, and generative search are first-class modules, not sidecars
- **First-class multi-tenancy** — shard-per-tenant with dynamic activation is unique among the four
- **Pricing is the most predictable managed model** — per-dimension + per-GiB rates, with a hard $45 floor on Flex
- **BSD-3 license** — the most permissive of the four, no patent-grant ambiguity
- **HNSW snapshotting + RQ compression** cut memory costs substantially on existing data without reindexing

#### Cons
- **Highest single-threaded latency of the "big three" OSS engines** — ~87–88 QPS vs Qdrant's 216 on the same study's SIFT1M run (recall trades off against speed)
- **Heavier operational footprint** — Go + gRPC cluster; upgrades across 1.27→1.40 dropped older clients, so you must track releases
- **Lowest GitHub traction of the OSS pair** — ~16.9K stars vs Qdrant's ~35.4K and Milvus's ~46.6K
- **Free tier is tight** (100K objects, 1 collection) — prototyping outgrows it quickly
- **Premium dedicated pricing is sales-gated** — no public number

### 4. Milvus — The Distributed Scale King

Milvus is the most-starred project in this comparison (~46.6K) and the only one architected for **billion-vector scale from day one**: a fully distributed system with storage-compute separation, tiered storage (hot data in memory, cold in object storage), DiskANN for disk-based search, and GPU indexes. Version 3.0.0 (July 29, 2026) added **external collections** that index lakehouse files (Parquet) in place, plus online schema column add/drop. Since 2.5, Milvus has native full-text search (BM25 converted to sparse vectors). The managed path is Zilliz Cloud: free tier with 5 GB + 2.5M vCUs, serverless at $4 per million vCUs and $0.04/GB/mo storage (an 87% storage-price cut standardized in January 2026), and dedicated clusters from ~$197/mo on the Enterprise plan.

**Typical Use Cases:** large-scale production retrieval (billions of vectors), multimodal search, lakehouse-integrated analytics, and data-engineering teams that want vector search inside an existing object-storage architecture.

#### Pros
- **Proven at the largest scales** — the only engine with a credible public track record at 100M–10B+ vectors (e.g. Zilliz's VectorDBBench XLarge case)
- **Best price-per-query at scale** — $0.04/GB/mo storage + $4/M vCU compute means a big, quiet index costs pennies; in the community 100M benchmark Milvus hit $0.21/M queries
- **Storage-compute separation + tiered storage** — keep cold data on S3-class storage and pay for it accordingly
- **Lakehouse integration (3.0)** — index Parquet in object storage without copying data in
- **Broadest index menu** — HNSW, IVF, DiskANN, GPU index, sparse (BM25)
- **Active project** — 3.0 shipped in July 2026; ~46.6K stars

#### Cons
- **Hardest to self-host** — six+ microservices (proxy, query node, index node, etcd, MinIO, Pulsar/Kafka); a "Docker run" story like Qdrant/Weaviate is not realistic
- **No built-in embedding modules** — you bring your own vectorizer pipeline
- **Smaller ops talent pool** — fewer engineers know Milvus internals than Postgres or Qdrant
- **Managed entry (Enterprise $197/mo dedicated) is pricier than Qdrant/Weaviate entry points** for mid-size workloads
- **Community benchmarks show strong but not best recall@QPS tradeoff** — 0.988 recall at 4,600 QPS in the 100M test, behind Weaviate on QPS and Qdrant on recall

## Pricing Comparison

All four have a meaningful free tier; the managed paid tiers bill on very different meters, which is where budgets diverge.

| Cost Factor | Pinecone | Qdrant Cloud | Weaviate Cloud | Zilliz Cloud (Milvus) |
|-------------|----------|--------------|----------------|------------------------|
| **Free Tier** | 2 GB, 1M read units, AWS us-east-1 | 0.5 vCPU / 1 GB RAM / 4 GB disk (~1M vectors @ 768d) | 100K objects, 1 GB RAM, 10 GB disk | 5 GB storage, 2.5M vCUs, 5 collections |
| **Paid Entry** | Builder $20/mo flat (hard quotas) | ~$26/mo (smallest Standard cluster) | Flex from $45/mo | $4/M vCUs, no minimum |
| **Mid-Production** | Standard from $50/mo min. | $68–103/mo (1–3 nodes, ~0.5–1M vectors) | Flex/Premium shared from ~$400/mo | Enterprise from $197/mo (dedicated) |
| **Top Tier** | Enterprise from $500/mo min., 99.95% SLA | Premium, min-spend, up to 99.95% multi-AZ | Premium dedicated, 99.95%, HIPAA | Business Critical / BYOC (sales) |
| **Storage Rate** | $0.33/GB/mo | Hourly (billed with vCPU/RAM/disk) | From $0.12/GiB (Flex) | **$0.04/GB/mo** (unified across AWS/Azure/GCP) |
| **Read/Query Meter** | $16–18 per 1M read units | Included in cluster cost | Included (per-dimension + storage model) | 6+ vCUs per query workload |
| **Write Meter** | $4–4.50 per 1M write units | Included in cluster cost | Included | 0.25 vCU/KB inserted |
| **Egress** | 100 GB incl., then $0.10/GB | n/a | Free (promo period) | n/a |
| **HIPAA** | $190/mo add-on (Standard) / incl. Enterprise | ❌ | ✅ (dedicated) | ❌ |
| **Self-Host Cost** | ❌ Not possible | $0 (Apache-2.0) + your infra | $0 (BSD-3) + your infra | $0 (Apache-2.0) + your infra + ops |

**Cost intuition:** for a read-heavy RAG app doing ~100M queries/month, Pinecone's read meter alone ($1.6–1.8M) can exceed the entire Qdrant/Weaviate cluster bill. For a write-heavy, rarely-queried index, Zilliz Cloud's metering (writes billed per KB, idle compute free) is structurally the cheapest. Self-hosted Qdrant on your own hardware has the lowest possible marginal cost but your ops time is the real expense.

## Performance Benchmarks

Three published sources, each with different scope. Treat all as directional, not absolute — hardware, quantization settings, and workload mix dominate results.

### Community Benchmark: 100M Vectors, 1536-dim, HNSW

From a 2026 community benchmark (jhondados/vector-database-benchmark), same data size across all four managed services:

| Database | Recall@10 | QPS | P99 Latency | Cost per 1M Queries |
|----------|-----------|-----|-------------|---------------------|
| **Qdrant** | **0.991** | 4,200 | 12 ms | **$0.18** |
| Weaviate | 0.989 | **5,100** | **9 ms** | $0.24 |
| Milvus | 0.988 | 4,600 | 11 ms | $0.21 |
| Pinecone | 0.985 | 3,800 | 14 ms | $0.42 |

Read it as: recall differences are small (<0.7%); **Qdrant is the best cost-per-query**, Weaviate is the fastest at P99, Pinecone is the most expensive per query, and pgvector (not in this lineup) remains the cheapest by far at $0.08.

### Independent Academic Study (arXiv 2608.12812)

A July 2026 study benchmarked seven systems (FAISS, Qdrant, Milvus, Weaviate, Chroma, pgvector, LanceDB) across six datasets up to 4M vectors, measuring 15 quality/latency/throughput/resource metrics. Single-threaded SIFT1M results:

| System | SIFT1M QPS (single-thread) | Notable |
|--------|---------------------------|---------|
| FAISS (in-process lib) | 866 | No database features (no persistence/filtering) |
| **Qdrant** | **216** | Best P50 latency of full DBs: 4.55 ms |
| pgvector | 154 | SQL-integrated, ACID |
| Chroma | 133 | RAG prototyping focus |
| Weaviate | ~88 | **Best default recall (>99%)** |
| Milvus | ~87 | Best high-dim recall (GIST1M 960-d: 0.971) |
| LanceDB | 53 | 11× faster index build than Weaviate |

**Takeaways:** FAISS wins raw throughput but is a library, not a database. Among full databases, Qdrant leads on speed, Weaviate on out-of-the-box accuracy, and Milvus on high-dimensional and distributed scale. No single system dominated every metric — the study's selection table recommends Qdrant for "balanced production" and Milvus for "high-dim / scale."

### Zilliz's VectorDBBench (vendor-sponsored, June 2026 update)

VectorDBBench (maintained by Zilliz, Milvus's company — read it as vendor-favorable) runs standardized cases up to LAION-100M. On its Medium case (Cohere, 1M × 768-d, unfiltered), Milvus on 16 vCPU/64 GB with HNSW scored **2,098 QPS at 100% recall** vs lower QPS for Pinecone and pgVector on the same hardware class. Since June 2026 the suite also benchmarks **full-text (BM25) search**, which all four databases now support.

## When to Choose Which

### 🎯 Choose Pinecone When:
- You want **zero infrastructure** and a single billable line item
- You need **HIPAA, private endpoints, or BYOC** without running your own cluster
- Your workload is read-light; your priority is speed-to-production over cost

### 🎯 Choose Qdrant When:
- You want **open source with the best filtering + latency profile**
- You run a **multi-tenant SaaS** and need cheap, fast payload-tenant isolation
- You may self-host in Docker today and move to managed cloud later (same engine)

### 🎯 Choose Weaviate When:
- You want the **database to embed, rerank, and even generate answers** (modules)
- You need **per-customer tenant isolation** with dynamic enable/disable
- **Predictable pricing** matters more than last-ms latency

### 🎯 Choose Milvus When:
- You're heading to **hundreds of millions+ of vectors** or multimodal data
- You already have **object storage / lakehouse** and want to index in place (3.0 external collections)
- You can run (or pay for) a **distributed system** and want tiered storage economics

## Verdict

| Scenario | Best Choice | Why |
|----------|------------|-----|
| **Zero-ops, fastest start** | **Pinecone** 🔥 | No cluster to think about; serverless end-to-end |
| **Self-hosted default** | **Qdrant** 🏆 | Single binary, Apache-2.0, best latency/QPS balance of full DBs |
| **Multi-tenant SaaS** | **Qdrant** or **Weaviate** | Qdrant for payload-tenant speed; Weaviate for shard-tenant isolation |
| **Built-in embeddings + generative search** | **Weaviate** | 50+ modules, hybrid fusion, best default recall |
| **Billion-scale / multimodal** | **Milvus** | Only credible distributed architecture; tiered storage |
| **Lakehouse integration** | **Milvus 3.0** | Index Parquet in object storage in place |
| **Cheapest big-and-quiet index** | **Zilliz Cloud** | $0.04/GB/mo storage, idle compute free |
| **HIPAA-compliant search** | **Pinecone** or **Weaviate dedicated** | Both offer a published compliance path |
| **Tight budget, already on Postgres** | **pgvector** (outside this lineup) | $0.08/M queries in the community benchmark |

**Bottom line:** For most teams in 2026 the practical shortlist is **Qdrant for self-hosted control and Pinecone for hands-off managed** — they bracket the ops spectrum, with the same recall quality in practice (0.985–0.991 at 100M vectors in the community benchmark). Choose **Weaviate** when you want the database to also be your embedding and retrieval pipeline, and choose **Milvus** when the word "scale" in your roadmap means *billions of vectors* or *petabytes of object storage*.

The real decision variable is rarely the database itself: it's your **ops tolerance** (managed vs self-hosted), your **tenant model** (per-customer isolation?), and your **billing meter** (per-query like Pinecone vs per-resource like Qdrant/Weaviate vs per-usage like Zilliz). Pick the meter that matches your traffic shape, then verify with each vendor's free tier.

## Data Sources

- Qdrant GitHub: https://github.com/qdrant/qdrant (v1.20.1, ~35.4K stars, November 2026)
- Qdrant Cloud Pricing: https://qdrant.tech/pricing
- Qdrant Cloud Free/Standard tiers: https://qdrant.tech/documentation/cloud/create-cluster
- Weaviate GitHub: https://github.com/weaviate/weaviate (v1.40.4, ~16.9K stars, November 2026)
- Weaviate Release Notes: https://docs.weaviate.io/weaviate/release-notes
- Weaviate Cloud Pricing (Sept 2026 price-book update): https://weaviate.io/pricing
- Milvus GitHub: https://github.com/milvus-io/milvus (3.0.0, ~46.6K stars, November 2026)
- Zilliz Cloud Pricing: https://zilliz.com/pricing
- Pinecone Pricing & cost model: https://www.pinecone.io/pricing, https://docs.pinecone.io/guides/cost/understand-cost
- VectorDBBench (Zilliz, incl. June 2026 full-text update): https://github.com/zilliztech/VectorDBBench
- Community 100M-vector benchmark: https://github.com/jhondados/vector-database-benchmark
- Academic ANN benchmark study: https://arxiv.org/abs/2608.12812

---

*Last updated: November 17, 2026*
