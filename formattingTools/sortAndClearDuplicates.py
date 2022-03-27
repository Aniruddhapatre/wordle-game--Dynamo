from json import load, dump
from msvcrt import getch
import re
dataDict = {}
# https://stackoverflow.com/questions/4836710/is-there-a-built-in-function-for-string-natural-sort
def naturalSort(arr): 
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(arr, key=alphanum_key)

print("Reading data file...")
with open("words.old.json", "r", encoding="utf-8") as fil:
    dataDict = load(fil)
print("Reading data file completed!")

print("Sorting data...")
dataDict["data"] = naturalSort(list(set([word for word in dataDict["data"]])))
print("Sorting completed")

# https://stackoverflow.com/questions/18337407/saving-utf-8-texts-with-json-dumps-as-utf8-not-as-u-escape-sequence
print("Writing data file...")
with open("words.json", "w", encoding="utf-8") as fil:
    dump(dataDict, fil, ensure_ascii=False, indent=4)
print("Writing data file completed!")
print("Press any key to exit...")
getch()