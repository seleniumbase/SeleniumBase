""" Solve the Wordle game using SeleniumBase.
    The latest version of Wordle no longer uses Shadow-DOM. """

import ast
import random
import requests
from seleniumbase import BaseCase


class WordleTests(BaseCase):

    word_list = []

    def initialize_word_list(self):
        txt_file = "https://seleniumbase.io/cdn/txt/wordle_words.txt"
        word_string = requests.get(txt_file).text
        self.word_list = ast.literal_eval(word_string)

    def modify_word_list(self, word, letter_status):
        new_word_list = []
        correct_letters = []
        present_letters = []
        for i in range(len(word)):
            if letter_status[i] == "correct":
                correct_letters.append(word[i])
                for w in self.word_list:
                    if w[i] == word[i]:
                        new_word_list.append(w)
                self.word_list = new_word_list
                new_word_list = []
        for i in range(len(word)):
            if letter_status[i] == "present":
                present_letters.append(word[i])
                for w in self.word_list:
                    if word[i] in w and word[i] != w[i]:
                        new_word_list.append(w)
                self.word_list = new_word_list
                new_word_list = []
        for i in range(len(word)):
            if (
                letter_status[i] == "absent"
                and word[i] not in correct_letters
                and word[i] not in present_letters
            ):
                for w in self.word_list:
                    if word[i] not in w:
                        new_word_list.append(w)
                self.word_list = new_word_list
                new_word_list = []

    def skip_if_incorrect_env(self):
        if self.headless:
            message = "This test doesn't run in headless mode!"
            print(message)
            self.skip(message)

    def test_wordle(self):
        self.skip_if_incorrect_env()
        self.open("https://www.nytimes.com/games/wordle/index.html")
        self.click('svg[data-testid="icon-close"]')
        self.initialize_word_list()
        word = random.choice(self.word_list)
        num_attempts = 0
        success = False
        for attempt in range(6):
            num_attempts += 1
            word = random.choice(self.word_list)
            letters = []
            for letter in word:
                letters.append(letter)
                button = 'button[data-key="%s"]' % letter
                self.click(button)
            button = 'button[class*="oneAndAHalf"]'
            self.click(button)
            row = (
                'div[class*="lbzlf"] div[class*="Row-module"]:nth-of-type(%s) '
                % num_attempts
            )
            tile = row + 'div:nth-child(%s) div[class*="module_tile__3ayIZ"]'
            self.wait_for_element(tile % "5" + '[data-state*="e"]')
            letter_status = []
            for i in range(1, 6):
                letter_eval = self.get_attribute(tile % str(i), "data-state")
                letter_status.append(letter_eval)
            if letter_status.count("correct") == 5:
                success = True
                break
            self.word_list.remove(word)
            self.modify_word_list(word, letter_status)

        self.save_screenshot_to_logs()
        if success:
            print('\nWord: "%s"\nAttempts: %s' % (word.upper(), num_attempts))
        else:
            print('Final guess: "%s" (Not the correct word!)' % word.upper())
            self.fail("Unable to solve for the correct word in 6 attempts!")
        self.sleep(3)
