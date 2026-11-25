# Báo cáo cá nhân — CaoThanhTung-2A202603982


## 1. Thông tin thành viên

- Họ tên: Cao Thanh Tùng
- MSSV: 2A202603982
- Email: cutcutchch123@gmail.com
- Vai trong nhóm (người viết code, người kiểm số, người gắn nhãn 1, người gắn nhãn 2 kiêm giữ hồ sơ): Đảm nhiệm cả 4 vai (người viết code, người kiểm số, người gắn nhãn 1 & 2, người giữ hồ sơ — làm đơn, nhóm CTY1TV, lớp L3B)

## 2. Phần việc phụ trách

- Thực hiện đơn toàn bộ quy trình Lab 13 (CP1–CP5): cài đặt môi trường Python trong `src/.venv`, triển khai `src/lab13.py` (Nhiệm vụ A, B, D1, E1) và hoàn thiện bộ hồ sơ launch v0 tại `report/team/` cho hội đồng Gate 2a.

## 3. Đóng góp cụ thể

- **CP1 & CP2 (`src/lab13.py`, `report/team/bang_chi_phi.md`):** Hoàn thiện ba hàm A1 (`1,20` · `1,25` · `1,25`), `mo_hinh` và phân tích A2–A4, B1–B4. Xác định CPS toàn mẫu 4.472 đ (`simulated`, gấp 16,3× hoá đơn 274,7 đ), thu hẹp phạm vi về `noi_dia` (0,22×) + `hang_nang` (0,69× `simulated`), giới hạn 2 lần chạy cho chi phí cả hệ thống thấp nhất (6.901.220 đ `simulated`), và làm rõ kịch bản xem lại 100% không tiết kiệm (0,98×–1,03× `simulated`).
- **CP3 (`report/team/bang_loi.md`):** Thực hiện 2 lượt gắn nhãn độc lập theo nguyên nhân gốc cho 20 ca lỗi Google PAIR (đồng thuận 20/20 = 100%), viết 5 quy tắc phân biệt ranh giới và bảng khắc phục 5 ca đại diện đủ 5 loại có event/ngưỡng đo được và vai trò phụ trách riêng.
- **CP4 (`src/lab13.py`, `report/team/pilot_plan.yaml`):** Triển khai tính cỡ mẫu `co_mau` + `statsmodels` cho 5 câu D1, chọn chia cụm 20+20 nhân viên phân tầng theo depot, chấp nhận đánh đổi MDE 6 điểm (`n = 859`, `m >= 299`, `DE = 6,96`; ghi rõ `power = 0,64` nếu chênh thật 5 điểm) và viết 3 luật dừng đủ 4 vế `NẾU – TRONG – THÌ – KHÔNG THÌ`.
- **CP5 (`report/team/chi_so.md`, `report/team/ho_so_launch_v0.md`, `report/team/group_report.md`):** Tính thử 3 chỉ số E1 trên 1.200 yêu cầu (82,83% / 27,12% / 4,25%), đề xuất thêm 2 chỉ số, thiết kế 11 event có `trace_id`, 3 rủi ro kinh tế và tổng hợp hồ sơ 1 trang 7 mục với đề xuất **Go có điều kiện**.

## 4. Bằng chứng

- Code hoàn chỉnh chạy từ đầu đến cuối (exit code 0, A1 in `ĐẠT` và đủ bảng A2–E1): `src/lab13.py`.
- Hồ sơ nhóm đã hoàn thiện (giữ đúng tên file theo quy ước): `report/team/bang_chi_phi.md`, `report/team/bang_loi.md`, `report/team/pilot_plan.yaml`, `report/team/chi_so.md`, `report/team/ho_so_launch_v0.md`, `report/team/group_report.md`, `TEAM.md` (riêng `report/team/phieu_cham.md` đã điền tên hội đồng `CTY1TV` và giữ trống bảng chấm chờ phiên duyệt chéo tại lớp).
- Kiểm tra tự động đạt toàn bộ: `yaml.safe_load` hợp lệ, không còn dấu `?` ngoài dòng chú thích, đủ nhãn `simulated` cho các số giả lập và không xuất hiện từ cấm.

## 5. Công cụ AI đã dùng

- **Công cụ:** Trợ lý AI tích hợp trên IDE (Antigravity).
- **Mục đích sử dụng:** Giải thích khái niệm kinh tế agent và thiết kế cụm, hỗ trợ dựng môi trường `.venv`, gợi ý cài đặt hàm trong `src/lab13.py` và rà soát tính nhất quán giữa các tài liệu hồ sơ.
- **Cách tự kiểm tra:** Chạy trực tiếp `src/.venv/Scripts/python.exe lab13.py` kiểm tra 3 phép thử A1 đạt 100% và đối chiếu toàn bộ số A2–A4, B1–B4, D1, E1 trong sai số ≤ 2% so với công thức trong `docs/du_lieu_va_cong_thuc.md`; chạy kiểm tra `yaml.safe_load`, kiểm tra sạch dấu `?`, sạch từ cấm và tự rà lại lập luận nguyên nhân gốc cho 20 ca lỗi cùng các điều kiện Go có điều kiện.

## 6. Tự đánh giá

- Hoàn thành đầy đủ 100% nội dung kỹ thuật của 5 checkpoint (CP1–CP5) với số liệu nhất quán giữa code và toàn bộ hồ sơ.
- Các việc còn lại để hoàn tất trước deadline: ghi nhận kết quả phiên duyệt chéo tại lớp vào `report/team/phieu_cham.md` và `report/team/group_report.md`, điền mã commit chốt vào `TEAM.md`, push lên `origin main` và nộp link repo trên LMS trước 23:59 GMT+7.
