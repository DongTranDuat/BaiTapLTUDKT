#Check model bạn có thể dùng
#Khuyên dùng nếu có: gemini-flash-latest
import google.generativeai as genai
from config import api_key

api_key

def main():
    print("Đang kết nối với Google AI Studio...")
    
    try:
        genai.configure(api_key=api_key)

        print("\nDANH SÁCH CÁC MODEL BẠN CÓ QUYỀN DÙNG:")
        print()

        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"{m.name}")
            
    except Exception as e:
        print(f"\nLỗi: {e}")
        print("Kiểm tra lại Internet hoặc API Key.")

if __name__ == "__main__":
    main()