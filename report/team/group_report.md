# Báo cáo nhóm

Báo cáo ngắn, tối đa 2 trang. Số liệu chi tiết nằm trong các file hồ sơ; ở đây chỉ dẫn lại con số chính.

## 1. Thông tin nhóm

- Tên nhóm: CTY1TV (làm đơn)
- Lớp: L3B
- Thành viên: xem [TEAM.md](../../TEAM.md)

## 2. Mục tiêu và cách tiếp cận

Dựng bộ hồ sơ launch v0 cho trợ lý hoàn phí LogiX-VN từ dữ liệu giả lập chạy thử (1.200 yêu cầu, 1.624 lần chạy) nhằm trả lời bốn câu hỏi trước cổng **Gate 2a**: chi phí thật mỗi việc thành công, mức độ sử dụng và bộ event cần ghi, phân loại và khắc phục lỗi, cùng thiết kế pilot tách được tác động.

## 3. Giải pháp

- **Nhiệm vụ A & B (Mô hình chi phí & độ nhạy):** Triển khai `mo_hinh`, tính chi phí toàn mẫu, tách theo 4 loại `loai`, cộng chi phí cố định 40 triệu đ/tháng, chạy 9 kịch bản độ nhạy và kịch bản xem lại 100% trong [lab13.py](../../src/lab13.py) và [bang_chi_phi.md](bang_chi_phi.md).
- **Nhiệm vụ C (Bảng lỗi & khắc phục):** Thực hiện 2 lượt gắn nhãn độc lập theo nguyên nhân gốc trên 20 ca Google PAIR và lập bảng khắc phục cho 5 ca đại diện đủ 5 loại trong [bang_loi.md](bang_loi.md).
- **Nhiệm vụ D (Kế hoạch pilot):** Tính cỡ mẫu theo cụm và chọn phương án chia 20+20 nhân viên trong [lab13.py](../../src/lab13.py) và [pilot_plan.yaml](pilot_plan.yaml).
- **Nhiệm vụ E (Chỉ số, rủi ro & hồ sơ v0):** Đặc tả 5 chỉ số, 11 event có `trace_id`, 3 rủi ro kinh tế trong [chi_so.md](chi_so.md) và tổng hợp thành hồ sơ một trang trong [ho_so_launch_v0.md](ho_so_launch_v0.md).

## 4. Kết quả

- **Kinh tế đơn vị:** Chi phí mỗi việc thành công toàn mẫu là **4.472 đ** (`simulated`, gấp 16,3× hoá đơn token + tool/yêu cầu), chi phí cả hệ thống là **5.865 đ/yêu cầu = 0,49×** (`simulated`). Thu hẹp phạm vi pilot về `noi_dia` (0,22×) + `hang_nang` (0,69× `simulated`), loại `quoc_te` (1,88×) và `doi_tac` (0,85×); cộng cố định 40 triệu đ/tháng cho **4.599 đ = 0,38×** ở 45.000 yc/tháng (`simulated`). Giới hạn **2 lần chạy** tối ưu chi phí cả hệ thống (**6.901.220 đ** `simulated`).
- **Rủi ro & sử dụng:** Ba yếu tố nhạy nhất là làm lại (+51,8%), xem lại (+40,7%) và lương (+23,1% `simulated`); xem lại 100% triệt tiêu tiết kiệm (**0,98×–1,03×** `simulated`). Đợt chạy thử (chưa có đối chứng) đạt chỉ số chính **82,83%**, bỏ qua gợi ý **27,12%**, mở lại 7 ngày **4,25%** (phạm vi 3,97%).
- **Thiết kế pilot & đề xuất:** Chia cụm **20+20 nhân viên**, chấp nhận **MDE = 6 điểm** (`n = 859`, `m >= 299`, `DE = 6,96`; `power = 0,64` nếu chênh thật 5 điểm), 3 luật dừng 4 vế. Đề xuất cuối trong [ho_so_launch_v0.md](ho_so_launch_v0.md): **Go có điều kiện**.
- **Kết quả duyệt chéo:** *(chờ cập nhật sau phiên duyệt chéo Gate 2a tại lớp trong [phieu_cham.md](phieu_cham.md))*.

## 5. Khó khăn và cách xử lý

- Với 40 nhân viên hiện có, chia cụm không đủ 1.251 mẫu cho MDE 5 điểm (tối đa < 1.000) nên phải chấp nhận MDE 6 điểm (`power = 0,64` ở mức 5 điểm) và ghi nhận điều kiện ký duyệt trước khi mở pilot.
- Thực hiện ở chế độ làm đơn 1 thành viên nên tách thành 2 lượt gắn nhãn độc lập theo 5 câu hỏi nhận diện Google PAIR ở Nhiệm vụ C để giữ tính nhất quán.

## 6. Tổng hợp đóng góp

Chi tiết đóng góp của thành viên nằm trong [TEAM.md](../../TEAM.md).

## 7. Hạn chế và hướng cải thiện

- Dữ liệu thời gian xem lại và làm lại hiện là giá trị `simulated`, cần bật đủ 11 event có `trace_id` để thay bằng thời gian đo thật sau tuần 1 của pilot.
- Cần triển khai khoá chống trùng `idempotency_key`, đối soát sổ cái mỗi giờ và lộ trình giảm xem lại theo bậc trước khi tăng tỉ lệ rollout.

## 8. Tài liệu tham khảo

- Erol và cộng sự, *Cost-of-Pass: An Economic Framework for Evaluating Language Models*, [arxiv.org/abs/2504.13359](https://arxiv.org/abs/2504.13359)
- Google PAIR, *People + AI Guidebook*, chương "Errors + Graceful Failure", [pair.withgoogle.com](https://pair.withgoogle.com)
- Tài liệu `statsmodels`, lớp `NormalIndPower` (`statsmodels.stats.power`)
