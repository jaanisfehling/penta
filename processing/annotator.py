import spacy, jsonlines


# Load raw text from JSON file
with jsonlines.open('../data/instagram_comments.json', encoding='UTF-8') as f:
    comment_data = f.read()

# Load existing word data
with jsonlines.open('../data/word_classification.json', encoding='UTF-8') as f:
    word_classification = f.read()


# Load german pipeline for Tokenizer
nlp = spacy.load('de_dep_news_trf')



# Calculate new value for big-five
# (old_value * occurances + added_value) / (occurances + 1)
def calc(old_value, added_value, occurances):
    return (old_value * occurances + added_value) / (occurances + 1)



for user in comment_data.keys():
    print(comment_data.get(user))
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

    for token in nlp(comment_data.get(user)):
        # Lemmatize Words
        word = token.lemma_
        if word not in word_classification.keys():
            word_classification.update({word: ([o, c, e, a, n], 1)})
        else:
            old_o = word_classification.get(word)[0][0]
            old_c = word_classification.get(word)[0][1]
            old_e = word_classification.get(word)[0][2]
            old_a = word_classification.get(word)[0][3]
            old_n = word_classification.get(word)[0][4]
            occurances = word_classification.get(word)[1]

            new_o = calc(old_o, o, occurances)
            new_c = calc(old_c, c, occurances)
            new_e = calc(old_e, e, occurances)
            new_a = calc(old_a, a, occurances)
            new_n = calc(old_n, n, occurances)

            word_classification.update({word: ([new_o, new_c, new_e, new_a, new_n], occurances + 1)})


with jsonlines.open('../data/word_classification.json', mode='w') as f:
    f.write(word_classification)
