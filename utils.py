import os
import requests
from flask import json
from app import bcrypt
from google.cloud import language_v1
from google.cloud import translate
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
    def predict_food_cate(text):
        data = {
            "instances": [{
                "text": text
            }]
        }
        response = requests.post('http://localhost:8080/predict', json=data)
        result = json.loads(response.content)
        rsfm = result['predictions'][0]
        type_store = {}
        print(rsfm)
        for i in range(len(rsfm["classes"])):
            type_store[rsfm["classes"][i]] = rsfm["scores"][i]
        # type_filtered = {k: v for k, v in type_store.items() if v >= 0.1}
        # type_sorted = {k: v for k, v in sorted(type_filtered.items(), key=lambda item: item[1], reverse=True)}
        return type_store
    

    @staticmethod
    def predict_sentiment_score(text):
        data = {
            "instances": [{
                "text": text
            }]
        }
        response = requests.post('http://localhost:8080/predict', json=data)
        result = json.loads(response.content)
        rsfm = result['predictions'][0]
        type_store = {}
        print(rsfm)
        for i in range(len(rsfm["classes"])):
            type_store[rsfm["classes"][i]] = rsfm["scores"][i]
        type_sorted = {k: v for k, v in sorted(type_store.items(), key=lambda item: item[1], reverse=True)}
        sc = -type_store["0"] + type_store["2"]
        return sc
        

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

    @staticmethod
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