# Đặc tả chỉ số, event và rủi ro kinh tế · Nhiệm vụ E1, E2

## E1 · Đặc tả chỉ số

| Loại | Chỉ số | Công thức | Tính thử trên 1.200 yêu cầu |
| --- | --- | --- | --- |
| Chính (kết quả) | % yêu cầu đóng trong 24 giờ và không mở lại trong 7 ngày | `dong_trong_24h` bằng 1 và `mo_lai_trong_7_ngay` bằng 0, chia tổng số yêu cầu | 82,83% (994/1.200) |
| Dùng | Tỉ lệ bỏ qua gợi ý | `quyet_dinh_xem_lai` là `sua` hoặc `bo`, chia số yêu cầu được xem lại | 27,12% (48/177) |
| An toàn | Tỉ lệ lỗi lọt đến khách | `mo_lai_trong_7_ngay` bằng 1, chia tổng số yêu cầu | 4,25% (51/1.200) |
| Dùng | Nhóm tự đề xuất: % yêu cầu nhóm can thiệp (`noi_dia` + `hang_nang`) được mở bằng trợ lý | Số `request_id` duy nhất có `agent_suggestion_shown` chia tổng `refund_request_created` thuộc nhóm can thiệp | Không cần tính |
| An toàn | Nhóm tự đề xuất: % đơn hoàn sai tiền qua kiểm tra mẫu hằng tuần (bắt lỗi ngầm Ca 5, 17) | Số `audit_sample_checked` có `so_tien_da_hoan != so_tien_dung` chia tổng số đơn được kiểm tra mẫu (100 đơn/tuần) | Không cần tính |

Chỉ số trong đợt chạy thử là **82,83%** (không viết "trợ lý đã nâng chỉ số từ 0,70" vì đợt chạy thử không có nhóm đối chứng).

## Danh sách event

Mười một event có `trace_id` để nối với trace của agent, phục vụ đủ 5 chỉ số E1, tính chi phí thật và đối soát lỗi hệ thống (Ca 7, 20):

| Event | Ai tạo | Thuộc tính chính | Thời điểm |
| --- | --- | --- | --- |
| `refund_request_created` | App khách | `request_id`, `loai`, `so_tien_vnd`, `staff_id`, `arm`, `trace_id` | Khi khách gửi yêu cầu hoàn phí |
| `agent_run_completed` | Agent | `attempt`, `tokens_in`, `tokens_out`, `tool_calls`, `status`, `pricing_version`, `trace_id` | Sau mỗi lần chạy, kể cả khi lỗi |
| `agent_suggestion_shown` | Giao diện CSKH | `staff_id`, `so_tien_de_xuat`, `trace_id` | Khi gợi ý hiện ra trên màn hình nhân viên |
| `staff_review_decision` | Nhân viên CSKH | `staff_id`, `quyet_dinh` (`giu`/`sua`/`bo`), `phut_xem_lai`, `trace_id` | Khi nhân viên bấm gửi, sửa hoặc bỏ gợi ý |
| `staff_rework_completed` | Nhân viên CSKH | `staff_id`, `phut_lam_lai`, `ly_do`, `trace_id` | Khi nhân viên xử lý xong ca `lam_lai` |
| `refund_ledger_write` | Dịch vụ sổ cái | `idempotency_key`, `so_tien_vnd`, `status` (`ok`/`loi`), `trace_id` | Khi ghi bút toán hoàn tiền vào sổ cái |
| `refund_confirmation_sent` | Dịch vụ thông báo | `kenh`, `noi_dung_tom_tat`, `trace_id` | Khi gửi thông báo kết quả hoàn tiền cho khách |
| `handoff_to_staff` | Agent | `reason`, `tom_tat`, `loai`, `trace_id` | Khi hết giới hạn chạy hoặc ngoài phạm vi |
| `ticket_closed` | Hệ thống ticket | `closed_at`, `dong_trong_24h`, `trace_id` | Khi đóng yêu cầu hoàn phí |
| `ticket_reopened` | Khách hàng | `reopened_at`, `reason`, `mo_lai_trong_7_ngay`, `trace_id` | Khi khách mở lại yêu cầu trong 7 ngày |
| `audit_sample_checked` | Kế toán | `so_tien_da_hoan`, `so_tien_dung`, `pricing_version`, `trace_id` | Kiểm tra mẫu 100 đơn hằng tuần |

**Kiểm tra chéo:** mọi chỉ số đều đo được từ các event trên:
- Chỉ số chính (`82,83%` trong chạy thử): tính từ `refund_request_created`, `ticket_closed` (`dong_trong_24h`) và `ticket_reopened` (`mo_lai_trong_7_ngay`).
- Chỉ số dùng (bỏ qua gợi ý `27,12%` và tỉ lệ mở bằng trợ lý): tính từ `refund_request_created`, `agent_suggestion_shown` và `staff_review_decision`.
- Chỉ số an toàn (mở lại 7 ngày `4,25%` và % sai tiền qua kiểm tra mẫu): tính từ `refund_request_created`, `ticket_reopened` và `audit_sample_checked`.
- Chi phí thật & đối soát Ca 7, Ca 20: tính chi phí thật từ `agent_run_completed`, `staff_review_decision` (`phut_xem_lai`), `staff_rework_completed` (`phut_lam_lai`); đối soát Ca 7/20 từ `refund_confirmation_sent` và `refund_ledger_write`.

## E2 · Rủi ro kinh tế

Số liệu lấy trực tiếp từ bảng độ nhạy và kịch bản B4 trong `report/team/bang_chi_phi.md` (các con số tính từ cột `_simulated` được gắn nhãn `simulated`):

| Rủi ro | Tác động đã tính | Dấu hiệu theo dõi | Hành động | Người phụ trách |
| --- | --- | --- | --- | --- |
| Số ca làm lại tăng gấp đôi | CPS tăng **+51,8%**, từ 4.472 đ lên **6.787 đ** (`simulated`) | Tỉ lệ `lam_lai` theo tuần > 7% (nền phạm vi `noi_dia` + `hang_nang` là 4,89%) | Thu hẹp phạm vi về `noi_dia`, giới hạn 2 lần chạy và rà 20 trace làm lại gần nhất | PM trợ lý hoàn phí |
| Phải xem lại 100% kéo dài | CPS tăng lên **11.743 đ = 0,98×** (9 phút làm lại) hoặc **12.415 đ = 1,03×** (15,3 phút từ dữ liệu, `simulated`) | Tỉ lệ yêu cầu được xem lại > 50% cuối bước `0,25` hoặc thời gian xem lại > 5,1 phút/ca | Giảm tỉ lệ xem lại theo bậc khi `sua + bo < 15%` và tối ưu giao diện rút ngắn dưới 4,8 phút/ca | Trưởng nhóm CSKH |
| Khối lượng thấp hơn dự kiến | Cố định 40 triệu đ/tháng: +1.185 đ/việc (4.599 đ = 0,38×) ở 45.000 yc/tháng, tăng thành **+2.370 đ/việc** (5.784 đ = 0,48×) nếu còn một nửa (`simulated`) | Số việc thành công theo tuần < 50% kế hoạch quy mô | Không mở rộng pilot và rà lại hợp đồng chi phí cố định 40 triệu đ/tháng | PM trợ lý hoàn phí |
