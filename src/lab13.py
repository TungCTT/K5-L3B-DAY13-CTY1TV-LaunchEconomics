"""Lab 13 · Định giá agent và lập kế hoạch pilot (Gate 2a) — bài làm của nhóm (file nộp).
Chạy trong thư mục src/: python3 lab13.py   (cần pandas; Nhiệm vụ D cần thêm statsmodels)
Không cần khoá API. Điền các chỗ ghi VIẾT Ở ĐÂY (đánh dấu TODO CP1…CP4). Dữ liệu trong hai file CSV là giả lập.
Bản gốc chưa sửa nằm ở lab13_starter.py.
"""
import math
import sys
from statistics import NormalDist
import pandas as pd
from statsmodels.stats.proportion import proportion_effectsize
from statsmodels.stats.power import NormalIndPower

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Bảng giá GIẢ ĐỊNH của lab (không phải giá thật của nhà cung cấp nào)
GIA_VAO = 26        # đồng cho 1.000 token đầu vào
GIA_RA = 130        # đồng cho 1.000 token đầu ra
GIA_TOOL = 15       # đồng cho 1 lần gọi tool
LUONG_PHUT = 2000   # đồng cho 1 phút của nhân viên (đã gồm bảo hiểm, văn phòng)
BASELINE = 12000    # đồng cho 1 yêu cầu khi nhân viên tự làm (6 phút)


# ---------- Nhiệm vụ A1 · Kinh tế của việc chạy lại ----------
# TODO CP1: viết ba hàm dưới đây cho tới khi kiem_tra_dap_an_biet_truoc() in ĐẠT.
def so_lan_chay_ky_vong(p, k=None):
    """Số lần chạy trung bình cho 1 yêu cầu khi mỗi lần đúng với xác suất p.
    k = số lần chạy tối đa; k=None nghĩa là chạy lại đến khi đúng."""
    return 1 / p if k is None else (1 - (1 - p) ** k) / p


def ti_le_thanh_cong(p, k=None):
    """Xác suất yêu cầu thành công sau tối đa k lần chạy."""
    return 1.0 if k is None else 1 - (1 - p) ** k


def he_so_chi_phi_moi_viec_thanh_cong(p, k=None):
    """Chi phí mỗi việc thành công, tính bằng bội số của giá một lần chạy."""
    return so_lan_chay_ky_vong(p, k) / ti_le_thanh_cong(p, k)


def kiem_tra_dap_an_biet_truoc():
    """Ba phép thử bắt buộc đạt 100% trước khi tính trên dữ liệu."""
    assert abs(so_lan_chay_ky_vong(0.8, 2) - 1.20) < 1e-9, 'p=0,8, tối đa 2 lần → 1,20 lần chạy'
    assert abs(so_lan_chay_ky_vong(0.8) - 1.25) < 1e-9, 'p=0,8, chạy đến khi đúng → 1,25 lần chạy'
    assert abs(he_so_chi_phi_moi_viec_thanh_cong(0.8, 3) - 1.25) < 1e-9, 'p=0,8, tối đa 3 lần → 1,25 lần giá một lần chạy'
    print('Ba phép thử đáp án biết trước: ĐẠT')


# ---------- Nhiệm vụ A2 · Mô hình chi phí từ trace ----------
# TODO CP1: viết mo_hinh; CP2 gọi lại hàm này với tham số giá và hệ số đã đổi.
def mo_hinh(runs, reqs, gia_vao=26, gia_ra=130, gia_tool=15, luong_phut=2000,
            he_so_xem_lai=1.0, he_so_lam_lai=1.0, max_lan_chay=None):
    """Trả về dict gồm: token, tool, xem_lai, lam_lai, tong, thanh_cong, cps (chi phí mỗi việc thành công).
    - token, tool: cộng trên MỌI lần chạy trong runs, kể cả lần lỗi.
    - xem_lai, lam_lai: số phút (cột *_simulated) × LUONG_PHUT. Đây là số GIẢ LẬP, phải ghi nhãn simulated khi báo cáo.
    - thanh_cong: số yêu cầu có ket_qua == 'thanh_cong'.
    - Các tham số giá/hệ số/max_lan_chay dùng cho Nhiệm vụ B (độ nhạy, giới hạn số lần chạy); giữ mặc định ở A2.
    """
    reqs = reqs.copy()
    runs = runs[runs['request_id'].isin(reqs['request_id'])]
    if max_lan_chay is not None:
        runs = runs[runs['attempt'] <= max_lan_chay]
        vuot = reqs['so_lan_chay'] > max_lan_chay
        reqs.loc[vuot, 'ket_qua'] = 'chuyen_nhan_vien'
        reqs.loc[vuot, ['phut_xem_lai_simulated', 'phut_lam_lai_simulated']] = 0
    tien_token = runs['tokens_in'] / 1000 * gia_vao + runs['tokens_out'] / 1000 * gia_ra
    tien_tool = runs['tool_calls'] * gia_tool
    xem_lai = reqs['phut_xem_lai_simulated'].sum() * luong_phut * he_so_xem_lai
    lam_lai = reqs['phut_lam_lai_simulated'].sum() * luong_phut * he_so_lam_lai
    tong = tien_token.sum() + tien_tool.sum() + xem_lai + lam_lai
    thanh_cong = int((reqs['ket_qua'] == 'thanh_cong').sum())
    return dict(
        token=tien_token.sum(),
        tool=tien_tool.sum(),
        chay_lai=(tien_token + tien_tool)[runs['attempt'] > 1].sum(),
        xem_lai=xem_lai,
        lam_lai=lam_lai,
        tong=tong,
        thanh_cong=thanh_cong,
        cps=tong / thanh_cong,
        hoa_don_moi_yc=(tien_token.sum() + tien_tool.sum()) / len(reqs),
        khong_thanh_cong=len(reqs) - thanh_cong,
    )


