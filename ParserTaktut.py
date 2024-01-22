import requests as r
from bs4 import BeautifulSoup as bs
from fake_useragent import UserAgent
import csv

URLS = {
	'https://taktut.myprintbar.ru/muzhskiye-tovari/': 1724, 
	'https://taktut.myprintbar.ru/zhenskiye-tovari/': 1707, 
	'https://taktut.myprintbar.ru/detskiye-tovari-dlya-machikov/': 1564,
	'https://taktut.myprintbar.ru/detskiye-tovari-dlya-devochek/': 1552
}

class ParserItems:
	def __init__(self, start_page) -> None:
		self.headers = {'user-agent': UserAgent().chrome}
		self.current_page = start_page

	def save_items(self, items: list[str], encoding):
		with open('items.csv', 'a', encoding=encoding, newline='') as file:
			writer = csv.writer(file, dialect='excel', delimiter=',')
			writer.writerows(items)

	def get_item_info(self, date):
		items = []
		for i in date:
			link = i.get('href')
			title = ''
			count = 0
			for i in i.find_all('span', {'class':'shirt__art'}):
				if count == 0:
					title += i.text
					count = 1
				else:
					title += ' ' + i.text

			items.append([title, link])

		return items

	def get_item_links(self, response: r.Response):
		html = bs(response.text, 'lxml')
		data = html.find_all('a', {'class': "mainHref"})

		return data

	def run_parse(self):
		for URL in URLS:
			while self.current_page < URLS[URL]:
				response = r.get(f'{URL}?p={self.current_page}', headers=self.headers)

				links = self.get_item_links(response)
				info = self.get_info(links)

				self.save_items(info, response.encoding)
				self.current_page += 1


def main():
	parser = ParserItems(0)
	parser.run_parse()


if __name__ == "__main__":
	main()
