from openai.embeddings_utils import get_embedding, cosine_similarity
import pandas as pd
from config import openai_key
import openai
import numpy as np


openai.api_key = openai_key


def get_embedding(text, model="text-embedding-ada-002"):
   text = text.replace("\n", " ")
   return openai.Embedding.create(input = [text], model=model)['data'][0]['embedding']


def get_top_results_df(query, n=10):
   df = pd.read_csv('static_data_with_emebddings.csv')
   df['ada_embedding'] = df.ada_embedding.apply(eval).apply(np.array)

   query_embedding = get_embedding(query, model='text-embedding-ada-002')
   df['similarities'] = df.ada_embedding.apply(lambda x: cosine_similarity(x, query_embedding))
   res = df.sort_values('similarities', ascending=False).head(n)
   return res


def get_top_results_json(query, n=10):
   df = get_top_results_df(query, n)
#    print(df)
   df.drop(columns=['ada_embedding', 'similarities', 'n_tokens', 'acad_org', 'class_nbr', 'subject'], inplace=True)
   df = df.rename(columns={'subject_descr': 'name',
                           'acad_career_descr' : 'level',
                           'catalog_nbr': 'catalog_number',
                           'class_nbr': 'class_number',
                           'subject_descr': 'subject'
                           })
   return df.to_json(orient='records')





# catalog number        -->  catalog_number
# department   --> subject
# course title --> name
# course description  --> description
# undergraduate or graduate --> level
# credits --> credits