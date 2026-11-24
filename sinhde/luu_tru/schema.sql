-- Lược đồ CSDL (mục 10 của thiết kế v1.2).
CREATE TABLE IF NOT EXISTS phien_ban_nen_tang (
  id INTEGER PRIMARY KEY,
  ma_bam TEXT UNIQUE,               -- mã băm nền tảng (mục 3.3)
  lean_toolchain TEXT, mathlib_rev TEXT,
  olean_ma_bam TEXT,                -- JSON: tệp .olean của ThuVienGT và tệp thực thi kiem_khop -> SHA-256
  trang_thai TEXT,                  -- cho_duyet | da_duyet | thay_the
  nguoi_duyet TEXT, duyet_luc TEXT, ghi_chu TEXT, tao_luc TEXT);

CREATE TABLE IF NOT EXISTS khuon (
  id INTEGER PRIMARY KEY, ma TEXT, phien_ban INTEGER, ma_dang_bai TEXT,
  json_goc TEXT, cay_json TEXT, ten_tham_so TEXT,
  rang_buoc TEXT, rang_buoc_siet TEXT, diem TEXT, huong TEXT,
  mien_hop_le TEXT,                 -- JSON: danh sách giá trị tham số
  goi_y TEXT,                       -- JSON: giá trị tham số -> gợi ý (mục 11.4)
  trang_thai TEXT,                  -- ung_vien | dat_cu_phap | da_dich | da_thu | da_kich_hoat | tam_dung | het_hieu_luc | bi_loai
  nhan TEXT,                        -- cm_theo_khuon | cm_mot_phan | cm_theo_cau
  truong_da_cm TEXT,                -- JSON: ["xacDinh", "dungDang", ...]
  module_lean TEXT, lean_hash TEXT, olean_hash TEXT, dang_chuan_hash TEXT,
  nen_tang_id INTEGER REFERENCES phien_ban_nen_tang(id),
  ly_do_loai TEXT, tao_luc TEXT,
  UNIQUE(ma, phien_ban));

CREATE TABLE IF NOT EXISTS cau (
  id INTEGER PRIMARY KEY, khuon_id INTEGER REFERENCES khuon(id),
  tham_so TEXT, seed INTEGER,
  cay_json TEXT,                    -- cây đã chuẩn hóa phía sinh (không tin cậy)
  cay_doc_json TEXT,                -- cây thô đọc được từ câu chữ (B10)
  diem TEXT, huong TEXT, ma_mau_cau TEXT, latex TEXT,
  cau_chu TEXT,                     -- chuỗi hiển thị, đúng như đã chứng nhận
  module_lean TEXT, lean_hash TEXT, axioms TEXT,
  dap_an_da_cm TEXT,                -- tùy chọn: giá trị giới hạn đã chứng minh
  nhan_de TEXT,                     -- da_chung_nhan_theo_khuon | da_chung_nhan_theo_cau
  trang_thai TEXT,                  -- dang_xu_ly | thu_nghiem | trong_ngan_hang | bi_loai | can_kiem_lai | bi_go
  ly_do_loai TEXT, dot_sinh_id INTEGER,
  nen_tang_id INTEGER REFERENCES phien_ban_nen_tang(id), tao_luc TEXT);

CREATE TABLE IF NOT EXISTS kiem_mau (
  id INTEGER PRIMARY KEY, cau_id INTEGER REFERENCES cau(id), nguoi_kiem TEXT,
  loai_mau TEXT,                    -- ngau_nhien | phat_hien | ca_hai (mục 14.2)
  bieu_thuc_go_lai TEXT, diem_go_lai TEXT, huong_go_lai TEXT,
  khop INTEGER, mot_nghia INTEGER,
  nhan_xet_chat_luong TEXT, luc TEXT);

CREATE TABLE IF NOT EXISTS lan_goi_llm (
  id INTEGER PRIMARY KEY, muc_dich TEXT, mo_hinh TEXT, prompt_phien_ban TEXT,
  dau_vao TEXT, dau_ra TEXT, token_vao INTEGER, token_ra INTEGER,
  chi_phi REAL, thoi_gian_ms INTEGER, khuon_id INTEGER, cau_id INTEGER, tao_luc TEXT);

CREATE TABLE IF NOT EXISTS lan_chay_lean (
  id INTEGER PRIMARY KEY, che_do TEXT,      -- kiem_tep_tam | build_module | kiem_khop
  muc_tieu TEXT, tep_hash TEXT, ket_qua TEXT, thong_bao TEXT, thoi_gian_ms INTEGER,
  khuon_id INTEGER, cau_id INTEGER, tao_luc TEXT);

CREATE TABLE IF NOT EXISTS lan_kiem (
  id INTEGER PRIMARY KEY, doi_tuong TEXT, doi_tuong_id INTEGER, buoc TEXT,
  dat INTEGER, ma_loi TEXT, chi_tiet TEXT, tao_luc TEXT);

CREATE TABLE IF NOT EXISTS dot_sinh (
  id INTEGER PRIMARY KEY, loai TEXT, tham_so TEXT, seed INTEGER, che_do TEXT,
  trang_thai TEXT, tao_luc TEXT, xong_luc TEXT);
