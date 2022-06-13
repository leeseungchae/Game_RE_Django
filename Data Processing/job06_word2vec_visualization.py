# 1. 모듈 불러오기
import pandas as pd
import matplotlib.pyplot as plt
from gensim.models import Word2Vec
from sklearn.manifold import TSNE
from matplotlib import font_manager, rc
import matplotlib as mpl

# 2. 한국어 폰트 사용
font_path = './malgun.ttf'
font_name = font_manager.FontProperties(
    fname=font_path).get_name()
mpl.rcParams['axes.unicode_minus']=False
rc('font', family=font_name)

# # !apt -qq -y install fonts-nanum
# import matplotlib as mpl
# import matplotlib.font_manager as fm
# fontpath = '/usr/share/fonts/truetype/nanum/NanumBarunGothic.ttf'
# font = fm.FontProperties(fname=fontpath, size=9)
# plt.rc('font', family='NanumBarunGothic')
# mpl.font_manager._rebuild()

# 3. 모델 불러오기
embedding_model = Word2Vec.load('./models/word2vecModel_Game.model')
print(list(embedding_model.wv.index_to_key))
print(len(list(embedding_model.wv.index_to_key)))
key_word = '혜자'  #유사한 20개 불러오기
sim_word = embedding_model.wv.most_similar(key_word, topn=10)
print(sim_word)
print(len(sim_word))

vectors = []
labels = []
for label, _ in sim_word:
    labels.append(label)
    vectors.append(embedding_model.wv[label])
df_vectors = pd.DataFrame(vectors)
print(df_vectors.head())


#4 .유사도 보기
tsne_model = TSNE(perplexity=40, n_components=2,   #인접 값 , 차원의 개수
                  init='pca', n_iter=2500)         #주성분 개수  #반복 횟수,
new_value = tsne_model.fit_transform(df_vectors)
df_xy = pd.DataFrame({'word':labels,
                      'x':new_value[:, 0],
                      'y':new_value[:, 1]})
print(df_xy)
print(df_xy.shape)
df_xy.loc[df_xy.shape[0]] = (key_word, 0, 0)

#5. 차트 그리기
plt.figure(figsize=(8, 8))
plt.scatter(0, 0, s=1500, marker='*')
label = '키워드 : '+key_word
title = '단어 유사도 '
for i in range(len(df_xy.x) - 1):
    a = df_xy.loc[[i, (len(df_xy.x) - 1)], :]

    plt.plot(a.x, a.y, '-D', linewidth=1 )
    plt.annotate(df_xy.word[i], xytext=(1, 1),
                 xy=(df_xy.x[i], df_xy.y[i]),
                 textcoords='offset points',
                 ha='right', va='bottom')



plt.title(title)

plt.legend()
plt.show()
plt.savefig('./sim_score_vi.png')