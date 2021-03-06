# from google.cloud import automl_v1beta1 as automl
from pymongo import MongoClient
from google.cloud import language_v1
from google.cloud.language_v1 import enums
from google.cloud import translate
from app.model.comment import CommentModel
import nltk,re
import pandas
import datetime, time
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from mongoengine.queryset.visitor import Q

from app import create_app
import os
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/home/pain/Downloads/Britcat3-dd9d79d99d97.json"
import csv, random, json

from functools import wraps
import time
import math
import requests
from constants import Pages, POS_DICT, BAD_DICT, NEG_WORDS, TEMP_DICT, NEUTRAL_WORDS
from flask import redirect, render_template, Blueprint, session, request, request, jsonify, make_response


from app.model.store import StoreModel
from app.model.comment import CommentModel
from app.model.category import CategoryModel
from app.model.address import AddressModel


from utils import Utils
from constants import CLASS_LIST

from flask.helpers import url_for

analyze_blueprint = Blueprint(
    'analyze', __name__, template_folder='templates')

# do not run manual
@analyze_blueprint.route("/remove_character17273747", methods=["GET","POST"])
def remove_inv_char():
    all_stores = StoreModel().query_all()
    for store in all_stores:
        entity = store.entity_score
        invalid_key = []
        for k,v in entity.items():
            if '.' in k or '$' in k:
                print(k)
                invalid_key.append(k)
        for k in invalid_key:
            newkey = k.replace("."," ")
            newkey = newkey.replace("$"," ")
            entity[newkey] = entity.pop(k)
            print("----->", newkey)
        if len(invalid_key) > 0:
            store.update(set__entity_score=entity)
            

# do not run manual
@analyze_blueprint.route("/analyze17273747", methods=["GET","POST"])
def analyze():
    # all_stores = StoreModel().query_all()
    c =0
    stores = StoreModel().find_by_categories('5e95c640d971b716129d2ff4')
    for store in all_stores:
    # sid = '5e95d6a8d971b716129e158f'
    
    # store = StoreModel().find_by_id(sid)[0]
    
        cmts = CommentModel().find_by_store_id(store.id)
        print(len(cmts))
        # if store.entity_score:
        #     continue

        # entity_dict = {}
        entire_text = ""
        # entire_text_2 = ""
        # entire_text_3 = ""
        loops_no = 0
        for cmt in cmts:
            if cmt.detail is None or cmt.detail=="":
                continue
            text = cmt.detail
            if text.startswith('(Translated by Google)'):
                print(text)
                text = text.split('(Translated by Google)')[-1][1:]
                text = text.split('(Original)')[0]
            # if loops_no <= 400:
            entire_text += text
            # elif loops_no <= 800:
            #     entire_text_2 += text
            # else:
            #     entire_text_3 += text
            loops_no += 1
        
        # for sub_entire in (entire_text_1, entire_text_2, entire_text_3):
        #     if sub_entire == "":
        #         continue
        
        cleaned = re.sub(r"[^(a-zA-Z')\s]",'', entire_text)
        tokenized = word_tokenize(cleaned)
        stop_words = list(set(stopwords.words('english')))
        stopped = [w for w in tokenized if not w in stop_words]
        # print(tokenized)
        pos = nltk.pos_tag(stopped)
        all_words = ""
        allowed_word_types = ['J','N']
        for w in pos:
            if w[1][0] in allowed_word_types:
                if w[0].lower() not in("food", 'service', 'staff', 'place', 'space', 'restaurant', 'good', 'delicious', 'great'):
                    all_words += w[0].lower() + " "
        all_words += store.name_translate + " " +store.name_translate +" " + store.name_translate
        rs = Utils.predict_food_cate(all_words)
        print(all_words)
        print(rs)
        print(store.name)
        c+=1
        category_predict = max(rs, key=rs.get)
        store.update(set__type_store=rs, set__category_predict=category_predict)
    # if c==1:
    #     break
    return jsonify({})

                
        # for entity in response.entities:
        #     name = entity.name.upper()
        #     name = name.replace("$","")
        #     if not entity_dict.get(name, False):
        #         entity_dict[name] = {
        #             "quantity": 1,
        #             "sentiment": entity.sentiment.score
        #         }
        #     else:
        #         entity_dict[name] = {
        #             "quantity": entity_dict[name]["quantity"]+1,
        #             "sentiment": entity_dict[name]["sentiment"]+entity.sentiment.score                   
        #         }
        #     print((name, entity.sentiment.score))
        # store.update(set__entity_score=entity_dict)
        # print(store.entity_score)
                    
        


# @analyze_blueprint.route("/update_comment17273747", methods=["GET","POST"])
# def update_comment_to_analyze(store_id=None, page = 1, db = list(), form=None, error=None):
#     all_stores = StoreModel().query_all()
#     for store in all_stores:
#         cmts = CommentModel().findAllById(store.comment_list)
#         for cmt in cmts:
#             text = cmt[0].detail
#             if text.startswith('(Translated by Google)'):
#                 print(text)
#                 text = text.split('(Translated by Google)')[-1][1:]
#                 text = text.split('(Original)')[0]
#                 cmt[0].update(set__detail=text)
#                 print(cmt[0].detail)
                
# do not run manual 
@analyze_blueprint.route("/remove_duplicate17273747", methods=["GET", "POST"])
def remove_duplicate():
    all_stores = StoreModel().query_all()
    for store in all_stores:
        for k,v in store.entity_sentiment.items():
            if k[-1] == "S":
                print((k, v))
                text = k[:-1]
                quant_l = v["quantity"]
                sentiment_l = v["sentiment"]
                entity_r = store.entity_sentiment.get(text, False)
                if entity_r:
                    quant = quant_l + entity_r["quantity"] 
                    sentiment = sentiment_l + entity_r["sentiment"]
                    print(text, quant, sentiment)
            if k[-3:len(k)] == 1:
                print((k, v))
                text = k[:-3]
                quant_l = v["quantity"]
                sentiment_l = v["sentiment"]
                entity_r = store.entity_sentiment.get(text, False)
                if entity_r:
                    quant = quant_l + entity_r["quantity"] 
                    sentiment = sentiment_l + entity_r["sentiment"]
                    print(text, quant, sentiment)


# do not run manual 
@analyze_blueprint.route("/add_position17273747", methods=["GET", "POST"])
def add_position():
    all_stores = StoreModel().query_all()
    for store in all_stores:
        address = AddressModel().find_by_id(store.address_id)[0]
        pos={
            "lat": address.latitude,
            "lng": address.longtitude
        }
        store.update(set__position=pos)
        print(store.name)
    return jsonify({})


