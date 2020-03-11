from google.cloud import automl_v1beta1 as automl
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/home/pain/Downloads/britcat2-0026abc98690.json"

PROJECT_ID = "britcat2" #@param {type:"string"}
COMPUTE_REGION = "us-central1" # Currently only supported region.

automl_client = automl.AutoMlClient()
tables_client = automl.TablesClient(project=PROJECT_ID, region=COMPUTE_REGION)
# List the models.
list_models = tables_client.list_models()
inputs = {
    "Age" : 18,
    "Categories": '["quan-nhau"]',
    "Cmt_1": 64,
    "Cmt_2": 11,
    "Cmt_3": 14,
    "Cmt_4": 7,
    "Cmt_5": 6,
    "Cmt_6": 1,
    "Cmt_7": 2,
    "Cmt_8": 1,
    "Cmt_9": 0,
    "Cmt_10": 1,
    "Distances": 30,
    "Max_prices": 490000,
    "Min_prices": 70000,
    "Star_s1": 108,
    "Star_s2": 60,
    "Star_s3": 21,
    "Star_s4": 3,
    "Star_s5": 3
}
for model in list_models:
    if model.display_name == "data_training_v3__20200308094451":
        prediction_result = tables_client.predict(model=model, inputs=inputs)

print(prediction_result)
# predictions = [(prediction.tables.score, prediction.tables.value.string_value) 
#                for prediction in prediction_result.payload]
# predictions = sorted(
#     predictions, key=lambda tup: (tup[0],tup[1]), reverse=True)
# print('Prediction is: ', predictions[0])