from google.cloud import automl_v1beta1 as automl
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/home/pain/Downloads/Britcat3-dd9d79d99d97.json"

PROJECT_ID = "britcat3" #@param {type:"string"}
COMPUTE_REGION = "us-central1" # Currently only supported region.

# automl_client = automl.AutoMlClient()
# project_location = client.location_path(PROJECT_ID, COMPUTE_REGION)

from google.cloud import automl

# TODO(developer): Uncomment and set the following variables
# project_id = "YOUR_PROJECT_ID"
model_id = "TST6346658192453271552"
# content = "text to predict"

prediction_client = automl.PredictionServiceClient()

# Get the full path of the model.
model_full_id = prediction_client.model_path(
    PROJECT_ID, "us-central1", model_id
)
# entity_client = automl.TablesClient(project=PROJECT_ID, region=COMPUTE_REGION)
# # List the models.
# list_models = tables_client.list_models()
# inputs = {
#     "Age" : 18,
#     "Categories": '["quan-nhau"]',
#     "Cmt_1": 64,
#     "Cmt_2": 11,
#     "Cmt_3": 14,
#     "Cmt_4": 7,
#     "Cmt_5": 6,
#     "Cmt_6": 1,
#     "Cmt_7": 2,
#     "Cmt_8": 1,
#     "Cmt_9": 0,
#     "Cmt_10": 1,
#     "Distances": 30,
#     "Max_prices": 490000,
#     "Min_prices": 70000,
#     "Star_s1": 108,
#     "Star_s2": 60,
#     "Star_s3": 21,
#     "Star_s4": 3,
#     "Star_s5": 3
# }
# for model in list_models:
#     if model.display_name == "data_training_v3__20200308094451":
#         prediction_result = tables_client.predict(model=model, inputs=inputs)

# print(prediction_result)
# predictions = [(prediction.tables.score, prediction.tables.value.string_value) 
#                for prediction in prediction_result.payload]
# predictions = sorted(
#     predictions, key=lambda tup: (tup[0],tup[1]), reverse=True)
# print('Prediction is: ', predictions[0])


import sys

from google.api_core.client_options import ClientOptions
from google.cloud import automl_v1
from google.cloud.automl_v1.proto import service_pb2

def inline_text_payload(file_path):
    with open(file_path, 'rb') as ff:
        content = ff.read()
    return {'text_snippet': {'content': content, 'mime_type': 'text/plain'} }

def pdf_payload(file_path):
    return {'document': {'input_config': {'gcs_source': {'input_uris': [file_path] } } } }

def get_prediction(file_path, model_name):
    options = ClientOptions(api_endpoint='automl.googleapis.com')
    prediction_client = automl_v1.PredictionServiceClient(client_options=options)
    payload = {'text_snippet': {'content': file_path, 'mime_type': 'text/plain'} }
    # payload = inline_text_payload(file_path)
    # Uncomment the following line (and comment the above line) if want to predict on PDFs.
    # payload = pdf_payload(file_path)

    params = {}
    request = prediction_client.predict(model_name, payload, params)
    return request  # waits until request is returned

if __name__ == '__main__':
    # file_path = sys.argv[1]
    # model_name = sys.argv[2]

    print(get_prediction("what a pretty box", 'sentiment_analyze_20200419014442'))