@analyze_blueprint.route("/gen-entity17273747", methods=["GET", "POST"])
def gen_entity():
    random.seed()
    food_cate = {}
    food_cate['japanese'] = {
        'tiramisu':1, 'sushi':3, 'tempura':1, 'sashimi':1, 'kaiseki':1, 'ryori':1,    
        'yakitori':1, 'mochi':1, 'tonkatsu':1, 'shabu':1, 'shabu-shabu':1, 'soba':1, 
        'ramen':1, 'donburi':1, 'onigiri':1, 'japan':4, 'japanese':4, 'dorayaki':1,
        'somen':1, 'miso':1, 'bento':1, 'salmon':1, 'wasabi':2, 'tokyo':3, 'miya':1
    }
    food_cate['korean'] = {
        'kimchi':2, 'tteokbokki':1, 'spicy':1, 'korea':3 , 'korean':4, 'bulgogi':1,
        'tobboki':1, 'bibimbap':1, 'kimbap':1, 'tok':1, 'udon':1, 'tokbokki':1, 'jjajangmyeon':1,
        'blackbean':1, 'koreans':3
    }
    food_cate['seafood'] = {
        'shrimp':3, 'crab':3, 'fish':2, 'oysters':3, 'scallops':1, 'clam':1, 'seafood':3,
        'crabs':3, 'shrimps':3, 'fishes':1, 'oyster':3, 'scallop':1, 'crustacean':1, 'crustaceans':1,
        'lobster':1, 'sea':1, 'seafoods':1, 'snail':1, 'squid':1, 'squids':1, 'octopus':1
    }
    food_cate['fastfood'] = {
        'pizza':1, 'pizzas':1, 'fastfood':1, 'fastfoods':1, 'hamburger':1, 'hamburgers':1, 'pasta':1, 'pastas':1,
        'spaghetti':1, 'spaghetties':1, 'snack':1, 'snacks':1
    }
    food_cate['vegetarian'] = {
        'vegetarian':3, 'veggie':3, 'mushroom':2, 'mushrooms':2, 'veggies':3, 'buddha':1, 'chay':3,
        'bean':2, 'tofu':3, 'soy':2, 'vegetarians':3, 'tofus':3, 'soys':1, 'beans':1, 'veterinarian':1,
        'veterinarians':1, 'seitan':1, 'seitans':1, 'vegan':3, 'vegans':3, 'monk':1, 'monks':1, 'vegie':2,
        'vegies':2
    }
    food_cate['cafe'] = {
        'drink':1, 'drinks':1, 'drinking':1, 'drinkings':1, 'cafe':1, 'coffee':1, 'matcha':1,
        'ice':1, 'cream':1, 'parfait':1, 'tea':1, 'milks':1, 'milk':1, 'water':1, 'waters':1,
        'topping':1, 'toppings':1, 'peach':1, 'music':1, 'espresso':1, 'machiato':1,
        'capuchino':1, 'bubble':1, 'latte':1, ' cocktail':1
    }
    food_cate['smoothie'] = {
        'fruit':1, 'fruits':1, 'smoothie':1, 'juice':1, 'juices':1, 'beams':1, 'beam':1,
        'avocado':1, 'avocados':1, 'durian':1, 'durians':1, 'yogurt':1, 'yogurts':1,
        'yoghurt':1, 'yoghurts':1, 'butter':1, 'peach':1
    }
    food_cate['cake'] = {
        'cake':2, 'cakes':2, 'chocolate':1, 'chocolates':1, 'dessert':1, 'desserts':1, 'tiramisu':1,
        'cookie':1, 'cookies':1, 'pastry':1, 'muffin':1, 'bakery':1, 'bread':1, 'breads':1
    }
    food_cate['drinking'] = {
        'beer':2, 'beers':2, 'wine':1, 'wines':1, 'pot':1, 'pots':1, 'sheep':1,
        'lamb':1, 'goat':1, 'calve':1, 'calves':1, 'goats':1, 'lamps':1, 'sheeps':1,
        'gang':1, 'gangs':1, 'cider':1, 'ciders':1, 'ancohol':1, 'heineken':1
    }
    food_cate['meat-beaf'] = {
        'meat':1, 'meats':1, 'rib':1, 'dip':1, 'grill':1, 'grills':1, 'ribs':1, 'dips':1,
        'beef':1, 'beefs':1, 'bbq':1, 'steak':1, 'steaks':1, 'barbecues':1, 'barbecue':1,
        'beefsteak':1, 'beefsteaks':1, 'cow':1, 'cows':1, 'pig':1, 'pigs':1, 'kebab':1, 'kebabs':1,
        'shawarma':1, 'roll':1, 'rolls':1
    }
    food_cate['chicken'] = {
        'chicken':1, 'chickens':1, 'kfc':1, 'texas':1, 'french':1, 'lotteria':1
    }
    food_cate['water-dish'] = {
        'soup':2, 'soups':2, 'vermicelli':1, 'vermicellies':2, 'noodles':1, 'noodle':1,
        'bun':1, 'pho':1, 'powder':1, 'broth':1, 'broths':1, 'porridge':1, 'porridges':1,
        'bowl':1, 'bowls':1
    }
    food_cate['bar-club'] = {
        'bar':1, 'bars':1, 'pub':1, 'pubs':1, 'beers':1, 'beer':1, 'wine':1, 'club':1,
        'clubs':1, 'dance':1, 'edm':1, 'vinahouse':1
    }
    other = {
        'staff':3, 'staffs':3, 'food':3, 'foods':3, 'place':3, 'places':3, 'service':3,
        'services':1, 'restaurant':1, 'restaurants':1, 'space':1, 'spaces':1,
        'atmosphere':1, 'price':1, 'prices':1, 'people':1}
    neutral = {
        'taste':1, 'table':1, 'shop':1, 'seat':1,
        'seats':1, 'family':1, 'meal':1, 'meals':1, 'dinner':1, 'view':1, 'design':1,
        'friend':1, 'friends':1, 'customer':1, 'customers':1, 'waiter':1, 'waitress':1, 'dish':1, 'dishes':1,
        'time':1, 'times':1, 'quality':1, 'location':1, 'decoration':1, 'lunch':1, 'style':1, 'town':1, 'experience':1,
        'floor':1, 'cuisine':1, 'center':1, 'everything':1, 'air':1, 'money':1, 'one':1, 'some':1, 'more':1, 'choice':1
    }
    with open('food_entity2.csv', mode='w') as f:
        f_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        f_writer.writerow(['text', 'classsification'])
        
        for i in range(100):
            text_noise = ""
            sentence_neutral = random.randint(1, 20)
            for j in range(sentence_neutral):
                noise = random.choice(list(neutral.keys()))
                temp = random.choice(list(other.keys()))
                text_noise += temp + " " + noise + " " + noise + " " + noise + " "
            print(text_noise)
            f_writer.writerow([text_noise, 'other'])    
        for k,v in food_cate.items():
            choice = []
            for text,factor in v.items():
                for i in range(factor):
                    choice.append(text)
                f_writer.writerow([text, k])

            for i in range(len(v.items())*250):
                sentence1 = random.randint(2, 100)
                sentence2 = random.randint(101, 500)
                sentence3 = random.randint(500, 1000)
                text1 = ""
                text2 = ""
                text3 = ""
                for j in range(sentence1):
                    temp = random.choice(choice)
                    noise = random.choice(list(neutral.keys()))
                    text1 += temp + " " + noise + " " + noise + " " + noise + " "
                for j in range(sentence2):
                    temp = random.choice(choice)
                    noise = random.choice(list(neutral.keys()))
                    text2 += temp + " " + noise + " " + noise + " " + noise + " "
                for j in range(sentence3):
                    temp = random.choice(choice)
                    noise = random.choice(list(neutral.keys()))
                    text3 += temp + " " + noise + " " + noise + " " + noise + " "
                print(text1)
                print(text2)
                print(text3)
                f_writer.writerow([text1, k])
                f_writer.writerow([text2, k])
                f_writer.writerow([text3, k])
        
    f.close()
    return jsonify({})


