#cấu hình
#gọi thợ1
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv

#load file .env
load_dotenv()

#gọi key2
api_key = os.getenv("GOOGLE_API_KEY")
print("KEY:", os.getenv("GOOGLE_API_KEY"))

if not api_key:
    raise RuntimeError("Please set GOOGLE_API_KEY in environment.")

#gọi đường dẫn pdf3
pdf_path = "ComputerOrganizationandArchitecture10th-WilliamStallings.pdf"
#gọi đường dẫn kho lưu trữ4
db_path = "./chroma_db"

# trả về em bé phiên dịch tiền giấy thành vàng thỏi5
def get_embedding_function():
    return GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
#chỉ chạy trong file (ẩn các câu lệnh test trong file này nếu file khác gọi mượn đồ)6
if __name__ == "__main__":
    print("Config loaded successfully.")
    embedding = get_embedding_function()
    print("Embedding model ready: ", embedding)