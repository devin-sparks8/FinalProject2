from PyQt6.QtWidgets import *

import wordList
from hangmanGui import *
import random

class Logic(QMainWindow, Ui_MainWindow):
    '''
    Class for Logic, and the GUI
    '''
    lives = 6
    guessed_letters = []
    def __init__(self) -> None:
        '''
        Method to setup the GUI, connects buttons with difficulty levels, hides gui visuals like the hangman
        '''
        super().__init__()
        self.setupUi(self)

        self.level1Button.clicked.connect(self.level1)
        self.level2Button.clicked.connect(self.level2)
        self.level3Button.clicked.connect(self.level3)
        self.guessButton.clicked.connect(self.levelGuess)

        self.head.hide()
        self.rightArm.hide()
        self.leftArm.hide()
        self.body.hide()
        self.rightLeg.hide()
        self.leftLeg.hide()

    def level1(self) -> None:
        '''
        Method to build the first level once button level 1 is clicked
        :return: Spaces for the level 1 word, sets lives
        '''
        self.hangmanPages.setCurrentWidget(self.gamescreen)
        self.Word = random.choice(wordList.easyWords)
        self.blanks = ('____')
        self.blanksArea.setText(self.blanks)
        self.livesBox.setText(f'{self.lives}')

    def level2(self) -> None:
        '''
        Method to build the second level once button level 2 is clicked
        :return: Spaces for the level 2 word, sets lives
        '''
        self.hangmanPages.setCurrentWidget(self.gamescreen)
        self.Word = random.choice(wordList.mediumWords)
        self.blanks = ('_______')
        self.blanksArea.setText(self.blanks)
        self.livesBox.setText(f'{self.lives}')

    def level3(self) -> None:
        '''
        Method to build the third level once button level 3 is clicked
        :return: Spaces for the level 3 word, sets lives
        '''
        self.hangmanPages.setCurrentWidget(self.gamescreen)
        self.Word = random.choice(wordList.hardWords)
        self.blanks = ('__________')
        self.blanksArea.setText(self.blanks)
        self.livesBox.setText(f'{self.lives}')

    def levelGuess(self) -> None:
        '''
        Method to evaluate guesses, check for invalid guesses, exception handling, keeps track of previous guesses, checks win/loss
        :return: Letters on lines, Lives if the player guesses incorrectly, raises text errors for incorrect guesses
        '''
        try:
            self.guess = self.guessLine.text().strip().lower()
            self.invalidGuess.clear()
            if not self.guess.isalpha():
                raise TypeError
            elif len(self.guess) != 1:
                raise ValueError
            elif self.guess in self.guessed_letters:
                raise KeyError
            else:
                self.guessed_letters.append(self.guess)
        except TypeError:
            self.guessLine.clear()
            self.invalidGuess.setText('Please enter a lowercase letter')
        except ValueError:
            self.guessLine.clear()
            self.invalidGuess.setText('Please enter one lowercase letter')
        except KeyError:
            self.guessLine.clear()
            self.invalidGuess.setText('You already guessed that letter')
        else:
            self.guessLine.clear()
            if self.guess not in self.Word:
                self.lives -= 1
                self.livesBox.setText(f'{self.lives}')
                self.discardedLetters.setText(str(self.guessed_letters))
                self.showHangman()
            guessList = list(self.blanks[:].strip(' '))
            for letter in range(len(self.Word)):
                if self.guess == self.Word[letter]:
                    guessList[letter] = self.guess
            self.blanks = ''.join(guessList)
            self.blanksArea.setText(self.blanks)
            self.lostWordLabel.setText(f'Your word was: {self.Word}')
            if self.blanks == self.Word:
                self.hangmanPages.setCurrentWidget(self.youWonScreen)
                self.wonHomeButton.clicked.connect(self.goHome)
                (self.wonWordLabel.setText(f'Your word was: {self.Word}'))

    def showHangman(self) -> None:
        '''
        Method to show the hangman once a player incorrectly guesses
        :return: Body of the hangman, Moves player to lost screen if applicable
        '''
        if self.lives == 5:
            self.head.show()
        if self.lives == 4:
            self.body.show()
        if self.lives == 3:
            self.leftArm.show()
        if self.lives == 2:
            self.rightArm.show()
        if self.lives == 1:
            self.leftLeg.show()
        if self.lives == 0:
            self.rightLeg.show()
            self.hangmanPages.setCurrentWidget(self.youLostScreen)
            self.lostHomeButton.clicked.connect(self.goHome)

    def goHome(self) -> None:
        '''
        Method to hide the hangman once a player completes the game, resets lives, clears first list, clears text boxes
        :return: New lives, New list, New Text Boxes, covered hang man
        '''
        self.hangmanPages.setCurrentWidget(self.homescreen)
        self.head.hide()
        self.body.hide()
        self.rightArm.hide()
        self.leftArm.hide()
        self.leftLeg.hide()
        self.rightLeg.hide()
        self.discardedLetters.clear()
        self.livesBox.clear()
        self.lives = 6
        self.invalidGuess.clear()
        self.wonWordLabel.clear()
        self.lostWordLabel.clear()
        self.guessed_letters.clear()