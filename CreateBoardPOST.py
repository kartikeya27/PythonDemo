from selenium import webdriver
from selenium.webdriver.support.ui import Select
from utilities.configurations import *
from utilities.resources import *

import requests

key = "552e430e4d418cbd69b840fcdfd1b5b2"
token = "74bfe710cfc99c39652a23068624c32c7c5b1513d392f97138bef55d72411cf1"

# Create a new Board
board_url = getConfig()['API']['endpoint'] + ApiResources.create_board
board_query = {
    'key': key,
    'token': token,
    'name': 'test_board'
}
board_response = requests.post(board_url, params=board_query)
print(board_response.json())
response_json = board_response.json()
assert board_response.status_code == 200
board_id = response_json['id']

# Create a new list1
list_url1 = getConfig()['API']['endpoint'] + ApiResources.create_list
list_query1 = {
    'key': key,
    'token': token,
    'name': 'test_list1',
    'idBoard': board_id
}
list_response1 = requests.post(list_url1, params=list_query1)
print(list_response1.json())
list_json1 = list_response1.json()
assert list_response1.status_code == 200
list_id1 = list_json1['id']

# Create a new list
list_url = getConfig()['API']['endpoint'] + ApiResources.create_list
list_query = {
    'key': key,
    'token': token,
    'name': 'test_list',
    'idBoard': board_id
}
list_response = requests.post(list_url, params=list_query)
print(list_response.json())
list_json = list_response.json()
assert list_response.status_code == 200
list_id = list_json['id']

# Create new card 1
card_url = getConfig()['API']['endpoint'] + ApiResources.create_card
card_query = {
    'key': key,
    'token': token,
    'idList': list_id,
    'name': 'test_card'
}
card_response = requests.post(card_url, params=card_query)
print(card_response.json())
card_json = card_response.json()
assert card_response.status_code == 200
card_id = card_json['id']

# Create new card 2
card_url1 = getConfig()['API']['endpoint'] + ApiResources.create_card
card_query1 = {
    'key': key,
    'token': token,
    'idList': list_id,
    'name': 'test_card1'
}
card_response1 = requests.post(card_url1, params=card_query1)
print(card_response1.json())
card_json1 = card_response1.json()
assert card_response1.status_code == 200
card_id1 = card_json1['id']

# Create new card 2
card_url2 = getConfig()['API']['endpoint'] + ApiResources.create_card
card_query2 = {
    'key': key,
    'token': token,
    'idList': list_id,
    'name': 'test_card2'
}
card_response2 = requests.post(card_url2, params=card_query2)
print(card_response2.json())
card_json2 = card_response2.json()
assert card_response2.status_code == 200
card_id2 = card_json2['id']

# Put request moving card2 to list1
move_url = f"https://api.trello.com/1/cards/{card_id2}/idList?value={list_id1}"
move_query = {
    'key': key,
    'token': token
}
move_response = requests.put(move_url, params=move_query)
print(move_response.json())
move_json = move_response.json()
assert move_response.status_code == 200
move_id = move_json['id']

# Delete cars2 from list1
delete_url = f"https://api.trello.com/1/cards/{move_id}"
delete_query = {
    'key': key,
    'token': token
}
delete_response = requests.delete(delete_url, params=delete_query)
print(delete_response.text)
assert delete_response.status_code == 200

# Create a new comment on a card1
comment_url = f"https://api.trello.com/1/cards/{card_id1}/actions/comments"
comment_query = {
    'key': key,
    'token': token,
    'text': 'I am a new comment on this card'
}
comment_response = requests.post(comment_url, params=comment_query)
print(comment_response.text)
assert comment_response.status_code == 200

# ------------Part-2--------------------------

driver = webdriver.Chrome(executable_path="/Users/k-bhatt/pythonProject/chromedriver")
driver.maximize_window()
driver.get("https://id.atlassian.com/login")
driver.find_element_by_id("username").send_keys("kbhatt76@gmail.com")
driver.find_element_by_id("login-submit").click()
driver.implicitly_wait(10)
driver.find_element_by_id("password").send_keys("1200@Villa")
driver.find_element_by_id("login-submit").click()
driver.implicitly_wait(10)
driver.find_element_by_css_selector(".sc-bZQynM").click()
driver.implicitly_wait(10)
driver.find_element_by_css_selector(".board-tile-details.is-badged").click()

elements = driver.find_elements_by_css_selector(".list-cards.u-fancy-scrollbar.u-clearfix.js-list-cards.js-sortable."
                                                "ui-sortable")
for element in elements:
    if element.text == 'test_card' and element.text == 'test_card1':
        assert True
driver.find_element_by_css_selector(".list-cards.u-fancy-scrollbar.u-clearfix.js-list-cards.js-sortable.ui-sortable")\
    .click()
comment = (driver.find_element_by_css_selector("div.current-comment.js-friendly-links.js-open-card:nth-child(1)")).text
assert comment == 'I am a new comment on this card'
driver.find_element_by_css_selector("textarea.comment-box-input.js-new-comment-input")\
    .send_keys("I am your second comment")
driver.find_element_by_css_selector("input.nch-button.nch-button--primary.confirm.mod-no-top-bottom-margin."
                                    "js-add-comment").click()
driver.find_element_by_xpath("//span[contains(text(),'Move')]").click()
driver.find_element_by_css_selector("select.js-select-list").click()
select = Select(driver.find_element_by_css_selector("select.js-select-list"))
select.select_by_visible_text("Done")
print("Selected item - " + select.first_selected_option.text)
assert "Done" in select.first_selected_option.text
driver.find_element_by_css_selector("input.nch-button.nch-button--primary.wide.js-submit").click()
driver.find_element_by_css_selector("a.icon-md.icon-close.dialog-close-button.js-close-window").click()
driver.quit()
