# Lab 20: Hệ Thống Nghiên Cứu Đa Tác Nhân

Repo này là bài lab về **Multi-Agent Systems**. Mục tiêu là xây dựng một hệ thống nghiên cứu gồm **Supervisor + Researcher + Analyst + Writer**, có trace, có analysis, và có báo cáo benchmark.

Phiên bản hiện tại đã được hoàn thiện để chạy offline: không cần API key, không cần gọi LLM thật, nhưng vẫn giữ cấu trúc production để sau này có thể thay bằng OpenAI, Tavily, LangSmith hoặc provider khác.

## Kết Quả Học Tập

Sau bài lab, bạn có thể:

1. Thiết kế vai trò rõ ràng cho nhiều agent.
2. Xây dựng shared state đủ thông tin cho quá trình handoff.
3. Thêm guardrail: giới hạn vòng lặp, timeout, fallback và validation.
4. Trace được luồng chạy và giải thích agent nào làm gì.
5. Benchmark single-agent và multi-agent theo latency, cost và quality.

## Kiến Trúc

```text
User Query
   |
   v
Supervisor / Router
   |------> Researcher Agent  -> research_notes
   |------> Analyst Agent     -> analysis_notes
   |------> Writer Agent      -> final_answer
   |
   v
Trace + Báo Cáo Benchmark
```

## Cấu Trúc Repo

```text
.
├── src/multi_agent_research_lab/
│   ├── agents/              # Các agent
│   ├── core/                # Config, state, schema, error
│   ├── graph/               # Workflow điều phối nhiều agent
│   ├── services/            # LLM, search, storage client
│   ├── evaluation/          # Benchmark và report
│   ├── observability/       # Logging và tracing
│   └── cli.py               # CLI entrypoint
├── configs/                 # Cấu hình YAML
├── docs/                    # Hướng dẫn lab, rubric, thiết kế
├── tests/                   # Unit tests
├── notebooks/               # Notebook demo tùy chọn
├── scripts/                 # Script hỗ trợ
├── reports/                 # Báo cáo benchmark
├── pyproject.toml           # Cấu hình project Python
├── Dockerfile
└── Makefile
```

## Cách Chạy Nhanh

### 1. Cài dependency

```powershell
pip install -e ".[dev]"
```

Nếu chỉ muốn chạy trực tiếp trong repo mà chưa cài package:

```powershell
$env:PYTHONPATH="src"
```

### 2. Chạy test

```powershell
pytest
```

Nếu máy bị lỗi quyền ghi `.pytest_cache`, dùng:

```powershell
pytest -o cache_dir=$env:TEMP\pytest_cache
```

### 3. Chạy baseline single-agent

```powershell
python -m multi_agent_research_lab.cli baseline --query "Research GraphRAG state-of-the-art"
```

### 4. Chạy multi-agent workflow

```powershell
python -m multi_agent_research_lab.cli multi-agent --query "Research GraphRAG state-of-the-art"
```

Lệnh này sẽ:

- In toàn bộ `ResearchState` ra terminal.
- Tạo file `reports/benchmark_report.md`.
- Ghi rõ `Câu Trả Lời Cuối Cùng`, `Phân Tích`, `Trace`, `Lịch Sử Route`, `Nguồn`, `Chỉ Số` và `Lỗi Tiềm Ẩn Và Cách Khắc Phục`.

## Các Thành Phần Đã Triển Khai

| Thành phần | Mô tả |
|---|---|
| Supervisor | Chọn route tiếp theo dựa trên state |
| Researcher | Thu thập source mock local và tạo research notes |
| Analyst | Tạo analysis notes gồm key claims, risks và khuyến nghị đánh giá |
| Writer | Tổng hợp research + analysis thành final answer |
| SearchClient | Mock search deterministic để chạy offline |
| LLMClient | Mock completion deterministic để chạy offline |
| Benchmark | Đo latency, cost giả lập, quality score và lỗi |
| Report | Sinh markdown report có analysis và trace |

## Guardrail

- `MAX_ITERATIONS`: mặc định 6, tránh agent loop vô hạn.
- `TIMEOUT_SECONDS`: dành cho tích hợp provider thật.
- Pydantic schema dùng để validate input/output chính.
- Local fallback giúp demo ổn định khi không có API key.

## Deliverables

Khi nộp bài, cần có:

1. Repo GitHub cá nhân.
2. Screenshot trace hoặc file trace/report.
3. `reports/benchmark_report.md`.
4. Giải thích một failure mode và cách khắc phục.

## Ghi Chú

Phiên bản này dùng mock LLM/search nên kết quả không đại diện cho chất lượng nghiên cứu thật. Khi triển khai production, thay `LLMClient` và `SearchClient` bằng provider thật.
