
import os
from random import *
# import webbrowser
# import time


min_word_len_allowed = 4
the_alphabats = ('A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z')

#======================================== Word input ========================================
#test if word exist onc the list given
def is_word(word):
    word = word.upper()
    with open('Dictionary.txt', 'r') as dic:
        for line in dic:
            if line.rstrip() == word:
                return True
    return False

#test if input is of sufficient length
def is_fair(word):
    if len(word) >= min_word_len_allowed :
        return True
    else:
        return False

#get a random word
def rand_word(min_len):
    count = 0
    with open("Dictionary.txt", 'r') as dic:
        with open("Temp_Dictionary_Temp.txt", 'w+') as temp_dic:
            for line in dic:
                word = line.strip()
                if len(word) >= min_len:
                    count +=1
                    temp_dic.write(word+'\n')
    word_pos = randint(1, count)
    with open("Temp_Dictionary_Temp.txt", 'r') as temp_dic:
        for line in temp_dic:
            word_pos -=1
            if word_pos == 0:
                return line.strip()

#get valid input form user
def input_valid_word():
    while True:
        word = input("Enter a word of at least length {} (press enter for random word will be chosen): ".format(min_word_len_allowed)).upper()
        if word == '':
            return rand_word(min_word_len_allowed)
        if is_fair(word):
            if is_word(word):
                return word
            else:
                print("Input is not a word!!!")
                print("")
        else:
            print("Input is too short!!!")
            print("")

#======================================== Modify State ========================================

#print state in human friendly format
def print_state(state):
    to_print = ''
    for letter in state:
        to_print = to_print + ' ' + letter
    print(to_print)

# make current blank state of the guess
def make_state(word):
    state = ''
    for char in word:
        state = state + '_'
    return state

#Get letter or word input from user. return True if letter
def get_input():
    return input("Enter a letter or word to guess?: ").upper()

#test if alphabat is present in word and return state
def is_letter_present(alphabat, word, state):
    no_changes = 0
    position = 0
    for letter in word:
        if letter == alphabat:
            state = state[:position] + alphabat + state[position+1:]
            no_changes += 1
        position += 1
    if no_changes == 0:
        return state, 0
    else:
        return state, no_changes

#======================================== Game Modes ========================================
#PVP - Player word and player guess
#PVC - Player word and computer guess
#CVP - Computer word word and player guess

# Game mode setting
def game_set():
    ai_play = True
    no_rounds = int(input("How many people want to guess? (0 for just AI):"))
    if no_rounds != 0:
        if input("Do you want AI to play? (Y)").upper() != 'Y':
            ai_play = False
    return no_rounds, ai_play


#Player guess
def player_guess(word):
    win = False
    no_tries =0
    guessed = []

    print("The word is {} letters long.".format(len(word)))
    state = make_state(word)
    print_state(state)

    while win == False:
        print("")
        guess = get_input()
        if len(guess) == 0 or guess == ' ':
            print("You did not make an input. Please make a valid input")
            continue
        elif guess in guessed:
            print("You already guessed {}".format(guess))
            continue
        else:
            guessed.extend([guess])
            no_tries += 1

        if len(guess) == 1:
            state, no_changes  = is_letter_present(guess, word, state)
            if no_changes == 0:
                print("The letter you guessed is not in the word.")
            elif state == word:
                win = True
            else:
                print("The letter you guessed appeared {} times in the word.".format(no_changes))
            print_state(state)
        else:
            if guess == word:
                win = True
            else:
                print("The word you guess is wrong.")

    print("")
    print("The answer is {}".format(word))
    print("You took {} tries".format(no_tries))
    print("Congratulations")
    input("Press enter to contunue")

#======================================== AI Guess ========================================
#AI Guess
def ai_guess(word):
    guessed_letter_set = set()

    word_length = len(word)

    state = make_state(word)

    temp_dic_count = 0
    word_guess = 0

    state_set = set(state)
    state_set.remove('_')

    make_temp_dic(word_length)

    guess = cheap_proccess(word_length)

    while state != word:
        if temp_dic_count == 1:
            state = the_only_word()
            word_guess += 1
            break

        if len(guessed_letter_set) >0:
            guess = tele_letters("Temp_Dictionary.txt", guessed_letter_set)
        print("My guess is:", guess)
        guessed_letter_set.add(guess)
        state, no_changes = is_letter_present(guess, word, state)
        state_set = set(state)
        if state != word:
            state_set.remove('_')
        #print(state, state_set, guessed_letter_set) #for debugging
        temp_dic_count = append_temp_dic(state, state_set, guessed_letter_set)
        print("Current state is: ", end = ''), print_state(state)
        print('')
    # return state, len(guessed_letter_set)+word_guess
    print("The word is: ", state)
    print("AI took {} guesses".format(len(guessed_letter_set)+word_guess))

