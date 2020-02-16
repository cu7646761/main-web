from behave import *


@given('I open category')
def step_impl(context):
    context.browser.get(context.url + "/category")


@then('I click add new brand')
def step_impl(context):
    context.browser.find_element_by_css_selector('.btn.btn-lg.btn-accent.ml-auto').click()


@then('I add new brand into form')
def step_impl(context):
    brand_name = context.browser.find_element_by_name('brandName')
    brand_name.send_keys("Samsung")
    context.browser.find_element_by_css_selector('.mb-2.btn.btn-primary.mr-2.w-100').click()
    last_button = context.browser.find_element_by_css_selector(".page-item.last")
    last_button.click()
    rows = context.browser.find_elements_by_tag_name("tr")
    last_row = rows[len(rows) - 1]
    field_text = last_row.find_elements_by_tag_name("td")[1].text
    assert field_text == "Samsung"


@given('I open brand')
def step_impl(context):
    context.browser.get(context.url + "/brand")


@then('I print the category html')
def step_impl(context):
    title = context.browser.find_element_by_tag_name('h3')
    assert "Category Table" in title.text\



@then('I click add new {category}')
def step_impl(context, category):
    context.browser.find_element_by_css_selector('.btn.btn-lg.btn-accent.ml-auto').click()


@then('I add new {category} into form')
def step_impl(context, category):
    category_name = context.browser.find_element_by_name('category_name')
    category_name.send_keys(category)
    brand_ids = context.browser.find_element_by_name('brand_id')
    options = brand_ids.find_elements_by_tag_name('option')
    for option in options:
        if option.get_attribute("value") == "1":
            option.click()
    context.browser.find_element_by_css_selector('.mb-2.btn.btn-primary.mr-2.w-100').click()
    last_button = context.browser.find_element_by_css_selector(".page-item.last")
    last_button.click()
    rows = context.browser.find_elements_by_tag_name("tr")
    last_row = rows[len(rows) - 1]
    field_text = last_row.find_elements_by_tag_name("td")[1].text
    assert field_text == category


@then('I click edit the first category')
def step_impl(context):
    context.browser.find_elements_by_css_selector('.btn.btn-info')[0].click()



@then('I edit this category and submit form')
def step_impl(context):
    category_name = context.browser.find_element_by_name('category_name')
    category_name.clear()
    category_name.send_keys('Do an vat so 69 viet nam')
    brand_ids = context.browser.find_element_by_name('brand_id')
    options = brand_ids.find_elements_by_tag_name('option')
    for option in options:
        if option.get_attribute("value") == "1":
            option.click()
    context.browser.find_element_by_id('modify').click()
    title = context.browser.find_element_by_tag_name('h3')
    assert "Category Table" in title.text