
import os
import sys
import json

def run(target):
    if not (os.path.exists(target)):
        return -1
    handle = open(target, "r")
    content = handle.read()
    handle.close()
    data = json.loads(content.strip())
    for root, folders, files in os.walk(os.getcwd()):
        for name in files:
            if not ((name.endswith(".csv")) and (name.startswith("wn_"))):
                continue
            key = name[3:(len(name)-4)]
            if not (key in data):
                continue
            path = os.path.join(root, name)
            handle = open(path, "r")
            lines = handle.readlines()
            handle.close()
            lines = [",".join(data[key])]+lines
            handle = open(path, "w")
            for line in lines:
                handle.write(line.strip()+"\n")
            handle.close()
    return 0

def launch(arguments):
    if (len(arguments) < 1):
        return False
    target = os.path.basename(arguments[0])
    if not (target.endswith(".py")):
        return False
    target = target[:(len(target)-3)]+".json"
    result = run(os.path.join(os.getcwd(), target))
    print(str(result))
    if not (result == 0):
        return False
    return True

if (__name__ == "__main__"):
    print(str(launch(sys.argv)))

