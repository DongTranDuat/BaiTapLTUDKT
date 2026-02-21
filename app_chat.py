import time
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from config import db_path, get_embedding_function
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from chromadb.config import Settings

def main():
    if not os.path.exists(db_path):
        print("Lỗi: Chưa thấy kho dữ liệu!")
        return

    print("Đang mở kho dữ liệu...")
    embedding = get_embedding_function()
    db = Chroma(
        collection_name="chat_kientrucmaytinh",
        persist_directory=db_path,
        embedding_function=embedding,
        client_settings=Settings(anonymized_telemetry=False)
    )

    selected_model = "gemini-flash-latest"
    llm = ChatGoogleGenerativeAI(
        model=selected_model,
        temperature=0.3,
        max_output_tokens=1000
    )

    prompt = ChatPromptTemplate.from_template("""
        Bạn là một trợ lý AI hỗ trợ học tập môn kiến trúc máy tính. 
        Hãy sử dụng những thông tin được cung cấp trong phần ngữ cảnh (Context) dưới đây để giải đáp câu hỏi của sinh viên.
                                            
        Quy tắc:
        1. Chỉ trả lời dựa trên context được cung cấp.
        2. Nếu context không có thông tin, hãy nói "Xin lỗi, trong tài liệu bạn cung cấp không có thông tin này.".
        3. Trả lời chi tiết, đầy đủ và giải thích dễ hiểu bằng Tiếng Việt.
        4. Nếu câu hỏi của sinh viên viết không dấu hoặc có lỗi chính tả, hãy tự suy luận dựa trên ngữ cảnh môn Kiến trúc máy tính để trả lời.
        <context>
        {context}
        </context>
        Câu hỏi: {input}
    """)

    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    retriever = db.as_retriever(search_kwargs={"k": 5})
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)

    print("\nSẵn sàng lắng nghe câu hỏi!")

    while True:
        query = input("Câu hỏi: ")

        print(f"Câu hỏi {query}")

        if query.lower() in 'bai':
            print("Bai bai~")
            break
        if not query.strip(): continue

        Max_retries = 3
        retry_count = 0

        # Logic chạy có xử lý lỗi 429
        while retry_count < Max_retries:
            print(f"Vui lòng đợi (Lần thử {retry_count + 1})", end="\r")
            
            try:
                response = rag_chain.invoke({"input": query})
                
                print(f"Trả lời: \n{response['answer']}")

                #chống 429
                time.sleep(5)
                break

            except Exception as e:
                #bắt 429 để chống sụp đổ
                if "429" in str(e):
                    retry_count += 1
                    if retry_count == Max_retries:
                        break
                    wait_time = 30
                    time.sleep(30)
                    
                    continue
                else:
                    print(f"\nLỗi khác: {e}")
                    break
if __name__ == "__main__":
    main()