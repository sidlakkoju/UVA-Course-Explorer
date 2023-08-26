from semantic_search import *
from memory_profiler import profile

@profile
def test_semantic_search():
   data_dir = "data"
   with open(os.path.join(data_dir, 'embedding_matrix.pkl'), 'rb') as embedding_file:
      embedding_matrix = pickle.load(embedding_file)

   # Load data dictionary from pickle file
   with open(os.path.join(data_dir, 'index_to_data_dict.pkl'), 'rb') as data_dict_file:
      course_data_dict = pickle.load(data_dict_file)

   with open(os.path.join(data_dir, 'data_to_index_dict.pkl'), 'rb') as data_to_index_file:
      data_to_index_dict = pickle.load(data_to_index_file)

   acad_level_to_indices_map = {}

   for level in ['Undergraduate', 'Graduate', 'Law', 'Graduate Business', 'Medical School', 'Non-Credit']:
      filename = os.path.join(data_dir, f"{level}_indices.pkl")
      with open(filename, 'rb') as f:
         acad_level_to_indices_map[level] = pickle.load(f)
      
   with open(os.path.join(data_dir, "latest_sem_indices.pkl"), 'rb') as f:
      latest_semester_indices = pickle.load(f)


@profile
def get_top_n_data_with_filters(query_vector, academic_level_filter="all", semester_filter="all", n=10):
    filtered_embedding_matrix, original_indices = generate_filtered_embedding_matrix(academic_level_filter, semester_filter)
    similarities = cosine_similarity_search(query_vector, filtered_embedding_matrix)

    top_n_filtered_indices = np.argsort(similarities)[::-1][:n]
    top_n_original_indices = original_indices[top_n_filtered_indices]
    top_n_data = [course_data_dict[index] for index in top_n_original_indices]

    # add the similarity scores as values in the dictionaries
    for i in range(min(n, len(top_n_data))):
        matrix_index = top_n_filtered_indices[i]
        top_n_data[i]["similarity_score"] = similarities[matrix_index]
    return top_n_data


# @profile
# def get_top_n_data_with_filters(query_vector, academic_level_filter="all", semester_filter="all", n=10):
#    filtered_embedding_matrix, original_indices = generate_filtered_embedding_matrix(academic_level_filter, semester_filter)
#    similarities = cosine_similarity_search(query_vector, filtered_embedding_matrix)

#    top_n_filtered_indices = np.argsort(similarities)[::-1][:n]
#    top_n_original_indices = original_indices[top_n_filtered_indices]
#    top_n_data = [course_data_dict[index] for index in top_n_original_indices]

#    # add the similarity scores as values in the dictionaries
#    for i in range(min(n, len(top_n_data))):
#       matrix_index = top_n_filtered_indices[i]
#       top_n_data[i]["similarity_score"] = similarities[matrix_index]
#    end = time.time()
#    return top_n_data


get_top_n_data_with_filters(get_embedding("agi"), academic_level_filter="Undergraduate", semester_filter="all", n=10)


