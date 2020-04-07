# from google.cloud import automl_v1beta1 as automl
from pymongo import MongoClient
from google.cloud import language_v1
from google.cloud.language_v1 import enums
# from app.main.comment.models import CommentModel

import os

from app import create_app
import os

from functools import wraps
import time
import math
import requests
from constants import Pages
from flask import redirect, render_template, Blueprint, session, request, request, jsonify, make_response


# from app.main.store.models import StoreModel
# from app.main.comment.models import CommentModel
# from app.main.category.models import CategoryModel
# from app.main.address.models import AddressModel


# from utils import Utils
# from constants import CLASS_LIST
# from app.main.comment.models import CommentModel

# from flask.helpers import url_for

# store_blueprint = Blueprint(
#     'analyze', __name__, template_folder='templates')

# @store_blueprint.route("/analyze17273747", methods=["GET","POST"])
# def analyze(store_id=None, page = 1, db = list(), form=None, error=None):
#     all_stores = StoreModel().query_all()
#     for store in all_stores:
#         cmts = CommentModel().findAllById(store.id)
#         print(cmts)


os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/home/pain/Downloads/britcat2-0026abc98690.json"

PROJECT_ID = "britcat2" #@param {type:"string"}
COMPUTE_REGION = "us-central1" # Currently only supported region.

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

def sample_analyze_entity_sentiment(text_content):
    """
    Analyzing Entity Sentiment in a String

    Args:
      text_content The text content to analyze
    """

    client = language_v1.LanguageServiceClient()

    # text_content = 'Grapes are good. Bananas are bad.'

    # Available types: PLAIN_TEXT, HTML
    type_ = enums.Document.Type.PLAIN_TEXT

    # Optional. If not specified, the language is automatically detected.
    # For list of supported languages:
    # https://cloud.google.com/natural-language/docs/languages
    language = "en"
    document = {"content": text_content, "type": type_, "language": language}

    # Available values: NONE, UTF8, UTF16, UTF32
    encoding_type = enums.EncodingType.UTF8

    response = client.analyze_entity_sentiment(document, encoding_type=encoding_type)
    # Loop through entitites returned from the API
    for entity in response.entities:
        print(u"Representative name for the entity: {}".format(entity.name))
        # Get entity type, e.g. PERSON, LOCATION, ADDRESS, NUMBER, et al
        print(u"Entity type: {}".format(enums.Entity.Type(entity.type).name))
        # Get the salience score associated with the entity in the [0, 1.0] range
        print(u"Salience score: {}".format(entity.salience))
        # Get the aggregate sentiment expressed for this entity in the provided document.
        sentiment = entity.sentiment
        print(u"Entity sentiment score: {}".format(sentiment.score))
        print(u"Entity sentiment magnitude: {}".format(sentiment.magnitude))
        # Loop over the metadata associated with entity. For many known entities,
        # the metadata is a Wikipedia URL (wikipedia_url) and Knowledge Graph MID (mid).
        # Some entity types may have additional metadata, e.g. ADDRESS entities
        # may have metadata for the address street_name, postal_code, et al.
        for metadata_name, metadata_value in entity.metadata.items():
            print(u"{} = {}".format(metadata_name, metadata_value))

        # Loop over the mentions of this entity in the input document.
        # The API currently supports proper noun mentions.
        for mention in entity.mentions:
            print(u"Mention text: {}".format(mention.text.content))
            # Get the mention type, e.g. PROPER for proper noun
            print(
                u"Mention type: {}".format(enums.EntityMention.Type(mention.type).name)
            )

    # Get the language of the text, which will be the same as
    # the language specified in the request or, if not specified,
    # the automatically-detected language.
    print(u"Language of the text: {}".format(response.language))


a = sample_analyze_entity_sentiment("")
print(a)
