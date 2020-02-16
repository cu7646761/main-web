Feature: Test all function of /brand

  Scenario Outline: Open a table, then create city
    Given When get into "brand" page with blank list and click the create button.
    When When redirected to create window, at "brandName" form, I type in <brandName> and click on button with css ".btn.btn-primary"
    Then When redirected back to brand list window, I should see <brandName>

    Examples:
        | brandName |
        | Samsung   |
        | LG        |
        | Apple     |
        | Microsoft |

  Scenario Outline: Given a table with datas, create duplicate data
    Given When get into "brand" page with blank list and click the create button.
    When When redirected to create window, at "brandName" form, i type in <brandName> and click on button with css ".btn.btn-primary"
    Then We should not be able to create brand.

    Examples:
        | brandName |
        | Samsung   |
        | LG        |
        | Apple     |
        | Microsoft |

  Scenario: Open website and edit brand
    Given I open brand list
    Then I click edit the first brand
    Then I edit this brand and submit form