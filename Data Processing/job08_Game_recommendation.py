import pandas as pd
from sklearn.metrics.pairwise import linear_kernel
from scipy.io import mmread, mmwrite
import pickle
from gensim.models import Word2Vec
from matplotlib import pyplot as plt
from matplotlib import font_manager, rc
import matplotlib as mpl
import numpy as np

df_reviews = pd.read_csv('./DataSets/Game_reviews_ALL_Preprocessing_2.csv')
df_reviews.info()
# 추천 함수
def getRecommendation(cosine_sim):
    simScore = list(enumerate(cosine_sim[-1]))
    # 유사도 측정
    # print(simScore)
    # 키 , 벨류 추출
    simScore = sorted(simScore, key=lambda x:x[1],
                      reverse=True)
    # print(len(simScore))
    # 상위 10개만 추출
    simScore = simScore[1:10]
    # simScore = simScore *867
    # print(simScore)
    score_list=[]
    for score in simScore:
        score = score[1]
        score = score * len(simScore) *100
        score_list.append(score)
        
    print(score_list)
    top_10_df = pd.DataFrame()

    movieidx = [i[0] for i in simScore]
    recMovieList = df_reviews.iloc[movieidx]
    game_title = recMovieList['title'].tolist()
    game_title_2 = []
    for game in game_title:
        game = game.split(sep=':')
        game = game[0]
        game_title_2.append(game)


    top_10_df['score'] = score_list
    top_10_df['title'] = game_title

    font_path = './malgun.ttf'
    font_name = font_manager.FontProperties(
        fname=font_path).get_name()
    mpl.rcParams['axes.unicode_minus'] = False
    rc('font', family=font_name)

    label = '키워드 : '+key_word

    plt.rcParams["figure.figsize"] = (4, 6)
    plt.plot(game_title_2,score_list,label=label)
    plt.xticks(game_title_2, rotation=90, fontsize=7)
    plt.ylabel('sim_score')
    plt.savefig('./sim_score.png')

    title = '게임 댓글 유사도 '
    plt.title(title)
    plt.legend()

    plt.savefig('./sim_score.png')

    plt.show()

    print(top_10_df)

    return recMovieList.iloc[:, 0]
    # print(recMovieList)

# 가중치 불러오기
Tfidf_matrix = mmread('./models/Tfidf_Game_review01.mtx').tocsr()
with open('./models/tfidf01.pickle', 'rb') as f:
    Tfidf = pickle.load(f)
# 모델 불러오기
embedding_model = Word2Vec.load('./models/word2vecModel_Game.model')
key_word = '혜자'
# print(key_word)
sim_word = embedding_model.wv.most_similar(key_word, topn=10)
sentence = [key_word] * 11

words = []

for word, _ in sim_word:
    words.append(word)
for i, word in enumerate(words):
    sentence += [word] * (10 - 1)

sentence = ' '.join(sentence)
sentence_vec = Tfidf.transform([sentence])
cosine_sim = linear_kernel(sentence_vec, Tfidf_matrix)


#cosine_sim = linear_kernel(Tfidf_matrix[movie_idx], Tfidf_matrix)
recommendation = getRecommendation(cosine_sim)
# print(recommendation)