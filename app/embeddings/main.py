import os
import openai
import pandas as pd
from pathlib import Path

os.environ["OPENAI_API_KEY"] = "56dc6d2fdf8c48debea0493b8db17bfa"
os.environ["OPENAI_API_VERSION"] = "2022-12-01"
os.environ["OPENAI_API_type"] = "azure"
os.environ["OPENAI_API_base"] = "https://dattaraj-openai-demo.openai.azure.com/"

openai.api_key = os.getenv("OPENAI_API_KEY")

def get_embedding(good):
    response = openai.Embedding.create(
        # model="text-embedding-ada-002",
        engine="davinci",
        input=[good]
    )
    embedding = response["data"][0]["embedding"]

    return embedding

root_folder = Path(os.path.dirname(os.path.abspath(__file__))).parent.parent
print(root_folder)

csv_file = os.path.join(root_folder, "data", "data.csv")
# data_URL =  "https://raw.githubusercontent.com/keitazoumana/Experimentation-Data/main/Musical_instruments_reviews.csv"


review_df = pd.read_csv(csv_file)
review_df.head()

review_df = review_df[['reviewText']]
print("Data shape: {}".format(review_df.shape))
print(review_df.head())
# Data shape: (10261, 1)

review_df = review_df.sample(100)
review_df["embedding"] = review_df["reviewText"].astype(str).apply(get_embedding)

# Make the index start from 0
review_df.reset_index(drop=True)

review_df.head(10)