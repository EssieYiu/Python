# Problem Set 4C
# Name: 17340027 姚洁倩
# Collaborators:None
# Time Spent: 

import string
import copy
from ps4a import get_permutations

### HELPER CODE ###
def load_words(file_name):
    '''
    file_name (string): the name of the file containing 
    the list of words to load    
    
    Returns: a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    '''
    
    print("Loading word list from file...")
    # inFile: file
    inFile = open(file_name, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.extend([word.lower() for word in line.split(' ')])
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.
    
    Returns: True if word is in word_list, False otherwise

    Example:
    >>> is_word(word_list, 'bat') returns
    True
    >>> is_word(word_list, 'asdf') returns
    False
    '''
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list


### END HELPER CODE ###

WORDLIST_FILENAME = 'words.txt'

# you may find these constants helpful
VOWELS_LOWER = 'aeiou'
VOWELS_UPPER = 'AEIOU'
CONSONANTS_LOWER = 'bcdfghjklmnpqrstvwxyz'
CONSONANTS_UPPER = 'BCDFGHJKLMNPQRSTVWXYZ'

class SubMessage(object):
    def __init__(self, text):
        self.message_text = text
        self.valid_words = load_words('words.txt')
    
    def get_message_text(self):
        return self.message_text

    def get_valid_words(self):
        valid_words = copy.deepcopy(self.valid_words)
        return valid_words
                
    def build_transpose_dict(self, vowels_permutation):
        transpose_dict = {}
        for char in string.ascii_lowercase:
            if char not in VOWELS_LOWER:
                transpose_dict[char] = char
        for char in string.ascii_uppercase:
            if char not in VOWELS_UPPER:
                transpose_dict[char] = char
        for i in range(5):
            transpose_dict[VOWELS_LOWER[i]] = vowels_permutation[i]
            transpose_dict[VOWELS_UPPER[i]] = chr(ord(vowels_permutation[i])-ord(' '))
        return transpose_dict
    
    def apply_transpose(self, transpose_dict):
        
        text = self.get_message_text()
        transpose_text = ""
        for char in text:
            if transpose_dict.get(char,0):
                transpose_text = transpose_text + transpose_dict[char]
            else:
                transpose_text = transpose_text + char
        return transpose_text

class EncryptedSubMessage(SubMessage):
    def __init__(self, text):
        SubMessage.__init__(self,text)

    def decrypt_message(self):
        maximum_valid = 0
        best_text = self.get_message_text()
        all_permutation = get_permutations('aeiou')
        for possible_permutation in all_permutation:
            transpose_dict = self.build_transpose_dict(possible_permutation)
            possible_text = self.apply_transpose(transpose_dict)
            possible_text = possible_text.split(' ')
            valid_word_num = 0
            for word in possible_text:
                if is_word(self.get_valid_words(),word):
                    valid_word_num = valid_word_num + 1
            if valid_word_num > maximum_valid:
                maximum_valid = valid_word_num
                best_text = " ".join(possible_text)
        return best_text

if __name__ == '__main__':

    # Example test case
    message = SubMessage("Hello World!")
    permutation = "eaiuo"
    enc_dict = message.build_transpose_dict(permutation)
    print("Original message:", message.get_message_text(), "Permutation:", permutation)
    print("Expected encryption:", "Hallu Wurld!")
    print("Actual encryption:", message.apply_transpose(enc_dict))
    enc_message = EncryptedSubMessage(message.apply_transpose(enc_dict))
    print("Decrypted message:", enc_message.decrypt_message())
     
    #TODO: WRITE YOUR TEST CASES HERE
    #Test case 1
    message1 = SubMessage("It's a good idea.")
    permutation1 = 'iouea'
    enc_dict1 = message1.build_transpose_dict(permutation1)
    print("Original message:",message1.get_message_text(),"Permutation:",permutation1)
    print("Expected encryption:","Ut's i geed udoi.")
    print("Actual encryption:",message1.apply_transpose(enc_dict1))
    enc_message1 = EncryptedSubMessage(message1.apply_transpose(enc_dict1))
    print("Decrypted message:",enc_message1.decrypt_message())

    #Test case 2
    message2 = SubMessage("Bravo! This code is splendid")
    permutation2 = 'oueai'
    enc_dict2 = message2.build_transpose_dict(permutation2)
    print("Original message:",message2.get_message_text(),"Permutation:",permutation2)
    print("Expected encryption:","Brova! Thes cadu es splunded")
    print("Actual encryption:",message2.apply_transpose(enc_dict2))
    enc_message2 = EncryptedSubMessage(message2.apply_transpose(enc_dict2))
    print("Decrypted message:",enc_message2.decrypt_message())