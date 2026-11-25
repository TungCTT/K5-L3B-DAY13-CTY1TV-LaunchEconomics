# Hồ sơ launch v0 · Trợ lý hoàn phí LogiX-VN · Gate 2a

Một trang. Cột trạng thái chỉ nhận: **Xong, có bằng chứng · Chưa · Giả lập**. Mục nào dựa trên cột `_simulated` ghi Giả lập. Người phụ trách là một vai trò, không ghi "cả đội". Gate 2a chỉ duyệt kế hoạch pilot: không viết như thể trợ lý đã được duyệt chạy chính thức (xem quy tắc 5 trong `README.md`).

Nhóm: CTY1TV (làm đơn) · Lớp: L3B

| Mục | Con số chính | Trạng thái | Người phụ trách |
| --- | --- | --- | --- |
| 1 · Chi phí mỗi việc thành công | Toàn mẫu **4.472 đ** (`simulated`, gấp 16,3× hoá đơn 274,7 đ); phạm vi `noi_dia + hang_nang` là **3.414 đ** biến đổi, cộng cố định 40 triệu/tháng thành **4.599 đ** (45k yc/tháng) hoặc **5.784 đ** (nửa khối lượng, `simulated`) | Giả lập | PM trợ lý hoàn phí |
| 2 · Ba yếu tố nhạy nhất | **1. Số ca làm lại (+51,8%) · 2. Tỉ lệ xem lại (+40,7%) · 3. Lương nhân viên (+23,1%)** (`simulated`); giá token gấp đôi chỉ tăng +5,6% | Giả lập | PM trợ lý hoàn phí |
| 3 · So với nhân viên tự làm | Cả hệ thống toàn mẫu **5.865 đ/yc = 0,49×**; phạm vi `noi_dia` **0,22×**, `hang_nang` **0,69×** (cộng cố định **0,38×–0,48×**); loại `quoc_te` lỗ (**1,88×**, thành công 27,3%) và `doi_tac` (**0,85×**); bất lợi: xem lại 100% lên **0,98×–1,03×** (`simulated`) | Giả lập | Giám đốc vận hành LogiX-VN |
| 4 · Chỉ số chính, chỉ số dùng, chỉ số an toàn | Đợt chạy thử (chưa có đối chứng): chính **82,83%** (994/1.200), bỏ qua gợi ý **27,12%** (48/177), mở lại 7 ngày **4,25%** (phạm vi 3,97%); đề xuất thêm 2 chỉ số và 11 event có `trace_id` | Xong, có bằng chứng | Trưởng nhóm CSKH |
| 5 · Bảng lỗi và cách khắc phục | 20 ca theo 5 loại Google PAIR (đồng thuận 20/20 = 100%, làm đơn 2 lượt); 5 ca đại diện đủ 5 loại có event/ngưỡng phát hiện đo được (ưu tiên chặn Ca 7 sổ cái & Ca 20 hoàn trùng) | Xong, có bằng chứng | Kỹ sư trưởng agent |
| 6 · Pilot plan | Chia cụm **20+20 nhân viên** phân tầng depot, `rollout [0.10, 0.25, 0.50]`, 3 luật dừng 4 vế, rollback ≤ 30 phút, quyết định `2027-01-05`; bất lợi: nhận **MDE 6 điểm** (`n=859`, `m>=299`, `DE=6,96`), power còn **0,64** nếu chênh thật 5 điểm | Xong, có bằng chứng | Giám đốc vận hành LogiX-VN |
| 7 · Rủi ro kinh tế | 3 rủi ro định lượng (`simulated`): làm lại ×2 (+51,8%, lên 6.787 đ), xem lại 100% kéo dài (0,98×–1,03×), giảm nửa khối lượng (+2.370 đ cố định/việc); đủ ngưỡng cảnh báo và hành động | Giả lập | Kế toán trưởng |

**Đề xuất:** **Go có điều kiện** (áp dụng cho kế hoạch pilot phạm vi `noi_dia + hang_nang`, giới hạn tối đa 2 lần chạy để tối ưu chi phí cả hệ thống 6.901.220 đ `simulated`, loại `quoc_te` và `doi_tac`). Các điều kiện bắt buộc:

- Bổ sung khoá chống trùng `idempotency_key` (Ca 20) và chỉ báo "đã hoàn tiền" khi sổ cái trả `ok` kèm đối soát mỗi giờ (Ca 7) — Phụ trách: **Kỹ sư trưởng agent** — Kiểm tra: **2026-12-01** (trước khi mở pilot).
- Ký xác nhận thu hẹp phạm vi còn `noi_dia + hang_nang` và chấp nhận đánh đổi **MDE = 6 điểm** (`power = 0,64` nếu tác động thật là 5 điểm) — Phụ trách: **Giám đốc vận hành LogiX-VN** — Kiểm tra: **2026-12-01**.
- Bật đủ 11 event có `trace_id` và thay toàn bộ số phút `simulated` bằng thời gian đo thật từ `staff_review_decision` và `staff_rework_completed` — Phụ trách: **Kỹ sư trưởng agent** — Kiểm tra: **2026-12-08** (cuối tuần 1).
- Áp dụng lộ trình giảm tỉ lệ xem lại theo bậc khi `sua + bo < 15%` và rút thời gian xem lại xuống dưới `4,8 phút/ca` để tránh mất lợi ích tiết kiệm (0,98×–1,03× `simulated`) — Phụ trách: **Trưởng nhóm CSKH** — Kiểm tra: **2026-12-15** (cuối bước rollout 0,25).
