import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string


def preprocess_text(text):
    tokens = word_tokenize(text.lower())
    
    table = str.maketrans('', '', string.punctuation)
    tokens = [w.translate(table) for w in tokens]
    
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]
    
    return " ".join(tokens)


def load_data_from_json(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)
    return data


def search_videos(json_file, search_query, threshold=0.03):
    data = load_data_from_json(json_file)
    print(data)
    
    preprocessed_captions = []
    for item in data:
        concatenated_captions = " ".join(item["captions"])
        preprocessed_captions.append(preprocess_text(concatenated_captions))
    print("\n",preprocessed_captions)
    
    vectorizer = TfidfVectorizer()  
    tfidf_matrix = vectorizer.fit_transform(preprocessed_captions)
    print("\n",tfidf_matrix)
    
    preprocessed_query = preprocess_text(search_query)
    print("\n",preprocessed_query)
    query_vector = vectorizer.transform([preprocessed_query])
    print("\n",query_vector)
    
    print("TF-IDF matrix shape:", tfidf_matrix.shape)
    print("Length of data:", len(data))
    
    similarities = cosine_similarity(query_vector, tfidf_matrix)
    print(similarities)
    print(len(similarities[0]))

    relevant_videos = []
    for idx, sim_score in enumerate(similarities[0]):
        if sim_score >= threshold:
            relevant_videos.append(data[idx]["video_id"])
    
    return relevant_videos
