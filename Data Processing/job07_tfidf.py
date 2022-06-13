import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.io import mmwrite, mmread
import pickle

df_reviews = pd.read_csv('./crawling_data/datasets/Game_reviews_ALL_Preprocessing_2.csv')
df_reviews.info()

# 단어 등장 횟수 ,문장 단어 횟수 측정
Tfidf = TfidfVectorizer(sublinear_tf=True)
Tfidf_matrix = Tfidf.fit_transform(df_reviews['cleaned_sentences'])

# 바이너리 형식으로 저장
with open('./models/tfidf01.pickle', 'wb') as f:
    pickle.dump(Tfidf, f)
# 단어 유사도 저장
mmwrite('./models/Tfidf_Game_review01.mtx', Tfidf_matrix)
print('end')