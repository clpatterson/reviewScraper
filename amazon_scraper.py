#!/usr/bin/python
import requests
from bs4 import BeautifulSoup as soup
from datetime import datetime

#creates csv file for product review data
filename = "Pennzoil20_amazon_reviews.csv"
f = open(filename, "w")
headers = "stars_rating, review_title, author, date, review_text, comments\n"
f.write(headers)

#loop to capture multiple pages
for pageNumber in range(1,17,1):
	my_url = 'https://www.amazon.com/Pennzoil-550046122-Platinum-quart-Synthetic/product-reviews/B01M8JY4V3/ref=cm_cr_arp_d_paging_btm_2?ie=UTF8&reviewerType=all_reviews&pageNumber={}'.format(pageNumber)
	headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'} #changes user agent 
	my_page = requests.get(my_url,headers = headers) #gets page

	#off loads the contents of the url into a variable
	page_html = my_page.text
	
	#using package from bs4, open url and conduct html parsing
	page_soup = soup(page_html, "html.parser")
	
	#grabs each review container
	containers = page_soup.findAll("div",{"class":"a-section review"})
	
	for container in containers:
		stars_container = container.find("span",{"class":"a-icon-alt"})
		stars_string = stars_container.text
		stars = float(stars_string.split()[0])

		title_container = container.find("a",{"data-hook":"review-title"})
		review_title = title_container.text
	
		author_container = container.find("a",{"data-hook":"review-author"})
		author = author_container.text
	
		date_container = container.find("span",{"data-hook":"review-date"})
		date_string = date_container.text
		date_written = date_string.split(' ', 1)[1]
		date_converted = datetime.strptime(date_written, '%B %d, %Y')
		date = date_converted.strftime('%Y-%m-%d')

		review_container = container.find("span",{"data-hook":"review-body"})
		review_text = review_container.text
	
		comments_container = container.find("span",{"class":"review-comment-total aok-hidden"})
		comments = comments_container.text
	
		print("stars: " + str(stars))
		print("review_title: " + review_title)
		print("author: " + author)
		print("date: " + str(date))
		print("review_text: " + review_text)
		print("comments: " + comments)
	
		f.write(str(stars) + "," +review_title.replace(",", "|") + "," +author.replace(",", "|") + "," +str(date) + "," +review_text.replace(",", "|") + "," +comments.replace(",", "|") +  "\n")

f.close()
