from bs4 import BeautifulSoup as soup
from datetime import datetime
from time import sleep
import requests
import csv
import re

class amazonScraper():
	"""Scrapes Amazon consumer reviews and outputs csv data table"""
	consumerReviews = []
	
	def __init__(self, filename, url, pagesDesired):
		self.filename = filename + ".csv"
		self.url = url
		self.pagesDesired = pagesDesired

#writes consumerReview data to a csv file
	def write_csv(self):
		keys = self.consumerReviews[0].keys()

		with open(self.filename, 'w') as output_file:
			dict_writer = csv.DictWriter(output_file, keys)
			dict_writer.writeheader()
			dict_writer.writerows(self.consumerReviews)

#Gets page, then scrapes containers and stores data for consumer reviews as dictionary in consumerReviews list
	def scraper(self):
		for pageNumber in range(1,self.pagesDesired+1,1):
			url = self.url[:-1] +'{}'.format(pageNumber)
			headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'} #changes user agent 
			my_page = requests.get(url,headers = headers) #gets page
			page_html = my_page.text
			page_soup = soup(page_html, "html.parser")
			containers = page_soup.findAll("div",{"class":"a-section review"})
			
			for container in containers:
				review_data = {}

				stars_container = container.find("span",{"class":"a-icon-alt"})
				stars_string = stars_container.text
				stars = str(float(stars_string.split()[0]))
		
				title_container = container.find("a",{"data-hook":"review-title"})
				review_title = title_container.text.replace(",", "|") 
			
				author_container = container.find("a",{"data-hook":"review-author"})
				author = author_container.text.replace(",", "|")
			
				date_container = container.find("span",{"data-hook":"review-date"})
				date_string = date_container.text
				date_written = date_string.split(' ', 1)[1]
				date_converted = datetime.strptime(date_written, '%B %d, %Y')
				date = str(date_converted.strftime('%Y-%m-%d'))
		
				review_container = container.find("span",{"data-hook":"review-body"})
				review_text = review_container.text.replace(",", "|")
			
				comments_container = container.find("span",{"class":"review-comment-total aok-hidden"})
				comments = comments_container.text.replace(",", "|")


				review_data = {'date': date, 
								'stars':stars,
								'author':author,
								'title':review_title,
								'review':review_text,
								'comments':comments}

				self.consumerReviews.append(review_data)

#runs program
	def run(self):
		self.scraper()
		self.write_csv()

		print('Your review data has been scraped and dumped into a csv file')



class tripadvisorScraper():
	"""Scrapes Tripadvisor consumer reviews and outputs csv data table"""
	consumerReviews = []

	def __init__(self, filename, url, pagesDesired):
		self.filename = filename + ".csv"
		self.url = url
		self.pagesDesired = pagesDesired

	#writes consumerReview data to a csv file
	def write_csv(self):
		keys = self.consumerReviews[0].keys()

		with open(self.filename, 'w') as output_file:
			dict_writer = csv.DictWriter(output_file, keys)
			dict_writer.writeheader()
			dict_writer.writerows(self.consumerReviews)

	def scraper(self):
		for pagenumber in range(5,self.pagesDesired+1,5):
			url = 'https://www.tripadvisor.com/Hotel_Review-g45963-d91674-Reviews-or{}-Four_Seasons_Hotel_Las_Vegas-Las_Vegas_Nevada.html'.format(pagenumber)
			headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'} #changes user agent 
			my_page = requests.get(url, headers=headers)
			page_html = my_page.text
			page_soup = soup(page_html, "html.parser")
			containers = page_soup.find_all("div",{"class":"review-container"})

			#get the url for each individual review on the page
			for container in containers:
				review_url_conatiner = str(container.find(href=re.compile("^/Show")))
				review_url_conatiner_soup = soup(review_url_conatiner, "html.parser")
				review_url_tag = review_url_conatiner_soup.a
				review_url_string = review_url_tag['href']
				review_url = 'https://www.tripadvisor.com' + review_url_string

				#get individual review page html and begin parsing
				review_page = requests.get(review_url, headers=headers)
				review_page_html = review_page.text
				review_page_soup = soup(review_page_html, "html.parser")
				
				#get review data
				username = (review_page_soup.find("span",{"onclick":"ta.trackEventOnPage('Reviews', 'show_reviewer_info_window', 'user_name_name_click')"})).text
				
				hometown = (review_page_soup.find("span",{"class":"expand_inline userLocation"})).text
				title = (review_page_soup.find("span",{"class":"noQuotes"})).text.strip()
				
				stars_container = str(review_page_soup.find(alt=re.compile("bubbles")))
				stars_soup = soup(stars_container, "html.parser")
				stars_tag = stars_soup.span
				stars = stars_tag['alt'] 
				
				review = (review_page_soup.find("p",{"class":"partial_entry"})).text
				
				date_and_trip_type = (review_page_soup.find("span",{"class":"recommend-titleInline"})).text
				date_type_list = date_and_trip_type.split(", traveled ")
				
				date = date_type_list[0]
				
				if len(date_type_list) == 2:
					trip_type = date_type_list[1]
				else:
					trip_type = ""

				review_data = {'date': date,
								'stars':stars,
								'hometown':hometown, 
								'trip_type':trip_type,
								'author':username,
								'title':title,
								'review':review}

				self.consumerReviews.append(review_data)

#runs program
	def run(self):
		self.scraper()
		self.write_csv()

		print('Your review data has been scraped and dumped into a csv file')








