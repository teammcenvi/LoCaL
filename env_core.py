#!/usr/bin/env python
# coding: utf-8

import pandas as pd 
import numpy as np
import pytesseract
import cv2
from PIL import Image, ImageEnhance, ImageFilter
import json
import string
from nltk.corpus import words as nltk_words

def is_english_word(word):
    # creation of this dictionary would be done outside of 
    #     the function because you only need to do it once.
    dictionary = dict.fromkeys(nltk_words.words(), None)
    try:
        x = dictionary[word]
        return True
    except KeyError:
        return False
    
def word2vec(word):
    from collections import Counter
    from math import sqrt

    # count the characters in word
    cw = Counter(word)
    # precomputes a set of the different characters
    sw = set(cw)
    # precomputes the "length" of the word vector
    lw = sqrt(sum(c*c for c in cw.values()))

    # return a tuple
    return cw, sw, lw
def cosinedistance(v1, v2):
    # which characters are common to the two words?
    common = v1[1].intersection(v2[1])
    # by definition of cosine distance we have
    return sum(v1[0][ch]*v2[0][ch] for ch in common)/v1[2]/v2[2]

def get_similarity(x,y):
    threshold = 0.80 
    content = []
    for key in x:
        for word in y:
            try:
                res = cosinedistance(word2vec(word), word2vec(key))
                if res > threshold:
                    content.append(word)
                    print(key,word,res)
            except IndexError:
                pass
    return content

def main_core(filename):
    ### Input Image  and perform Optical Character Recognition  ### 
    ### Future: Image processing: to apply image detection and image clean-up to address bad quality and complex images ###
    ### Future: Natural Language Process using Named Entity Recognition/Transfer Learning model i.e. BERT, ROBERTA ###

    filename = "static/"+filename
    im = Image.open(filename)
    #im = im.convert("L")
    im = im.filter(ImageFilter.DETAIL)
    text = pytesseract.image_to_string(im)
    text = text.replace("\r"," ").replace("\n"," ").replace("  "," ").replace("  "," ")
    y0 = text.split(" ")
    y =[]
    for y1 in y0:
        if len(y1) > 3:
           y1=string.capwords(y1)
           word = y1.lower()
           if is_english_word(word) is True:
              y.append(y1)    
    y = list(filter(None, y))
    print("y")
    print(y)


    ### Dataset with CO2 consumption ###
    ### Analytics data - future: A/I machine learning models ###
    df = pd.read_csv("data/Food_Production.csv")
    x = df['Food product'].values
    print("x")
    print(x)

    ### Compare OCR Text found  against the  datasource,  ###
    if len(y) > 0:
        ### Get the words with highest cosine similarity ###
        
        content = get_similarity(x,y)
        print("content")
        print(content)
        if len(content) > 0:
            ### Get the CO2 values per distribution with values more than "0" ###
            for content1 in content:
                q = df[df['Food product'] == content1]
                result = q.to_json(orient="records")
                parsed = json.loads(result)[0]
                #print(parsed)
                data ={}
                data['product'] = content1
                for key, value in parsed.items():
                    try:
                        #if value > 0 and "per" not in key:
                        if "per" not in key:
                            key = key.replace(" ","_")
                            data[key] = value
                            #print(key,value)
                    except:
                        pass

                #print(data)
                return data
        else:
            data={}
            return data
    else:
        data={}
        return data



