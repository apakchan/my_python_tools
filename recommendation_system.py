from flask import Flask, request, jsonify
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from functools import lru_cache

app = Flask(__name__)

# 假设你已经有一个包含多个 JSON 的列表
json_list = [
    {"name": "John", "age": 30, "interests": ["music", "sports"]},
    {"name": "Jane", "age": 25, "interests": ["movies", "books"]},
    {"name": "Bob", "age": 35, "interests": ["music", "travel"]}
]

# 定义字段权重
field_weights = {
    "age": 0.8,
    "interests": 0.2
}

# 使用 TF-IDF 向量化器将文本列表转换为特征向量
vectorizer = TfidfVectorizer()
text_list = []
for json_obj in json_list:
    json_obj.pop("name", None)  # 移除"name"字段
    text_list.append(json.dumps(json_obj))
tfidf_matrix = vectorizer.fit_transform(text_list)

# 选择与给定 JSON 最相似的 n 个个体
@lru_cache(maxsize=128)  # 使用缓存
def get_top_similar(json_str, n):
    query_vector = vectorizer.transform([json_str])
    similarity_scores = cosine_similarity(query_vector, tfidf_matrix)[0]

    # 计算综合相似度分数
    weighted_scores = []
    for i, score in enumerate(similarity_scores):
        json_obj = json_list[i]
        weighted_score = 0.0
        for field, weight in field_weights.items():
            if field in json_obj:
                weighted_score += weight * score
        weighted_scores.append(weighted_score)

    top_indices = sorted(range(len(weighted_scores)), key=lambda i: weighted_scores[i], reverse=True)[:n]
    top_similar = [json_list[i] for i in top_indices]
    return top_similar

@app.route('/recommend', methods=['POST'])
def recommend():
    try:
        input_json = request.get_json()
        num_recommendations = input_json['num_recommendations']
        recommendations = get_top_similar(json.dumps(input_json), num_recommendations)
        return jsonify(recommendations)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run()
