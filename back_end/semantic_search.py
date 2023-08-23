from openai.embeddings_utils import get_embedding, cosine_similarity
import pandas as pd
from config import openai_key
import openai
import numpy as np
import pickle
import json


openai.api_key = openai_key
"""
{
   "catalog_number":1040,
   "mnemonic":"RELG",
   "subject":"General Religion",
   "name":"Introduction to Eastern Religious Traditions",
   "credits":"3",
   "level":"Undergraduate",
   "description":"Introduces various aspects of the religious traditions of India, China, and Japan.",
   "similarity_score":0.835}
"""


with open('embedding_matrix.pkl', 'rb') as embedding_file:
    embedding_matrix = pickle.load(embedding_file)

# Load data dictionary from pickle file
with open('course_data_dict.pkl', 'rb') as data_dict_file:
    course_data_dict = pickle.load(data_dict_file)


with open('data_to_index_dict.pkl', 'rb') as data_to_index_file:
   data_to_index_dict = pickle.load(data_to_index_file)


def get_embedding(text, model="text-embedding-ada-002"):
   text = text.replace("\n", " ")
   return openai.Embedding.create(input = [text], model=model)['data'][0]['embedding']


def get_top_results_df(query, n=10):
   df = pd.read_csv('static_data_with_emebddings.csv')
   df['ada_embedding'] = df.ada_embedding.apply(eval).apply(np.array)

   query_embedding = get_embedding(query, model='text-embedding-ada-002')
   df['similarities'] = df.ada_embedding.apply(lambda x: cosine_similarity(x, query_embedding))
   df['similarities'] = df['similarities'].round(3)
   res = df.sort_values('similarities', ascending=False).head(n)
   return res


def cosine_similarity_search(query_vector, embedding_matrix):
    similarities = np.dot(embedding_matrix, query_vector) / (np.linalg.norm(embedding_matrix, axis=1) * np.linalg.norm(query_vector))
    return similarities


def get_top_n_data(query_vector, n=10):
   similarities = cosine_similarity_search(query_vector, embedding_matrix)

   top_n_indices = np.argsort(similarities)[::-1][:n]
   top_n_data = [course_data_dict[index] for index in top_n_indices]
   
   # add the similarity scores as values in the dictionaries
   for i in range(n):
      matrix_index = top_n_indices[i]
      top_n_data[i]["similarity_score"] = similarities[matrix_index]
   return top_n_data


def get_top_search_results_json(query, n=10):
   query_vector = get_embedding(query, model='text-embedding-ada-002')
   top_n_data = get_top_n_data(query_vector, n)
   return json.dumps(top_n_data)



def get_similar_courses(mnemonic, catalog_number, n=10):
   id_tuple = (mnemonic, catalog_number)
   if not id_tuple in data_to_index_dict.keys():
      print("no matching")
      return json.dumps([])   # no matching courses
   index = data_to_index_dict[id_tuple]
   query_vector = embedding_matrix[index]
   top_n_data = get_top_n_data(query_vector, n+1)
   return json.dumps(top_n_data[1:])



def get_top_results_json_old(query, n=10):
   df = get_top_results_df(query, n)
   df.drop(columns=['ada_embedding', 'n_tokens', 'acad_org', 'class_nbr'], inplace=True)
   df = df.rename(columns={'descr': 'name',
                           'acad_career_descr' : 'level',
                           'catalog_nbr': 'catalog_number',
                           'class_nbr': 'class_number',
                           'subject_descr': 'subject',
                           'subject': 'mnemonic',
                           'similarities': 'similarity_score',
                           'units': 'credits'})
