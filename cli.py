
import os
import csv
import sys

def run(relation, target = None):
    if (relation == "s"):
        return -1
    relations = {}
    keys = {}
    for root, folders, files in os.walk(os.getcwd()):
        for name in files:
            if not ((name.endswith(".csv")) and (name.startswith("wn_"))):
                continue
            path = os.path.join(root, name)
            relation = name[3:(len(name)-4)]
            relations[relation] = path
            handle = open(path, "r")
            line = handle.readline()
            handle.close()
            keys[relation] = line.strip().split(",")
    if not (relation in relations):
        return -2
    if not ("s" in relations):
        return -3
    synsets = {}
    words = {}
    handle = open(relations["s"], "r")
    reader = csv.DictReader(handle)
    for row in reader:
        synset = row["synset_id"]
        number = row["w_num"]
        word = row["word"]
        if not (synset in synsets):
            synsets[synset] = {}
        synsets[synset][number] = word
        if not (word in words):
            words[word] = []
        if not (synset in words[word]):
            words[word].append(synset)
    handle.close()
    handle = open(relations[relation], "r")
    reader = csv.DictReader(handle)
    data = {}
    for row in reader:
        pair = []
        #print(str(keys[relation])+" "+str(list(row.keys())))
        for key in keys[relation]:
            if ((key.startswith("synset_id") and (key in row))):
                pair.append(row[key])
                #print(str(pair))
                if (len(pair) == 2):
                    break
            else:
                print(key)
        if (len(pair) == 2):
            left = pair[0]
            right = pair[1]
            if ((left in synsets) and (right in synsets)):
                if not (left in data):
                    data[left] = []
                if not (right in data[left]):
                    data[left].append(right)
                    #print(left+" -> "+right)
    handle.close()
    quit = False
    while not (quit):
        query = ""
        if (target == None):
            print("Query:")
            try:
                query += input().strip()
            except:
                quit = True
        else:
            query += target.strip()
        if (len(query) == 0):
            quit = True
            continue
        occurrences = []
        for synset in synsets:
            #print(synset)
            if not (synset in data):
                #print(synset)
                continue
            for number in synsets[synset]:
                #print(synset+" = "+str(synsets[synset][number]))
                word = synsets[synset][number]
                #print("\t"+word+" @ "+number)
                if (word == query):
                    occurrences.append(synset)
        for occurrence in occurrences:
            print(query+" @ "+occurrence)
            for link in data[occurrence]:
                print("\t-> "+link)
                for number in synsets[link]:
                    word = synsets[link][number]
                    print("\t\t= "+word+" @ "+number) 
    print(str(len(list(synsets.keys()))))
    return 0

def launch(arguments):
    target = None
    if (len(arguments) < 2):
        return False
    relation = arguments[1].strip()
    if (len(arguments) > 2):
        target = arguments[2].strip()
    result = run(relation, target)
    print(str(result))
    if not (result == 0):
        return False
    return True

if (__name__ == "__main__"):
    print(str(launch(sys.argv)))

