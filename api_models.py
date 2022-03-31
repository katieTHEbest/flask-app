import requests
import re
import random

MODEL = 'ruwikiruscorpora_upos_cbow_300_10_2021'
FORMAT = 'csv'
WORD = 'свинья'

def api_neighbor(m, w, f):
    neighbors = {}
    url = '/'.join(['http://rusvectores.org', m, w, 'api', f]) + '/'
    r = requests.get(url=url, stream=True)
    for line in r.text.split('\n'):
        try: # первые две строки в файле -- служебные, их мы пропустим
            word, sim = re.split('\s+', line) # разбиваем строку по одному или более пробелам
            neighbors[word] = sim
        except:
            continue
    return neighbors

def one_neighb(dict):
    neighb, simil = random.choice(list(dict.items()))
    neighb = neighb.split('_')[0]
    simil = round(float(simil), 2)
    return str(neighb) + ' ' + str(simil)

#print(api_neighbor(MODEL, WORD, FORMAT))

def api_similarity(m, w1, w2):
    url = '/'.join(['https://rusvectores.org', m, w1 + '__' + w2, 'api', 'similarity/'])
    r = requests.get(url, stream=True)
    sim = float(r.text.split('\t')[0])
    return round(sim, 2), closeness(w1, w2, sim)

def closeness(w1,w2,sim):
    if w1 == w2:
        return "Абсолютно верно"
    elif sim < 0.2:
        return "Холодно"
    elif sim < 0.5:
        return "Тепло"
    else:
        return "Горячо"
