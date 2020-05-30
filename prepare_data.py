import nltk
# nltk.download('stopwords')
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re
import os
import csv

files_pos = os.listdir('/home/pain/Downloads/aclImdb_v1/aclImdb/train/pos')
files_pos = [open('/home/pain/Downloads/aclImdb_v1/aclImdb/train/pos/'+f, 'r').read() for f in files_pos]
files_neg = os.listdir('/home/pain/Downloads/aclImdb_v1/aclImdb/train/neg')
files_neg = [open('/home/pain/Downloads/aclImdb_v1/aclImdb/train/neg/'+f, 'r').read() for f in files_neg]

with open('sentiment_data.csv', mode='w') as f:
    f_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    f_writer.writerow(['text', 'neg_word' ,'sentiment'])
    all_words = []
    for p in  files_pos:
        stop_words = list(set(stopwords.words('english')))
        allowed_word_types = ["J"]
        # p = "I am a big fan of Arnold Vosloo. Finally seeing him as the star of a recent movie, not just a bit part, made me happy.<br /><br />Unfortunately I took film appreciation in college and the only thing I can say that I didn't like was that the film was made in an abandoned part of town and there was no background traffic or lookie loos.<br /><br />I have to say that the acting leaves something to be desired, but Arnold is an excellent actor, I have to chalk it up to lousy direction and the supporting cast leaves something to be desired.<br /><br />I love Arnold Vosloo, and he made the film viewable. Otherwise, I would have written it off as another lousy film.<br /><br />I found the rape scene brutal and unnecessary, but the actors that got away at the end were pretty good. But the sound effects of the shoot-out were pretty bad. There are some glitches in the film (continuity) but they are overlookable considering the low-caliber of the film.<br /><br />All in all I enjoyed the film, because Arnold Vosloo was in it.<br /><br />Jackie"
        # p = p.lower()
        cleanr = re.compile('<.*?>')
        text = re.sub(cleanr, '', p)
        cleaned = re.sub(r"[^(a-zA-Z')\s]",'', text)
        tokenized = word_tokenize(cleaned)
        # stopped = [w for w in tokenized if not w in stop_words]
        # print(tokenized)
        pos = nltk.pos_tag(tokenized)
        for w in pos:
            if w[1][0] in allowed_word_types:
                all_words.append(w[0].lower())
        print(pos)
        print(all_words)
        doc = ' '.join(all_words)
        print(doc)
        f_writer.writerow([doc,0,1])
    all_words2 = []
    for p in files_neg:
        stop_words = list(set(stopwords.words('english')))
        allowed_word_types = ["J"]
        # p = "I am a big fan of Arnold Vosloo. Finally seeing him as the star of a recent movie, not just a bit part, made me happy.<br /><br />Unfortunately I took film appreciation in college and the only thing I can say that I didn't like was that the film was made in an abandoned part of town and there was no background traffic or lookie loos.<br /><br />I have to say that the acting leaves something to be desired, but Arnold is an excellent actor, I have to chalk it up to lousy direction and the supporting cast leaves something to be desired.<br /><br />I love Arnold Vosloo, and he made the film viewable. Otherwise, I would have written it off as another lousy film.<br /><br />I found the rape scene brutal and unnecessary, but the actors that got away at the end were pretty good. But the sound effects of the shoot-out were pretty bad. There are some glitches in the film (continuity) but they are overlookable considering the low-caliber of the film.<br /><br />All in all I enjoyed the film, because Arnold Vosloo was in it.<br /><br />Jackie"
        # p = p.lower()
        cleanr = re.compile('<.*?>')
        text = re.sub(cleanr, '', p)
        cleaned = re.sub(r"[^(a-zA-Z')\s]",'', text)
        tokenized = word_tokenize(cleaned)
        # stopped = [w for w in tokenized if not w in stop_words]
        # print(tokenized)
        pos = nltk.pos_tag(tokenized)
        for w in pos:
            if w[1][0] in allowed_word_types:
                all_words2.append(w[0].lower())
        print(pos)
        print(all_words2)
        doc = ' '.join(all_words2)
        print(doc)
        f_writer.writerow([doc,0,0])
f.close()