# do not run manual 
@analyze_blueprint.route("/add-classify-cate17273747", methods=["GET", "POST"])
def add_classify():
    all_stores = StoreModel().query_all()
    j=0
    for store in all_stores:
        j+=1
        print(j)
        if store.category_predict !="":
            continue
        dict_entity = store.entity_score
        text = ""
        for entity in dict_entity.keys():
            for i in range(dict_entity[entity]["quantity"]):
                text += entity.lower() + " "
        text += " " + store.name_translate
        data = {
            "instances": [{
                "text": text
            }]
        }
        response = requests.post('http://localhost:8080/predict', json=data)
        result = json.loads(response.content)
        print(text)
        rsfm = result['predictions'][0]
        type_store = {}
        for i in range(len(rsfm["classes"])):
            type_store[rsfm["classes"][i]] = rsfm["scores"][i]
        category_predict = max(type_store, key=type_store.get)
        store.update(set__type_store=type_store, set__category_predict=category_predict)
    return jsonify({})


@analyze_blueprint.route("/add-name-translate17273747", methods=["GET", "POST"])
def add_classify_result():
    all_stores = StoreModel().query_all()
    i=0
    for store in all_stores:
        i+=1
        print(i)
        if store.name_translate:
            print(store.name_translate)
            continue
        tsl = sample_translate_text(store.name, "en-US", "britcat3")
        text = tsl.translations[0].translated_text.lower()
        store.update(set__name_translate=text)
        print(store.name_translate)
    return jsonify({})


@analyze_blueprint.route("/reset-type-store17273747", methods=["GET", "POST"])
def reset_type_store():
    all_stores = StoreModel().query_all()
    i=0
    for store in all_stores:
        i+=1
        print(i)
        if store.category_predict != "":
            store.update(set__category_predict="")
    return jsonify({})


@analyze_blueprint.route("/gen-sentiment-dictionary", methods=["GET", "POST"])
def gen_sentiment_dictionary():
    
    pos_dict = {
        'good':1, 'best':1, 'yami':1, 'yumi':1, 'clean':1, 'nice':1, 'beautiful':1, 'ok':1, 'oke':1, 'love':1, 'like':1,
        'polite':1, 'awesome':1, 'happy':1, 'great':1, 'perfect':1, 'delicious':1, 'well':1, 'cool':1, 'appreciate':1,
        'cozy':1, 'lovely':1, ' reasonably':1, 'cheap':1, 'fast':1 ,'tasty':1, 'affordable':1, 'attractive':1, 'cute':1
    }
    neg_dict = {
        'bad':1, 'worst':1, 'disgusting':1, 'dirty':1, 'ugly':1, 'hate':1, 'impolite':1, 'sad':1, 'disappointed':1, 'dislike':1,
        'poor':1, 'noisy':1, 'expensive':1
        
    }
    return jsonify({})

@analyze_blueprint.route("/update-sentiment-comment17273747", methods=["GET", "POST"])
def update_sentiment_comment():
    all_stores = StoreModel().query_all()
    all_comments = CommentModel().query_all()
    i=0
    for store in all_stores:
        cmts = CommentModel().find_by_store_id(store.id)
        for comment in cmts:
            
            i+=1
            print(i)
            cmt = comment
            if cmt.sentiment_dict or not cmt.detail:
                continue
            else:
                raw_text = cmt.detail
                if raw_text.startswith('(Translated by Google)'):
                    raw_text = raw_text.split('(Translated by Google)')[-1][1:]
                    raw_text = raw_text.split('(Original)')[0]
                text = raw_text.lower()
                data = {
                    "instances": [{
                        "text": text
                    }]
                }
                response = requests.post('http://localhost:8080/predict', json=data)
                result = json.loads(response.content)
                print(text)
                rsfm = result['predictions'][0]
                cmt.update(set__sentiment_dict=rsfm)
        
    return jsonify({})
    

@analyze_blueprint.route("/update-sentiment-store17273747", methods=["GET", "POST"])
def update_sentiment_store():
    all_stores = StoreModel().query_all()
    count = 0
    id = "5e963eb3d971b71612a3f5f5"
    store = StoreModel().find_by_id(id)[0]
    # for store in all_stores:
    count+=1
    print(count)
    print(store.name)
    # if store.score_sentiment:
    #     continue
    cmts = CommentModel().find_by_store_id(store.id)
    all_sentiment = 0
    j=0
    for comment in cmts:
        cmt = comment
        if not cmt.detail:
            continue
        j+=1
        print(j)

        raw_text = cmt.detail
        if raw_text.startswith('(Translated by Google)'):
            raw_text = raw_text.split('(Translated by Google)')[-1][1:]
            raw_text = raw_text.split('(Original)')[0]
        text = raw_text.lower()
        data = {
            "instances": [{
                "text": text
            }]
        }
        response = requests.post('http://localhost:8080/predict', json=data)
        result = json.loads(response.content)
        print(text)
        rsfm = result['predictions'][0] 
        cmt.update(set__sentiment_dict=rsfm)
        sentiment_cmt = {}
        for i in range(len(rsfm["classes"])):
            sentiment_cmt[rsfm["classes"][i]] = rsfm["scores"][i]
        sentiment = sentiment_cmt["0"]*(-1) + sentiment_cmt["2"]
        print(sentiment)
        all_sentiment += sentiment
    if j != 0:
        score_stm = all_sentiment/j
    else:
        score_stm = all_sentiment
    print(score_stm)
    store.update(set__score_sentiment=score_stm)
    print(store.name)

    return jsonify({})

@analyze_blueprint.route("/update-reviewer-quant17273747", methods=["GET", "POST"])
def update_reviewer_quant():
    all_stores = StoreModel().query_all()
    all_comments = CommentModel().query_all()
    count = 0
    for store in all_stores:
        count+=1
        print(count)
        print(store.fixed)
        if store.fixed:
            continue
        print(store.name)
        cmts = CommentModel().find_by_store_id(store.id)
        quant = len(cmts)
        store.update(set__reviewer_quant=quant, set__fixed=True)
        # if store.name =="Quán Hải Hiền - Quán Nhậu Bình Dân":
        #     break
        print(store.name)

    return jsonify({})


@analyze_blueprint.route("/test-predict-online17273747", methods=["GET", "POST"])
def test_predict_online():
    text = "very delicious The bread is super crunchy (not dry) I don't bad dare to eat pork, I think it 's delicious shocked 45000VND / 1 serving"
    tokenized = word_tokenize(text)
    # stopped = [w for w in tokenized if not w in stop_words]
    # print(tokenized)
    # allowed_word_types = ['J']
    pos = nltk.pos_tag(tokenized)
    ci = 0
    neg_good = 0
    neg_bad = 0
    for k,v in pos:
        ci+=1
        if k in ('not', "n't", 'hardly', 'never'):
            cj = ci
            for w in pos[ci:]:
                cj+=1
                if cj-ci>3:
                    break
                if w[0] in POS_DICT:
                    neg_good +=1
                    break
                if w[0] in BAD_DICT:
                    neg_bad +=1
                    break
                
    print(pos)
    print(neg_good)
    print(neg_bad)
    return jsonify({})


