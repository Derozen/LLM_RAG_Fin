from TextPreprocessing.TxtVector import EmbedChunks
from dotenv import load_dotenv
import os
import numpy as np
from DatabaseManagement.StoreVector import store_vector


load_dotenv()

embeddings, textChunks = EmbedChunks(os.getenv("PDF_FILE_PATH"), chunksize=128) 
#You can also pass a list of file paths to ptocess multiple PDF files at once. For example: EmbedChunks(["file1.pdf", "file2.pdf"], chunksize=128)

store_vector(textChunks, embeddings.tolist(), os.getenv("DB_NAME"), os.getenv("DB_USER"), os.getenv("DB_HOST"), os.getenv("DB_PASSWORD"))