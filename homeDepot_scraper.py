import requests
import json
import re

filename = "home_depot_reviews.csv"
f = open(filename, "w")
headers = 'userId, date, gender, age, userLocation, home_improvement_profile, overallRating, recommendation, featuresRating, qualityRating, valueRating, reviewTitle, reviewText\n'
f.write(headers)

#User inputs key info and extract product id from url
url = "https://www.homedepot.com/p/GE-25-4-cu-ft-Side-by-Side-Refrigerator-in-Stainless-Steel-GSS25GSHSS/205599120"
pagesDesired = 60
pageStop= pagesDesired + 1
product_id2 = re.search(r'/(\d{9})',url)
product_id = product_id2.groups(0)[0]

#get text/javascript page content from server for each review page
for pageNumber in range(1,pageStop,1):
	ajax_url = 'https://homedepot.ugc.bazaarvoice.com/1999aa/{}/reviews.djs?format=embeddedhtml&page={}&scrollToTop=true'.format(product_id, pageNumber)
	headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'} #changes user agent 
	ajax_page = requests.get(ajax_url)
	responseText = ajax_page.text

	#parse raw text into review_containers in a list
	review_container = re.findall(r'itemprop=\\"review\\(.*?)BVRRSeparator BVRRSeparatorContentBodyBottom',responseText)

	for review in review_container:
		
		userId_search = re.search(r'BVRRNickname\\">(.*?)<',review)
		userId = userId_search.groups(0)[0]
		
		date_search = re.search(r'datePublished\\" content=\\"(.*?)\\',review) 
		date = date_search.groups(0)[0]
		

		gender_search = re.search(r'BVRRContextDataValueGender\\">(.*?)<',review)
		if gender_search == None:
			gender = ''
		else:
			gender = gender_search.groups(0)[0]

		age_search = re.search(r'BVRRContextDataValueAge\\">(.*?)<',review)
		if age_search == None:
			age = ''
		else:
			age = age_search.groups(0)[0]

		userLocation_search = re.search(r'BVRRValue BVRRUserLocation\\">(.*?)<',review)
		if userLocation_search == None:
			userLocation = ''
		else:
			userLocation = userLocation_search.groups(0)[0]

		#this is either a diy or professional
		home_improvement_profile_search = re.search(r'BVRRContextDataValueHomeGoodsProfile\\">(.*?)<',review) 
		if home_improvement_profile_search == None:
			home_improvement_profile = ''
		else:
			home_improvement_profile = home_improvement_profile_search.groups(0)[0]

		overallRating_search = re.search(r'BVRRNumber BVRRRatingNumber\\">(.*?)<',review)
		overallRating_string = overallRating_search.groups(0)[0]
		overallRating = overallRating_string[0]

		recommendation_search = re.search(r'BVRRValue BVRRRecommended\\">(.*?)<',review)
		if recommendation_search == None:
			recommendation = ''
		else:
			recommendation = recommendation_search.groups(0)[0]

		featuresRating_search =re.search(r'Features\xa0<\\/div><div class=\\"BVRRRatingNormalOutOf\\"> <span class=\\"BVRRNumber BVRRRatingNumber\\">(.*?)<',review)
		if featuresRating_search == None:
			featuresRating = ''
		else:
			featuresRating = featuresRating_search.groups(0)[0]

		energyRating_search = re.search(r'Energy efficiency\xa0<\\/div><div class=\\"BVRRRatingNormalOutOf\\"> <span class=\\"BVRRNumber BVRRRatingNumber\\">(.*?)<',review)
		if energyRating_search == None:
			energyRating = ''
		else:
			energyRating = energyRating_search.groups(0)[0]

		qualityRating_search = re.search(r'Quality\xa0<\\/div><div class=\\"BVRRRatingNormalOutOf\\"> <span class=\\"BVRRNumber BVRRRatingNumber\\">(.*?)<',review)
		if qualityRating_search == None:
			qualityRating = ''
		else:
			qualityRating = qualityRating_search.groups(0)[0]

		valueRating_search = re.search(r'Value\xa0<\\/div><div class=\\"BVRRRatingNormalOutOf\\"> <span class=\\"BVRRNumber BVRRRatingNumber\\">(.*?)<',review)
		if valueRating_search == None:
			valueRating = ''
		else:
			valueRating = valueRating_search.groups(0)[0]

		reviewTitle_search = re.search(r'BVRRValue BVRRReviewTitle\\">(.*?)<',review)  
		reviewTitle = reviewTitle_search.groups(0)[0]
		
		#returns a list with all paragraphs/parts included...(will need to merge elements in list into one string using list comprehension?)
		reviewText_search = re.findall(r'<span class=\\"BVRRReviewText\\">(.*?)<',review)
		if reviewText_search == None:
			reviewText = ''
		elif len(reviewText_search) > 1:
			reviewText = ''.join(reviewText_search)
		elif len(reviewText_search) == 1:
			reviewText = reviewText_search[0]

		print(userId)
		print(str(date))
		print(gender)

		f.write(userId.replace(",","|") + "," + str(date) + "," + gender + "," + age.replace("to","-") + "," + userLocation.replace(",","|") + "," + home_improvement_profile + "," + overallRating.replace(",","|") + "," + recommendation.replace(",","|") + "," + featuresRating.replace(",","|") + "," + qualityRating.replace(",","|") + "," + valueRating.replace(",","|") + "," + reviewTitle.replace(",","|") + "," + reviewText.replace(",","|") + "\n")

f.close()


#https://homedepot.ugc.bazaarvoice.com/1999aa/205599120/reviews.djs?format=embeddedhtml&page=4&scrollToTop=true



