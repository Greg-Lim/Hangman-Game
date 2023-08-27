

length = 8

with open("Dictionary.txt") as dict:
    with open(f"{length}.txt", 'w+') as lengthDict:
        dict = dict.read().splitlines()
        for word in dict:
            if len(word)==length:
                lengthDict.write(word+'\n')
