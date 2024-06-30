import requests
from bs4 import BeautifulSoup
import html2text
import re

class ShutdownBot:
    def __init__(self):
        self.base_url = 'https://hoe.com.ua'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:127.0) Gecko/20100101 Firefox/127.0',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            'Origin': self.base_url,
            'Connection': 'keep-alive',
            'Referer': f'{self.base_url}/shutdown/new',
            'Cookie': 'ViewedPost=postId_13790=1',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Priority': 'u=1',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'TE': 'trailers'
        }

    def get_current_shutdown(self, street_id, house):
        url = f'{self.base_url}/shutdown-events'
        data = {
            'streetId': street_id,
            'house': house
        }
        response = requests.post(url, headers=self.headers, data=data)
        text = convert_html_to_markdown(response.text)
        if text.startswith("За вказаною адресою відсутнє зареєстроване"):
            return "За обраною адресою відключення не зареєстроване"
        if text.startswith("Вид робіт"):
            regex = r"Вид робіт.*.\n.*.\n"
            subst = ""
            text = re.sub(regex, subst, text, 0, re.MULTILINE)
        return text

    def get_shutdown_queue(self, street_id, house):
        url = f'{self.base_url}/shutdown-queues'
        data = {
            'streetId': street_id,
            'house': house
        }
        response = requests.post(url, headers=self.headers, data=data)
        return convert_html_to_markdown(response.text)

    def get_shutdown_schedule_image(self):
        url = f'{self.base_url}/page/pogodinni-vidkljuchennja'
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        img_tag = soup.select_one('body main div:nth-of-type(2) div div:nth-of-type(1) div:nth-of-type(2) img')
        
        if img_tag:
            img_url = img_tag['src']
            return f'{self.base_url}{img_url}'
        else:
            return 'Image not found'
        
def convert_html_to_markdown(html_text):
    h = html2text.HTML2Text()
    h.ignore_links = False
    return h.handle(html_text)
