Feature: Check feature of /create

  Scenario: Open website
    Given I open address page
    Then I print the address page

  Scenario: Open city website
    Given I open city page
    Then I click add new city
    Then I add new city into form

  Scenario: Open district website
    Given I open district page
    Then I click add new district
    Then I add new district into form

  Scenario Outline: Open website and add a new <address>
    Given I open address page
    Then I print the address page
    Then I click add a new <address>
    Then I add a new <address> into form

    Examples:
        | address            |
        | số 17, hàng trống  |
        | 83 Phan Đình Phùng |
        | 99 Hoà Thân        |

  Scenario: Open website and edit address
    Given I open address page
    Then I print the address page
    Then I click edit the first address
    Then I edit this address and submit form