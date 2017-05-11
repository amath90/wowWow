import locators

from behave import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@given("I have google.pl displayed in Google Chrome")
def step_impl(context):
    context.browser.get("https://www.google.pl/")


@when("I type wowair in search bar")
def step_impl(context):
    type = locators.SEARCH(context.browser).send_keys("wowair")


@then("I have search results displayed and clicked link")
def step_impl(context):
    click_search = locators.CLICK_SEARCH(context.browser).click()
