# https://www.youtube.com/watch?v=F0kGZjkmG18&t=1069s --- > Youtube taking top 4 to 5 sentence for
# summary usimg Spacy -- > extraction based text summary 

# https://www.youtube.com/watch?v=Y6UsgLmU4UM ---> project purely based on spacy and frequency anfd use the spacy ModuleNotFoundError

# https://towardsdatascience.com/text-summarization-using-tf-idf-e64a0644ace3 -- > extraction based using TF - IDF/


import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest

text = """Role in Freedom Struggle Subhas Chandra Bose joined the Indian National 
Congress (INC) under the influence of Mahatma Gandhi and started the newspapers called 
“Swaraj” which means self-governance which marks his entry into politics and his role in 
the freedom struggle in India has just started. Chittaranjan Das was his mentor. In the year
 1923, he became the President of the All India Youth Congress and became the editor of the 
 newspaper “Forward” started by C.R. Das himself. He had also been elected as the mayor of 
 Calcutta back then. He gained leadership spirit and made his way up to the top in the INC
   very soon. In 1928, the Motilal Nehru Committee demanded Dominion Status in India but 
   Subhash Chandra Bose along with Jawaharlal Nehru asserted that nothing would satisfy
     other than complete independence of India from the British. Gandhiji strongly opposed 
the ways of Bose, who wanted independence by hook or by crook, as he was a firm believer of 
non-violence itself. He was sent to jail in 1930 during the Civil Disobedience movement but 
was related along with other prominent leaders in the year 1931 when the Gandhi-Irwin pact 
was signed. In 1938, he was elected as President at the Haripura session of the INC and 
re-elected at the Tripuri Session in 1939 by competing against Dr P. Sitaramayya who was 
supported by Gandhi himself. He maintained strict standards during the commencement of the 
first World War and demanded full independence of India from the British within six months. 
He faced vehement objections from inside the Congress which led him to resign from INC and 
form a more progressive group called the “Forward Bloc”"""


def summarizer(rawdocs):
    stopwords = list(STOP_WORDS)
    # print(stopwords)
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(rawdocs)
    # print(doc)
    tokens = [token.text for token in doc]
    # print(tokens)
    word_freq = {}
    for word in doc:
        if word.text.lower() not in stopwords and word.text.lower() not in punctuation:
            if word.text not in word_freq.keys():
                word_freq[word.text] = 1 
            else:
                word_freq[word.text] += 1
    # print(word_freq)

    # return doc ,word_freq

    max_freq = max(word_freq.values())
    # print(max_freq)

    for word in word_freq.keys():
        word_freq[word] = word_freq[word]/max_freq
    # print(word_freq)

    sent_tokens = [sent for sent in doc.sents]
    # print(sent_tokens)

    sent_scores = {}
    for sent in sent_tokens:
        for word in sent:
            if word.text in word_freq.keys():
                if sent not in sent_scores.keys():
                    sent_scores[sent] = word_freq[word.text]
                else:
                    sent_scores[sent] += word_freq[word.text]
    # print(sent_scores)

    select_len = int (len(sent_tokens) * 0.45 )
    # print(select_len)

    summary = nlargest(select_len , sent_scores , key = sent_scores.get)
    # print(summary)

    final_summary = [ word.text for word in summary]
    summary = ' '.join(final_summary)
    # print(text)
    # print(summary)
    # print('Length of original Text', len(text.split(' ')))
    # print('Length of summary' , len(summary.split(' ')))
    return summary, doc, len(rawdocs.split(' ')), len(summary.split(' '))