def in_bao_cao_chi_phi(runs, reqs):
    """In kết quả A2, A3, A4 và B1–B4 từ dữ liệu trace."""
    a2 = mo_hinh(runs, reqs)
    print('\n=== A2 · Mô hình chi phí từ trace ===')
    for ten, gia_tri in a2.items():
        if ten == 'hoa_don_moi_yc':
            print(f'{ten:16s} {gia_tri:>14,.1f}')
        else:
            print(f'{ten:16s} {gia_tri:>14,.0f}')
    print(f"Gấp hoá đơn/yc:  {a2['cps'] / a2['hoa_don_moi_yc']:.1f} lần")
    print(f"Tỉ trọng làm lại (simulated): {a2['lam_lai'] / a2['tong'] * 100:.1f}%")
    print(f"Tỉ trọng xem lại (simulated): {a2['xem_lai'] / a2['tong'] * 100:.1f}%")
    sys_per_req = (a2['tong'] + a2['khong_thanh_cong'] * BASELINE) / len(reqs)
    print(f"Chi phí cả hệ thống/yêu cầu (simulated): {sys_per_req:,.0f} đ ({sys_per_req / BASELINE:.2f}x của {BASELINE:,} đ)")

    print('\n=== A3 · Tách theo loại yêu cầu ===')
    for loai in ['noi_dia', 'hang_nang', 'quoc_te', 'doi_tac']:
        sub = reqs[reqs['loai'] == loai]
        r = mo_hinh(runs, sub)
        tc_pct = r['thanh_cong'] / len(sub) * 100
        lan_tb = sub['so_lan_chay'].mean()
        print(f"{loai:10s} | n={len(sub):3d} | tc={tc_pct:5.1f}% | lần/yc={lan_tb:.2f} | cps(sim)={r['cps']:8,.0f} đ | vs12k={r['cps'] / BASELINE:.2f}x")

    merged = runs.merge(reqs[['request_id', 'loai']], on='request_id')
    merged['is_ok'] = (merged['status'] == 'ok').astype(int)
    pivot_ok = (merged.pivot_table(index='loai', columns='attempt', values='is_ok', aggfunc='mean') * 100).round(1)
    print('\nTỉ lệ status == ok theo loai x attempt (%):')
    print(pivot_ok.to_string())

    print('\n=== A4 · Chi phí cố định (phạm vi noi_dia + hang_nang) ===')
    chi_phi_co_dinh = 40_000_000
    scope_reqs = reqs[reqs['loai'].isin(['noi_dia', 'hang_nang'])]
    r_scope = mo_hinh(runs, scope_reqs)
    ti_le_tc_mau = r_scope['thanh_cong'] / len(reqs)
    for nhan, khoi_luong in [('45.000 yêu cầu/tháng', 45_000), ('Một nửa khối lượng (22.500)', 22_500)]:
        viec_tc_thang = khoi_luong * ti_le_tc_mau
        co_dinh_moi_viec = chi_phi_co_dinh / viec_tc_thang
        tong_cps = r_scope['cps'] + co_dinh_moi_viec
        print(f"{nhan:30s} | tc/tháng={viec_tc_thang:8,.0f} | cố định/việc={co_dinh_moi_viec:6,.0f} đ | cps+cố định(sim)={tong_cps:6,.0f} đ ({tong_cps / BASELINE:.2f}x)")

    print('\n=== B1 · Bảng độ nhạy ===')
    kich_ban = {
        'Giá token gấp đôi': dict(gia_vao=52, gia_ra=260),
        'Giá token giảm một nửa': dict(gia_vao=13, gia_ra=65),
        'Tỉ lệ xem lại gấp đôi': dict(he_so_xem_lai=2.0),
        'Tỉ lệ xem lại giảm một nửa': dict(he_so_xem_lai=0.5),
        'Số ca làm lại gấp đôi': dict(he_so_lam_lai=2.0),
        'Số ca làm lại giảm một nửa': dict(he_so_lam_lai=0.5),
        'Lương nhân viên tăng 25%': dict(luong_phut=2500),
        'Chỉ cho chạy tối đa 2 lần': dict(max_lan_chay=2),
        'Chỉ cho chạy 1 lần': dict(max_lan_chay=1),
    }
    goc = a2['cps']
    for ten, kw in kich_ban.items():
        cps = mo_hinh(runs, reqs, **kw)['cps']
        print(f"{ten:28s} | cps(sim)={cps:6,.0f} đ | {(cps / goc - 1) * 100:+6.1f}%")

    print('\n=== B2 · Đổi một cặp và xếp hạng ===')
    b2_cps = mo_hinh(runs, reqs, gia_vao=52, gia_ra=260, he_so_xem_lai=2.0)['cps']
    print(f"Token x2 + Xem lại x2: cps(sim)={b2_cps:,.0f} đ ({(b2_cps / goc - 1) * 100:+.1f}%)")

    print('\n=== B3 · Giới hạn chạy lại và chi phí cả hệ thống ===')
    for k in [1, 2, 3]:
        r = mo_hinh(runs, reqs, max_lan_chay=k)
        ca_he_thong = r['tong'] + BASELINE * r['khong_thanh_cong']
        print(f"{k} lần | tổng trợ lý(sim)={r['tong']:10,.0f} đ | không tc={r['khong_thanh_cong']:3d} | cả hệ thống(sim)={ca_he_thong:10,.0f} đ | cps(sim)={r['cps']:6,.0f} đ")

    print('\n=== B4 · Xem lại 100% (phạm vi noi_dia + hang_nang) ===')
    scope_runs = runs[runs['request_id'].isin(scope_reqs['request_id'])]
    n_ok_req = scope_runs[scope_runs['status'] == 'ok']['request_id'].nunique()
    n_lam_lai = int((scope_reqs['ket_qua'] == 'lam_lai').sum())
    tok_tool_scope = r_scope['token'] + r_scope['tool']
    avg_ll_all = reqs.loc[reqs['ket_qua'] == 'lam_lai', 'phut_lam_lai_simulated'].mean()
    for mo_ta, phut_ll in [('Theo đề (9 phút/ca làm lại)', 9.0), (f'Theo trung bình dữ liệu ({avg_ll_all:.1f} phút/ca)', avg_ll_all)]:
        tong_b4 = tok_tool_scope + n_ok_req * 5 * LUONG_PHUT + n_lam_lai * phut_ll * LUONG_PHUT
        cps_b4 = tong_b4 / r_scope['thanh_cong']
        hoa_von_xem_lai = (BASELINE * r_scope['thanh_cong'] - tok_tool_scope - n_lam_lai * phut_ll * LUONG_PHUT) / (n_ok_req * LUONG_PHUT)
        print(f"{mo_ta:38s} | cps(sim)={cps_b4:7,.0f} đ ({cps_b4 / BASELINE:.2f}x) | hoà vốn xem lại <= {hoa_von_xem_lai:.1f} phút")


