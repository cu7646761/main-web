import csv, random
import pandas as pd
import re
pos_dict = {
    'good':3, 'best':3, 'yummy':3, 'clean':1, 'nice':3, 'beautiful':4, 'ok':1, 'oke':1, 'love':1, 'like':1,
    'polite':1, 'awesome':1, 'happy':1, 'great':1, 'perfect':1, 'delicious':3, 'well':1, 'cool':1, 'appreciate':1,
    'cozy':1, 'lovely':1, ' reasonably':1, 'cheap':1, 'fast':1 ,'tasty':1, 'affordable':1, 'attractive':1, 'cute':1,
    'pretty':3, "vibe":1, "dedicated":1, 'quiet':1, 'convenient':1, 'exciting':1, 'excited':1, 'amazing':1, 'enjoy':1,
    'enjoyed':1, 'pleasure':1, 'pleased':1, 'friendly':1, 'quick':1, 'satisfied':1, 'wonderfull':1, 'okay':1, 
    'enthusiastic':1, 'loved':1, 'highly':1, 'impress':1 ,'impressed':1, 'impression':1, 'liked':1, 'appreciate':1
}
neg_dict = {
    'bad':1, 'worst':1, 'disgusting':1, 'dirty':1, 'ugly':1, 'hate':1, 'impolite':1, 'sad':1, 'disappointed':1, 'dislike':1,
    'poor':1, 'noisy':1, 'expensive':1, 'fuck':3, 'fucking':3, 'lousy':2, 'slow':1, 'slowly':1, 'small':1, 'lack':1, 'weak':1,
    'broken':1, 'disregard':1, 'wasted':1, 'boring':1, 'horrible':1, 'angry':1, 'careless':1, 'failed':1, 'dissatisfied':1,
    'chemicals':1 , 'chemical':1, 'unsafe':1, 'unloading':1, 'suck':1, 'shit':1
}
neg_words = {
    'no':1, 'not':1, 'nerver':1, "won't":1, "aren't":1, "don't":1, "isn't":1, "doesn't":1, "can't":1, "couldn't":1, 'none':1,
    "haven't":1, "hasn't":1, "didn't":1, "wasn't":1, "weren't":1, "wouldn't":1, 'hardly':1, , 'k':1, 'ko':1
}
temp_dict = {
    'simple':1, 'normal':1, 'temporary':1, 'ordinary':1, 'dc':1, 'tam':1, 'normally':1, 'average':1 
}
neutrals = {
    'staff':3, 'staffs':3, 'i':1, 'me':1,
    'food':3, 'foods':3, 'place':3, 'places':3, 'service':3,
    'service':1, 'services':1, 'restaurant':1, 'restaurants':1, 'space':1, 'spaces':1,
    'atmosphere':1, 'price':1, 'prices':1, 'taste':1, 'table':1, 'shop':1, 'seat':1,
    'seats':1, 'family':1, 'meal':1, 'people':1, 'meals':1, 'dinner':1, 'view':1, 'design':1,
    'friend':1, 'friends':1, 'customer':1, 'customers':1, 'waiter':1, 'waitress':1, 'dish':1, 'dishes':1,
    'time':1, 'times':1, 'quality':1, 'location':1, 'decoration':1, 'lunch':1, 'style':1, 'town':1, 'experience':1,
    'floor':1, 'cuisine':1, 'center':1, 'everything':1, 'air':1, 'money':1, 'one':1, 'some':1, 'more':1, 'choice':1
}
# with open('', 'a+', newline='') as write_obj:
#     # Create a writer object from csv module
#     csv_writer = writer(write_obj)
#     # Add contents of list as last row in the csv file
#     csv_writer.writerow(list_of_elem)