def cheap_proccess(word_length):
    if word_length > 11:
        return 'I'
    elif word_length > 5:
        return 'E'
    elif word_length == 5:
        return 'S'
    elif word_length == 2:
        return 'O'
    else:
        return 'A'

#Return True if state is posible
def state_match(state, dic_word):
    state = state.strip()
    position = -1
    for letter in state:
        position += 1
        if letter =='_':
            continue
        elif letter != dic_word[position]:
            return False
    return True

#Return True if no wrong letter is not in word
def guessed_match(guessed_set, state_set, word_set):
    diff_guessed_set_state_set = guessed_set - state_set
    if len(diff_guessed_set_state_set.intersection(word_set))<1:
        return True
    else:
        return False

#Return True if the word in dic is possible with current infomation
def is_possible(dic_word, state, state_set, guessed_letter_set):
    if state_match(state, dic_word):
        dic_word_set = set(dic_word)
        if guessed_match(guessed_letter_set, state_set, dic_word_set):
            return True
            #seems wrong
    else:
        return False

#make a tempoary dictionary of words with same length as answer
def make_temp_dic(word_length):
    with open("Dictionary.txt", 'r') as dic:
        with open("Temp_Dictionary.txt", 'w+') as temp_dic:
            for line in dic:
                word = line.rstrip()
                if len(word) == word_length:
                    temp_dic.write(word+'\n')

#append temp_dic for all current posible words
def append_temp_dic(state, state_set, guessed_letter_set):
    count = 0
    with open("Temp_Dictionary.txt", 'r') as temp_dic:
        with open("Temp_Dictionary_Temp.txt", 'w') as temp:
            for line in temp_dic:
                dic_word = line.strip()
                if is_possible(dic_word, state, state_set, guessed_letter_set):
                    temp.write(dic_word + '\n')

    with open("Temp_Dictionary_Temp.txt", 'r') as temp:
        with open("Temp_Dictionary.txt", 'w') as temp_dic:
            for line in temp:
                temp_dic.write(line)
                count += 1
    return count

def the_only_word():
    with open("Temp_Dictionary.txt", 'r') as temp_dic:
        return temp_dic.readline().strip()

def com_letter_picker(state, guessed):
    pass

#return letter with highest unique count
def tele_letters(file, guessed_set):
    count = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    current_letter = -1 #0 is A and 25 is Z
    highest_count = 0
    current_highest = ''

    for letters in the_alphabats:
        current_letter += 1
        if letters in guessed_set:
            continue
        else:
            with open(file, 'r') as temp_file:
                for line in temp_file:
                    word = line.strip()
                    for letter in word:
                        if letter == letters:
                            count[current_letter] += 1
                            break
            #print ("test1", letters)
            if count[current_letter] > highest_count:
                highest_count = count[current_letter]
                current_highest = the_alphabats[current_letter]

    return current_highest



#======================================== Main ========================================
word = input_valid_word()
no_rounds, ai_play = game_set()

while no_rounds>0:
    os.system('CLS')
    print("Player {}.".format(no_rounds))
    player_guess(word)
    no_rounds-=1

if ai_play == True:
    os.system('CLS')
    ai_guess(word)
    input("Press a key to continue...")



# answer = ''
# no_guess = 0
# word = ''

# highest_guess = 0
# hardest_word = set()

# with open("Dictionary.txt", 'r') as dic:
#     with open("Dictionary_and_freq.txt", 'w+') as data:
#         for line in dic:
#             word = line.strip()
#             answer, no_guess = ai_guess(word)
#             data.write(str(no_guess))
#             data.write(' '+word)
#             data.write('\n')
#             if no_guess>highest_guess:
#                 hardest_word = set()
#                 highest_guess = no_guess
#                 hardest_word.add(word)
#             elif no_guess == highest_guess:
#                 hardest_word.add(word)

# with open("Stats.txt", 'w+') as stats:
#     states.write(highest_guess)
#     states.write('\n')
#     for word in hardest_word:
#         states.write(hardest_word+'\n')








#state_set = set(state)
#state_set.remove('_')

# with open('Dictionary.txt', 'r') as dic:
#     for line in dic:
#         dic_word = line.rstrip()
#         if is_possible(dic_word, state, state_set, guessed_letter_set, answer_length):
#             print(dic_word)



#time.sleep(2)
#webbrowser.open("https://youtu.be/PHgc8Q6qTjc?t=14")