@analyze_blueprint.route("/get-comment-data17273747", methods=["GET", "POST"])
def get_comment_data():
    comments_good = CommentModel().objects(Q(star_num__gte=4) & Q(detail__ne='') & Q(detail__ne=None))[:5000]
    # comments_good_test = CommentModel().objects(Q(star_num__gte=4) & Q(detail__ne='') & Q(detail__ne=None))[:10000]
    comments_bad = CommentModel().objects(Q(star_num__lte=2) & Q(detail__ne='') & Q(detail__ne=None))[:5000]
    comments_temp = CommentModel().objects(Q(star_num__exact=3) & Q(detail__ne='') & Q(detail__ne=None))[:500]
    df = pandas.read_csv("Reviews.csv", usecols = ['Text', 'Score'])
    document = df.values

    with open('testset_sentiment.csv', mode='w') as f:
        f_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        f_writer.writerow(['split','text', 'score'])

        for s,t in document:
            # print(s)
            raw = t
            text = raw.lower()
            text = text.replace('\"','')
            cleaned = re.sub(r"[^(a-zA-Z')\s]",'', text)
            tokenized = word_tokenize(cleaned)
            allowed_word_types = ["J", "V", "R"]
            pos = nltk.pos_tag(tokenized)
            print(pos)
            text_input = ""
            for w in pos:
                if w[1][0] in allowed_word_types:
                    # all_words.append(w[0])
                    text_input += w[0] + " "
            score = s
            if score in (1,2,3):
                f_writer.writerow(['UNASSIGNED', text_input , 0])
            # elif score==3:
            #     f_writer.writerow([text_input , 1])
            elif score==5:
                f_writer.writerow(['UNASSIGNED', text_input , 2])
            print([text_input, score])

        for comment in comments_good:
            if comment.detail:
                raw_text = comment.detail
                if raw_text.startswith('(Translated by Google)'):
                    raw_text = raw_text.split('(Translated by Google)')[-1][1:]
                    raw_text = raw_text.split('(Original)')[0]
                text = raw_text.lower()
                input = text.replace('\"','')
                print(input)
                f_writer.writerow(['UNASSIGNED',input, 2])
        for comment in comments_bad:
            if comment.detail:
                raw_text = comment.detail
                if raw_text.startswith('(Translated by Google)'):
                    raw_text = raw_text.split('(Translated by Google)')[-1][1:]
                    raw_text = raw_text.split('(Original)')[0]
                text = raw_text.lower()
                text = text.replace('\"','')
                f_writer.writerow(['UNASSIGNED',text, 0])
        for comment in comments_temp:
            if comment.detail:
                raw_text = comment.detail
                if raw_text.startswith('(Translated by Google)'):
                    raw_text = raw_text.split('(Translated by Google)')[-1][1:]
                    raw_text = raw_text.split('(Original)')[0]
                text = raw_text.lower()
                text = text.replace('\"','')
                f_writer.writerow(['UNASSIGNED',text, 1])
        # df = pandas.read_csv("train.tsv", usecols = ['Phrase', 'Sentiment'], sep="\t")
        # document = df.values
        # for record in document:
        #     raw = record['Pharse']
        #     text = raw.lower()
        #     text = text.replace('\"','')

        pos_dict = {
            'good':3, 'best':3, 'yummy':3, 'clean':1, 'nice':3, 'beautiful':4, 'ok':1, 'oke':1  , 'love':1, 'like':1,
            'polite':1, 'awesome':1, 'happy':1, 'great':1, 'perfect':1, 'delicious':3, 'well':1, 'cool':1, 'appreciate':1,
            'cozy':1, 'lovely':1, ' reasonably':1, 'cheap':1, 'fast':1 ,'tasty':1, 'affordable':1, 'attractive':1, 'cute':1,
            'pretty':3, "vibe":1, "dedicated":1, 'quiet':1, 'convenient':1, 'exciting':1, 'excited':1, 'amazing':1, 'enjoy':1,
            'enjoyed':1, 'pleasure':1, 'pleased':1, 'friendly':1, 'quick':1, 'satisfied':1, 'wonderfull':1, 'okay':1, 
            'enthusiastic':1, 'loved':1, 'highly':1, 'impress':1 ,'impressed':1, 'impression':1, 'liked':1, 'appreciate':1, 'special':1,
            'lively':1, 'excellent':3, 'wonderful':1
        }
        neg_dict = {
            'bad':1, 'worst':1, 'disgusting':1, 'dirty':1, 'ugly':1, 'hate':1, 'impolite':1, 'sad':1, 'disappointed':1, 'dislike':1,
            'poor':1, 'noisy':1, 'expensive':1, 'fuck':3, 'fucking':3, 'lousy':2, 'slow':1, 'slowly':1, 'small':1, 'lack':1, 'weak':1,
            'broken':1, 'disregard':1, 'wasted':1, 'boring':1, 'horrible':1, 'angry':1, 'careless':1, 'failed':1, 'dissatisfied':1,
            'chemicals':1 , 'chemical':1, 'unsafe':1, 'unloading':1, 'suck':1, 'shit':1, 'hated':1, 'abhor':1, 'abominable':1
        }
        neg_words = {
            'no':1, 'not':1, 'nerver':1, "won't":1, "aren't":1, "don't":1, "isn't":1, "doesn't":1, "can't":1, "couldn't":1, 'none':1,
            "haven't":1, "hasn't":1, "didn't":1, "wasn't":1, "weren't":1, "wouldn't":1, 'hardly':1, 'k':1, 'ko':1
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
        choice = []
        for k,v in pos_dict.items():
            for i in range(v):
                choice.append(k)
            f_writer.writerow(['TRAIN', k, 2])
        for i in range(6000):
            sentence = random.randint(2, 20)
            text = ""
            for j in range(sentence):
                temp = random.choice(choice)
                noise = random.choice(list(neutrals.keys()))
                text += noise + " " + noise + " " + temp + " " + noise + " " + noise + " "
            f_writer.writerow(['TRAIN', text, 2])
            print([text, 2])
        for i in range(500):
            sentence = random.randint(2, 20)
            text = ""
            for j in range(sentence):
                temp = random.choice(choice)
                noise = random.choice(list(neutrals.keys()))
                text += noise + " " + noise + " " + temp + " " + noise + " " + noise + " "
            f_writer.writerow(['TRAIN', text, 2])
            print([text, 2])
        # negative pos
        for i in range(500):
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
                f_writer.writerow(['TRAIN', text, 0])
                print([text, 0])
        # bad sentiment
        choice = []
        for k,v in neg_dict.items():
            for i in range(v):
                choice.append(k)
            f_writer.writerow(['TRAIN', k, 0])
        for i in range(6000):
            sentence = random.randint(2, 20)
            text = ""
            for j in range(sentence):
                temp = random.choice(choice)
                noise = random.choice(list(neutrals.keys()))
                text += noise + " " + noise + " " + temp + " " + noise + " " + noise + " "
            f_writer.writerow(['TRAIN', text, 0])
            print([text, 0])

        for i in range(500):
            sentence = random.randint(2, 20)
            text = ""
            for j in range(sentence):
                temp = random.choice(choice)
                noise = random.choice(list(neutrals.keys()))
                text += noise + " " + noise + " " + temp + " " + noise + " " + noise + " "
            f_writer.writerow(['TRAIN', text, 0])
            print([text, 0])
        # negative neg
        for i in range(500):
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
                f_writer.writerow(['TRAIN', text, 1])
                print([text, 1])
        # temp sentiment
        choice = []
        for k,v in temp_dict.items():
            f_writer.writerow(['TRAIN', k, 1])
            for i in range(v):
                choice.append(k)
        for k,v in neutrals.items():
            choice.append(k)

        for i in range(10000):
            sentence = random.randint(2, 20)
            text = ""
            for j in range(sentence):
                temp = random.choice(choice)
                noise = random.choice(list(neutrals.keys()))
                text += noise + " " + noise + " " + temp + " " + noise + " " + noise + " "
            f_writer.writerow(['UNASSIGNED', text, 1])
            print([text, 1])
        
        for i in range(500):
            sentence = random.randint(2, 20)
            text = ""
            for j in range(sentence):
                temp = random.choice(choice)
                noise = random.choice(list(neutrals.keys()))
                text += noise + " " + noise + " " + temp + " " + noise + " " + noise + " "
            f_writer.writerow(['UNASSIGNED', text, 1])
            print([text, 1])
        # negative temp
        for i in range(500):
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
                f_writer.writerow(['TRAIN', text, 0])
                print([text, 0])
    f.close()


    return jsonify({})


@analyze_blueprint.route("/gen-comment-data17273747", methods=["GET", "POST"])
def gen_comment_data():
    comments_good = CommentModel().objects(Q(star_num__gte=4) & Q(detail__ne='') & Q(detail__ne=None))[:5000]
    # comments_good_test = CommentModel().objects(Q(star_num__gte=4) & Q(detail__ne='') & Q(detail__ne=None))[:10000]
    comments_bad = CommentModel().objects(Q(star_num__lte=2) & Q(detail__ne='') & Q(detail__ne=None))[:5000]
    comments_temp = CommentModel().objects(Q(star_num__exact=3) & Q(detail__ne='') & Q(detail__ne=None))[:500]
    with open('testset_sentiment.csv', mode='w') as f:
        f_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        f_writer.writerow(['split','text','neg_good','neg_bad', 'score'])
        for comment in comments_good:
            if comment.detail:
                raw_text = comment.detail
                if raw_text.startswith('(Translated by Google)'):
                    raw_text = raw_text.split('(Translated by Google)')[-1][1:]
                    raw_text = raw_text.split('(Original)')[0]
                text = raw_text.lower()
                text = text.replace('\"','')
                print(text)
                g,b = Utils.preprocessing_input(text)
                f_writer.writerow(['TEST', text, g, b, 2])
        for comment in comments_bad:
            if comment.detail:
                raw_text = comment.detail
                if raw_text.startswith('(Translated by Google)'):
                    raw_text = raw_text.split('(Translated by Google)')[-1][1:]
                    raw_text = raw_text.split('(Original)')[0]
                text = raw_text.lower()
                text = text.replace('\"','')
                g,b = Utils.preprocessing_input(text)
                f_writer.writerow(['TEST',text,g,b, 0])
        for comment in comments_temp:
            if comment.detail:
                raw_text = comment.detail
                if raw_text.startswith('(Translated by Google)'):
                    raw_text = raw_text.split('(Translated by Google)')[-1][1:]
                    raw_text = raw_text.split('(Original)')[0]
                text = raw_text.lower()
                text = text.replace('\"','')
                g,b = Utils.preprocessing_input(text)
                f_writer.writerow(['TEST',text,g,b, 1])
        # df = pandas.read_csv("train.tsv", usecols = ['Phrase', 'Sentiment'], sep="\t")
        # document = df.values
        # for record in document:
        #     raw = record['Pharse']
        #     text = raw.lower()
        #     text = text.replace('\"','')

        pos_dict = POS_DICT
        neg_dict = BAD_DICT
        neg_words = NEG_WORDS
        temp_dict = TEMP_DICT
        neutrals = NEUTRAL_WORDS
        choice = []
        for k,v in pos_dict.items():
            for i in range(v):
                choice.append(k)
            f_writer.writerow(['UNASSIGNED', k,0,0, 2])
        for i in range(60000):
            sentence = random.randint(2, 20)
            text = ""
            for j in range(sentence):
                temp = random.choice(choice)
                noise = random.choice(list(neutrals.keys()))
                text += noise + " " + noise + " " + temp + " " + noise + " " + noise + " "
            f_writer.writerow(['UNASSIGNED', text,0,0, 2])
            print([text,0,0, 2])
        for i in range(5000):
            sentence = random.randint(2, 20)
            text = ""
            for j in range(sentence):
                temp = random.choice(choice)
                noise = random.choice(list(neutrals.keys()))
                text += noise + " " + noise + " " + temp + " " + noise + " " + noise + " "
            f_writer.writerow(['TEST', text,0,0, 2])
            print([text,0,0, 2])
        # negative pos
        for i in range(2000):
            for k,v in neg_words.items():
                temp = random.choice(choice)
                distance_s = random.randint(0, 3)
                distance_l = random.randint(4, 20)
                s_distance = []
                l_distance = []
                for c in range(distance_s):
                    s_distance.append(random.choice(list(neutrals.keys())))
                for c in range(distance_l):
                    l_distance.append(random.choice(list(neutrals.keys())))
                noise3 = random.choice(list(neutrals.keys()))
                noise4 = random.choice(list(neutrals.keys()))
                sentence = random.randint(1, 5)

                #short dis
                text = ""
                for j in range(sentence):
                    noise = random.choice(list(neutrals.keys()))
                    text += noise + " "
                text += k+" "
                for ele in s_distance:
                    text += ele + " "
                text += temp + " " + noise3 + " " + noise4 + " "
                f_writer.writerow(['UNASSIGNED', text,1,0,0])
                print([text,1,0, 0])
                
                #long dis
                text = ""
                for j in range(sentence):
                    noise = random.choice(list(neutrals.keys()))
                    text += noise + " "
                text += k+" "
                for ele in l_distance:
                    text += ele + " "
                text += temp + " " + noise3 + " " + noise4 + " "
                f_writer.writerow(['UNASSIGNED', text,0,0,2])
                print([text,0,0,2])

                #revert
                text = ""
                distance_r = random.randint(1, 7)
                r_distance = []
                for c in range(distance_r):
                    r_distance.append(random.choice(list(neutrals.keys())))
                for j in range(sentence):
                    noise = random.choice(list(neutrals.keys()))
                    text += noise + " "
                text += temp+" "
                for ele in r_distance:
                    text += ele + " "
                text += k + " " + noise3 + " " + noise4 + " "
                f_writer.writerow(['UNASSIGNED', text,0,0,2])
                print([text,0,0,2])
        # bad sentiment
        choice = []
        for k,v in neg_dict.items():
            for i in range(v):
                choice.append(k)
            f_writer.writerow(['UNASSIGNED', k,0,0, 0])
        for i in range(60000):
            sentence = random.randint(2, 20)
            text = ""
            for j in range(sentence):
                temp = random.choice(choice)
                noise = random.choice(list(neutrals.keys()))
                text += noise + " " + noise + " " + temp + " " + noise + " " + noise + " "
            f_writer.writerow(['UNASSIGNED', text,0,0, 0])
            print([text,0,0, 0])

        for i in range(5000):
            sentence = random.randint(2, 20)
            text = ""
            for j in range(sentence):
                temp = random.choice(choice)
                noise = random.choice(list(neutrals.keys()))
                text += noise + " " + noise + " " + temp + " " + noise + " " + noise + " "
            f_writer.writerow(['TEST', text,0,0, 0])
            print([text,0,0, 0])
        # negative neg
        for i in range(2000):
            for k,v in neg_words.items():
                temp = random.choice(choice)
                distance_s = random.randint(0, 3)
                distance_l = random.randint(4, 20)
                s_distance = []
                l_distance = []
                for c in range(distance_s):
                    s_distance.append(random.choice(list(neutrals.keys())))
                for c in range(distance_l):
                    l_distance.append(random.choice(list(neutrals.keys())))
                noise3 = random.choice(list(neutrals.keys()))
                noise4 = random.choice(list(neutrals.keys()))
                sentence = random.randint(1, 5)

                #short dis
                text = ""
                for j in range(sentence):
                    noise = random.choice(list(neutrals.keys()))
                    text += noise + " "
                text += k+" "
                for ele in s_distance:
                    text += ele + " "
                text += temp + " " + noise3 + " " + noise4 + " "
                f_writer.writerow(['UNASSIGNED', text,0,1,1])
                print([text,0,1 ,1])
                
                #long dis
                text = ""
                for j in range(sentence):
                    noise = random.choice(list(neutrals.keys()))
                    text += noise + " "
                text += k+" "
                for ele in l_distance:
                    text += ele + " "
                text += temp + " " + noise3 + " " + noise4 + " "
                f_writer.writerow(['UNASSIGNED', text,0,0,0])
                print([text,0,0, 0])

                #revert
                text = ""
                distance_r = random.randint(1, 7)
                r_distance = []
                for c in range(distance_r):
                    r_distance.append(random.choice(list(neutrals.keys())))
                for j in range(sentence):
                    noise = random.choice(list(neutrals.keys()))
                    text += noise + " "
                text += temp+" "
                for ele in r_distance:
                    text += ele + " "
                text += k + " " + noise3 + " " + noise4 + " "
                f_writer.writerow(['UNASSIGNED', text,0,0,0])
                print([text,0,0, 0])
        # temp sentiment
        choice = []
        for k,v in temp_dict.items():
            f_writer.writerow(['UNASSIGNED', k,0,0, 1])
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
            f_writer.writerow(['UNASSIGNED', text,0,0, 1])
            print([text,0,0, 1])
        
        for i in range(500):
            sentence = random.randint(2, 20)
            text = ""
            for j in range(sentence):
                temp = random.choice(choice)
                noise = random.choice(list(neutrals.keys()))
                text += noise + " " + noise + " " + temp + " " + noise + " " + noise + " "
            f_writer.writerow(['TEST', text,0,0, 1])
            print([text,0,0,1])
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
                f_writer.writerow(['UNASSIGNED', text,0,0, 0])
                print([text,0,0, 0])
        
        g_choice = []
        for k,v in pos_dict.items():
            for i in range(v):
                g_choice.append(k)
        b_choice = []
        for k,v in neg_dict.items():
            for i in range(v):
                b_choice.append(k)

        #good
        for count in range(5000):
            distance_s = random.randint(0, 3)
            s_distance = []
            for c in range(distance_s):
                s_distance.append(random.choice(list(neutrals.keys())))
            text = ""
            
            loop_nbad = random.randint(3,7)
            loop_ngood = random.randint(0,loop_nbad)

            for loop in range(loop_nbad):
                bow = random.choice(b_choice)
                # gow = random.choice(g_choice)
                now = random.choice(list(neg_words.keys()))

                noise3 = random.choice(list(neutrals.keys()))
                noise4 = random.choice(list(neutrals.keys()))
                sentence = random.randint(2, 5)
                for j in range(sentence):
                    noise = random.choice(list(neutrals.keys()))
                    text += noise + " "
                text += now+" "
                for ele in s_distance:
                    text += ele + " "
                text += bow + " " + noise3 + " " + noise4 + " "

            for loop in range(loop_ngood):
                # bow = random.choice(b_choice)
                gow = random.choice(g_choice)
                now = random.choice(list(neg_words.keys()))

                noise3 = random.choice(list(neutrals.keys()))
                noise4 = random.choice(list(neutrals.keys()))
                sentence = random.randint(2, 5)
                for j in range(sentence):
                    noise = random.choice(list(neutrals.keys()))
                    text += noise + " "
                text += now+" "
                for ele in s_distance:
                    text += ele + " "
                text += gow + " " + noise3 + " " + noise4 + " "

            f_writer.writerow(['UNASSIGNED', text,loop_ngood,loop_nbad,1])
            print([text,loop_ngood,loop_nbad, 1])

        # bad
        for count in range(5000):
            distance_s = random.randint(0, 3)
            s_distance = []
            for c in range(distance_s):
                s_distance.append(random.choice(list(neutrals.keys())))
            text = ""
            
            loop_ngood = random.randint(3,7)
            loop_nbad = random.randint(0,loop_ngood-2)

            for loop in range(loop_nbad):
                bow = random.choice(b_choice)
                # gow = random.choice(g_choice)
                now = random.choice(list(neg_words.keys()))

                noise3 = random.choice(list(neutrals.keys()))
                noise4 = random.choice(list(neutrals.keys()))
                sentence = random.randint(2, 5)
                for j in range(sentence):
                    noise = random.choice(list(neutrals.keys()))
                    text += noise + " "
                text += now+" "
                for ele in s_distance:
                    text += ele + " "
                text += bow + " " + noise3 + " " + noise4 + " "

            for loop in range(loop_ngood):
                # bow = random.choice(b_choice)
                gow = random.choice(g_choice)
                now = random.choice(list(neg_words.keys()))

                noise3 = random.choice(list(neutrals.keys()))
                noise4 = random.choice(list(neutrals.keys()))
                sentence = random.randint(2, 5)
                for j in range(sentence):
                    noise = random.choice(list(neutrals.keys()))
                    text += noise + " "
                text += now+" "
                for ele in s_distance:
                    text += ele + " "
                text += gow + " " + noise3 + " " + noise4 + " "

            f_writer.writerow(['UNASSIGNED', text,loop_ngood,loop_nbad,0])
            print([text,loop_ngood,loop_nbad, 0])
        
    f.close()


    return jsonify({})


@analyze_blueprint.route("/create-comment-data17273747", methods=["GET", "POST"])
def create_comment_data():
    comments_good = CommentModel().objects(Q(star_num__gte=4) & Q(detail__ne='') & Q(detail__ne=None))[:5000]
    # comments_good_test = CommentModel().objects(Q(star_num__gte=4) & Q(detail__ne='') & Q(detail__ne=None))[:10000]
    comments_bad = CommentModel().objects(Q(star_num__lte=2) & Q(detail__ne='') & Q(detail__ne=None))[:5000]
    comments_temp = CommentModel().objects(Q(star_num__exact=3) & Q(detail__ne='') & Q(detail__ne=None))[:500]
    with open('testset_sentiment.csv', mode='w') as f:
        f_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        # f_writer.writerow(['split','text', 'score'])
        for comment in comments_good:
            if comment.detail:
                raw_text = comment.detail
                if raw_text.startswith('(Translated by Google)'):
                    raw_text = raw_text.split('(Translated by Google)')[-1][1:]
                    raw_text = raw_text.split('(Original)')[0]
                text = raw_text.lower()
                text = text.replace('\"','')
                print(text)
                g,b = Utils.preprocessing_input(text)
                # f_writer.writerow(['TEST', text, 2])
        for comment in comments_bad:
            if comment.detail:
                raw_text = comment.detail
                if raw_text.startswith('(Translated by Google)'):
                    raw_text = raw_text.split('(Translated by Google)')[-1][1:]
                    raw_text = raw_text.split('(Original)')[0]
                text = raw_text.lower()
                text = text.replace('\"','')
                g,b = Utils.preprocessing_input(text)
                # f_writer.writerow(['TEST',text, 0])
        for comment in comments_temp:
            if comment.detail:
                raw_text = comment.detail
                if raw_text.startswith('(Translated by Google)'):
                    raw_text = raw_text.split('(Translated by Google)')[-1][1:]
                    raw_text = raw_text.split('(Original)')[0]
                text = raw_text.lower()
                text = text.replace('\"','')
                g,b = Utils.preprocessing_input(text)
                # f_writer.writerow(['TEST',text, 1])
        # df = pandas.read_csv("train.tsv", usecols = ['Phrase', 'Sentiment'], sep="\t")
        # document = df.values
        # for record in document:
        #     raw = record['Pharse']
        #     text = raw.lower()
        #     text = text.replace('\"','')

        pos_dict = POS_DICT
        neg_dict = BAD_DICT
        neg_words = NEG_WORDS
        temp_dict = TEMP_DICT
        neutrals = NEUTRAL_WORDS
        choice = []
        for k,v in pos_dict.items():
            for i in range(v):
                choice.append(k)
            f_writer.writerow(['UNASSIGNED', k, 2])
        for i in range(10000):
            sentence = random.randint(2, 20)
            text = ""
            for j in range(sentence):
                temp = random.choice(choice)
                noise = random.choice(list(neutrals.keys()))
                text += noise + " " + noise + " " + temp + " " + noise + " " + noise + " "
            f_writer.writerow(['UNASSIGNED', text, 2])
            print([text,0,0, 2])
        # for i in range(5000):
        #     sentence = random.randint(2, 20)
        #     text = ""
        #     for j in range(sentence):
        #         temp = random.choice(choice)
        #         noise = random.choice(list(neutrals.keys()))
        #         text += noise + " " + noise + " " + temp + " " + noise + " " + noise + " "
        #     f_writer.writerow(['TEST', text, 2])
        #     print([text,0,0, 2])
        # negative pos
        for i in range(500):
            for k,v in neg_words.items():
                temp = random.choice(choice)
                distance_s = random.randint(0, 3)
                distance_l = random.randint(4, 20)
                s_distance = []
                l_distance = []
                for c in range(distance_s):
                    s_distance.append(random.choice(list(neutrals.keys())))
                for c in range(distance_l):
                    l_distance.append(random.choice(list(neutrals.keys())))
                noise3 = random.choice(list(neutrals.keys()))
                noise4 = random.choice(list(neutrals.keys()))
                sentence = random.randint(1, 5)

                #short dis
                text = ""
                for j in range(sentence):
                    noise = random.choice(list(neutrals.keys()))
                    text += noise + " "
                text += k+" "
                for ele in s_distance:
                    text += ele + " "
                text += temp + " " + noise3 + " " + noise4 + " "
                f_writer.writerow(['UNASSIGNED', text,0])
                print([text,1,0, 0])
                
                #long dis
                text = ""
                for j in range(sentence):
                    noise = random.choice(list(neutrals.keys()))
                    text += noise + " "
                text += k+" "
                for ele in l_distance:
                    text += ele + " "
                text += temp + " " + noise3 + " " + noise4 + " "
                f_writer.writerow(['UNASSIGNED', text,2])
                print([text,0,0,2])

                #revert
                text = ""
                distance_r = random.randint(1, 7)
                r_distance = []
                for c in range(distance_r):
                    r_distance.append(random.choice(list(neutrals.keys())))
                for j in range(sentence):
                    noise = random.choice(list(neutrals.keys()))
                    text += noise + " "
                text += temp+" "
                for ele in r_distance:
                    text += ele + " "
                text += k + " " + noise3 + " " + noise4 + " "
                f_writer.writerow(['UNASSIGNED', text,2])
                print([text,0,0,2])
        # bad sentiment
        choice = []
        for k,v in neg_dict.items():
            for i in range(v):
                choice.append(k)
            f_writer.writerow(['UNASSIGNED', k, 0])
        for i in range(10000):
            sentence = random.randint(2, 20)
            text = ""
            for j in range(sentence):
                temp = random.choice(choice)
                noise = random.choice(list(neutrals.keys()))
                text += noise + " " + noise + " " + temp + " " + noise + " " + noise + " "
            f_writer.writerow(['UNASSIGNED', text, 0])
            print([text,0,0, 0])

        # for i in range(5000):
        #     sentence = random.randint(2, 20)
        #     text = ""
        #     for j in range(sentence):
        #         temp = random.choice(choice)
        #         noise = random.choice(list(neutrals.keys()))
        #         text += noise + " " + noise + " " + temp + " " + noise + " " + noise + " "
        #     f_writer.writerow(['TEST', text, 0])
        #     print([text,0,0, 0])
        # negative neg
        for i in range(500):
            for k,v in neg_words.items():
                temp = random.choice(choice)
                distance_s = random.randint(0, 3)
                distance_l = random.randint(4, 20)
                s_distance = []
                l_distance = []
                for c in range(distance_s):
                    s_distance.append(random.choice(list(neutrals.keys())))
                for c in range(distance_l):
                    l_distance.append(random.choice(list(neutrals.keys())))
                noise3 = random.choice(list(neutrals.keys()))
                noise4 = random.choice(list(neutrals.keys()))
                sentence = random.randint(1, 5)

                #short dis
                text = ""
                for j in range(sentence):
                    noise = random.choice(list(neutrals.keys()))
                    text += noise + " "
                text += k+" "
                for ele in s_distance:
                    text += ele + " "
                text += temp + " " + noise3 + " " + noise4 + " "
                f_writer.writerow(['UNASSIGNED', text,1])
                print([text,0,1 ,1])
                
                #long dis
                text = ""
                for j in range(sentence):
                    noise = random.choice(list(neutrals.keys()))
                    text += noise + " "
                text += k+" "
                for ele in l_distance:
                    text += ele + " "
                text += temp + " " + noise3 + " " + noise4 + " "
                f_writer.writerow(['UNASSIGNED', text,0])
                print([text,0,0, 0])

                #revert
                text = ""
                distance_r = random.randint(1, 7)
                r_distance = []
                for c in range(distance_r):
                    r_distance.append(random.choice(list(neutrals.keys())))
                for j in range(sentence):
                    noise = random.choice(list(neutrals.keys()))
                    text += noise + " "
                text += temp+" "
                for ele in r_distance:
                    text += ele + " "
                text += k + " " + noise3 + " " + noise4 + " "
                f_writer.writerow(['UNASSIGNED', text,0])
                print([text,0,0, 0])
        # temp sentiment
        choice = []
        for k,v in temp_dict.items():
            f_writer.writerow(['UNASSIGNED', k, 1])
            for i in range(v):
                choice.append(k)
        for k,v in neutrals.items():
            choice.append(k)

        for i in range(500):
            sentence = random.randint(2, 20)
            text = ""
            for j in range(sentence):
                temp = random.choice(choice)
                noise = random.choice(list(neutrals.keys()))
                text += noise + " " + noise + " " + temp + " " + noise + " " + noise + " "
            f_writer.writerow(['UNASSIGNED', text, 1])
            print([text,0,0, 1])
        
        # for i in range(500):
        #     sentence = random.randint(2, 20)
        #     text = ""
        #     for j in range(sentence):
        #         temp = random.choice(choice)
        #         noise = random.choice(list(neutrals.keys()))
        #         text += noise + " " + noise + " " + temp + " " + noise + " " + noise + " "
        #     f_writer.writerow(['TEST', text, 1])
        #     print([text,0,0,1])
        # negative temp
        for i in range(100):
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
                f_writer.writerow(['UNASSIGNED', text, 0])
                print([text,0,0, 0])
        
        g_choice = []
        for k,v in pos_dict.items():
            for i in range(v):
                g_choice.append(k)
        b_choice = []
        for k,v in neg_dict.items():
            for i in range(v):
                b_choice.append(k)

        #good
        for count in range(5000):
            distance_s = random.randint(0, 3)
            s_distance = []
            for c in range(distance_s):
                s_distance.append(random.choice(list(neutrals.keys())))
            text = ""
            
            loop_nbad = random.randint(3,7)
            loop_ngood = random.randint(0,loop_nbad)

            for loop in range(loop_nbad):
                bow = random.choice(b_choice)
                # gow = random.choice(g_choice)
                now = random.choice(list(neg_words.keys()))

                noise3 = random.choice(list(neutrals.keys()))
                noise4 = random.choice(list(neutrals.keys()))
                sentence = random.randint(2, 5)
                for j in range(sentence):
                    noise = random.choice(list(neutrals.keys()))
                    text += noise + " "
                text += now+" "
                for ele in s_distance:
                    text += ele + " "
                text += bow + " " + noise3 + " " + noise4 + " "

            for loop in range(loop_ngood):
                # bow = random.choice(b_choice)
                gow = random.choice(g_choice)
                now = random.choice(list(neg_words.keys()))

                noise3 = random.choice(list(neutrals.keys()))
                noise4 = random.choice(list(neutrals.keys()))
                sentence = random.randint(2, 5)
                for j in range(sentence):
                    noise = random.choice(list(neutrals.keys()))
                    text += noise + " "
                text += now+" "
                for ele in s_distance:
                    text += ele + " "
                text += gow + " " + noise3 + " " + noise4 + " "

            f_writer.writerow(['UNASSIGNED', text,1])
            print([text,loop_ngood,loop_nbad, 1])

        # bad
        for count in range(5000):
            distance_s = random.randint(0, 3)
            s_distance = []
            for c in range(distance_s):
                s_distance.append(random.choice(list(neutrals.keys())))
            text = ""
            
            loop_ngood = random.randint(3,7)
            loop_nbad = random.randint(0,loop_ngood-2)

            for loop in range(loop_nbad):
                bow = random.choice(b_choice)
                # gow = random.choice(g_choice)
                now = random.choice(list(neg_words.keys()))

                noise3 = random.choice(list(neutrals.keys()))
                noise4 = random.choice(list(neutrals.keys()))
                sentence = random.randint(2, 5)
                for j in range(sentence):
                    noise = random.choice(list(neutrals.keys()))
                    text += noise + " "
                text += now+" "
                for ele in s_distance:
                    text += ele + " "
                text += bow + " " + noise3 + " " + noise4 + " "

            for loop in range(loop_ngood):
                # bow = random.choice(b_choice)
                gow = random.choice(g_choice)
                now = random.choice(list(neg_words.keys()))

                noise3 = random.choice(list(neutrals.keys()))
                noise4 = random.choice(list(neutrals.keys()))
                sentence = random.randint(2, 5)
                for j in range(sentence):
                    noise = random.choice(list(neutrals.keys()))
                    text += noise + " "
                text += now+" "
                for ele in s_distance:
                    text += ele + " "
                text += gow + " " + noise3 + " " + noise4 + " "

            f_writer.writerow(['UNASSIGNED', text,0])
            print([text,loop_ngood,loop_nbad, 0])
        
    f.close()


    return jsonify({})


@analyze_blueprint.route("/make-time-late17273747", methods=["GET", "POST"])
def reset_sentiment_store():
    all_stores = StoreModel().query_all()
    i =0
    for store in all_stores:
        i+=1
        all_comments = CommentModel().find_by_store_id(store.id)
        for comment in all_comments:
            past = comment.updated_on
            p = time.mktime(past.timetuple())
            now = datetime.datetime.now()
            n = time.mktime(now.timetuple())
            if comment.detail and comment.detail != "": 
                if n - p > 172800:
                    comment.update(set__sync_time=True, set__updated_on=now)
                    print(comment.detail)
        print(store.name)
        print(i)
    return jsonify({})


@analyze_blueprint.route("/make-address17273747", methods=["GET", "POST"])
def make_address():
    all_stores = StoreModel().query_all()
    i =0
    for store in all_stores:
        i+=1
        lat = float(store.position['lat'])
        lng = float(store.position['lng'])
        store.update(set__lat=lat, set__lng=lng)
        print(store.name)
        print(i)
    return jsonify({})


def sample_translate_text(text, target_language, project_id):
    """
    Translating Text

    Args:
      text The content to translate in string format
      target_language Required. The BCP-47 language code to use for translation.
    """

    client = translate.TranslationServiceClient()

    # TODO(developer): Uncomment and set the following variables
    # text = 'Text you wish to translate'
    # target_language = 'fr'
    # project_id = '[Google Cloud Project ID]'
    contents = [text]
    parent = client.location_path(project_id, "global")

    response = client.translate_text(
        parent=parent,
        contents=contents,
        mime_type='text/plain',  # mime types: text/plain, text/html
        source_language_code='vi',
        target_language_code=target_language)
    # Display the translation for each input text provided
    for translation in response.translations:
        print(u"Translated text: {}".format(translation.translated_text))

    return response


        
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/home/pain/Downloads/britcat2-0026abc98690.json"

# PROJECT_ID = "britcat2" #@param {type:"string"}
# COMPUTE_REGION = "us-central1" # Currently only supported region.

# conn = MongoClient()    
# db = conn['main_1']
# stores_collection = db.store
# all_stores = stores_collection.find()

# for store in all_stores:
#     cmts = CommentModel.findAllById(store["_id"])
#     print(cmts)
    

# def find_all_cmt_by_id(listIds):
#     comments_sorted = self.objects.order_by("-star_num").all()
#     comments =[]
#     for x in listIds: 
#         comments = comments + [comments_sorted(id=x)]
#     return comments    

# def sample_analyze_entity_sentiment(text_content):
#     """
#     Analyzing Entity Sentiment in a String

#     Args:
#       text_content The text content to analyze
#     """

#     client = language_v1.LanguageServiceClient()

#     # text_content = 'Grapes are good. Bananas are bad.'

#     # Available types: PLAIN_TEXT, HTML
#     type_ = enums.Document.Type.PLAIN_TEXT

#     # Optional. If not specified, the language is automatically detected.
#     # For list of supported languages:
#     # https://cloud.google.com/natural-language/docs/languages
#     language = "en"
#     document = {"content": text_content, "type": type_, "language": language}

#     # Available values: NONE, UTF8, UTF16, UTF32
#     encoding_type = enums.EncodingType.UTF8

#     response = client.analyze_entity_sentiment(document, encoding_type=encoding_type)
#     # Loop through entitites returned from the API
#     for entity in response.entities:
#         print(u"Representative name for the entity: {}".format(entity.name))
#         # Get entity type, e.g. PERSON, LOCATION, ADDRESS, NUMBER, et al
#         print(u"Entity type: {}".format(enums.Entity.Type(entity.type).name))
#         # Get the salience score associated with the entity in the [0, 1.0] range
#         print(u"Salience score: {}".format(entity.salience))
#         # Get the aggregate sentiment expressed for this entity in the provided document.
#         sentiment = entity.sentiment
#         print(u"Entity sentiment score: {}".format(sentiment.score))
#         print(u"Entity sentiment magnitude: {}".format(sentiment.magnitude))
#         # Loop over the metadata associated with entity. For many known entities,
#         # the metadata is a Wikipedia URL (wikipedia_url) and Knowledge Graph MID (mid).
#         # Some entity types may have additional metadata, e.g. ADDRESS entities
#         # may have metadata for the address street_name, postal_code, et al.
#         for metadata_name, metadata_value in entity.metadata.items():
#             print(u"{} = {}".format(metadata_name, metadata_value))

#         # Loop over the mentions of this entity in the input document.
#         # The API currently supports proper noun mentions.
#         for mention in entity.mentions:
#             print(u"Mention text: {}".format(mention.text.content))
#             # Get the mention type, e.g. PROPER for proper noun
#             print(
#                 u"Mention type: {}".format(enums.EntityMention.Type(mention.type).name)
#             )

#     # Get the language of the text, which will be the same as
#     # the language specified in the request or, if not specified,
#     # the automatically-detected language.
#     print(u"Language of the text: {}".format(response.language))

# a = sample_analyze_entity_sentiment("the table is nice but the store is bad")
# print(a)
