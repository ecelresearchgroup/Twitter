#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 11:48:32 2020

@author: kevinrojas
"""

#### Program to classify twitter based on emotions

#### Libraries to be used:

import pandas as pd
import twitter
import time
import re
import matplotlib.pyplot as plt
import numpy as np
#### Initiliaze twitter access:

### Define conditions for session controller:

consumer_key_kevin = '1VxNNcBF3JoL9yAJz49nHC3Nq'
consumer_secret_kevin = 'kNWX45PLxNHlDQlSRKNes0ZkL2dB7ibUE8AZn40uWaudXCCB4C'
access_token_kevin = '2969205766-t3ddErHvufp0voxtXrTyPhcWRSWrsDFx7WCh1NZ'
access_secret_kevin = '2AtK6D3RlaM1gTc7SaabGhsaujXEQgNTJg7rkrRUBkeop'

#Creo las credenciales

kevintool = twitter.Api(consumer_key=consumer_key_kevin,
                      consumer_secret=consumer_secret_kevin,
                      access_token_key=access_token_kevin,
                      access_token_secret=access_secret_kevin)

#### Functions involved:

def get_tweets(api=None, screen_name=None):
    timeline = api.GetUserTimeline(screen_name=screen_name, count=200)
    earliest_tweet = min(timeline, key=lambda x: x.id).id
    print("getting tweets before:", earliest_tweet)

    while True:
        tweets = api.GetUserTimeline(
            screen_name=screen_name, max_id=earliest_tweet, count=200
        )
        new_earliest = min(tweets, key=lambda x: x.id).id

        if not tweets or new_earliest == earliest_tweet:
            break
        else:
            earliest_tweet = new_earliest
            print("getting tweets before:", earliest_tweet)
            timeline += tweets

    return timeline

def get_tendency():
    Tendencias = kevintool.GetTrendsWoeid(23424801)
    return Tendencias

def countOccurences(str, word): 
      

    a = str.split(" ") 
  

    count = 0
    for i in range(0, len(a)): 
          
        # if match found increase count  
        if (word == a[i]): 
           count = count + 1
             
    return count
### First, lets handle the dictionary:

filepath = "NRC-VAD-Lexicon-ForVariousLanguages.txt"
DiccTot = pd.read_csv(filepath, sep='\t')

### Classify information (defining specific dictionary):

DiccTotEsp = DiccTot[["Word", "Valence", "Arousal", "Dominance","Spanish-es"]]

DiccEsp = DiccTotEsp["Spanish-es"].values.tolist()
DiccVal = DiccTotEsp["Valence"].values.tolist()
DiccAro = DiccTotEsp["Arousal"].values.tolist()
DiccDom = DiccTotEsp["Dominance"].values.tolist()

### Ask user to define screen_name of the people searching

target = input("Inserta el nombre de usuario")

################################################################



### Import tweets from a particular person

files_in_twitter = get_tweets(kevintool, screen_name = target)
tweets = []

### Clean text information from tweets

for i in files_in_twitter:
    tweets.append(i.text)

### Remove extra unused information
    
for i in range(0, len(tweets)-1):
    tweets[i] = tweets[i].replace("RT", "")
    tweets[i] = re.sub(r"http\S+", "", tweets[i])
    tweets[i] = re.sub(r"@\S+", "", tweets[i])     

### Convert into a dataframe

tweets_df = pd.DataFrame(tweets)

### Check elements of the tweet

# First break words of the tweet and then analyse each one

Valoraciones = []
Arrechos = []
Dominancias = []

PalabrasUsadas = []

for i in range(0,len(tweets_df)-1):
    Valoracion = 0
    Medibles = 0
    Arrecho = 0
    Dominancia = 0
    palabras = tweets_df.iat[i,0].split()
    for j in range(0,len(palabras)-1):
        if palabras[j] in DiccEsp:
            Valoracion += DiccVal[DiccEsp.index(palabras[j])]
            Arrecho += DiccAro[DiccEsp.index(palabras[j])]
            Dominancia += DiccDom[DiccEsp.index(palabras[j])]
            Medibles += 1
            
            
    Valoraciones.append(Valoracion)
    Arrechos.append(Arrecho)
    Dominancias.append(Dominancia)
    PalabrasUsadas.append(Medibles)
    


#### Generacion de los graficos:
    
sizetweets = [i for i in range(0, len(tweets_df)-1)]
valoraciones_np = np.array(Valoraciones)
arrechos_np = np.array(Arrechos)
dominantes_np = np.array(Dominancias)

zval = np.polyfit(sizetweets, Valoraciones, 1)
zare = np.polyfit(sizetweets, Arrechos, 1)
zdom = np.polyfit(sizetweets, Dominancias, 1)
pval = np.poly1d(zval)
pare = np.poly1d(zare)
pdom = np.poly1d(zdom)

    
fig = plt.figure()
ax = fig.add_subplot(111)
ax.hlines(valoraciones_np.mean(), 0, len(tweets_df)-1)
ax.plot(sizetweets,pval(sizetweets),"b--")
ax.plot(sizetweets, Valoraciones, 'o', label='Valence ' + target,
        markersize=0.4, color = "green")
ax.set_xlabel('Time (tweets)')
ax.set_ylabel('Valencia' + target)

plt.show()

fig.savefig( 'Valencia' + target + ".png")   


fig1 = plt.figure()
ax1 = fig1.add_subplot(111)
ax1.hlines(arrechos_np.mean(), 0, len(tweets_df)-1)
ax1.plot(sizetweets,pare(sizetweets),"b--")
ax1.plot(sizetweets, Arrechos, 'o', label='Arousal ' + target,
        markersize=0.4, color = "yellow")
ax1.set_xlabel('Time (tweets)')
ax1.set_ylabel('Arousal' + target)

plt.show()

fig1.savefig( 'Arousal' + target + ".png") 


fig2 = plt.figure()
ax2 = fig2.add_subplot(111)
ax2.hlines(dominantes_np.mean(), 0, len(tweets_df)-1)
ax2.plot(sizetweets,pdom(sizetweets),"b--")
ax2.plot(sizetweets, Dominancias, 'o', label='Dominance ' + target,
        markersize=0.4, color = "red")
ax2.set_xlabel('Time (tweets)')
ax2.set_ylabel('Dominance' + target)


plt.show()

fig2.savefig( 'Dominance' + target + ".png")    

    
    
