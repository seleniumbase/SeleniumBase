Feature: SeleniumBase scenarios for the RealWorld App

  Scenario: Verify RealWorld App (log in / sign out)
    Given Open the RealWorld Login Page
    When Login to the RealWorld App
    Then Assert exact text "Welcome!" in "h1"
    When Highlight element "img#image1"
    And Click element 'a:contains("This Page")'
    Then Save a screenshot to the logs
    When Click link "Sign out"
    Then Assert element 'a:contains("Sign in")'
    And Assert text "You have been signed out!"
