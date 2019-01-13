import requests
import json
import re

#create csv and write in column headers
filename = "home_depot_reviews.csv"
f = open(filename, "w")
headers = 'userId, date, gender, age, userLocation, home_improvement_profile, overallRating, recommendation, featuresRating, qualityRating, valueRating, reviewTitle, reviewText\n'
f.write(headers)

#User inputs url and pages desired, then product id is extracted from url
url = "https://www.homedepot.com/p/KitchenAid-Top-Control-Built-In-Tall-Tub-Dishwasher-in-PrintShield-Stainless-with-Fan-Enabled-PRODRY-39-dBA-KDPE334GPS/302853788"
pagesDesired = 60
pageStop= pagesDesired + 1
product_id2 = re.search(r'/(\d{9})',url)
product_id = u''.join(product_id2.groups(0)[0]).encode('ascii', 'ignore')

#get text/javascript page content from server for each review page
for pageNumber in range(1,pageStop,1):
	ajax_url = 'https://homedepot.ugc.bazaarvoice.com/1999aa/{}/reviews.djs?format=embeddedhtml&page={}&scrollToTop=true'.format(product_id, pageNumber)
	headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'} #changes user agent 
	ajax_page = requests.get(ajax_url)
	responseText = ajax_page.text

	#parse raw text into review_containers in a list
	review_container = re.findall(r'itemprop=\\"review\\(.*?)BVRRSeparator BVRRSeparatorContentBodyBottom',responseText)

	#loop through review containers and scrape desired data
	for review in review_container:
		
		userId_search = re.search(r'BVRRNickname\\">(.*?)<',review)
		userId = u''.join(userId_search.groups(0)[0]).encode('ascii', 'ignore')
		
		date_search = re.search(r'datePublished\\" content=\\"(.*?)\\',review) 
		date = u''.join(date_search.groups(0)[0]).encode('ascii', 'ignore')
		

		gender_search = re.search(r'BVRRContextDataValueGender\\">(.*?)<',review)
		if gender_search == None:
			gender = ''
		else:
			gender = u''.join(gender_search.groups(0)[0]).encode('ascii', 'ignore')

		age_search = re.search(r'BVRRContextDataValueAge\\">(.*?)<',review)
		if age_search == None:
			age = ''
		else:
			age = u''.join(age_search.groups(0)[0]).encode('ascii', 'ignore')

		userLocation_search = re.search(r'BVRRValue BVRRUserLocation\\">(.*?)<',review)
		if userLocation_search == None:
			userLocation = ''
		else:
			userLocation = u''.join(userLocation_search.groups(0)[0]).encode('ascii', 'ignore')

		#this outputs either a 'diy' or 'professional'
		home_improvement_profile_search = re.search(r'BVRRContextDataValueHomeGoodsProfile\\">(.*?)<',review) 
		if home_improvement_profile_search == None:
			home_improvement_profile = ''
		else:
			home_improvement_profile = u''.join(home_improvement_profile_search.groups(0)[0]).encode('ascii', 'ignore')

		overallRating_search = re.search(r'BVRRNumber BVRRRatingNumber\\">(.*?)<',review)
		overallRating_string = u''.join(overallRating_search.groups(0)[0]).encode('ascii', 'ignore')
		overallRating = overallRating_string[0]

		recommendation_search = re.search(r'BVRRValue BVRRRecommended\\">(.*?)<',review)
		if recommendation_search == None:
			recommendation = ''
		else:
			recommendation = u''.join(recommendation_search.groups(0)[0]).encode('ascii', 'ignore')

		featuresRating_search =re.search(r'Features\xa0<\\/div><div class=\\"BVRRRatingNormalOutOf\\"> <span class=\\"BVRRNumber BVRRRatingNumber\\">(.*?)<',review)
		if featuresRating_search == None:
			featuresRating = ''
		else:
			featuresRating = u''.join(featuresRating_search.groups(0)[0]).encode('ascii', 'ignore')

		energyRating_search = re.search(r'Energy efficiency\xa0<\\/div><div class=\\"BVRRRatingNormalOutOf\\"> <span class=\\"BVRRNumber BVRRRatingNumber\\">(.*?)<',review)
		if energyRating_search == None:
			energyRating = ''
		else:
			energyRating = u''.join(energyRating_search.groups(0)[0]).encode('ascii', 'ignore')

		qualityRating_search = re.search(r'Quality\xa0<\\/div><div class=\\"BVRRRatingNormalOutOf\\"> <span class=\\"BVRRNumber BVRRRatingNumber\\">(.*?)<',review)
		if qualityRating_search == None:
			qualityRating = ''
		else:
			qualityRating = u''.join(qualityRating_search.groups(0)[0]).encode('ascii', 'ignore')

		valueRating_search = re.search(r'Value\xa0<\\/div><div class=\\"BVRRRatingNormalOutOf\\"> <span class=\\"BVRRNumber BVRRRatingNumber\\">(.*?)<',review)
		if valueRating_search == None:
			valueRating = ''
		else:
			valueRating = u''.join(valueRating_search.groups(0)[0]).encode('ascii', 'ignore')

		reviewTitle_search = re.search(r'BVRRValue BVRRReviewTitle\\">(.*?)<',review)  
		reviewTitle = u''.join(reviewTitle_search.groups(0)[0]).encode('ascii', 'ignore')
		
		#because review text can be broken into different parts, this finds all parts and joins them
		reviewText_search = re.findall(r'<span class=\\"BVRRReviewText\\">(.*?)<',review)
		if reviewText_search == None:
			reviewText = ''
		elif len(reviewText_search) > 1:
			reviewText = ''.join(reviewText_search).encode('ascii', 'ignore')
		elif len(reviewText_search) == 1:
			reviewText = reviewText_search[0].encode('ascii', 'ignore')

		#for your viewing pleasure
		print(userId)
		print(str(date))
		print(gender)

		#write review data to csv
		f.write(userId.replace(",","|") + "," + str(date) + "," + gender + "," + age.replace("to","-") + "," + userLocation.replace(",","|") + "," + home_improvement_profile + "," + overallRating.replace(",","|") + "," + recommendation.replace(",","|") + "," + featuresRating.replace(",","|") + "," + qualityRating.replace(",","|") + "," + valueRating.replace(",","|") + "," + reviewTitle.replace(",","|") + "," + reviewText.replace(",","|") + "\n")

f.close()


