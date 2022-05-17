Feature: SeleniumBase scenarios for the Swag Labs App

  Background:
    Given Open the Swag Labs Login Page

  Scenario: User can log in and log out successfully
    When Login to Swag Labs with standard_user
    Then Verify that the current user is logged in
    When Logout from Swag Labs
    Then Verify on Login page

  Scenario: User can order a backpack from the store
    When Login to Swag Labs with standard_user
    Then Verify that the current user is logged in
    And Save price of "Backpack" to <item_price>
    When Add "Backpack" to Cart
    Then Verify shopping cart badge shows 1 item(s)
    When Click on shopping cart icon
    And Click Checkout
    And Enter checkout info: First, Last, 12345
    And Click Continue
    Then Verify 1 "Backpack"(s) in cart
    And Verify cost of "Backpack" is <item_price>
    And Verify item total is $29.99
    And Verify tax amount is $2.40
    And Verify total cost is $32.39
    When Click Finish
    Then Verify order complete
    When Logout from Swag Labs
    Then Verify on Login page

  Scenario: User can order two items from the store
    When Login to Swag Labs with standard_user
    And Add "Bike Light" to Cart
    And Add "Fleece Jacket" to Cart
    Then Verify shopping cart badge shows 2 item(s)
    When Click on shopping cart icon
    And Click Checkout
    And Enter checkout info: First, Last, 54321
    And Click Continue
    Then Verify 1 "Bike Light"(s) in cart
    Then Verify 1 "Fleece Jacket"(s) in cart
    And Verify item total is $59.98
    And Verify tax amount is $4.80
    And Verify total cost is $64.78
    When Click Finish
    Then Verify order complete
    When Logout from Swag Labs
    Then Verify on Login page

  Scenario: User can sort items by name from Z to A
    When Login to Swag Labs with standard_user
    And Sort items from Z to A
    Then Verify "Test.allTheThings() T-Shirt" on top
    When Logout from Swag Labs
    Then Verify on Login page

  Scenario: User can add & remove 6 items to/from cart
    When Login to Swag Labs with standard_user
    And Add "Backpack" to Cart
    And Add "Bike Light" to Cart
    And Add "Bolt T-Shirt" to Cart
    And Add "Fleece Jacket" to Cart
    And Add "Onesie" to Cart
    And Add "Test.allTheThings() T-Shirt" to Cart
    Then Verify shopping cart badge shows 6 item(s)
    When Remove "Backpack" from Cart
    And Remove "Bike Light" from Cart
    And Remove "Bolt T-Shirt" from Cart
    And Remove "Fleece Jacket" from Cart
    And Remove "Onesie" from Cart
    And Remove "Test.allTheThings() T-Shirt" from Cart
    Then Verify shopping cart badge is missing
    When Logout from Swag Labs
    Then Verify on Login page
