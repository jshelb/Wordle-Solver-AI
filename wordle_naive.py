import random
from termcolor import colored


### Taken from the github repo
class Wordle:
   ''' Class representing one wordle game.
   methods include initiating a secret word,
   returning green/yellow/grey results,
   keeping track of guessed letters
   '''

   def __init__(self, words_list, correct_word=None):
       # the word to guess
       self.correct_word = random.choice(words_list) if correct_word == None else correct_word


       # list of guesses so far
       self.guesses = []
       self.results = []


   def __str__(self):
       out = f"::{self.correct_word}::"
       for i, guess in enumerate(self.guesses):
           out += f"\n{i+1}. {guess}"
       return out


   def guess(self, word):
       ''' One turn of the game
       get guessed word, add new Guess in guesses list
       if guessed correctly, return True, else False
       '''
       self.guesses.append(word)
       out = ""
       for guess_letter, correct_letter in zip(word, self.correct_word):
           if guess_letter == correct_letter:
               out += "G"
           elif guess_letter in self.correct_word:
               out += "Y"
           else:
               out += "_"
       self.results.append(out)
       # Return True/False if you got the word right
       return word ==  self.correct_word
   
   # works well, I think we could use the old possible guess list rather than regenerating for future scaling
   def naive_filter(self, validGuesses):
      # get last result and guess
       result = self.results[-1]
       lastGuess = self.guesses[-1]

       failedWords = list()
       for guess in validGuesses:
           for i in range(5):
               if result[i] == '_':
                   # this letter isn't in the word
                   if lastGuess[i] in guess:
                       failedWords.append(guess)
               elif result[i] == 'Y':
                   # this letter isn't here
                   if (lastGuess[i] not in guess) or (guess[i] == lastGuess[i]):
                       failedWords.append(guess)
               elif result[i] == 'G':
                   # this location must be this letter
                   if guess[i] != lastGuess[i]:
                       failedWords.append(guess)

       filteredGuesses = list()
       for guess in validGuesses:
           if guess not in failedWords:
               filteredGuesses.append(guess)

       return filteredGuesses

    # play a wordle game with naive strat, given startword
    # returns i, the number of guesses to find the word
   def play_game(self, startword, verbose=True):
       if verbose: print('GUESSING: ', startword)
        
       prevGuess = startword
       # simulate one game
       possible_words = words_list
       while(not (self.guess(prevGuess))):
           if verbose: print('RESULT: ', self.results[len(self.guesses) - 1])
           possible_words = self.naive_filter(possible_words)
           if verbose: print('POSSIBLE ANSWERS: (', str(len(possible_words)), ') ' , possible_words)

           nextGuess = random.choice(possible_words)
           if verbose: print('GUESSING: ', nextGuess)
           prevGuess = nextGuess

       if verbose: 
           if len(self.guesses) > 6: print(colored('Guess max (6) exceded', 'red'))
           strout = 'correct word: '+ self.correct_word + ' found in ' + str(len(self.guesses)) + ' guesses!'
           print(colored(strout, 'green'))

       return len(self.guesses)




def get_word_list(filename):
   words = []
   with open(filename, "r", encoding="UTF-8") as in_file:
           for line in in_file:
               words.append(line.strip())
   return words


words_list = get_word_list("data/words-guess.txt")

if __name__ == '__main__':

    wordle = Wordle(words_list)

    wordle.play_game('tares')