from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from azure.cognitiveservices.vision.customvision.training.models import ImageFileCreateBatch, ImageFileCreateEntry, Region
from msrest.authentication import ApiKeyCredentials
import os, time, uuid

# Replace with valid values
ENDPOINT = "https://strokevision-prediction.cognitiveservices.azure.com/"
prediction_key = "d260ad67dc73424a83d249f50631f96c"

prediction_resource_id = "/subscriptions/59d64684-e7c9-4397-8982-6b775a473b74/resourceGroups/UCL_Jacob_MSc/providers/Microsoft.CognitiveServices/accounts/stroke-vision"

#project id
project = 'Stroke_class'
project_id = '6faeb988-9af6-4e9a-9b92-4ca37069ec8e'

#iteration name
iteration = "Iteration1"

base_image_location = os.path.join (os.path.dirname(__file__), "Test")


# Now there is a trained endpoint that can be used to make a prediction
prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": prediction_key})
predictor = CustomVisionPredictionClient(ENDPOINT, prediction_credentials)

def StrokeClassifier(name):
    for ind, filename in enumerate(os.listdir('pose/Test')):
        if filename.endswith('.jpg') or filename.endswith('.png') or filename.endswith('.jpeg'): 
            with open(os.path.join (base_image_location, (name + f'{ind}.jpg')), "rb") as image_contents:
                results = predictor.classify_image(
                    project_id, iteration, image_contents.read())

                # Display the results.
                for prediction in results.predictions:
                    print( f'Stroke Frame # {ind}:'+ "\t" + prediction.tag_name +
                        ": {0:.2f}%".format(prediction.probability * 100))
        else:
            print("you are a failure")

def StrokeList(name):
    for ind, filename in enumerate(os.listdir('pose/Test')):
        if filename.endswith('.jpg') or filename.endswith('.png') or filename.endswith('.jpeg'): 
            with open(os.path.join (base_image_location, (name + f'{ind}.jpg')), "rb") as image_contents:
                results = predictor.classify_image(
                    project_id, iteration, image_contents.read())

                # Display the results.
                first = results.predictions[0]
                firstresult = first.probability
                firstlabel = first.tag_name
                print(firstlabel, firstresult)
        else:
            print("NA")

#StrokeList('djok')
StrokeClassifier('djok')
