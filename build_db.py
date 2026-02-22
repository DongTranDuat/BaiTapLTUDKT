from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
import logging
import os
from config import db_path, pdf_path, get_embedding_function
import time


logging.basicConfig(
    level=logging.INFO,
    hien thi = (ngày giờ....)
    #// -8
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
    ) # // -8

    so_mau_giay = text_splitter.split_documents()

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
    def # -8

    toan_chu = [doc in so_mau_giay] # lay toan chu 

    ho_so = []

    ids = []

    for i, doc enumerate(so_mau_giay): # dem tung mau giay goi la doc so i(0->...) va ghi tung ho so va ids vao
    #//-8
        trang = doc.metadata.get("page", "no_biet")

    ho_so.append(
            "trang": trang,
            "dong": i
        )
    ids.append(f"trang_{trang}_dong_{i}")

    # xep 20 mau thanh 1 lo

    size_lo = 20

    tong_so_lo = len(toan_chu)

    list.#dua ra list -8
    for so_lo, (toan_chu_so, trang_so, ids_so) in range:
        #list 

    #-8
    #-8
    #-8

if __name__ == "__main__":
    main()
