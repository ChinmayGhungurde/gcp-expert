import chromadb
import glob
import re
import demoji
from pathos.multiprocessing import ProcessingPool
import inspect
from langchain.embeddings import VertexAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from app.embeddings.settings import CHROMA_COLLECTION_NAME, DATA_PATH, CHUNK_SIZE

def get_embeddings(data: list) -> list:
    """ Return the embeddings for given data list """
    try:
      # Divide the data into groups of 20K to satisfy Vertex AI limit
      text_splitter = CharacterTextSplitter.from_tiktoken_encoder(chunk_size=CHUNK_SIZE, chunk_overlap=20)
      texts = text_splitter.split_text(data)
      print("Here")
      e_model = VertexAIEmbeddings()
      embeddings = e_model.embed_documents(texts)

      # Combine the split embedding chunks into one
      all_embed = []
      for embedding in embeddings:
        all_embed.extend(embedding)

      return all_embed
  
    except Exception as e:
      frame = inspect.currentframe()
      print(f"Error in {inspect.getframeinfo(frame).function}: {e}")

class ChromaWrapper:
  def __init__(self):
    """ Create the client and the collection"""
    try:
      self.chroma_client = chromadb.PersistentClient()
      self.collection = self.chroma_client.get_or_create_collection(CHROMA_COLLECTION_NAME)

    except Exception as e:
      frame = inspect.currentframe()
      print(f"Error in {inspect.getframeinfo(frame).function}: {e}")

  def __preprocess_text(self, text: str) -> str:
    """ Preprocess text files """
    try:
      # Replace tabs, multiple spaces, and newlines with single spaces
      text = re.sub(r'\s+', ' ', text)
      text = re.sub(r'\n+', ' ', text)
      # Remove links from the review
      text = re.sub(r'http\S+', '', text)
      text = demoji.replace(text, '')
      return text
    
    except Exception as e:
      frame = inspect.currentframe()
      print(f"Error in {inspect.getframeinfo(frame).function}: {e}")

  def __fetch_data(self) -> list:
    """ Fetch the data from data folder and return content in a list"""
    doc_list = []
    try:
      for file in glob.glob(f"{DATA_PATH}/*.txt"):
        with open(file, encoding="utf8") as f:
          content = f.readlines()
          # print(content)
          processed_content = self.__preprocess_text(''.join(content))
          doc_list.append(processed_content)

      return doc_list

    except Exception as e:
      frame = inspect.currentframe()
      print(f"Error in {inspect.getframeinfo(frame).function}: {e}")

  def data_to_collection(self) -> list:
    """ Execute the entire sequence of operations """
    
    try:
      pool = ProcessingPool()

      # TODO Fetch and serialize the metadata

      # Get the embeddings for each document
      doc_list = self.__fetch_data()
      embeddings = pool.map(get_embeddings, doc_list)

      # Store embeddings in ChromaDB instance
      # self.collection.add(
      #   embeddings=embeddings,
      #   documents=doc_list,
      #   # metadata=metadata
      # )

    except Exception as e:
      frame = inspect.currentframe()
      print(f"Error in {inspect.getframeinfo(frame).function}: {e}")
  
  