# ---------- Nhiệm vụ D · Cỡ mẫu và nền chỉ số an toàn ----------
def co_mau(p1, p2, alpha=0.05, power=0.80):
    """Cỡ mẫu mỗi nhóm khi so hai tỉ lệ (công thức chuẩn tắc hai phía)."""
    za = NormalDist().inv_cdf(1 - alpha / 2)
    zb = NormalDist().inv_cdf(power)
    pb = (p1 + p2) / 2
    return math.ceil(
        (za * math.sqrt(2 * pb * (1 - pb)) + zb * math.sqrt(p1 * (1 - p1) + p2 * (1 - p2))) ** 2
        / (p2 - p1) ** 2
    )


def in_bao_cao_pilot(reqs, baseline=0.70, alpha=0.05, power=0.80, icc=0.02):
    """In kết quả D1 (a–e) và tỉ lệ mở lại trong 7 ngày hiện tại từ trace."""
    n5 = co_mau(baseline, baseline + 0.05, alpha=alpha, power=power)
    n5_sm = math.ceil(NormalIndPower().solve_power(
        effect_size=proportion_effectsize(baseline + 0.05, baseline), alpha=alpha, power=power
    ))
    de_75 = 1 + (75 - 1) * icc
    n_b = math.ceil(n5 * de_75)
    staff_per_arm = math.ceil(n_b / 75)

    n6 = co_mau(baseline, baseline + 0.06, alpha=alpha, power=power)
    m_e = math.ceil(n6 * (1 - icc) / (20 - n6 * icc))
    de_e = 1 + (m_e - 1) * icc
    n_eff_e = 20 * m_e / de_e
    power_at_5 = NormalIndPower().power(
        effect_size=proportion_effectsize(baseline + 0.05, baseline), nobs1=n6, alpha=alpha
    )

    reopen_all = reqs['mo_lai_trong_7_ngay'].mean() * 100
    scope_reqs = reqs[reqs['loai'].isin(['noi_dia', 'hang_nang'])]
    reopen_scope = scope_reqs['mo_lai_trong_7_ngay'].mean() * 100

    print('\n=== D1 · Cỡ mẫu theo ba cách chia (baseline 0,70; alpha 0,05; power 0,80; ICC 0,02) ===')
    print(f"a) Chia theo yêu cầu (+5 điểm)     : {n5:,} yêu cầu/nhóm (statsmodels: {n5_sm:,})")
    print(f"b) Theo nhân viên, m=75            : DE={de_75:.2f}; n={n_b:,}/nhóm -> {staff_per_arm} NV/nhóm (tổng {staff_per_arm * 2} > 40: không đủ)")
    print(f"c) 20 nhân viên/nhóm               : tối đa < {20 / icc:,.0f} (< {n5:,}: không đạt +5 điểm)")
    print(f"d) 6 depot/nhóm                    : tối đa < {6 / icc:,.0f} (và < 20 cụm/nhóm)")
    print(f"e) MDE 6 điểm ({n6}/nhóm), 20 NV/nhóm: m >= {m_e} yêu cầu/NV (DE={de_e:.2f}, n_eff={n_eff_e:.1f}; power nếu chênh thật 5 điểm: {power_at_5:.2f})")
    print(f"Nền mở lại 7 ngày hiện tại         : toàn mẫu {reopen_all:.2f}% ({int(reqs['mo_lai_trong_7_ngay'].sum())}/{len(reqs)}); phạm vi pilot {reopen_scope:.2f}% ({int(scope_reqs['mo_lai_trong_7_ngay'].sum())}/{len(scope_reqs)})")


