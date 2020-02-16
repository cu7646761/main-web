from behave import then, given


@given('I open address page')
def step_impl1(context):
    context.browser.get(context.url + "/address")


@given('I open city page')
def step_impl13(context):
    context.browser.get(context.url + "/city")


@given('I open district page')
def step_impl14(context):
    context.browser.get(context.url + "/district")


@then('I click add new city')
def step_impl2(context):
    context.browser.find_element_by_css_selector(
        '.btn.btn-lg.btn-accent.ml-auto').click()


@then('I add new city into form')
def step_impl3(context):
    brand_name = context.browser.find_element_by_name('cityName')
    brand_name.send_keys("Ha Noi")
    context.browser.find_element_by_css_selector(
        '.mb-2.btn.btn-primary.mr-2.w-100').click()
    last_button = context.browser.find_element_by_css_selector(
        ".page-item.last")
    last_button.click()
    rows = context.browser.find_elements_by_tag_name("tr")
    last_row = rows[len(rows) - 1]
    field_text = last_row.find_elements_by_tag_name("td")[1].text
    assert field_text == "Ha Noi"


@then('I click add new district')
def step_impl9(context):
    context.browser.find_element_by_css_selector(
        '.btn.btn-lg.btn-accent.ml-auto').click()


@then('I add new district into form')
def step_impl31(context):
    brand_name = context.browser.find_element_by_name('district_name')
    brand_name.send_keys("Quan 1")

    context.browser.find_element_by_css_selector(
        '.mb-2.btn.btn-primary.mr-2.w-100').click()
    last_button = context.browser.find_element_by_css_selector(
        ".page-item.last")
    last_button.click()
    rows = context.browser.find_elements_by_tag_name("tr")
    last_row = rows[len(rows) - 1]
    field_text = last_row.find_elements_by_tag_name("td")[2].text
    assert field_text == "Quan 1"


@then('I print the address page')
def step_impl5(context):
    title = context.browser.find_element_by_tag_name('h3')
    assert "Address Table" in title.text


@then('I click add a new {address}')
def step_impl6(context, address):
    context.browser.find_element_by_css_selector(
        '.btn.btn-lg.btn-accent.ml-auto').click()


@then('I add a new {address} into form')
def step_impl7(context, address):
    address_detail = context.browser.find_element_by_name('address')
    address_detail.send_keys(address)
    citys = context.browser.find_element_by_name('select-city')
    options = citys.find_elements_by_tag_name('option')
    for option in options:
        if option.get_attribute("value") == "1":
            option.click()

    districts = context.browser.find_element_by_name('select-district')
    options = districts.find_elements_by_tag_name('option')
    for option in options:
        if option.get_attribute("value") == "1":
            option.click()

    context.browser.find_element_by_css_selector(
        '.mb-2.btn.btn-primary.mr-2.w-100').click()
    last_button = context.browser.find_element_by_css_selector(
        ".page-item.last")
    last_button.click()
    rows = context.browser.find_elements_by_tag_name("tr")
    last_row = rows[len(rows) - 1]
    field_text = last_row.find_elements_by_tag_name("td")[1].text
    assert field_text == address


@then('I click edit the first address')
def step_impl8(context):
    context.browser.find_elements_by_css_selector('.btn.btn-info')[0].click()


@then('I edit this address and submit form')
def step_impl91(context):
    address_name = context.browser.find_element_by_id('address-edit')
    address_name.clear()
    address_name.send_keys('so 18')

    citys = context.browser.find_element_by_id('city_edit')
    options = citys.find_elements_by_tag_name('option')
    for option in options:
        if option.get_attribute("value") == "1":
            option.click()

    context.browser.find_element_by_id('modify').click()
    title = context.browser.find_element_by_tag_name('h3')
    assert "Address Table" in title.text
