import spacy
from pymongo import MongoClient
from crawler.crawler import settings


client = MongoClient(settings.MONGO_URI)
db = client[settings.MONGO_DATABASE]

# Load raw text from JSON file
comment_collection = db['comments']
comments = comment_collection.find_one()

# Load existing word data
word_collection = db['classified_words']
classified_words = word_collection.find_one()


# Load german pipeline for Tokenizer
nlp = spacy.load('de_dep_news_trf')



# Calculate new value for big-five
# (old_value * occurances + added_value) / (occurances + 1)
def calc(old_value, added_value, occurances):
    return (old_value * occurances + added_value) / (occurances + 1)



for username in comments.keys():
    print(comments.get(username))
    o = input('Openess to Experience: 0.')
    o = float('0.' + o)
    c = input('Conscientiousness: 0.')
    c = float('0.' + c)
    e = input('Extraversion: 0.')
    e = float('0.' + e)
    a = input('Agreeableness: 0.')
    a = float('0.' + a)
    n = input('Neuroticism: 0.')
    n = float('0.' + n)

    for token in nlp(comments.get(username)):
        # Lemmatize Words
        word = token.lemma_
        if word not in classified_words.keys():
            classified_words.update({word: ([o, c, e, a, n], 1)})
        else:
            old_o = classified_words.get(word)[0][0]
            old_c = classified_words.get(word)[0][1]
            old_e = classified_words.get(word)[0][2]
            old_a = classified_words.get(word)[0][3]
            old_n = classified_words.get(word)[0][4]
            occurances = classified_words.get(word)[1]

            new_o = calc(old_o, o, occurances)
            new_c = calc(old_c, c, occurances)
            new_e = calc(old_e, e, occurances)
            new_a = calc(old_a, a, occurances)
            new_n = calc(old_n, n, occurances)

            # Update DB
            word_collection.update_one({word: ([old_o, old_c, old_e, old_a, old_n], occurances)}, {'$set': {word: ([new_o, new_c, new_e, new_a, new_n], occurances + 1)}})

client.Close()
