# 1. 모듈 불러오기
from gensim.models import Word2Vec
import pandas as pd

# 2. 파일 불러오기
review_word = pd.read_csv('./DataSets/Game_reviews_ALL_Preprocessing_2.csv')
review_word.dropna(inplace=True)
review_word['scores'] = review_word['scores'].astype(str)
# print(review_word.iloc[-1])
cleaned_token_review = list(review_word['cleaned_sentences'])
cleaned_tokens = []
# 3. 분리 시켜서 합치기
for sentence in cleaned_token_review:
    token = sentence.split()
    cleaned_tokens.append(token)
print(cleaned_tokens[0])

# 4. 모델 사용
embedding_model = Word2Vec(cleaned_tokens, vector_size = 100, window = 4, min_count = 20,
                           # 100차원 설정 , window 크기 앞 뒤 단위
                           # min_count최소 빈도수
                           # workers cpu개수 epochs = 학습개수 sg = 1 고정
                           workers = 4, epochs = 100, sg = 1)

embedding_model.save('./models/word2vecModel_Game.model')
print(embedding_model.wv.vocab.key())
print(len(embedding_model.wv.vocab.key()))