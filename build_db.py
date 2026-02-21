from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from config import pdf_path, db_path, get_embedding_function
import time
import os
import shutil
from chromadb.config import Settings

def main():
    # print("CẢNH BÁO: Bạn sắp xóa sạch kho dữ liệu cũ để nạp lại từ đầu!")
    # xac_nhan = input("Bạn có chắc chắn muốn chạy không? (y/n): ")
    
    # if xac_nhan.lower() != 'y':
    #     print("Đã hủy lệnh. Kho dữ liệu vẫn an toàn.")
    #     return

    print("Bắt đầu xây kho dữ liệu.")

    # if os.path.exists(db_path):
    #     shutil.rmtree(db_path)
    #     print(f"Đã dọn dẹp kho cũ tại {db_path}")

    if not os.path.exists(pdf_path):
        print(f"Không tìm thấy file sách tại {pdf_path}")
        return
    
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()[25:69]
    print(f"Đã đọc xong {len(docs)} trang tài liệu.")

    text_splitter = RecursiveCharacterTextSplitter (chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)
    print(f"Đã cắt thành {len(splits)} đoạn nhỏ.")

    embedding = get_embedding_function()

    vectorstore = Chroma(
        collection_name="chat_kientrucmaytinh",
        embedding_function=embedding,
        persist_directory=db_path,
        client_settings=Settings(anonymized_telemetry=False)
    )

    total_splits = len(splits)

    for i, doc in enumerate(splits):
        doc.metadata["source_id"] = f"page_{page_number}_chunk_{i}"

        max_retries = 3
        
        for attempt in range(max_retries):
            try:
                print(f"Đang nạp đoạn {i+1}/{total_splits}...", end=" ")
                vectorstore.add_documents([doc])
                ids = [doc.metadata["source_id"] for doc in splits]

                vectorstore.add_documents(splits, ids=ids)

                time.sleep(3)
                break

            except Exception as e:
                if "429" in str(e):
                    wait_time = 30
                    print(f"Hồi mana {wait_time}s rồi tiếp tục lần {attempt+1}")
                    time.sleep(wait_time)
                else:
                    print(f"{e}")
                    break
    print("Current vector count:", vectorstore._collection.count())
    print("Đã xây xong kho dữ liệu.")

if __name__ == "__main__":
    main()