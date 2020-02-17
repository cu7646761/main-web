from behave import given, when, then


@given(u'When get into "brand" page with blank list and click the create button.')
def when_click_create(context):
    print("HERE" + context.url + "/brand")
    context.browser.get(context.url + "/brand")
    create_button = context.browser.find_element_by_css_selector(
        ".btn.btn-lg.btn-accent.ml-auto")
    print(create_button)
    create_button.click()


@when(u'When redirected to create window, at "brandName" form, i type in {brandName} and click on button with css ".btn.btn-primary"')
def when_typing(context, brandName):
    city_form = context.browser.find_element_by_name("brandName")
    city_form.send_keys(brandName)
    create_button = context.browser.find_element_by_css_selector(
        ".mb-2.btn.btn-primary.mr-2.w-100")
    create_button.click()


@then(u'When redirected back to brand list window, i should see {brandName}')
def step_impl_344124(context, brandName):
    last_button = context.browser.find_element_by_css_selector(
        ".page-item.last")
    last_button.click()
    rows = context.browser.find_elements_by_tag_name("tr")
    last_row = rows[len(rows) - 1]
    ciy_field_text = last_row.find_elements_by_tag_name("td")[1].text
    assert ciy_field_text == brandName


@then(u'We should not be able to create brand.')
def step_impl(context):
    error_div = context.browser.find_elements_by_css_selector(
        ".error__content.mt-4")[0]
    error_h3 = error_div.find_element_by_tag_name("h3")
    assert "error" in error_h3.text


@given('I open brand list')
def step_impl5(context):
    context.browser.get(context.url + "/brand")


@then('I click edit the first brand')
def step_impl6(context):
    context.browser.find_elements_by_css_selector('.btn.btn-info')[0].click()


@then('I edit this brand and submit form')
def step_impl7(context):
    brand_name = context.browser.find_element_by_name('brand_name')
    brand_name.clear()
    brand_name.send_keys('Google')
    context.browser.find_element_by_id('modify').click()
    title = context.browser.find_element_by_tag_name('h3')
    assert "Brand Table" in title.text
