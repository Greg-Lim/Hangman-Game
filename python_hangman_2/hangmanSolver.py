

# rules used for this hang man
# guessing the final word does not use a guess if correct
# guessing all letters and wrong words use a guess


import time

ALPHA_LETTERS = {'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z'}

def hangman_solver(dictionary):
    # dictionary is the base for everything
    memoizationTable = {}

    functionCalls = [0]*5



    # returns the best character and expected number of guess
    def hangman_best_letter(dictionaryLeft: list[int]):
        functionCalls[0]+=1

        dictLength = len(dictionaryLeft)
        if dictLength == 1: return [dictionaryLeft[0:1], 0] # final word is free
        if dictLength == 2: return [dictionaryLeft[0:1], 0.5] # 50 50 to get final word
        hash = uniqueHasher(dictionaryLeft)
        # print(len(memoizationTable))
        # print(hash)
        if hash in memoizationTable: return memoizationTable[hash]

        # return all letters and their posible states
        # TODO improvement: count the states of the same word many times
        letterDictionary = allStatesCounter(dictionaryLeft)

        letterAndExpected = {}

        for letter, stateList in letterDictionary.items():
            letterAndExpected[letter] = 1
            for state, stateCount in stateList.items():
                if stateCount == dictLength : # the number of state is the entire dictionary left
                    break 
                # (number of occurence/total dictionary) * expected guess of given state
                # print("state: ", state)
                # print("dic:", dictionaryLeft)
                # print("letter:", letter)
                # print("after reduced: ", filterDictWithState(dictionaryLeft, state, letter))
                # print("lhs", (stateCount/dictLength))
                t = hangman_best_letter(filterDictWithState(dictionaryLeft, state, letter))
                # print("the t: ", t)
                letterAndExpected[letter] += (stateCount/dictLength) * t[1]
            
            # print(stateList, dictionaryLeft, letter, letterAndExpected)
            # TODO Improve performance: is more the least, can skip???
            if letterAndExpected[letter] == 1: break # increase performance

        key = min(zip(letterAndExpected.values(), letterAndExpected.keys()))[1]
        memoizationTable[hash] = [key, letterAndExpected[key]]
        return [key, letterAndExpected[key]]

    def allStatesCounter(dictionaryLeft: list[int]):
        functionCalls[1]+=1

        allLetters:set[chr] = set(''.join([dictionary[i] for i in dictionaryLeft]))

        letterDict = {}

        for letter in allLetters:
            letterPatternFrequencyDict = {}
            for wordIdx in dictionaryLeft:
                key = toIndexesStr(dictionary[wordIdx], letter)
                if key in letterPatternFrequencyDict: letterPatternFrequencyDict[key] +=1
                else: letterPatternFrequencyDict[key]=1
            
            # print(letterPatternFrequencyDict)
            letterDict[letter] = letterPatternFrequencyDict
                
        # print(letterDict)
        return letterDict


    def toIndexesStr(word: str, letter: chr) -> str:
        functionCalls[2]+=1

        stateWord = ''
        for i in word:
            if i == letter: stateWord+=i
            else: stateWord+="_"
            
        return stateWord

    # state in format "a_a_"
    def filterDictWithState(dictionaryLeft, state, guessed_letter):
        functionCalls[3]+=1

        tempDictionaryIdxes = []

        if set(state) == {"_"}:
            # tempDictionaryIdxes = list(filter(lambda x: (not guessed_letter in x), [dictionary[i] for i in dictionaryLeft]))
            tempDictionaryIdxes = list(filter(lambda x: (not guessed_letter in dictionary[x]), dictionaryLeft))
            return tempDictionaryIdxes

        for wordIdx in dictionaryLeft:
            for dLetter, sLetter in zip(dictionary[wordIdx],state):
                if sLetter == "_" and dLetter == guessed_letter: break
                if sLetter == "_": continue
                if sLetter == dLetter: continue
                break
            else:
                tempDictionaryIdxes.append(wordIdx)
        return tempDictionaryIdxes
    
    def uniqueHasher(tempDictIdxes: list[int]):
        functionCalls[4]+=1

        hash = 0
        for i in tempDictIdxes:
            hash+=pow(2,i)
        return hash

    r = hangman_best_letter([*range(len(dictionary))])
    # print(functionCalls)
    print(memoizationTable)
    return r


# print(hangman_best_letter(["ab", "cb", "ca"]))
# print(hangman_best_letter(["abc", "acb","dac","eba","aba","aac"]))
# print(hangman_solver([
#         "b123", 
#         "ac45",
#         "abc6",
#         "ab7c",
#         "a89c",
#         "zaby",
#         "bxaw",
#         "bvua",
#     ]))

# print(hangman_solver([
#     "AB12",
#     "AC34",
#     "AD56",
#     "AE78",
#     "ZYBC",
#     "XWCB"
# ]))

# best counter example
# print(hangman_solver([
#     "ABC", "ABD", "AEF", "EGH"
# ]))

length = 8
noWords = 10
with open(f"{length}.txt", 'r') as dict:
    dict = dict.read().splitlines()
    # print(dict)
    tic = time.perf_counter()
    print(hangman_solver(dict[0:noWords]))
    toc = time.perf_counter()
    print(dict[0:noWords])
    print(f"Ran in  {toc - tic:0.4f} seconds")




def test_hangman_best_letter():

    assert hangman_solver([
        "ab", "cb", "ca"
    ])[0] == 'a'

    assert hangman_solver([
        "abc", 
        "acb",
        "dac",
        "eba",
        "aba",
        "aac",
    ])[0] == 'a'

    # ai says a b and c are all good choices
    assert hangman_solver([
        "abcd", 
        "abce",
        "acbd",
        "acbe",
        "acce",
        "zaby",
        "bxaw",
        "bvua",
    ])[0] == 'a'

    # v this test may not be correct
    assert hangman_solver([
        "a123", 
        "ac45",
        "abc6",
        "ab7c",
        "a89c",
        "zaby",
        "bxaw",
        "bvua",
    ])[0] == 'a' # Should be c
