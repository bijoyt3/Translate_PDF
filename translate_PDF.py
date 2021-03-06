#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 09:50:56 2021

@author: bijoy

@description: This script receives a PDF input specified by the user, extracts the text, detects the language, 
translates the input to English, and finally outputs the value to a text file.

"""
### Apache Tika: https://tika.apache.org/
from tika import parser 

### Google Cloud Translate API
from google.cloud import translate

def get_display_name(lang_code):
    '''
    Returns full display name from language code 
    
    :param lang_code: language code from Google's supported language dictionary, e.g. 'zh-CN'
    :return: Language name/display name of language code
    '''
    try:
        response = client.get_supported_languages(display_language_code="en", parent=parent)
    except: 
        print("Cannot locate specified language code. Try again.")
      
    for language in response.languages:
        if language.language_code == lang_code:
            return language.display_name
    
        
def detect_lang_basic(text):
    '''
    Detects language from text input (basic); Returns only the language code 
    
    :param text: text input 
    :return: language code
    '''
    try:
        response = client.detect_language(
            content=text,
            parent=parent,
            mime_type="text/plain",
        )
    except:
        print("Invalid text input. Try again.")
    
    for language in response.languages:
        return language.language_code


def detect_lang_adv(text):
    '''
    Detects language from text input (advanced); Returns the original input, the language code,
    the display name, and confidence value from 0.0 to 1.0 
    
    :param text: text input 
    :return: input, language name, language code, and confidence value from 0.0 to 1.0
    '''
    try:
        response = client.detect_language(
            content=text,
            parent=parent,
            mime_type="text/plain",
        )
    except:
        print("Invalid text input. Try again.")
    
    for language in response.languages:
        return ("Input: {}".format(text), 
                "Language: {}".format(get_display_name(language.language_code)),
                "Language Code: {}".format(language.language_code), 
                "Confidence: {}".format(language.confidence))
    
def translate_lang(text):
    '''
    Translates a detected language to English; Returns the translated text
    
    :param text: text input 
    :return: translated text
    '''
    try:
        response = client.translate_text(
            request={
                "parent": parent,
                "contents": [text],
                "mime_type": "text/plain",
                "source_language_code": detect_lang_basic(text),
                "target_language_code": "en",
                }
            )
    except:
        print("Invalid text input. Try again.")
    
    for translation in response.translations:
        return translation.translated_text

### Credentials
project_id = 'PROJECT ID'
location = 'global'
parent = f"projects/{project_id}/locations/{location}"

### Create Google Translate Client
client = translate.TranslationServiceClient.from_service_account_json('credentials.json')

### Import PDF File
filepath = 'FILEPATH'
text = parser.from_file(filepath)

### Extract Text from PDF File
txt_extract = str(text['content']).replace("\n", "")


### Print Results to Console
for value in detect_lang_adv(txt_extract):
    print (value)
    
print("\nOutput: {}".format(translate_lang(txt_extract)))

### Write Output to File 
txt_file = open('output.txt', 'w')
output = txt_file.write(translate_lang(txt_extract))
txt_file.close()
