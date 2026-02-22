from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
import logging
import os
from config import db_path, pdf_path, get_embedding_function
import time
import math


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s"
)

logger = logging.getLogger()

def main():
    logger.info("Start!")

    # 1 la xac nhan su ton tai cua file
    if not os.path.exists(pdf_path):
        logger.info("cant find pdf.")
        return
    
    #doc file dang pdf
    loader = PyPDFLoader(pdf_path)

    so_trang_da_doc = loader.load()[45:55]

    logger.info(f"Load done {len(so_trang_da_doc)} trang.")

    #cat file
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    so_mau_giay = text_splitter.split_documents(so_trang_da_doc)

    logger.info(f"Split done {len(so_mau_giay)} mau giay.")

    #goi embe
    embedding = get_embedding_function()

    #mo phong trong kho
    vectorstore = Chroma(
        embedding_function=embedding,
        persist_directory=db_path,
        collection_name="chat_kientrucmaytinh"
    )

    #chuan bi data
    toan_chu = [doc1.page_content for doc1 in so_mau_giay] # lay toan chu 

    ho_so = []

    ids = []

    for i, doc2 in enumerate(so_mau_giay): # dem tung mau giay goi la doc so i(0->...) va ghi tung ho so va ids vao
        trang = doc2.metadata.get("page", "no_biet")

        ho_so.append(
            "trang": trang,
            "dong": i
        )

        ids.append(f"trang_{trang}_dong_{i}")

    # xep 20 mau thanh 1 lo

    size_lo = 20
    tong_lo = len(toan_chu)

    #may dong lo
    def may_dong_lo(tong_chu, size_lo):
        for i in range(0, len(tong_chu), size_lo):
            yield tong_chu[i:i+size_lo]
    
    so_lo_dong_duoc = math.ceil(tong_lo / size_lo)

    for i in enumerate(size_lo, (toan_chu_so, ho_so_so, ids_so),
        zip(
            may_dong_lo(toan_chu, size_lo),
            may_dong_lo(ho_so, size_lo),
            may_dong_lo(ids_so, size_lo)
        ),
        start=1
    ):
        max_tries = 3

        if attempt > max_tries:

            try:

                    logger.info(f"Nạp {i}/{so_lo_dong_duoc}")

                    vectorstore.add_texts(
                        texts=toan_chu_so,
                        metadatas=ho_so_so,
                        ids=ids_so
                    )

                    time.sleep(1)
            
            except Exception as e:

                if "429" in str(e):
                    ngoi_cho = 5

                    time.sleep(5 * 2 ** (attempt - 1))

                    logger.info(f"Hoi mana {ngoi_cho}s roi lam tiep.")
                
                else:
                    logger.info(f"Loi {e}.")
        

    logger.info("done.")


if __name__ == "__main__":
    main()
