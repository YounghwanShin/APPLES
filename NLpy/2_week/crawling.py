from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import csv

class CustomScraper:
    def __init__(self, driver_path):
        """
        스크래퍼 클래스의 생성자입니다. 

        Args(인자):
            driver_path (str): 웹 드라이버(Chrome)의 파일 경로입니다.
        """

        # 크롬 드라이버 초기화
        self.driver = webdriver.Chrome(driver_path)
        # 방문한 공지사항의 href(hypertext reference 의 줄임말, 즉 외부 하이퍼링크) 값을 저장할 집합
        self.visited_notices = set()

    def wait_for_page_load(self, seconds=1):
        """
        지정된 시간만큼 대기합니다.

        Args:
            seconds (int, optional): 대기할 시간(초). 기본값은 1로 지정.
        """

        time.sleep(seconds)

    def scrape_notice(self, href, writer):
        """
        개별 공지사항 페이지를 스크랩하고, 제목과 내용을 CSV 파일에 작성합니다.

        Args:
            href (str): 스크랩할 공지사항의 URL입니다.
            writer (csv.writer): CSV 파일에 쓰기 위한 writer 객체입니다.
        """

        # 새 탭에서 공지사항 페이지 열기
        self.driver.execute_script(f"window.open('{href}');")
        self.wait_for_page_load()

        # 새로 연 탭으로 전환
        self.driver.switch_to.window(self.driver.window_handles[1])
        self.wait_for_page_load()

        # 페이지 소스 가져오기 및 BeautifulSoup 객체 생성
        html_source = self.driver.page_source
        soup = BeautifulSoup(html_source, 'html.parser')

        # 제목과 내용 추출
        title = soup.find('h2', class_='view-title').text.strip()
        content = soup.find('div', class_='view-con').text.strip()
        # 제목과 내용을 CSV 파일에 작성
        writer.writerow([title, content])

        # 현재 탭 닫기 및 원래 탭으로 전환
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])

    def scrape_site(self, url, output_file):
        """
        지정된 URL의 사이트를 스크랩합니다.

        Args:
            url (str): 스크랩할 사이트의 URL입니다.
            output_file (str): 스크랩한 데이터를 저장할 CSV 파일의 경로입니다.
        """
        # 사이트 접속
        self.driver.get(url)
        current_page = 1
        FIRST_NOTICE_INDEX, LAST_NOTICE_INDEX, SKIP_NOTICE_INDEX = 1, 21, 12

        # CSV 파일 오픈
        with open(output_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['제목', '내용'])

            while current_page < 4: #현재 페이지가 4 미만일때만 진행
                for i in range(FIRST_NOTICE_INDEX, LAST_NOTICE_INDEX + 1):
                    if i < SKIP_NOTICE_INDEX and current_page > 1:
                        continue
                    try:
                        # CSS 선택자를 이용해 공지사항 링크 선택
                        selector = f"#menu4875_obj412 > div._fnctWrap > form:nth-child(2) > div > table > tbody > tr:nth-child({i}) > td.td-subject > a"
                        element = self.driver.find_element(By.CSS_SELECTOR, selector)
                        href = element.get_attribute('href')
                        
                        # 방문하지 않은 공지사항이면 스크랩
                        if href not in self.visited_notices:
                            self.visited_notices.add(href)
                            self.scrape_notice(href, writer)

                    except Exception as e:
                        print(f"Error scraping post: {e}")
                        continue

                current_page += 1
                # 다음 페이지로 이동
                next_page_selector = self.get_next_page_selector(current_page)
                try:
                    next_page = self.driver.find_element(By.CSS_SELECTOR, next_page_selector)
                    next_page.click()
                    self.wait_for_page_load()
                except Exception as e:
                    print(f"End of pages or error: {e}")
                    break

    def get_next_page_selector(self, current_page):
        """
        현재 페이지 번호에 따라 다음 페이지로 이동하는 버튼의 CSS 선택자를 반환합니다.
        Args:
            current_page (int): 현재 페이지 번호입니다.

        Returns:
            str: 다음 페이지 버튼의 CSS 선택자입니다.
        """
        # 페이지 번호가 10의 배수일 때와 아닐 때의 다음 페이지 버튼 선택자가 다름
        return "#menu4875_obj412 > div._fnctWrap > form:nth-child(3) > div > div > a._next" if current_page % 10 == 0 else f"#menu4875_obj412 > div._fnctWrap > form:nth-child(3) > div > div > ul > li:nth-child({current_page}) > a"

    def close(self):
        """
        웹 드라이버를 종료합니다.
        """
        self.driver.quit()

#크롬 드라이버 파일 경로
driver_path = "C:\webdriver\chromedriver.exe"
#출력될 CSV 파일 경로
output_file = "scraped_data.csv"
#CustomScraper 인스턴스 생성
scraper = CustomScraper(driver_path)
#사이트 스크랩 실행
scraper.scrape_site("https://ellt.hufs.ac.kr/ellt/m04_s01.do?enc=Zm5jdDF8QEB8JTJGYmJzJTJGZWxsdCUyRjkyOSUyRmFydGNsTGlzdC5kbyUzRnBhZ2UlM0QxJTI2c3JjaENvbHVtbiUzRCUyNnNyY2hXcmQlM0QlMjZiYnNDbFNlcSUzRCUyNmJic09wZW5XcmRTZXElM0QlMjZyZ3NCZ25kZVN0ciUzRCUyNnJnc0VuZGRlU3RyJTNEJTI2aXNWaWV3TWluZSUzRGZhbHNlJTI2", output_file)
#스크랩 작업이 끝나면 웹 드라이버 종료
scraper.close()