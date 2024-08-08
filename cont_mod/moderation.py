import os
import re
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
class Text_Moderator():
    def __init__(self):
        pass
        
    def read_file(self,file_path):
        with open(file_path, 'r') as file:
            return [line.strip() for line in file]

    def create_badwords_dictionary(self,lang_input):
        directory_for_words="cont_mod/bad_word"
        file_path = os.path.join(directory_for_words,f"bad_word.{lang_input}") 
        badwords_list = self.read_file(file_path) 
        return badwords_list

    def moderate_text(self,lang_input,text):
        moderation_results = []
        replacement_text = text
        profane_dict=self.create_badwords_dictionary(lang_input)
        for string_token in replacement_text.split():
            if string_token in profane_dict:
                replacement_text = replacement_text.replace(string_token, '*' * len(string_token))
                moderation_results.append({"moderation_type": "abuse",
                    "text": string_token,
                    "confidence": 1.00})
        return replacement_text,moderation_results
    
# object1=Text_Moderator()
# print(object1.moderate_text("en","shut up motherfucker"))
