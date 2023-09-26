Feature: SeleniumBase scenarios for the Simple App

  Scenario: Verify the Simple App (Login / Logout)
    Given Open "seleniumbase.io/simple/login"
    And Type "demo_user" into "#username"
    And Type "secret_pass" into "#password"
    And Click 'a:contains("Sign in")'
    And Assert exact text "Welcome!" in "h1"
    And Assert element "img#image1"
    And Highlight "#image1"
    And Click link "Sign out"
    And Assert text "signed out" in "#top_message"
