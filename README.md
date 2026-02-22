# Chatbot hỏi đáp tài liệu

Dự án chatbot sử dụng LangChain + Google Generative AI để trả lời câu hỏi từ file PDF.

# module dữ liệu & vector store (Google Gemini version)

Module này chịu trách nhiệm xử lý tài liệu pdf, cắt nhỏ văn bản và lưu trữ dưới dạng Vector bằng công nghệ của Google Gemini.

Dữ liệu đầu ra: thư mục **`chroma_db/`**.

## Cấu trúc file

- **`chroma_db/`**: **[QUAN TRỌNG]** Thư mục chứa dữ liệu Vector đã xử lý xong. Vui lòng không xóa hoặc sửa file bên trong. Phải để file code và thư mục chroma_db nằm chung một chỗ.
- **`config.py`**: Quản lý API key và cấu hình model.
- **`build_db.py`**: Code gốc dùng để nạp dữ liệu (Đã chạy hoàn tất, **KHÔNG ĐƯỢC CHẠY LẠI**).
- **`requirements.txt`**: Danh sách thư viện cần thiết.

## Cài đặt

# Cài đặt môi trường bằng các lệnh:

```bash
git clone <repo>
cd <repo>
conda create -n chatbot python=3.10 -y
conda activate chatbot
pip install -r requirements.txt
pip check
```
## Kiểm tra môi trường:

```bash
conda activate chatbot
python --version
where python
pip show langchain
pip check #hiện: No broken requirements found
```
### 3. Biến môi trường (.env)

```md
## Cấu hình API key

Tạo file `.env`:

# Tìm model được dùng

```bash
import google.generativeai as genai

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

print("Danh sách model bạn có quyền dùng:")
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(f"- {m.name}")
```

## Fix lỗi version langchain
### 5. Fix lỗi (bạn đã có nhưng nên viết gọn lại)

```md
## Lỗi thường gặp

Nếu lỗi langchain:

```bash
pip install -U langchain
