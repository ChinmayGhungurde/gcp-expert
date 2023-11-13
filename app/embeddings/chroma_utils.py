import chromadb
import glob
import re
import demoji
import inspect
from vertexai.language_models import TextEmbeddingModel
from app.embeddings.settings import CHROMA_COLLECTION_NAME, DATA_PATH

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
    data_list = []
    try:
      for file in glob.glob(f"{DATA_PATH}/*.txt"):
        with open(file, encoding="utf8") as f:
          content = f.readlines()
          # print(content)
          processed_content = self.__preprocess_text(''.join(content))
          data_list.append(processed_content)

      return data_list

    except Exception as e:
      frame = inspect.currentframe()
      print(f"Error in {inspect.getframeinfo(frame).function}: {e}")

  def __get_embeddings(self, data: list) -> list:
    """ Return the embeddings for given data list """
    print(len(data))
    print(len(max(data, key=len)))

    embeddings = []

    # Divide the data into groups of 20K to satisfy Vertex AI limit

    # model = TextEmbeddingModel.from_pretrained('textembedding-gecko@001')
    # embeddings = model.get_embeddings(data)
    # print(type(embeddings))

  def data_to_collection(self) -> list:
    """ Execute the entire sequence of operations """
    data = self.__fetch_data()
    self.__get_embeddings(data)
  
  

