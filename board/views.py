from django.shortcuts import render
import pandas as pd
from sklearn.metrics.pairwise import linear_kernel
from scipy.io import mmread, mmwrite
import pickle
from gensim.models import Word2Vec
import requests
from bs4 import BeautifulSoup
import time
import random
from django.template.base import Library
# Create your views here.
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36'}


def home(request):
    return render(request, 'home.html')



def getRecommendation(cosine_sim):
    df_reviews = pd.read_csv('C:/PJ/Game_RE_Django/board/Datasets/Game_reviews_ALL_Preprocessing_2.csv')
    simScore = list(enumerate(cosine_sim[-1]))
    # print(len(simScore))
    # print(simScore)
    simScore = sorted(simScore, key=lambda x:x[1],
                      reverse=True)
    simScore = simScore[1:9]
    movieidx = [i[0] for i in simScore]
    recMovieList = df_reviews.iloc[movieidx]
    return recMovieList.iloc[:, 0]

def getscores(cosine_sim):
    df_reviews = pd.read_csv('C:/PJ/Game_RE_Django/board/Datasets/Game_reviews_ALL_Preprocessing_2.csv')
    simScore = list(enumerate(cosine_sim[-1]))
    # print(len(simScore))
    # print(simScore)
    simScore = sorted(simScore, key=lambda x:x[1],
                      reverse=True)
    simScore = simScore[1:9]
    movieidx = [i[0] for i in simScore]
    recMovieList = df_reviews.iloc[movieidx]
    return recMovieList.iloc[:, 2]


def getgenres(cosine_sim):
    df_reviews = pd.read_csv('C:/PJ/Game_RE_Django/board/Datasets/Game_reviews_ALL_Preprocessing_2.csv')
    simScore = list(enumerate(cosine_sim[-1]))
    # print(len(simScore))
    # print(simScore)
    simScore = sorted(simScore, key=lambda x:x[1],
                      reverse=True)
    simScore = simScore[1:9]
    movieidx = [i[0] for i in simScore]
    recMovieList = df_reviews.iloc[movieidx]
    return recMovieList.iloc[:, 3]





def seacrh2(request):
    game_input = request.GET.get('st_name')
    Tfidf_matrix = mmread('C:/PJ/Game_RE_Django/board/Models/Tfidf_Game_review01.mtx').tocsr()

    with open('C:/PJ/Game_RE_Django/board/Models/tfidf01.pickle', 'rb') as f:
        Tfidf = pickle.load(f)
    embedding_model = Word2Vec.load('C:/PJ/Game_RE_Django/board/Models/word2vecModel_Game.model')
    key_word = game_input

    try:
        sim_word = embedding_model.wv.most_similar(key_word, topn=10)
    except:
        error = '제가 모르는 단어에요 ㅠㅠ'
        data = {'results': error}
        return False


    sentence = [key_word] * 11

    words = []

    for word, _ in sim_word:
        words.append(word)

    for i, word in enumerate(words):
        sentence += [word] * (10 - 1)

    sentence = ' '.join(sentence)
    sentence_vec = Tfidf.transform([sentence])
    cosine_sim = linear_kernel(sentence_vec, Tfidf_matrix)

    recommendation = getRecommendation(cosine_sim)
    recommendation = list(recommendation)

    getscore = getscores(cosine_sim)
    getscore = list(getscore)

    getgenre = getgenres(cosine_sim)
    getgenre = list(getgenre)

    ######################################
    game_link=[] # 공백제거필수
    image_link =[]
    # print(recommendation)
    for  i ,game in  enumerate (recommendation):

        game.split()
        # print(game)

        time_time = random.uniform(0,1)


        search = f'https://play.google.com/store/search?q={game}'+'&c=apps&hl=ko&gl=US'
        time.sleep(time_time)
        # print(search)

        # search =search + '&c=apps&hl=ko&gl=US'
        # print(search)
        requests.get(search)
        resp = requests.get(search, headers=headers)
        time.sleep(time_time)
        # print(resp)
        soup = BeautifulSoup(resp.text, 'html.parser')
        # print(soup)
        # print(soup)
        link = soup.find("div", {"class": "VfPpkd-EScbFb-JIbuQc TAQqTe"})
        # print(link)
        time.sleep(time_time)
        # print(link)
        link = link.find('a')['href']
        time.sleep(time_time)
        # print(str(link))
        # print(link)
        link = 'https://play.google.com' + link
        print(link)

        image = soup.find("div", {"class": "j2FCNc"})
        image = image.find('img')['src']

        game_link.append(link)
        image_link.append(image)

    results = []
    for i in range(8):
        result = {'recommendation':recommendation[i], 'game_link':game_link[i], 'image_link':image_link[i],
                  'genre':getgenre[i] , 'score':getscore[i]   }
        results.append(result)
    data = {'results':results}
    # error = {'error':error}
   

    print(game_input)
    return render(request, 'seacrh2.html',data)