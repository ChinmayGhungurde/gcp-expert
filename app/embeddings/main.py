from google.cloud import aiplatform
from app.embeddings.chroma_utils import ChromaWrapper

aiplatform.init(project='analytics-ai-poc')

# def text_embeddings() -> list:
#     """ Text embeddings with an LLM """
#     model = TextEmbeddingModel.from_pretrained('textembedding-gecko@001')
#     embeddings = model.get_embeddings(["What is life?"])
#     print(f"Embeddings: {embeddings}")
#     for embedding in embeddings:
#         vector = embedding.values
#         print(f"Length of Embedding Vector: {len(vector)}")
#     return vector


if __name__ == '__main__':
    chroma = ChromaWrapper()
    chroma.data_to_collection()