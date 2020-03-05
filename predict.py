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
    "Categories": "Quán",
    "Cmt_1": 204,
    "Cmt_2": 53,
    "Cmt_3": 38,
    "Cmt_4": 55,
    "Cmt_5": 76,
    "Cmt_6": 8,
    "Cmt_7": 10,
    "Cmt_8": 15,
    "Cmt_9": 19,
    "Cmt_10": 14,
    "Distances": 15,
    "Max_prices": 2000000,
    "Min_prices": 20000,
    "Star_s1": 47,
    "Star_s2": 26,
    "Star_s3": 187,
    "Star_s4": 387,
    "Star_s5": 545
}
for model in list_models:
    if model.display_name == "data_training_dem_20200130113713":
        prediction_result = tables_client.predict(model=model, inputs=inputs)

print(prediction_result)
predictions = [(prediction.tables.score, prediction.tables.value.string_value) 
               for prediction in prediction_result.payload]
predictions = sorted(
    predictions, key=lambda tup: (tup[0],tup[1]), reverse=True)
print('Prediction is: ', predictions[0])