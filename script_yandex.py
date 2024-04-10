from selenium import webdriver
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def scroll_to_element(driver, element):
    # Прокручиваем страницу до элемента
    driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center', inline: 'nearest' });",
                          element)


def click_next_button(driver):
    try:
        # Находим кнопку "Далее"
        next_button = driver.find_element(By.XPATH, "//a[@rel='next']")
        scroll_to_element(driver, next_button)
        time.sleep(10)
        # Нажимаем на кнопку "Далее"
        next_button.click()
        return True
    except:
        return False


def click_to_center(driver):
    from selenium.webdriver.common.action_chains import ActionChains

    # Выполняем прокрутку до середины страницы с помощью JavaScript
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 2);")

    # Находим элемент, по которому нужно выполнить нажатие
    element = driver.find_element(By.XPATH, "//xpath_to_your_element")

    # Выполняем нажатие на элемент в центре экрана
    action = ActionChains(driver)
    action.move_to_element(element).click().perform()


def get_whatsapp_numbers(search_text, city):
    ua = UserAgent()
    # Получаем случайный юзер-агент
    random_user_agent = ua.random
    from selenium.webdriver.chrome.options import Options
    # Настройки Chrome WebDriver
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--log-level=3')
    chrome_options.add_argument(f'user-agent={random_user_agent}')

    mobile_emulation = {
        "userAgent": "Mozilla/5.0 (Linux; Android 10; Pixel 3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Mobile Safari/537.36",
    }

    chrome_options = Options()
    # chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)

    # Создаем экземпляр веб-драйвера с использованием настроек
    driver = webdriver.Chrome(options=chrome_options)

    # driver.get("https://uslugi.yandex.ru/")  # Открываем Google для примера
    driver.get("https://uslugi.yandex.ru/213-moscow/category/raznoe/")  # Открываем Google для примера

    # click_search_box = WebDriverWait(driver, 7).until(
    #     EC.presence_of_element_located((By.CSS_SELECTOR, ".RubricSuggest-HandlerHeader"))
    # )
    # click_search_box.click()

    time.sleep(2)

    # Находим поле ввода и вводим запрос
    search_box = WebDriverWait(driver, 7).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".RubricSuggest-HandlerHeader"))
    )

    search_box = search_box.find_element(By.CSS_SELECTOR, ".Textinput-Control")
    search_box.click()

    search_box.send_keys(search_text)
    time.sleep(5)
    search_box.send_keys(Keys.ENTER)
    try:
        settings_button = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".Serp-TitleFilters"))
        )
        settings_button.click()
    except:
        pass

    search_city = WebDriverWait(driver, 7).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".textinput__control"))
    )
    time.sleep(3)
    search_city.send_keys(Keys.CONTROL + "a")  # Выбираем все содержимое
    search_city.send_keys(Keys.BACKSPACE)  # Удаляем
    # search_city.send_keys(Keys)
    time.sleep(1)
    search_city.send_keys(city)
    time.sleep(2)
    try:
        first_suggestion = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, ".control.textinput__suggest-item.textinput__suggest-item_type_text"))
        )
        first_suggestion.click()
    except:
        pass

    # first_suggestion.click()
    time.sleep(2)
    confirm_button = None
    try:
        confirm_button = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, ".YdoModal-BackButton"))
        )
        confirm_button.click()
    except:
        pass
    try:
        confirm_button = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, ".Filters-Apply"))
        )
        scroll_to_element(driver, confirm_button)
        confirm_button.click()
    except:
        pass

    time.sleep(2)

    while True:
        try:
            specialist_containers = WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".WorkerCard"))
            )

            for container in specialist_containers:
                # Попытка найти элементы, которые могут прервать выполнение цикла
                error = container.find_elements(By.CSS_SELECTOR, ".WorkerCard-AdvText")
                error1 = container.find_elements(By.CSS_SELECTOR,
                                                 ".Form.OrderForm2.WorkersListBlendered-OrderFormCard.Gap.Gap_bottom_l")

                # Проверка наличия элементов, которые могут прервать выполнение цикла
                if error or error1:
                    continue

                # chat_button = container.find_element(By.CSS_SELECTOR, ".WorkerControls-MessengersPopup")
                buttons = container.find_elements(By.CSS_SELECTOR, ".Button2_pin_circle")
                # Проверяем каждую кнопку на наличие текста "Чат"
                chat_button = None
                with open("phone_numbers.txt", "a") as file:
                    for button in buttons:
                        if "Чат" in button.text:
                            scroll_to_element(driver, button)
                            time.sleep(2)
                            button.click()
                            time.sleep(3)
                            try:
                                table_links = driver.find_elements(By.CSS_SELECTOR, ".SocialLinkList a")
                                for link in table_links:
                                    href = link.get_attribute("href")
                                    if "wa.me" in href:
                                        start_index = href.find("wa.me/") + len("wa.me/")
                                        phone_number = href[start_index:].split('?')[0]
                                        file.write(f"+{phone_number}\n")
                                        file.flush()  # Сбросить буфер, чтобы запись была доступна сразу
                                        print(f"Номер телефона {phone_number} добавлен в файл")
                                        # click_to_center(driver)
                            except:
                                click_to_center(driver)
                                print('except 0 no links')

                            # try:
                            #     close_button = driver.find_element(By.CSS_SELECTOR,
                            #                                        ".ui-icon-button.ui-icon-button_hoverable.yamb-cell")
                            #     close_button.click()
                            #     print("Окно успешно закрыто")
                            #     time.sleep(2)
                            # except:
                            #     print("Окно не найдено")
                            #     print('except 1')
                            time.sleep(2)

            if not click_next_button(driver):
                time.sleep(7)
                break
        except:
            print('main block error')

            # try:
            #     close_button = driver.find_element(By.CSS_SELECTOR,
            #                                        ".YdoModal-CloseButton_position_normal")
            #     close_button.click()
            # except:
            #     pass

    # specialist_containers.remove(container)
    # driver.get(driver.current_url)
    # time.sleep(10)
    # if not click_next_button(driver):
    #     break
    # else:
    #     break
    # if not click_next_button(driver):
    #     break
    # time.sleep(10)


# Пример использования функции
city = "Сочи"
search_text = "Психологи"
whatsapp_numbers = get_whatsapp_numbers(search_text, city)
