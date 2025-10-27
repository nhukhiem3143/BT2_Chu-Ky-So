ChuKySo/
│
├── assets/
│   ├── chuky.jpg
│   ├── signature_img.png
│   └── ten.jpg
│
├── docs/
│   ├── BaoCao_PDFChuKySo.pdf          ← Báo cáo ≤ 6 trang
│   ├── SoDo_CauTruc_PDF.drawio        ← Sơ đồ Catalog → SigDict
│   └── README_BaoCao.txt              ← Giải thích lý thuyết + chuẩn
│
├── keys/
│   ├── signer_key.pem                 ← private key
│   └── signer_cert.pem                ← certificate
│
├── scripts/
│   ├── gen_keys.py                    ← sinh RSA key + cert
│   ├── sign_pdf.py                    ← ký PDF
│   ├── verify_pdf.py                  ← xác thực PDF đã ký
│   ├── tamper_pdf.py                  ← tạo file PDF bị chỉnh sửa
│   └── quytrinh_tao_chuky.txt
├── venv/                              ← môi trường ảo
│
├── original.pdf                       ← PDF gốc
├── signed.pdf                         ← PDF đã ký
├── tampered.pdf                       ← PDF bị chỉnh sửa
├── README.md                          ← hướng dẫn chạy (git)
└── requirements.txt                   ← danh sách thư viện
