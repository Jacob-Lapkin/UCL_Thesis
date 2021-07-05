from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from azure.cognitiveservices.vision.customvision.training.models import ImageFileCreateBatch, ImageFileCreateEntry, Region
from msrest.authentication import ApiKeyCredentials
import os, time, uuid

# Replace with valid values
ENDPOINT = "https://stroke-prediction.cognitiveservices.azure.com/"
prediction_key = "a2870f2dd939408386e6b5b8927e8276"

prediction_resource_id = "/subscriptions/1a346baa-ff42-4c09-93e5-7801dc9ab2f9/resourceGroups/UCL/providers/Microsoft.CognitiveServices/accounts/Stroke"

#project id
project = 'Stoke_classifier'
project_id = '4d68f633-1b0f-44b0-987a-a32ea1410c0e'

#iteration name
iteration = "Iteration9"

base_image_location = os.path.join (os.path.dirname(__file__), "Test")


# Now there is a trained endpoint that can be used to make a prediction
prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": prediction_key})
predictor = CustomVisionPredictionClient(ENDPOINT, prediction_credentials)

def StrokeClassifier(name):
    for ind, filename in enumerate(os.listdir('Test')):
        if filename.endswith('.jpg') or filename.endswith('.png') or filename.endswith('.jpeg'): 
            with open(os.path.join (base_image_location, (name + f'{ind}.png')), "rb") as image_contents:
                results = predictor.classify_image(
                    project_id, iteration, image_contents.read())

                # Display the results.
                for prediction in results.predictions:
                    print( f'Stroke Frame # {ind}:'+ "\t" + prediction.tag_name +
                        ": {0:.2f}%".format(prediction.probability * 100))
        else:
            print("you are a failure")

StrokeClassifier('halep')
