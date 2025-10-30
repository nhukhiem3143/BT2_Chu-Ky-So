# 🧾 BÀI TẬP: CHỮ KÝ SỐ TRONG FILE PDF  
**Môn:** An toàn và Bảo mật Thông tin  
**Giảng viên:** Đỗ Duy Cốp  
**Lớp:** 58KTP  
**Sinh viên:** Nguyễn Như Khiêm  
**Hạn nộp:** 31/10/2025 – 23:59:59  

---

## I. MỤC TIÊU
Phân tích và hiện thực quy trình **tạo – nhúng – xác thực chữ ký số** trong file PDF.  
Bài làm tuân thủ chuẩn **PDF 1.7 / PAdES (ETSI EN 319 142)** và sử dụng các công cụ:
- `OpenSSL` – sinh cặp khóa và chứng thư số tự ký (self-signed)
- `PyPDF2` / `pikepdf` – thao tác PDF và nhúng vùng chữ ký
- `hashlib`, `base64` – băm dữ liệu và mã hóa chữ ký
- `Python` – viết script tự động hoá ký và xác minh  

---

## II. CẤU TRÚC DỰ ÁN

```
CHUKYSO/  
│
├── assets/                     # Tài nguyên minh họa
│   ├── chuky.jpg             
│   ├── signature_img.png    
│   └── ten.jpg                 # Hình ảnh chữ ký
│
├── docs/
│   └── original.pdf            # File PDF gốc cần ký
│
├── keys/                       # Chứa khóa và chứng thư
│   ├── signer_key.pem          # Khóa riêng RSA (private)
│   └── signer_cert.pem         # Chứng thư số (certificate)
│
├── scripts/                    # Toàn bộ mã nguồn chính
│   ├── gen_keys.py             # Sinh cặp khóa RSA và cert
│   ├── overlay.pdf             # Lớp phủ chữ ký lên PDF
│   ├── sign_pdf.py             # Script ký PDF
│   ├── verify_pdf.py           # Script xác minh chữ ký
│   ├── tamper_pdf.py           # Script giả mạo để test verify
│   ├── quytrinh_tao_chuky.txt  # Ghi chú quy trình kỹ thuật
│   ├── verify_log_ok.txt       # Log xác minh hợp lệ
│   └── verify_log.txt          # Log xác minh thất bại
│
├── signed.pdf                   # File PDF đã ký
├── tampered.pdf                 # File bị chỉnh sửa sau khi ký
├── readme_chukyso.md            # Ghi chú riêng cho quy trình ký
└── README.md                    # File mô tả chính
```

---

## III. QUY TRÌNH THỰC HIỆN

### 🔹 1. Sinh khóa RSA và chứng thư số

**File:** `scripts/gen_keys.py`  
**Thực hiện:**
```bash
cd scripts
python gen_keys.py
```

**Kết quả:**
- `keys/signer_key.pem`: Khóa riêng (RSA 2048-bit)
- `keys/signer_cert.pem`: Chứng thư số tự ký (self-signed)

**Mục đích:** Dùng để ký và xác thực chữ ký.  
**Thuật toán:** RSA 2048-bit, SHA-256, padding PKCS#1 v1.5

---

### 🔹 2. Tạo và ký file PDF

**File:** `scripts/sign_pdf.py`  
**Thực hiện:**
```bash
python sign_pdf.py
```

**Chức năng:**
1. Tải file `docs/original.pdf`
2. Tạo vùng Signature field (AcroForm)
3. Reserve vùng `/Contents` 8192 bytes
4. Tính hash SHA-256 trên vùng `/ByteRange`
5. Sinh PKCS#7 detached signature (bao gồm: messageDigest, signingTime, contentType, certificate chain)
6. Ghi blob PKCS#7 vào `/Contents`
7. Ghi file mới `signed.pdf` bằng incremental update

**Kết quả:**
- File `signed.pdf` (PDF đã có chữ ký số hợp lệ)
<img width="1757" height="741" alt="image" src="https://github.com/user-attachments/assets/34504e6a-7ded-406c-ac4c-e4cb9cf26207" />  

---

### 🔹 3. Xác minh chữ ký PDF

**File:** `scripts/verify_pdf.py`  
**Thực hiện:**
```bash
python verify_pdf.py
```

