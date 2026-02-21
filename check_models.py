#Check model bạn có thể dùng
import google.generativeai as genai
from config import api_key

def main():
    print("Đang kết nối với Google AI Studio...")
    
    try:
        genai.configure(api_key=api_key)

        print("\nDANH SÁCH CÁC MODEL BẠN CÓ QUYỀN DÙNG:")
        print()

        for m in genai.list_models():
            if hasattr(m, "supported_generation_methods") and "generateContent" in m.supported_generation_methods:
                model_name = m.name

                if "gemini-flash-latest" in model_name:
                    print(f"!!! {model_name} (khuyên dùng)")
                else:
                    print(f"{model_name}")
            
    except Exception as e:
        print(f"\nLỗi: {e}")
        print("Kiểm tra lại internet hoặc API key.")

if __name__ == "__main__":
    main()