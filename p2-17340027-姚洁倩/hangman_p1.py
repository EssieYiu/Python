import random
import string

WORDLIST_FILENAME = "words.txt"
GUESS = 6
def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist



def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)
wordlist = load_words()
def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!
    
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
    
    Follows the other limitations detailed in the problem write-up.
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    guess_time = GUESS
    already_guessed = []
    correct = 0
    letters_guessed=[]
    print('Welcome to the game Hangman!')
    print('I am thinking of a word that is',len(secret_word),'letters long.')
    while guess_time:
        print('-------------')
        print('You have',guess_time,'guesses left.')
        letter_guessing = input('Please guess a letter:\n')
        if letter_guessing in secret_word:
            if already_guessed.count(letter_guessing) == 0:
                already_guessed.append(letter_guessing)
                print('Good guess:',end='')
            else:
                print('This letter is already guessed\n')
            correct = 1
        else:
            print('This letter is not in my word')
            guess_time = guess_time -1 

        for i in secret_word:
            if already_guessed.count(i) != 0:
                print(i,end='')
            else:
                print('_',end='')
                correct = 0
        print('\n')

        if correct == 1:
            print('You win\n')
            return       
    print('You lose')
    print('The secret word is',secret_word)
# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
#(hint: you might want to pick your own
# secret_word while you're doing your own testing)

if __name__ == '__main__':
    secret_word = choose_word(wordlist)
    hangman(secret_word)
    input()