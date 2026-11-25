# Bảng lỗi và cách khắc phục · Nhiệm vụ C

20 ca lỗi nằm trong `docs/Ngay13_Lab13_De_bai_hoc_vien.docx`. Năm loại theo Google PAIR: **Do người dùng · Hệ thống · Ngữ cảnh · Giới hạn hệ thống · Ngầm**. Gắn nhãn theo nguyên nhân gốc, không theo chỗ cần sửa.

## Hai bộ nhãn độc lập

Người gắn nhãn 1: Cao Thanh Tùng (lượt 1 — gắn nhãn theo nguyên nhân gốc) · Người gắn nhãn 2: Cao Thanh Tùng (lượt 2 — soát độc lập theo 5 câu hỏi nhận diện Google PAIR; nhóm làm đơn CTY1TV)

| Ca | Nhãn người 1 | Nhãn người 2 | Trùng? | Nhãn thống nhất |
| --: | --- | --- | --- | --- |
| 1 | Do người dùng | Do người dùng | Có | Do người dùng |
| 2 | Hệ thống | Hệ thống | Có | Hệ thống |
| 3 | Ngữ cảnh | Ngữ cảnh | Có | Ngữ cảnh |
| 4 | Giới hạn hệ thống | Giới hạn hệ thống | Có | Giới hạn hệ thống |
| 5 | Ngầm | Ngầm | Có | Ngầm |
| 6 | Do người dùng | Do người dùng | Có | Do người dùng |
| 7 | Hệ thống | Hệ thống | Có | Hệ thống |
| 8 | Hệ thống | Hệ thống | Có | Hệ thống |
| 9 | Do người dùng | Do người dùng | Có | Do người dùng |
| 10 | Ngữ cảnh | Ngữ cảnh | Có | Ngữ cảnh |
| 11 | Giới hạn hệ thống | Giới hạn hệ thống | Có | Giới hạn hệ thống |
| 12 | Ngầm | Ngầm | Có | Ngầm |
| 13 | Giới hạn hệ thống | Giới hạn hệ thống | Có | Giới hạn hệ thống |
| 14 | Do người dùng | Do người dùng | Có | Do người dùng |
| 15 | Hệ thống | Hệ thống | Có | Hệ thống |
| 16 | Ngữ cảnh | Ngữ cảnh | Có | Ngữ cảnh |
| 17 | Ngầm | Ngầm | Có | Ngầm |
| 18 | Ngữ cảnh | Ngữ cảnh | Có | Ngữ cảnh |
| 19 | Giới hạn hệ thống | Giới hạn hệ thống | Có | Giới hạn hệ thống |
| 20 | Hệ thống | Hệ thống | Có | Hệ thống |

**Tỉ lệ đồng thuận:** 20 / 20 = 100% (làm đơn 2 lượt theo nguyên tắc nguyên nhân gốc)

## Quy tắc phân biệt cho các ca không trùng

Hai lượt gắn nhãn trùng 20/20 ca; dưới đây là 5 quy tắc phân biệt ranh giới cho các ca dễ lẫn trong quá trình rà soát và vận hành:

- **Ca 6, 9 (Do người dùng vs Hệ thống):** Gắn nhãn theo nguyên nhân gốc là khách chọn sai mục hoặc nhập sai mã; việc trợ lý chưa tự gợi ý nằm ở cột khắc phục.
- **Ca 8, 15 (Hệ thống vs Ngầm):** Lỗi đã lộ ra cho khách hoặc nhân viên xem lại bắt được (trích dẫn điều khoản không tồn tại, tính sai mức hoàn); chỉ gắn *Ngầm* khi không ai phát hiện cho tới khi kiểm tra mẫu.
- **Ca 12 (Ngầm vs Hệ thống):** Câu trả lời cuối vẫn đúng nhưng chi phí token đội gấp 3 lần suốt 3 tuần không ai hay — sai lệch chi phí âm thầm vẫn là lỗi *Ngầm*.
- **Ca 13 (Giới hạn hệ thống vs Hệ thống):** Yêu cầu ngoài phạm vi sản phẩm thuộc *Giới hạn hệ thống*, kể cả khi câu từ chối của trợ lý còn chung chung chưa nêu rõ giới hạn.
- **Ca 18 (Ngữ cảnh vs Hệ thống):** Số tiền tính đúng chính sách (15.000 đ = 50% × 30.000 đ), chỉ giả định "khách tự hiểu cách tính" không khớp hoàn cảnh thực tế.

## Bảng khắc phục cho 5 ca, mỗi loại một ca

Cách phát hiện phải đo được (event, ngưỡng, tần suất). Người phụ trách là một vai trò, không ghi "cả đội".

| Ca | Loại lỗi | Phát hiện bằng gì | Khắc phục thế nào | Ai phụ trách |
| --: | --- | --- | --- | --- |
| 9 | Do người dùng | Event `input_validation_failed` (`reason=invalid_tracking_code`, có `trace_id`); cảnh báo khi vượt 2% tổng yêu cầu/ngày | Nhận diện mã đơn sàn TMĐT để tra ngược sang mã vận đơn; nếu không tra được thì hiển thị hướng dẫn kèm ảnh mẫu | PM trợ lý hoàn phí |
| 7 | Hệ thống | Đối soát mỗi giờ giữa event `refund_confirmation_sent` và `refund_ledger_write` (`status=ok`) theo `trace_id`; ngưỡng > 0 ca/giờ | Chỉ báo "đã hoàn tiền thành công" khi sổ cái trả `ok` (kèm `idempotency_key`); lỗi 503 sau 2 lần thử thì báo "đang xử lý" và `handoff_to_staff` | Kỹ sư trưởng agent |
| 18 | Ngữ cảnh | Theo dõi hằng tuần tỉ lệ `ticket_reopened` có `reason=sai_so_tien` nhưng kiểm tra đúng chính sách; ngưỡng > 1%/tuần | Cập nhật mẫu tin nhắn luôn hiển thị rõ công thức (`30.000 đ × 50% = 15.000 đ`) và căn cứ chính sách hoàn phí | Trưởng nhóm CSKH |
| 4 | Giới hạn hệ thống | Event `handoff_to_staff` (`reason=thieu_du_lieu`, có `trace_id`) tổng hợp hằng ngày theo `loai`; cảnh báo nếu vượt 5% trong phạm vi pilot | Duy trì luồng chuyển nhân viên kèm tóm tắt thông tin và loại `quoc_te` (chi phí 1,88× tự làm) khỏi phạm vi pilot | PM trợ lý hoàn phí |
| 17 | Ngầm | Event `audit_sample_checked` kiểm tra mẫu 100 đơn/tuần so với bảng giá hiện hành; ngưỡng > 1% đơn lệch giá | Tự động xoá bộ nhớ đệm khi cập nhật bảng giá mới và ghi `pricing_version` vào mọi `trace_id` để truy vết | Kế toán trưởng |
