Feature: Check product

  Scenario Outline: Open website and add new <product>
    Given I open product
    Then I click a add new <product>
    Then I a add new <product> into form

    Examples:
      | product                  |
      | Bún mắm ngon nhat        |
      | Bánh đa ngon kinh khung  |
      | Đậu xanh tuyet nhat      |
      | Ly suong suong           |
      | Tivi huhu                |
      | Cửa sổ ban               |
      | Ghế moi                  |
      | Muỗng cu                 |
      | Dây cáp nao day          |
      | Áo khoác lanh lam        |
      | bánh tráng trộn huhu nha |

  Scenario: Open website and edit product
    Given I open product
    Then I click edit the first product
    Then I edit this product and submit form