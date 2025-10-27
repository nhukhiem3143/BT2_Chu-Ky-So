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
│   
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
│ 
├── venv/                           
│
├── original.pdf                       ← PDF gốc  
├── signed.pdf                         ← PDF đã ký  
├── tampered.pdf                       ← PDF bị chỉnh sửa  
└── README.md                            
      

