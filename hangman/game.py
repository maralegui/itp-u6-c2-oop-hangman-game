from .exceptions import *
import random

class GuessAttempt(object):
    def __init__(self, char, hit = None, miss = None):
        self.char = char
        if hit:
            self.hit = hit
            self.miss = not hit
        if miss:
            self.miss = miss
            self.hit = not miss
        if hit == miss:
            raise InvalidGuessAttempt
    
    def is_miss(self):
        if self.miss == True or self.hit == False:
            return True
        else:
            return False
        
    def is_hit(self):
        if self.hit == True or self.miss == False:
            return True
        else:
            return False
        
class GuessWord(object):
    def __init__(self, answer, masked = ""):
        self.answer = answer.lower()
        self.masked = "*" * len(answer)
        if len(self.answer) == 0 or len(self.answer) != len(self.masked):
            raise InvalidWordException
            
    def perform_attempt(self, char_m):  
        char= char_m.lower()
        if len(char) != 1:
            raise InvalidGuessedLetterException
        new_masked = ""
        for pos in range(0,len(self.answer)):
            if char == self.answer[pos] :
                new_masked += char
            else:
                new_masked += self.masked[pos]
        self.masked = new_masked
        if char in self.answer:
            return GuessAttempt(char, hit=True)
        else:
            return GuessAttempt(char, miss=True)     
        

class HangmanGame(object):
    WORD_LIST = ['rmotr', 'python', 'awesome']
    
    def __init__(self, WORD_LIST = None, number_of_guesses = None):
        self.previous_guesses = []
        if number_of_guesses:
            self.number_of_guesses = number_of_guesses
        else:
            self.number_of_guesses = 5
        if not WORD_LIST:
            WORD_LIST = HangmanGame.WORD_LIST
        self.WORD_LIST = WORD_LIST
        if len(WORD_LIST)>1:           
            self.answer = HangmanGame.select_random_word(HangmanGame.WORD_LIST)
        else:
            self.answer = self.WORD_LIST[0]
        self.remaining_misses = self.number_of_guesses 
        self.masked = "*" * len(self.answer)
        self.new_masked = ""
        self.word = GuessWord(self.answer, self.masked)
    
    @classmethod    
    def select_random_word(cls, lista):
        if len(lista) > 0:
            word_to_guess = random.choice(lista)
            return word_to_guess
        else:
            raise InvalidListOfWordsException
    
    def add_previous_guesses(self):        
        return self.previous_guesses.append(self.perform_attempt(char))
    
    def guess(self, char):
        if self.is_finished():
            raise GameFinishedException
        self.word.perform_attempt(char)    
        self.previous_guesses.append(char.lower())  
        if self.is_won():
            self.is_finished()
            raise GameWonException
        if char.lower() not in self.word.answer.lower():
            self.remaining_misses -= 1
            self.number_of_guesses -= 1
        if self.number_of_guesses == 0 and self.is_lost():
            self.is_finished()
            raise GameLostException        
        return self.word.perform_attempt(char)

    def is_finished(self):
        if self.word.answer.lower() == self.word.masked.lower() or self.number_of_guesses == 0 or self.remaining_misses == 0:
            return True
        else:
            return False
    
    def is_lost(self):
        if self.word.answer.lower() != self.word.masked.lower():
            return True
        else:
            return False
    def is_won(self):
        if self.word.answer.lower() == self.word.masked.lower():
            return True
        else:
            return False

        