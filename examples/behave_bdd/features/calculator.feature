Feature: SeleniumBase scenarios for the Calculator App

  Background:
    Given Open the Calculator App

  Scenario: Pressing "C" outputs "0"
    When Press C
    Then Verify output is "0"

  Scenario: 1 + 2 + 3 + 4 + 5 = 15
    When Press C
    And Press 1
    And Press +
    And Press 2
    And Press +
    And Press 3
    And Press +
    And Press 4
    And Press +
    And Press 5
    Then Verify output is "1+2+3+4+5"
    When Press =
    Then Verify output is "15"

  Scenario: 6 × 7 × 8 × 9 = 3024
    When Press C
    And Press 6
    And Press ×
    And Press 7
    And Press ×
    And Press 8
    And Press ×
    And Press 9
    Then Verify output is "6×7×8×9"
    When Press =
    Then Verify output is "3024"

  Scenario: 44 - 11 = 33
    When Press C
    And Press 4
    And Press 4
    And Press -
    And Press 1
    And Press 1
    Then Verify output is "44-11"
    When Press =
    Then Verify output is "33"

  Scenario: 7.0 × (3 + 3) = 42
    When Press C
    And Press 7
    And Press .
    And Press 0
    And Press ×
    And Press (
    And Press 3
    And Press +
    And Press 3
    And Press )
    Then Verify output is "7.0×(3+3)"
    When Press =
    Then Verify output is "42"

  Scenario: 4.5 × 68 = 306
    When Press C
    And Evaluate [4.5 × 68]
    Then Verify output is "306"

  Scenario Outline: <First> ÷ <Second> = <Result>
    When Press C
    And Press [<First>]
    And Press ÷
    And Press [<Second>]
    And Press =
    Then Verify output is "<Result>"
    Examples:
      | First | Second | Result |
      | 1948  | 4      | 487    |
      | 21    | 0      | Error  |

  Scenario: Save calculator screenshot to logs
    Given Press [1337]
    Given Save calculator screenshot to logs
