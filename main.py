# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pickle
import json

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class model_input(BaseModel):

    Temperature:int
    Humidity:int 
    Moisture:int
    SoilType:str
    CropType:str
    Nitrogen:int
    Potassium:int
    Phosphorous:int
    


recommendation_model = pickle.load(open('fertilizer_recommendation_trained.sav', 'rb'))
processor = pickle.load(open('preprocessor.sav', 'rb'))

@app.post('/predict')
def fert_recc(input_parameters: model_input):
    input_data = input_parameters.json()
    input_dictionary = json.loads(input_data)
    temp = input_dictionary['Temperature']
    hum = input_dictionary['Humidity']
    moist = input_dictionary['Moisture']
    soil = input_dictionary['SoilType']
    crop = input_dictionary['CropType']
    n = input_dictionary['Nitrogen']
    p = input_dictionary['Potassium']
    k = input_dictionary['Phosphorous']
    


    input_list = [[temp,hum,moist,soil,crop,n,p,k]]
    transformed_input = processor.transform(input_list)
    prediction = recommendation_model.predict(transformed_input)
    
    return prediction[0]