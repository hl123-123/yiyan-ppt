import pickle
from sklearn.metrics.pairwise import cosine_similarity
from config import Config
from yiyan import yiyan_embedding
def get_embedding(text):
    embedding = yiyan_embedding(text)
    return embedding

def answer_question(question , paragraphs , paragraph_embeddings , num_results=3): #参数分别是：问题，拆分文本 ，向量集 ， 寻找组数
    question_embedding = get_embedding(question) #获取对应向量
    similarity_scores = []
    for paragraph_embedding in paragraph_embeddings:
        # 使用余弦相似度计算问题和段落之间的相似性
        similarity_score = cosine_similarity([question_embedding], [paragraph_embedding])[0][0]
        similarity_scores.append(similarity_score)

    # 找到最相似的 num_results 个段落索引
    most_similar_indexes = sorted(range(len(similarity_scores)), key=lambda i: similarity_scores[i], reverse=True)[:num_results]
    similar_doc_list = [paragraphs[i] for i in most_similar_indexes]
    return similar_doc_list