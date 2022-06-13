import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import collections
from matplotlib import font_manager, rc
import matplotlib as mpl
import numpy as np
from PIL import Image

fontpath = './malgun.ttf'
font_name = font_manager.FontProperties(
    fname=fontpath).get_name()
mpl.rcParams['axes.unicode_minus']=False
rc('font', family=font_name)

df = pd.read_csv('./crawling_data/datasets/Game_reviews_ALL_Post.csv')
print(df.head())

words = df.iloc[3, 1]
print(words)

words = words.split()
print(words)

worddict_1 = collections.Counter(words)
worddict_1 = dict(worddict_1)
print(worddict_1)

words = df.iloc[4, 1]
print(words)

words = words.split()
print(words)

worddict_2 = collections.Counter(words)
worddict_2 = dict(worddict_2)

wordcloud_img_1 = WordCloud(
    background_color='white', max_words=2000,
    font_path=fontpath).generate_from_frequencies(worddict_1)

wordcloud_img_2 = WordCloud(
    background_color='white', max_words=2000,
    font_path=fontpath).generate_from_frequencies(worddict_2)

plt.figure(figsize=(12, 12))
plt.imshow(wordcloud_img_1, interpolation='bilinear')
plt.axis('off')

plt.figure(figsize=(12, 12))
plt.imshow(wordcloud_img_2, interpolation='bilinear')
plt.axis('off')
plt.show()