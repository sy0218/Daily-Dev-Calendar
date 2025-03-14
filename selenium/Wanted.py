#!/usr/bin/python3
from class_dir.selenium_class import session_get
from class_dir.properties_loader import ConfigLoader
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

from collections import deque
import sys

def _Get_browser(url):
    session = session_get(url)
    browser = session.get_browser()
    return session, browser

def _Value_get(start, end, browser):
    json_data = []
    job_queue, error_count = deque([i for i in range(start, end + 1)]), 0
    while job_queue:
        json_value = {}
        try:
            element = browser.find_element(By.XPATH, f"/html/body/div[1]/div[4]/div[3]/div[2]/div/div[3]/div[{job_queue[0]}]/a")
            # 필요 속성 추출
            json_value['job_category_id'], json_value['company_id'], json_value['position_id'], json_value['company_name'], json_value['position_name'], json_value['search_value'] = element.get_attribute("data-job-category-id"), element.get_attribute("data-company-id"), element.get_attribute("data-position-id"), element.get_attribute("data-company-name"), element.get_attribute("data-position-name"), element.get_attribute("data-search-value")
            json_data.append(json_value)
            job_queue.popleft()
            error_count = 0

        except Exception as e:
            if "no such element" in str(e).lower():
                if (error_count == 3):
                    print(f"error count is {error_count}")
                    break

                error_count += 1
                print(f"Scrolling down to load more elements... (number {job_queue[0]})")
                browser.find_element(By.CSS_SELECTOR, 'body').send_keys(Keys.END)  # 페이지 다운
                time.sleep(3)
                continue

            else:
                print(f"Error {job_queue[0]}: {type(e).__name__} - {e}")
                break
    return json_data

def _Quit_browser(session, browser):
    session.close()
    browser.quit()


# 실행
if __name__ == "__main__":
    url, start, end = ConfigLoader.get_conf_values("Wanted")
    session, browser = _Get_browser(url)
    print(session)
    json_value = _Value_get(start, end, browser)
    for i in range(end):
        print(json_value[i])
        print("")

    _Quit_browser(session, browser) # 브라우저 종료
