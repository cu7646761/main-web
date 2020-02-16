from behave import given, when, then
from app import db
from app.entity.mongo.city import City

@given(u'When get into "city" page with blank list and click the create button.')
def when_click_create(context):
    print("HERE" + context.url + "/city")
    context.browser.get(context.url + "/city")
    create_button = context.browser.find_element_by_css_selector(".btn.btn-lg.btn-accent.ml-auto")
    print(create_button)
    create_button.click()


@when(u'When redirected to create window, at "city_name" form, i type in {city_name} and click on button with css ".btn.btn-primary"')
def when_typing(context, city_name):
    city_form = context.browser.find_element_by_name("city_name")
    city_form.send_keys(city_name)
    create_button = context.browser.find_element_by_css_selector(".mb-2.btn.btn-primary.mr-2.w-100")
    create_button.click()

@then(u'When redirected back to list window, i should see {city_name}')
def step_impl_3(context, city_name):
    last_button = context.browser.find_element_by_css_selector(".page-item.last")
    last_button.click()
    rows = context.browser.find_elements_by_tag_name("tr")
    last_row = rows[len(rows) - 1]
    ciy_field_text = last_row.find_elements_by_tag_name("td")[1].text
    assert ciy_field_text in city_name

@then(u'We should not be able to create city.')
def step_impl(context):
    error_div = context.browser.find_elements_by_css_selector(".error__content.mt-4")[0]
    error_h3 = error_div.find_element_by_tag_name("h3")
    assert "error" in error_h3.text

@given('I open city')
def step_impl(context):
    context.browser.get(context.url + "/city")

@then('I click edit the first city')
def step_impl(context):
    context.browser.find_elements_by_css_selector('.btn.btn-info')[0].click()


@then('I edit this city and submit form')
def step_impl(context):
    city_name = context.browser.find_element_by_name('city_name')
    city_name.clear()
    city_name.send_keys('Viet nam vo dich')
    context.browser.find_element_by_id('modify').click()
    title = context.browser.find_element_by_tag_name('h3')
    assert "City Table" in title.text