from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
try:
    link = "http://suninjuly.github.io/selects1.html"
    browser = webdriver.Chrome()
    browser.get(link)

    sum1 = int(browser.find_element_by_id("num1").text)
    sum2 = int(browser.find_element_by_id("num2").text)
    summa = str(sum1 + sum2)

    select = Select(browser.find_element_by_tag_name("select"))
    select.select_by_value(summa)

    option1 = browser.find_element_by_class_name("btn-default")
    option1.click()



finally:
    # ожидание чтобы визуально оценить результаты прохождения скрипта
    time.sleep(10)
    # закрываем браузер после всех манипуляций
    browser.quit()
