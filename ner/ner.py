 
import json
import requests
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from constants.constant import INDOCORD_NER_URL,NER_DETECTOR_URL

class Entity_Extractor:
    def __init__(self) -> None:
        pass
    def ent_extractor(self,text,language):
        print(text)
        entities_found=[]
        entity_set=self.get_from_indocord_ner(text)
        if entity_set:
            entities_found.append(entity_set)
        entity_set_amount=self.get_amount_ner(text,language)
        entity_set_number=self.get_number_ner(text,language)
        entity_set_phone_number=self.get_phone_number_ner(text,language)
        entity_set_time=self.get_time_ner(text,language)
        entity_set_date=self.get_date_ner(text,language)

        if entity_set_amount:
            entities_found.append(entity_set_amount)
        if entity_set_number:
            entities_found.append(entity_set_number)
        if entity_set_date:
            entities_found.append(entity_set_date)
        if entity_set_time:
            entities_found.append(entity_set_time)
        if entity_set_phone_number:
            entities_found.append(entity_set_phone_number)
        return entities_found

    def get_from_indocord_ner(self,text):
        url = INDOCORD_NER_URL
        payload = json.dumps({
            "text": text
        })
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        resp = response.json()
        entities = []
        if resp["entities"]:
            for ent in resp["entities"]:
                x = list(ent.items())
                if len(x) > 0:
                    for item in x:
                        word = item[0]
                        score = "_".join([str(c) for c in item[1]])
                        entities.append((word, score))
        return entities

    def get_amount_ner(self,text, lang_input):
        url = NER_DETECTOR_URL+f"number/?&entity_name=number_of_unit&min_number_digits=1&max_number_digits=6&unit_type=currency&source_language={lang_input}&structured_value=&fallback_value=&bot_message=&message={text}"
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        entities=[]
        response = requests.request("GET", url, headers=headers)
        resp=response.json()
        entities = []
        if resp["data"]:
            for ent in resp["data"]:
                entities.append((ent["entity_value"]["value"],"Amount"))
        return entities

    def get_number_ner(self,text,lang_input):
        url = NER_DETECTOR_URL+f"number/?&entity_name=number_of_unit&min_number_digits=1&max_number_digits=6&unit_type=&source_language={lang_input}&structured_value=&fallback_value=&bot_message=&message={text}"
        headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
        }
        entities=[]
        response = requests.request("GET", url, headers=headers)
        resp=response.json()
        entities = []
        if resp["data"]:
            for ent in resp["data"]:
                entities.append((ent["entity_value"]["value"],"Number"))
        return entities

    def get_phone_number_ner(self,text, lang_input):
        url = NER_DETECTOR_URL+f"phone_number/?entity_name=phone_number&source_language={lang_input}&structured_value=&fallback_value=&bot_message=&message={text}"
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        entities=[]
        response = requests.request("GET", url, headers=headers)
        resp=response.json()
        entities = []
        if resp["data"]:
            for ent in resp["data"]:
                entities.append((ent["entity_value"]["value"],"Phone_Number"))
        return entities
  
    def get_date_ner(self,text, lang_input):
        url = NER_DETECTOR_URL+f"date/?entity_name=date&timezone=UTC&source_language={lang_input}&message={text}"
        headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
        }
        entities=[]
        response = requests.request("GET", url, headers=headers)
        resp=response.json()
        entities = []
        if resp["data"]:
            for ent in resp["data"]:
                entities.append((ent["entity_value"]["value"],"Date"))
        return entities
    
    def get_time_ner(self,text, lang_input):
        url = NER_DETECTOR_URL+f"time/?entity_name=time&timezone=UTC&source_language={lang_input}&message={text}"
        headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
        }
        entities=[]
        response = requests.request("GET", url, headers=headers)
        resp=response.json()
        entities = []
        if resp["data"]:
            for ent in resp["data"]:
                entities.append((f"{ent["entity_value"]["hh"]}:{ent["entity_value"]["mm"]} {ent["entity_value"]["nn"]}","Time"))
        return entities
    
# object1=Entity_Extractor()
# print(object1.get_number_ner(text="Hello my name is Snehil and I live in Bengaluru and the time is 11:00 PM",lang_input="en"))
# print(object1.get_from_indocord_ner(text="Hello my name is Snehil and I live in Bengaluru"))