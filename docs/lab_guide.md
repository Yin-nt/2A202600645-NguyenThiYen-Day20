# Hướng Dẫn Lab: Hệ Thống Nghiên Cứu Đa Tác Nhân

## Bối Cảnh

Bạn cần xây dựng một research assistant có thể nhận câu hỏi, thu thập bằng chứng, phân tích và viết câu trả lời cuối cùng. Lab so sánh hai cách làm:

1. **Single-agent baseline**: một agent làm toàn bộ nhiệm vụ.
2. **Multi-agent workflow**: Supervisor điều phối Researcher, Analyst và Writer.

## Quy Tắc Quan Trọng

- Mỗi agent phải có trách nhiệm rõ ràng.
- Shared state phải đủ chi tiết để debug.
- Mỗi bước cần để lại trace event hoặc agent result.
- Hệ thống phải có benchmark thay vì chỉ đánh giá output bằng cảm tính.
- Guardrail phải ngăn workflow chạy vô hạn.

## Milestone 1: Baseline

File liên quan:

- `src/multi_agent_research_lab/cli.py`
- `src/multi_agent_research_lab/services/llm_client.py`

Lệnh baseline gọi `LLMClient`. Trong phiên bản hoàn thiện này, `LLMClient` dùng fallback deterministic để chạy offline, không cần API key.

## Milestone 2: Supervisor

File liên quan:

- `src/multi_agent_research_lab/agents/supervisor.py`
- `src/multi_agent_research_lab/graph/workflow.py`

Supervisor đọc `ResearchState` để quyết định route:

- Thiếu research notes: gọi Researcher.
- Thiếu analysis notes: gọi Analyst.
- Thiếu final answer: gọi Writer.
- Đã đủ output hoặc đạt max iterations: dừng ở Done.

## Milestone 3: Worker Agents

File liên quan:

- `agents/researcher.py`
- `agents/analyst.py`
- `agents/writer.py`

Hành vi đã triển khai:

- Researcher thu thập local mock sources và tạo research notes.
- Analyst tạo key claims, risks và evaluation recommendations.
- Writer tổng hợp final answer thông qua `LLMClient`.

## Milestone 4: Trace Và Benchmark

File liên quan:

- `observability/tracing.py`
- `evaluation/benchmark.py`
- `evaluation/report.py`

Metric benchmark:

| Metric | Cách đo |
|---|---|
| Latency | Wall-clock time |
| Cost | Tổng cost metadata từ agent result |
| Quality | Điểm 0-10 dựa trên completeness và source coverage |
| Citation coverage | Số source thu thập được |
| Failure rate | Số lỗi trong state |

## Cách Kiểm Tra

Chạy test:

```powershell
pytest
```

Nếu bị lỗi quyền ghi `.pytest_cache`, chạy:

```powershell
pytest -o cache_dir=$env:TEMP\pytest_cache
```

Chạy baseline:

```powershell
$env:PYTHONPATH="src"
python -m multi_agent_research_lab.cli baseline --query "Research GraphRAG state-of-the-art"
```

Chạy multi-agent:

```powershell
$env:PYTHONPATH="src"
python -m multi_agent_research_lab.cli multi-agent --query "Research GraphRAG state-of-the-art"
```

Sau khi chạy multi-agent, xem report tại:

```text
reports/benchmark_report.md
```

Report cần có đủ `Câu Trả Lời Cuối Cùng`, `Phân Tích`, `Trace`, `Lịch Sử Route`, `Nguồn`, `Chỉ Số` và `Lỗi Tiềm Ẩn Và Cách Khắc Phục`.

## Exit Ticket

Nên dùng multi-agent khi bài toán cần nhiều vai trò tách biệt, handoff rõ ràng và trace dễ kiểm chứng. Không nên dùng multi-agent cho tác vụ đơn giản vì routing sẽ làm tăng latency và độ phức tạp.
