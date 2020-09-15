import requests 
from bs4 import BeautifulSoup as soup
from time import sleep
import re

filename = "Four_Seasons_reviews.csv"
f = open(filename, "w")
headers = "username, hometown, title, stars, review, date, trip_type\n"
f.write(headers)

#get the html for hotel reviews
for pagenumber in range(5,99,5):
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
		
		print("username: " + username)
		print("hometown: " + hometown)
		print("title: " + title)
		print("stars: " +stars)
		print("review: " + review)
		print("date: " + date)
		print("trip_type: " + trip_type)

		f.write(str(username.replace(",", "|")) + "," +str(hometown.replace(",", "|")) + "," +title.replace(",", "|") + "," +str(stars) + "," +str(review.replace(",", "|")) + "," +str(date) + "," +str(trip_type) + "\n")

f.close()
