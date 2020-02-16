from behave import *


@given('I open product')
def step_impl(context):
    context.browser.get(context.url + "/product")


@then('I click a add new {product}')
def step_impl(context, product):
    context.browser.find_element_by_css_selector('.btn.btn-lg.btn-accent.ml-auto').click()


@then('I a add new {product} into form')
def step_impl(context, product):
    product_name = context.browser.find_element_by_name('product_name')
    product_name.send_keys(product)
    category_ids = context.browser.find_element_by_name('category_id')
    options = category_ids.find_elements_by_tag_name('option')
    for option in options:
        if option.get_attribute("value") == "1":
            option.click()
    context.browser.find_element_by_css_selector('.mb-2.btn.btn-primary.mr-2.w-100').click()
    last_button = context.browser.find_element_by_css_selector(".page-item.last")
    last_button.click()
    rows = context.browser.find_elements_by_tag_name("tr")
    last_row = rows[len(rows) - 1]
    field_text = last_row.find_elements_by_tag_name("td")[1].text
    assert field_text == product


@then('I click edit the first product')
def step_impl(context):
    context.browser.find_elements_by_css_selector('.btn.btn-info')[0].click()


@then('I edit this product and submit form')
def step_impl(context):
    product_name = context.browser.find_element_by_name('product_name')
    product_name.clear()
    product_name.send_keys('Do an vat so 69 viet nam')
    category_ids = context.browser.find_element_by_name('category_id')
    options = category_ids.find_elements_by_tag_name('option')
    for option in options:
        if option.get_attribute("value") == "1":
            option.click()
    context.browser.find_element_by_id('modify').click()
    title = context.browser.find_element_by_tag_name('h3')
    assert "Product Table" in title.text
