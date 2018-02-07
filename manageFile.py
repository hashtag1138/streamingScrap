import os
import json

def getFilename(title):
    path = "fiches_films"
    return "{}/{}.json".format(path, title.replace(' ','-').replace('-streaming', ''))

def writeJson(film):
    with open(getFilename(film['title']), 'w') as fichier:
        jsonStr = json.dumps(film, ensure_ascii=False, sort_keys=True)
        fichier.write(jsonStr)
        return jsonStr

def existJson(title):
    return os.path.exists(getFilename(title))

if __name__ == "__main__":
    writeJson({'title' : 'titre de test', 'champ2' : [1,2,3]})
