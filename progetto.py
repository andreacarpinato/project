#progetto Start2Impact python

import requests as r
import json
import time
import schedule
from pprint import pprint
from datetime import datetime, timedelta
from threading import Timer
from requests import Session


url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
parameters = {
  'start':'1',
  'limit':'100',
  'convert':'USD'
}
headers = {
  'Accepts': 'application/json',
  
}

#funzione che aggiorna i dati sulle criptovalute presenti sul file .json
def scriviJson(data):
  crypto="crypto"+time.strftime("%Y%m%d")+".json"
  with open(crypto, "w") as outfile:
      json.dump(data,outfile,indent=1)
 

#esercizio 1 Trovare criptovaluta con il massimo volume nelle ultime 24h
def bestVolume(crypto):
  maxcap={'name':' ','cap_value':0 }
  for criptovaluta in crypto['data']:
    if criptovaluta['quote']['USD']['volume_24h'] > maxcap['cap_value']:
      maxcap['name']=criptovaluta['name']
      maxcap['cap_value']=criptovaluta['quote']['USD']['volume_24h']    
  print("\n1)La criptovaluta con maggiore volume e' "+maxcap['name']+" con la quantita "+str(maxcap['cap_value'])+"\n")
  return maxcap



#esercizio 2 Le migliori e peggiori 10 criptovalute (per incremento in percentuale delle ultime 24 ore)
#questa funzione mette in un dizionario{'name':cambio24h} tutti i cambi delle ultime 24 ore,con la funzione sort li ordina e poi selezioniamo i top e flop
def TopFlopCrypto(data):
  change={}
  change2={}
  min={}
  max={}
  for cont in data:
    change[cont['name']]=float(cont['quote']['USD']['percent_change_24h']) #inserisco dentro un dizionario con indice il nome e value il cambio in 24h 
 
  change2={k: v for k, v in sorted(change.items(), key=lambda item: item[1])}#fa la sort del value dal più piccolo al più grande
  print(change2) 
  min= {k: change2[k] for k in list(change2)[:10]}  #prende i più bassi
  max= {k: change2[k] for k in list(change2)[-10:]}  #prende i più alti
  print(" ")
  print("MINIMI: ")
  print(min)
  print("MASSIMI:")
  print(max)
  return


#esercizio 3
# La quantità di denaro necessaria per acquistare un' unità di ciascuna delle prime 20 criptovalute* 
def quantDenaro(data):
  somma=0     #la somma necessaria per acquistare
  c=0
  for cont in data:
    somma=somma+float(cont['quote']['USD']['price'])
    c=c+1
    if c==20 :
      break 
  somma=str(round(somma,2))
  print("La somma di denaro necessaria per acquistare un'unità delle prime 20 criptovalute è: "+somma+" dollari")
  return

#esercizio 4
#La quantità di denaro necessaria per acquistare una unità di tutte le criptovalute il cui volume delle ultime 24 ore sia superiore a 76.000.000$
def quantDen76(data):
  somma=0     #la somma necessaria per acquistare
  for cont in data:
    if float(cont['quote']['USD']['volume_24h']):
     somma=somma+float(cont['quote']['USD']['price']) 
  somma=str(round(somma,2))
  print("La somma di denaro necessaria per acquistare un'unità dellecriptovalute superiori a 76.000.000 è: "+somma+" dollari")
  return

def aggiornamentoGiornaliero():
  data=r.get(url=url,headers=headers,params=parameters).json()
  del data['status']  #elimina la parte delle informazioni come l'ora e la data del GET
  data2=data['data']
 # data=json.load(data)
  #risultati={}
 # temp=bestVolume(data)
  #risultati=temp

  TopFlopCrypto(data2)
  quantDenaro(data2)
  quantDen76(data2)
  #le altre funzioni degli esercizi
  #scrivi su file json risultati
  #pprint(data)
  #print("\n\n\n-------------------------------")
#  pprint(data2)
  return 


  

aggiornamentoGiornaliero()
'''
#autoesecuzione aggiorna dati, presa da https://www.youtube.com/watch?v=Gs5jGDROx1M, uso libreria schedule
schedule.every().day.at("10.30").do(scriviJson)

while True:
    schedule.run_pending()
    time.sleep(1)
'''