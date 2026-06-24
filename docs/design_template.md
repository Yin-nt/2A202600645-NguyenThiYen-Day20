# Mẫu Thiết Kế Hệ Thống

## Bài Toán

Xây dựng một research assistant nhận câu hỏi từ người dùng, thu thập nguồn thông tin, phân tích bằng chứng và viết câu trả lời cuối cùng. Toàn bộ quá trình cần có trace để giải thích từng bước trung gian.

## Vì Sao Dùng Multi-Agent?

Một single-agent có thể trả lời nhanh, nhưng thường trộn lẫn tìm kiếm, phân tích và viết trong một bước khó kiểm chứng. Thiết kế multi-agent tách rõ trách nhiệm để từng handoff có thể được xem lại, đánh giá và thay thế độc lập.

## Vai Trò Agent

| Agent | Trách nhiệm | Input | Output | Failure mode |
|---|---|---|---|---|
| Supervisor | Chọn worker tiếp theo hoặc dừng workflow | `ResearchState` | Route history | Routing sai có thể gây loop hoặc bỏ qua bước |
| Researcher | Thu thập source và tạo ghi chú nghiên cứu | Query, `max_sources` | `sources`, `research_notes` | Source yếu hoặc không liên quan |
| Analyst | Chuyển research notes thành claim, risk và metric | Research notes, sources | `analysis_notes` | Phân tích quá tự tin khi bằng chứng yếu |
| Writer | Viết final answer có caveat và reference | Research notes, analysis notes | `final_answer` | Thiếu citation hoặc claim không có căn cứ |

## Shared State

`ResearchState` lưu request, số vòng lặp, route history, sources, research notes, analysis notes, final answer, agent results, trace events và errors. Đây là nguồn dữ liệu trung tâm giúp debug workflow và tính benchmark.

## Routing Policy

Supervisor chọn route theo thứ tự:

1. Nếu thiếu `research_notes`, gọi `researcher`.
2. Nếu thiếu `analysis_notes`, gọi `analyst`.
3. Nếu thiếu `final_answer`, gọi `writer`.
4. Nếu đã đủ output hoặc đạt giới hạn vòng lặp, chuyển sang `done`.

## Guardrail

- Max iterations: cấu hình bằng `MAX_ITERATIONS`, mặc định là 6.
- Timeout: cấu hình bằng `TIMEOUT_SECONDS`, dùng khi tích hợp provider thật.
- Retry: có thể thêm ở tầng client mà không cần sửa logic agent.
- Fallback: `LLMClient` và `SearchClient` local giúp lab chạy offline.
- Validation: các schema Pydantic kiểm tra input/output chính.

## Kế Hoạch Benchmark

Dùng một bộ query cố định để so sánh baseline và multi-agent theo latency, estimated cost, quality score, số source, số route decision và số lỗi. Report sinh ra cần ghi rõ analysis, trace và failure mode.
