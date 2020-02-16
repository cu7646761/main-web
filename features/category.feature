Feature: Check website

  Scenario: Open website
    Given I open category
    Then I print the category html

  Scenario: Open brand website
    Given I open brand
    Then I click add new brand
    Then I add new brand into form

  Scenario Outline: Open website and add new <category>
    Given I open category
    Then I print the category html
    Then I click add new <category>
    Then I add new <category> into form

    Examples:
      | category            |
      | Bún mắm             |
      | Bánh đa             |
      | Đậu xanh            |
      | Ly                  |
      | Tivi                |
      | Cửa sổ              |
      | Ghế                 |
      | Muỗng               |
      | Dây cáp             |
      | Áo khoác            |
      | bánh tráng trộn new |

  Scenario: Open website and edit category
    Given I open category
    Then I print the category html
    Then I click edit the first category
    Then I edit this category and submit form