# odf = pd.read_csv('/home/pain/Downloads/Reviews.csv', usecols=['Text', 'Score'])
# df = odf[odf['Score'] != 2]
# df = df[df['Score'] != 3]
# df = df[df['Score'] != 4]
# print(df.iloc[0]['Score'])
with open('sentiment_data.csv', 'w') as f:
    f_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    # Create a writer object from csv module
    # csv_writer = writer(write_obj)
    # Add contents of list as last row in the csv file
    f_writer.writerow(['text', 'score'])
    # for index, row in df.iterrows():
    #     raw_text = row['Text'].lower()
    #     cleaned = re.sub(r'[^(a-zA-Z")\s]','', raw_text)
    #     score = 0 if row['Score']==1 else 2
    #     list_of_elem = [cleaned, score]
    #     f_writer.writerow(list_of_elem)
    #     print(list_of_elem)

    # good sentiment
    choice = []
    for k,v in pos_dict.items():
        for i in range(v):
            choice.append(k)
        f_writer.writerow([k, 2])
    for i in range(60000):
        sentence = random.randint(2, 20)
        text = ""
        for j in range(sentence):
            temp = random.choice(choice)
            noise = random.choice(list(neutrals.keys()))
            text += noise + " " + noise + " " + temp + " " + noise + " " + noise + " "
        f_writer.writerow([text, 2])appreciate
        print([text, 2])
    # negative pos
    for i in range(2000):
        for k,v in neg_words.items():
            temp = random.choice(choice)
            noise3 = random.choice(list(neutrals.keys()))
            noise4 = random.choice(list(neutrals.keys()))
            sentence = random.randint(2, 20)
            text = ""
            for j in range(sentence):
                noise = random.choice(list(neutrals.keys()))
                text += noise + " "
            
            text += " " + k + " " + temp + " " + noise3 + " " + noise4 + " "
            f_writer.writerow([text, 0])
            print([text, 0])
    # bad sentiment
    choice = []
    for k,v in neg_dict.items():
        for i in range(v):
            choice.append(k)
        f_writer.writerow([k, 0])
    for i in range(60000):
        sentence = random.randint(2, 20)
        text = ""
        for j in range(sentence):
            temp = random.choice(choice)
            noise = random.choice(list(neutrals.keys()))
            text += noise + " " + noise + " " + temp + " " + noise + " " + noise + " "
        f_writer.writerow([text, 0])
        print([text, 0])
    # negative neg
    for i in range(2000):
        for k,v in neg_words.items():
            temp = random.choice(choice)
            noise3 = random.choice(list(neutrals.keys()))
            noise4 = random.choice(list(neutrals.keys()))
            sentence = random.randint(2, 20)
            text = ""
            for j in range(sentence):
                noise = random.choice(list(neutrals.keys()))
                text += noise + " "
            text += " " + k + " " + temp + " " + noise3 + " " + noise4 + " "
            f_writer.writerow([text, 1])
            print([text, 1])
    # temp sentiment
    choice = []
    for k,v in temp_dict.items():
        f_writer.writerow([k, 1])
        for i in range(v):
            choice.append(k)
    for k,v in neutrals.items():
        choice.append(k)

    for i in range(60000):
        sentence = random.randint(2, 20)
        text = ""
        for j in range(sentence):
            temp = random.choice(choice)
            noise = random.choice(list(neutrals.keys()))
            text += noise + " " + noise + " " + temp + " " + noise + " " + noise + " "
        f_writer.writerow([text, 1])
        print([text, 1])
    # negative temp
    for i in range(2000):
        for k,v in neg_words.items():
            temp = random.choice(choice)
            noise3 = random.choice(list(neutrals.keys()))
            noise4 = random.choice(list(neutrals.keys()))
            sentence = random.randint(2, 20)
            text = ""
            for j in range(sentence):
                noise = random.choice(list(neutrals.keys()))
                text += noise + " "
            
            text += " " + k + " " + temp + " " + noise3 + " " + noise4 + " "
            f_writer.writerow([text, 0])
            print([text, 0])
f.close()