# ---------- Nhiệm vụ E1 · Tính thử chỉ số trên dữ liệu chạy thử ----------
def in_bao_cao_chi_so(reqs):
    """In ba chỉ số E1 trên 1.200 yêu cầu và tỉ lệ làm lại trong phạm vi pilot."""
    chinh_n = int(((reqs['dong_trong_24h'] == 1) & (reqs['mo_lai_trong_7_ngay'] == 0)).sum())
    xem = reqs[reqs['duoc_xem_lai'] == 1]
    bo_qua_n = int(xem['quyet_dinh_xem_lai'].isin(['sua', 'bo']).sum())
    an_toan_n = int((reqs['mo_lai_trong_7_ngay'] == 1).sum())

    scope_reqs = reqs[reqs['loai'].isin(['noi_dia', 'hang_nang'])]
    lam_lai_scope_n = int((scope_reqs['ket_qua'] == 'lam_lai').sum())

    print('\n=== E1 · Tính thử chỉ số trên 1.200 yêu cầu (đợt chạy thử, chưa có đối chứng) ===')
    print(f"Chính (đóng <=24h & không mở lại 7 ngày): {chinh_n / len(reqs) * 100:.2f}% ({chinh_n}/{len(reqs)})")
    print(f"Dùng (tỉ lệ bỏ qua gợi ý sua + bo)       : {bo_qua_n / len(xem) * 100:.2f}% ({bo_qua_n}/{len(xem)})")
    print(f"An toàn (tỉ lệ mở lại trong 7 ngày)      : {an_toan_n / len(reqs) * 100:.2f}% ({an_toan_n}/{len(reqs)})")
    print(f"Làm lại trong phạm vi noi_dia + hang_nang: {lam_lai_scope_n / len(scope_reqs) * 100:.2f}% ({lam_lai_scope_n}/{len(scope_reqs)})")


if __name__ == '__main__':
    runs = pd.read_csv('logix_runs.csv')
    reqs = pd.read_csv('logix_requests.csv', keep_default_na=False)
    kiem_tra_dap_an_biet_truoc()
    in_bao_cao_chi_phi(runs, reqs)
    in_bao_cao_pilot(reqs)
    in_bao_cao_chi_so(reqs)
