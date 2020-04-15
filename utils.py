import os

from flask import json
from app import bcrypt
from google.cloud import language_v1
from google.cloud.language_v1 import enums
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/home/pain/Downloads/Britcat3-dd9d79d99d97.json"

PROJECT_ID = "Britcat3" #@param {type:"string"}
COMPUTE_REGION = "us-central1" # Currently only supported region.


class Utils:
    @staticmethod
    def hash_password(str_psw):
        if str_psw is None:
            return None
        str_psw = bcrypt.generate_password_hash(str_psw)
        return str_psw

    @staticmethod
    def check_password(psw_1, psw_2):
        # psw_1: pass that you try to login
        # psw_2: pass that you save in db
        if bcrypt.check_password_hash(psw_2, psw_1):
            return True
        return False

    @staticmethod
    def decode_json(payload):
        return json.loads(payload.decode('utf-8'))

    @staticmethod
    def print_json(payload):
        return json.dumps(payload, indent=4, sort_keys=True)

    @staticmethod
    def get_classification_by_score(score):
        if score <= 2.5:
            return 'SS'
        elif score > 2.5 and score <= 4.5:
            return 'S'
        elif score > 4.5 and score <= 8.5:
            return 'A'
        elif score > 8.5 and score <= 12.5:
            return 'B'
        elif score > 12.5 and score <= 16.5:
            return 'C'
        elif score > 16.5 and score <= 20.5:
            return 'D'
        elif score > 20.5 and score <= 24.5:
            return 'E'
        elif score > 24.5:
            return 'F'

    @staticmethod
    def analyze_entity_sentiment(text_content):
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
        return response
        # Loop through entitites returned from the API
        # for entity in response.entities:
        #     print(u"Representative name for the entity: {}".format(entity.name))
        #     # Get entity type, e.g. PERSON, LOCATION, ADDRESS, NUMBER, et al
        #     print(u"Entity type: {}".format(enums.Entity.Type(entity.type).name))
        #     # Get the salience score associated with the entity in the [0, 1.0] range
        #     print(u"Salience score: {}".format(entity.salience))
        #     # Get the aggregate sentiment expressed for this entity in the provided document.
        #     sentiment = entity.sentiment
        #     print(u"Entity sentiment score: {}".format(sentiment.score))
        #     print(u"Entity sentiment magnitude: {}".format(sentiment.magnitude))
        #     # Loop over the metadata associated with entity. For many known entities,
        #     # the metadata is a Wikipedia URL (wikipedia_url) and Knowledge Graph MID (mid).
        #     # Some entity types may have additional metadata, e.g. ADDRESS entities
        #     # may have metadata for the address street_name, postal_code, et al.
        #     for metadata_name, metadata_value in entity.metadata.items():
        #         print(u"{} = {}".format(metadata_name, metadata_value))

        #     # Loop over the mentions of this entity in the input document.
        #     # The API currently supports proper noun mentions.
        #     for mention in entity.mentions:
        #         print(u"Mention text: {}".format(mention.text.content))
        #         # Get the mention type, e.g. PROPER for proper noun
        #         print(
        #             u"Mention type: {}".format(enums.EntityMention.Type(mention.type).name)
        #         )

        # # Get the language of the text, which will be the same as
        # # the language specified in the request or, if not specified,
        # # the automatically-detected language.
        # print(u"Language of the text: {}".format(response.language))