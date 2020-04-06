# from google.cloud import automl_v1beta1 as automl
from pymongo import MongoClient
from google.cloud import language_v1
from google.cloud.language_v1 import enums
from app.main.comment.models import CommentModel

import os

from app import create_app
import os

from functools import wraps
import time
import math
import requests
from constants import Pages
from flask import redirect, render_template, Blueprint, session, request, request, jsonify, make_response


from app.main.store.models import StoreModel
from app.main.comment.models import CommentModel
from app.main.category.models import CategoryModel
from app.main.address.models import AddressModel


from utils import Utils
from constants import CLASS_LIST
from app.main.comment.models import CommentModel

from flask.helpers import url_for

analyze_blueprint = Blueprint(
    'analyze', __name__, template_folder='templates')


# do not run manual
@analyze_blueprint.route("/analyze17273747", methods=["GET","POST"])
def analyze():
    all_stores = StoreModel().query_all()
    for store in all_stores:
        cmts = CommentModel().findAllById(store.comment_list)

        if store.entity_score:
            continue

        entity_dict = {}
        entire_text_1 = ""
        entire_text_2 = ""
        entire_text_3 = ""
        loops_no = 0
        for cmt in cmts:
            if cmt[0].detail is None:
                continue
            text = cmt[0].detail
            if text.startswith('(Translated by Google)'):
                print(text)
                text = text.split('(Translated by Google)')[-1][1:]
                text = text.split('(Original)')[0]
            if loops_no <= 400:
                entire_text_1 += text
            elif loops_no <= 800:
                entire_text_2 += text
            else:
                entire_text_3 += text
            loops_no += 1
        
        for sub_entire in (entire_text_1, entire_text_2, entire_text_3):
            if sub_entire == "":
                continue
            # response = Utils.analyze_entity_sentiment(sub_entire)
                
            for entity in response.entities:
                name = entity.name.upper()
                name = name.replace("$","")
                if not entity_dict.get(name, False):
                    entity_dict[name] = {
                        "quantity": 1,
                        "sentiment": entity.sentiment.score
                    }
                else:
                    entity_dict[name] = {
                        "quantity": entity_dict[name]["quantity"]+1,
                        "sentiment": entity_dict[name]["sentiment"]+entity.sentiment.score                   
                    }
                print((name, entity.sentiment.score))
        # store.update(set__entity_score=entity_dict)
        print(store.entity_score)
                    
        


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
