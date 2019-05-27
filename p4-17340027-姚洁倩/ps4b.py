# Problem Set 4B
# Name:17340027 姚洁倩
# Collaborators:None
# Time Spent: 

import string
import copy
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

def get_story_string():
    """
    Returns: a story in encrypted text.
    """
    f = open("story.txt", "r")
    story = str(f.read())
    f.close()
    return story

### END HELPER CODE ###

WORDLIST_FILENAME = 'words.txt'

class Message(object):
    def __init__(self, text):
        self.message_text = text
        self.valid_words = load_words("words.txt")

    def get_message_text(self):

        return self.message_text

    def get_valid_words(self):
        valid_words = copy.deepcopy(self.valid_words)
        return valid_words

    def build_shift_dict(self, shift):
        shift_dic = {}
        for lower in string.ascii_lowercase:
            shift_dic[lower] = chr((ord(lower)-ord('a')+shift)%26+ord('a'))
        for upper in string.ascii_uppercase:
            shift_dic[upper] = chr((ord(upper)-ord('A')+shift)%26+ord('A'))
        return shift_dic

    def apply_shift(self, shift):
        ciphertext = ""
        shift_dic = self.build_shift_dict(shift)
        text = self.get_message_text()
        for char in text:
            if shift_dic.get(char,0):
                ciphertext = ciphertext + shift_dic[char]
            else:
                ciphertext = ciphertext + char
        return ciphertext

class PlaintextMessage(Message):
    def __init__(self, text, shift):
        Message.__init__(self,text)
        self.shift = shift
        self.encryption_dict = self.build_shift_dict(shift)
        self.message_text_encrypted = self.apply_shift(shift)

    def get_shift(self):
        return self.shift

    def get_encryption_dict(self):
        encrypt_dic = copy.deepcopy(self.encryption_dict)
        return encrypt_dic

    def get_message_text_encrypted(self):
        return self.message_text_encrypted

    def change_shift(self, shift):
        self.shift = shift
        self.encryption_dict = self.build_shift_dict(shift)
        self.message_text_encrypted = self.apply_shift(shift)



class CiphertextMessage(Message):
    def __init__(self, text):
        Message.__init__(self,text)

    def decrypt_message(self):
        best_decrypt_text = ""
        best_decrypt_shift = -1
        maximum_match = 0
        for i in range(26):
            decrypt_text = self.apply_shift(i)
            decrypt_text = decrypt_text.split(' ')
            match = 0
            for word in decrypt_text:
                if is_word(self.get_valid_words(),word):
                    match = match + 1
            if match >= maximum_match:
                decrypt_text = ' '.join(decrypt_text)
                best_decrypt_text = decrypt_text
                best_decrypt_shift = i
                maximum_match = match
        best_tuple = (best_decrypt_shift,best_decrypt_text)
        return best_tuple



if __name__ == '__main__':

    
    #Example test case (PlaintextMessage)
    plaintext = PlaintextMessage('hello', 2)
    print('Expected Output: jgnnq')
    print('Actual Output:', plaintext.get_message_text_encrypted())

    #Example test case (CiphertextMessage)
    ciphertext = CiphertextMessage('jgnnq')
    print('Expected Output:', (24, 'hello'))
    print('Actual Output:', ciphertext.decrypt_message())
    

    #TODO: WRITE YOUR TEST CASES HERE
    #Test case 1(PlaintextMessage)
    print('')
    plaintext1 = PlaintextMessage('London bridge is falling down',5)
    print('Expected Output: Qtsits gwnilj nx kfqqnsl itbs')
    print('Actual Output:',plaintext1.get_message_text_encrypted())

    #Test case 1(CiphertextMessage)
    ciphertext1 = CiphertextMessage('Qtsits gwnilj nx kfqqnsl itbs')
    print('Expected Output:',(21, 'London bride is falling down'))
    print('Actual Output:',ciphertext1.decrypt_message())

    #Test case 2(PlaintextMessage)
    print('')
    plaintext2 = PlaintextMessage("Today's good!", 10)
    print("Expected Output: Dynki'c qyyn!")
    print('Actual Output:', plaintext2.get_message_text_encrypted())

    #Test case 2(CiphertextMessage)
    ciphertext2 = CiphertextMessage("Dynki'c qyyn!")
    print('Expected Output:', (16, "Today's good!"))
    print('Actual Output:', ciphertext2.decrypt_message())

    #TODO: best shift value and unencrypted story 
    print('')
    story_text = get_story_string()
    print('Original text:',story_text)
    story = CiphertextMessage(story_text)
    print('The decryption of the story:')
    print(story.decrypt_message())
