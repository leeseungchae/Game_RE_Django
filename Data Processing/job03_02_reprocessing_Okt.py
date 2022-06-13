#모듈 불러오기
import pandas as pd
from konlpy.tag import Okt
import re

df = pd.read_csv('./DataSets/GameData.csv')
df.dropna(inplace=True)
print(df.head())
df.info()

# 형태소 분석기 사용
okt = Okt()
count = 0
cleaned_sentences = []
for sentence in df.cleaned_sentences:
    count += 1
    if count % 10 ==0:
        print('.', end='')
    if count % 100 == 0:
        print()
    token = okt.pos(sentence, stem=True)
    # print(token)   
    df_token = pd.DataFrame(token,  columns=['word', 'class'])
    df_token = df_token[(df_token['class']=='Noun') |  #명사
                                (df_token['class']=='Verb') |  #동사
                                (df_token['class']=='Adjective')]  #형용사
    cleaned_sentence = ' '.join(df_token.word) #한문장으로 합치기
    # print(cleaned_sentence)
    cleaned_sentences.append(cleaned_sentence)
df['cleaned_sentences'] = cleaned_sentences
print(df.head())
df.info()
df.to_csv('./Datasets/GameData.csv',

          index=False)










