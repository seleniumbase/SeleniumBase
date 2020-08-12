""" This test has 2 fails on purpose to demonstrate
    form validation and proper alerting.  Also, example
    how to create a new random user each time by importing random py lib. """

from seleniumbase import BaseCase
import random

class FormValidations(BaseCase):

    def test_invalid_signup_registratio_pw1_too_short(self):
        # go to signup page
        self.open("https://www.allrecipes.com/")
        # wait for all initial page requests to complete before beginning tests
        self.wait_for_ready_state_complete(timeout=None)
        # click create profile
        self.find_element("#offCanvasDisplayName", timeout=10)
        self.click("#offCanvasDisplayName")
        # sign up with email
        self.click_link_text("Sign up with email")
        # sign up form
        self.type("#txtDisplayName", "Testing Display Name")
        # give random int for email signup
        self.type("#txtEmail", "seleniumBase.qaShortPw@gmail.com")
        self.type("#password", "shrtpw")
        # terms and conditions radio button
        self.click("#signupForm > div.terms > label.checkbox.lblsignUp.checkList__item.secure > span")
        # create my account
        self.click("#submitRegForm")
        # selector to assert for form validations
        alert = "#signupForm > div.mobile-notification"
        # assert the signup was invalid
        self.assert_text("Sorry, that password does not meet the requirements. Please try again.", alert)

    def test_invalid_signup_registration_pw2_no_upper_or_special_char(self):
        # go to signup page
        self.open("https://www.allrecipes.com/account/signup/")
        # wait for all initial page requests to complete before beginning tests
        self.wait_for_ready_state_complete(timeout=None)
        # sign up form
        self.type("#txtDisplayName", "Display Name")
        self.type("#txtEmail", "seleniumBase.qaNoUpperOrSpecChar@gmail.com")
        self.type("#password", "seleniumBase")
        # terms and conditions radio button
        self.click("#signupForm > div.terms > label.checkbox.lblsignUp.checkList__item.secure > span")
        # create my account
        self.click("#submitRegForm")
        # selector to assert for form validations
        alert = "#signupForm > div.mobile-notification"
        # assert the signup was invalid
        self.assert_text("Sorry, that password does not meet the requirements. Please try again.", alert)

    def test_invalid_signup_registration_pw3_none(self):
        # go to signup page
        self.open("https://www.allrecipes.com/account/signup/")
        # wait for all initial page requests to complete before beginning tests
        self.wait_for_ready_state_complete(timeout=None)
        # sign up form
        self.type("#txtDisplayName", "Display Name")
        self.type("#txtEmail", "seleniumBase.noPw@gmail.com")
        # terms and conditions radio button
        self.click("#signupForm > div.terms > label.checkbox.lblsignUp.checkList__item.secure > span")
        # create my account
        self.click("#submitRegForm")
        # selector to assert for form validations
        alert = "#signupForm > div.mobile-notification"
        # assert the signup was invalid
        self.assert_text("Oops! Don't forget a password!", alert)

    def test_invalid_signup_registration_already_member(self):
        # go to signup page
        self.open("https://www.allrecipes.com/account/signup/")
        # wait for all initial page requests to complete before beginning tests
        self.wait_for_ready_state_complete(timeout=None)
        # sign up form
        self.type("#txtDisplayName", "Display Name")
        self.type("#txtEmail", "seleniumBase.qa1@gmail.com")
        self.type("#password", "seleniumBase$$")
        # terms and conditions radio button
        self.click("#signupForm > div.terms > label.checkbox.lblsignUp.checkList__item.secure > span")
        # create my account
        self.click("#submitRegForm")
        # selector to assert for form validations
        alert = "#signupForm > div.mobile-notification"
        # assert the signup was invalid
        self.assert_text("Good news: You're already a member! Try logging in with that email address.", alert)
        # verify logging in URL works
        self.click("#signupForm > div.mobile-notification > a")
        signInExisting = "#account_login > div > section > section.uiForm.login > h4"
        self.assert_text("Existing Allrecipes users.", signInExisting)

    def test_invalid_signup_registration_email_invalid(self):
        # go to signup page
        self.open("https://www.allrecipes.com/account/signup/")
        # wait for all initial page requests to complete before beginning tests
        self.wait_for_ready_state_complete(timeout=None)
        # sign up form
        self.type("#txtDisplayName", "Display Name")
        self.type("#txtEmail", "seleniumBase.InvalidEmail@gmail")
        self.type("#password", "seleniumBase$$")
        # terms and conditions radio button
        self.click("#signupForm > div.terms > label.checkbox.lblsignUp.checkList__item.secure > span")
        # create my account
        self.click("#submitRegForm")
        # selector to assert for form validations
        alert = "#signupForm > div.mobile-notification"
        # assert the signup was invalid
        self.assert_text("Hmm. Doesn't look like that email address is valid. Try again!", alert)

    def test_invalid_signup_registration_age_terms_not_agreed(self):
        # go to signup page
        self.open("https://www.allrecipes.com/account/signup/")
        # wait for all initial page requests to complete before beginning tests
        self.wait_for_ready_state_complete(timeout=None)
        # sign up form
        self.type("#txtDisplayName", "Display Name")
        self.type("#txtEmail", "seleniumBase.noTerms@gmail.com")
        self.type("#password", "seleniumBase$$")
        # create my account
        self.click("#submitRegForm")
        # selector to assert for form validations
        alert = "#signupForm > div.mobile-notification"
        # assert the signup was invalid
        self.assert_text("You must be 13 years or older to become an Allrecipes member.", alert)

    def test_invalid_signup_registration_display_name_none(self):
        # go to signup page
        self.open("https://www.allrecipes.com/account/signup/")
        # wait for all initial page requests to complete before beginning tests
        self.wait_for_ready_state_complete(timeout=None)
        # sign up form
        self.type("#txtEmail", "seleniumBase.noDisplayName@gmail.com")
        self.type("#password", "seleniumBase$$")
        # terms and conditions radio button
        self.click("#signupForm > div.terms > label.checkbox.lblsignUp.checkList__item.secure > span")
        # create my account
        self.click("#submitRegForm")
        # selector to assert for form validations
        alert = "#signupForm > div.mobile-notification"
        # assert the signup was invalid
        self.assert_text("Oops! Make sure your display name is between 3 and 30 characters (letters and numbers only; no spaces, please).", alert)

    def test_invalid_signup_registration_display_name_too_short(self):
        # go to signup page
        self.open("https://www.allrecipes.com/account/signup/")
        # wait for all initial page requests to complete before beginning tests
        self.wait_for_ready_state_complete(timeout=None)
        # sign up form
        self.type("#txtDisplayName", "ab")
        self.type("#txtEmail", "seleniumBase.displayNameTooShort@gmail.com")
        self.type("#password", "seleniumBase$$")
        # terms and conditions radio button
        self.click("#signupForm > div.terms > label.checkbox.lblsignUp.checkList__item.secure > span")
        # create my account
        self.click("#submitRegForm")
        # selector to assert for form validations
        alert = "#signupForm > div.mobile-notification"
        # assert the signup was invalid
        self.assert_text("Oops! Make sure your display name is between 3 and 30 characters (letters and numbers only; no spaces, please).", alert)

    def test_invalid_signup_registration_display_name_too_long(self):
        # go to signup page
        self.open("https://www.allrecipes.com/account/signup/")
        # wait for all initial page requests to complete before beginning tests
        self.wait_for_ready_state_complete(timeout=None)
        # sign up form
        self.type("#txtDisplayName", "aLongDisplayName34Characters123456")
        self.type("#txtEmail", "seleniumBase.noDisplayName@gmail.com")
        self.type("#password", "seleniumBase$$")
        # terms and conditions radio button
        self.click("#signupForm > div.terms > label.checkbox.lblsignUp.checkList__item.secure > span")
        # create my account
        self.click("#submitRegForm")
        # selector to assert for form validations
        alert = "#signupForm > div.mobile-notification"
        # assert the signup was invalid
        self.assert_text("Oops! Make sure your display name is between 3 and 30 characters (letters and numbers only; no spaces, please).", alert)

    # bug?... form validation says no spaces in name but it allows... breaking tests
    def test_invalid_signup_registration_display_name_no_spaces(self):
        # go to signup page
        self.open("https://www.allrecipes.com/account/signup/")
        # wait for all initial page requests to complete before beginning tests
        self.wait_for_ready_state_complete(timeout=None)
        # sign up form
        self.type("#txtDisplayName", "Spaces In Name")
        randInt = random.randint(1,2000)
        self.type("#txtEmail", "seleniumBase.display_name_no_space" + str(randInt) + "@gmail.com")
        self.type("#password", "seleniumBase$$")
        # terms and conditions radio button
        self.click("#signupForm > div.terms > label.checkbox.lblsignUp.checkList__item.secure > span")
        # create my account
        self.click("#submitRegForm")
        # selector to assert for form validations
        alert = "#signupForm > div.mobile-notification"
        # assert the signup was invalid
        self.assert_text("Oops! Make sure your display name is between 3 and 30 characters (letters and numbers only; no spaces, please).", alert)

    # bug form validation says no letters and numbers only but it allows $ and ( ... breaking tests
    def test_invalid_signup_registration_display_name_no_special_chars(self):
        # go to signup page
        self.open("https://www.allrecipes.com/account/signup/")
        # wait for all initial page requests to complete before beginning tests
        self.wait_for_ready_state_complete(timeout=None)
        # sign up form
        self.type("#txtDisplayName", "$pecial (HAR5")
        randInt = random.randint(1,2000)
        self.type("#txtEmail", "seleniumBase.display_name_no_special_chars" + str(randInt) + "@gmail.com")
        self.type("#password", "seleniumBase$$")
        # terms and conditions radio button
        self.click("#signupForm > div.terms > label.checkbox.lblsignUp.checkList__item.secure > span")
        # create my account
        self.click("#submitRegForm")
        # selector to assert for form validations
        alert = "#signupForm > div.mobile-notification"
        # assert the signup was invalid
        self.assert_text("Oops! Make sure your display name is between 3 and 30 characters (letters and numbers only; no spaces, please).", alert)

    def test_invalid_signup_registration_email_none(self):
        # go to signup page
        self.open("https://www.allrecipes.com/account/signup/")
        # wait for all initial page requests to complete before beginning tests
        self.wait_for_ready_state_complete(timeout=None)
        # sign up form
        self.type("#txtDisplayName", "Display Name")
        self.type("#password", "seleniumBase$$")
        # terms and conditions radio button
        self.click("#signupForm > div.terms > label.checkbox.lblsignUp.checkList__item.secure > span")
        # create my account
        self.click("#submitRegForm")
        # selector to assert for form validations
        alert = "#signupForm > div.mobile-notification"
        # assert the signup was invalid
        self.assert_text("Oops! Add an email address.", alert)

   # Valid signup registration with dynammic random user name
    def test_valid_signup_registration(self):
        # go to signup page
        self.open("https://www.allrecipes.com/account/signup/")
        # sign up form
        self.type("#txtDisplayName", "Valid Display")
        randInt = random.randint(1,2000)
        self.type("#txtEmail", "seleniumBase.validSignUp" + str(randInt) + "@gmail.com")
        self.type("#password", "seleniumBase")
        # terms and conditions radio button
        self.click("#signupForm > div.terms > label.checkbox.lblsignUp.checkList__item.secure > span")
        # create my account
        self.click("#submitRegForm")
        # selector to assert for form validations
        alert = "#signupForm > div.mobile-notification"
        # assert the signup was valid
        loginName = "#offCanvasDisplayName"
        # assert login name showed in toolbar
        self.assert_text("VALID DISPLAY", loginName)
