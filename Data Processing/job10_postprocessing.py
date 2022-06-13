import pandas as pd

df = pd.read_csv('./crawling_data/datasets/Game_reviews_ALL_Preprocessing_2.csv')
df.dropna(inplace=True)
print(df.head())
df.info()

stopwords = pd.read_csv('./crawling_data/stopwords.csv')
stopwords_list = list(stopwords['stopword'])
cleaned_sentences = []
stopwords_movie = ['게임', '좋다','있다','없다','같다','리뷰','해주다','이다','재밌다','되다',
                   '있다','것','정도','오다','이건']
stopwords_list = stopwords_list + stopwords_movie
for review in df.cleaned_sentences:
    review_word = review.split(' ')

    words = []
    for word in review_word:
        if len(word) > 1:
            if word not in stopwords_list:
                words.append(word)
    cleaned_sentence = ' '.join(words)
    cleaned_sentences.append(cleaned_sentence)
df['cleaned_sentences'] = cleaned_sentences
df.dropna(inplace=True)
df.to_csv('./crawling_data/datasets/Game_reviews_ALL_Post.csv',encoding='utf-8-sig',
          index=False)
df.info()
print('end')