**Các bước xác minh:**
1. Đọc Signature dictionary: `/Contents`, `/ByteRange`
2. Tách chuỗi PKCS#7 từ PDF
3. Kiểm tra messageDigest so với hash thực tế
4. Xác minh chữ ký bằng public key trong `signer_cert.pem`
5. Kiểm tra chứng thư (chain, validity date)
6. Kiểm tra có bị sửa đổi (so sánh ByteRange)

**Kết quả:**
- `verify_log_ok.txt`: xác minh hợp lệ  
<img width="1406" height="251" alt="image" src="https://github.com/user-attachments/assets/33aeab25-18f4-4b55-89d4-eafa62485953" />  

- `verify_log.txt`: báo lỗi nếu file đã bị chỉnh sửa  
<img width="1417" height="250" alt="image" src="https://github.com/user-attachments/assets/3649fcc7-d7a3-4564-bbc7-704f4bcf9213" />  

---

### 🔹 4. Thử giả mạo file PDF (tamper test)

**File:** `scripts/tamper_pdf.py`  
**Thực hiện:**
```bash
python tamper_pdf.py
```

**Chức năng:**
1. Mở file `signed.pdf`
2. Thêm 1 ký tự hoặc ghi đè nội dung nhỏ (ví dụ "TEST")
3. Lưu thành `tampered.pdf`  
<img width="1078" height="804" alt="image" src="https://github.com/user-attachments/assets/667731d3-5972-42d4-90fa-d6e90a726b77" />  

Khi chạy lại `verify_pdf.py`, kết quả sẽ báo:
```
❌ Signature invalid – file modified after signing
```
<img width="1864" height="826" alt="image" src="https://github.com/user-attachments/assets/cd95ce1c-f573-4f9d-9700-171f0e9fa15b" />  

---

## IV. GIẢI THÍCH CHUẨN & THÀNH PHẦN TRONG PDF

| Thành phần | Mô tả | Vai trò |
|------------|-------|---------|
| `/Catalog` | Gốc của tài liệu PDF | Liên kết tới cây trang và form |
| `/Pages` | Danh sách các trang | Trỏ tới từng Page object |
| `/AcroForm` | Biểu mẫu chứa trường chữ ký | Quản lý SigField |
| `/SigField` | Widget thể hiện vùng ký | Nơi người dùng ký |
| `/Sig` | Signature dictionary | Chứa thông tin chữ ký số |
| `/ByteRange` | Mảng byte được hash | Xác định vùng dữ liệu không ký |
| `/Contents` | Dữ liệu PKCS#7 (chữ ký) | Chứa signature blob |
| Incremental Update | Phần ghi thêm cuối file PDF | Lưu chữ ký mà không thay đổi file gốc |
| DSS | Document Security Store | Lưu chứng thư, CRL, OCSP (nếu có) |

---

## V. THỜI GIAN KÝ

| Loại thời gian | Vị trí lưu | Ý nghĩa |
|----------------|------------|---------|
| `/M` | Trong Signature dictionary | Thời điểm ký (text, không có giá trị pháp lý) |
| signingTime | Trong PKCS#7 attribute | Thời điểm ký thực tế |
| timeStampToken | RFC 3161 timestamp server | Có giá trị pháp lý nếu từ TSA |
| Document timestamp | PAdES-level timestamp | Xác thực thời điểm toàn văn bản |

---

## VI. KẾT QUẢ DEMO

| File | Nội dung |
|------|----------|
| `original.pdf` | File gốc chưa ký |
| `signed.pdf` | File đã ký hợp lệ |
| `tampered.pdf` | File bị thay đổi sau khi ký |
| `verify_log_ok.txt` | Kết quả xác minh hợp lệ |
| `verify_log.txt` | Báo lỗi xác minh thất bại |

---

## VII. GHI CHÚ BẢO MẬT

- Sử dụng RSA ≥ 2048-bit và SHA-256.
- Tránh công khai khóa thực (dùng khóa sinh ngẫu nhiên).
- Không dùng private key thương mại.
- Có thể mở rộng RSA-PSS hoặc thêm RFC3161 timestamp.

---

## VIII. THAM KHẢO

- ISO 32000-2: PDF 2.0
- ETSI EN 319 142: PAdES
- RFC 3161: Time-Stamp Protocol
- iText7, OpenSSL, PyPDF2
