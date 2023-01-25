"""Solve the Wordle game using SeleniumBase.
This test runs on archived versions of Wordle, containing Shadow-DOM."""
import ast
import random
import requests
from seleniumbase import version_tuple
from seleniumbase import BaseCase

if __name__ == "__main__":
    from pytest import main
    main([__file__, "--sjw", "--pls=none"])


class WordleTests(BaseCase):

    word_list = []

    def initialize_word_list(self):
        txt_file = "https://seleniumbase.github.io/cdn/txt/wordle_words.txt"
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
            if letter_status[i] == "absent":
                if (
                    word[i] not in correct_letters
                    and word[i] not in present_letters
                ):
                    for w in self.word_list:
                        if word[i] not in w:
                            new_word_list.append(w)
                else:
                    for w in self.word_list:
                        if word[i] != w[i]:
                            new_word_list.append(w)
                self.word_list = new_word_list
                new_word_list = []

    def skip_if_incorrect_env(self):
        if self.headless:
            message = "This test doesn't run in headless mode!"
            print(message)
            self.skip(message)
        if not self.is_chromium():
            message = "This test requires a Chromium-based browser!"
            print(message)
            self.skip(message)
        if version_tuple < (4, 0, 0):
            message = "This test requires SeleniumBase 4.0.0 or newer!"
            print(message)
            self.skip(message)

    def test_wordle(self):
        self.skip_if_incorrect_env()
        random.seed()
        year = "2022"
        month = random.randint(3, 5)
        day = random.randint(1, 30)
        date = str(year) + "0" + str(month) + str(day)
        archive = "https://web.archive.org/web/"
        url = "https://www.nytimes.com/games/wordle/index.html"
        past_wordle = archive + date + "/" + url
        print("\n" + past_wordle)
        self.open(past_wordle)
        self.wait_for_element("#wm-ipp-base")
        self.remove_elements("#wm-ipp-base")
        self.click("game-app::shadow game-modal::shadow game-icon")
        self.initialize_word_list()
        keyboard_base = "game-app::shadow game-keyboard::shadow "
        word = random.choice(self.word_list)
        num_attempts = 0
        found_word = False
        for attempt in range(6):
            num_attempts += 1
            word = random.choice(self.word_list)
            letters = []
            for letter in word:
                letters.append(letter)
                button = 'button[data-key="%s"]' % letter
                self.click(keyboard_base + button)
            button = "button.one-and-a-half"
            self.click(keyboard_base + button)
            row = 'game-app::shadow game-row[letters="%s"]::shadow ' % word
            tile = row + "game-tile:nth-of-type(%s)"
            self.wait_for_element(tile % "5" + '::shadow [data-state$="t"]')
            self.wait_for_element(
                tile % "5" + '::shadow [data-animation="idle"]'
            )
            letter_status = []
            for i in range(1, 6):
                letter_eval = self.get_attribute(tile % str(i), "evaluation")
                letter_status.append(letter_eval)
            if letter_status.count("correct") == 5:
                found_word = True
                break
            self.word_list.remove(word)
            self.modify_word_list(word, letter_status)

        self.save_screenshot_to_logs()
        if found_word:
            print('Word: "%s"\nAttempts: %s' % (word.upper(), num_attempts))
        else:
            print('Final guess: "%s" (Not the correct word!)' % word.upper())
            self.fail("Unable to solve for the correct word in 6 attempts!")
        self.sleep(3)
