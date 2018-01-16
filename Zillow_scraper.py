from bs4 import BeautifulSoup as soup 
import requests
import json


filename = "Zillow.csv"
f = open(filename, "w")
headers = "agent, date, overall_rating, local_knowledge, process_expertise, responsiveness, negotiation_skills, work_done, review_body\n"
f.write(headers)

#Find data id for this review page
url = 'https://www.zillow.com/profile/Eric-I-Fox/#reviews'
pages_i_want = 10
pagesDesired = pages_i_want + 1
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
page = requests.get(url,headers=headers)

page_html = page.text
page_soup = soup(page_html, "html.parser")
data_id_tag = page_soup.findAll("a",{"data-zuid":True})
data_id_html = data_id_tag[0]
data_id = data_id_html['data-zuid']

#grab first page of reviews
for pageNumber in range(1,pagesDesired,1):
	ajax_url = "https://www.zillow.com/ajax/review/ReviewDisplayJSONGetPage.htm?id={}&size=5&page={}&page_type=received&moderator_actions=0&reviewee_actions=0&reviewer_actions=0&proximal_buttons=1&hasImpersonationPermission=0".format(data_id, pageNumber)
	ajax_page = requests.get(ajax_url,headers=headers)
	
	json_string = ajax_page.text
	parsed_json = json.loads(json_string)

	#loop through first review
	for review in parsed_json['reviews']:
		
		agentName = review['revieweeDisplayName']

		reviewDate = review['reviewMonth'] + "/" + review['reviewYear']

		overall_starRating_raw = review['overallRating']['amount']
		overall_starRating = overall_starRating_raw[0]

		localKnowledge_raw = review['subRatings'][0]['amount']
		localKnowledge = localKnowledge_raw[0]

		processExpertise_raw = review['subRatings'][1]['amount']
		processExpertise = processExpertise_raw[0]

		responsiveness_raw = review['subRatings'][2]['amount']
		responsiveness = responsiveness_raw[0]

		negotiationSkills_raw = review['subRatings'][3]['amount']
		negotiationSkills = negotiationSkills_raw[0]

		workDone = review['revieweeWorkDone']

		reviewBody = review['reviewBodyMain']

		print(agentName)
		print(reviewDate)
		print(overall_starRating)
		print(localKnowledge)
		print(processExpertise)
		print(responsiveness)
		print(negotiationSkills)
		print(workDone)
		print(reviewBody)
		print ("____")

		f.write(agentName + "," + str(reviewDate) + "," + str(overall_starRating) + "," + str(localKnowledge) + "," + str(processExpertise) + "," + str(responsiveness) + "," + str(negotiationSkills) + "," + workDone.replace(",","|") + "," + reviewBody.replace(",","|").replace('\r'," ").replace('\n'," ") + "\n")

f.close()
	

	#first_review = parsed_json['reviews'][0]
	#review_body = parsed_json['reviews'][0]['reviewBodyMain']
#
	#print(review_body)

#page_html = page.text 
#page_soup = soup(page_html, "html.parser")
#containers = page_soup.findall("div",{"class":"reviews-list"})
#
#for container in containers:
#
#	stars =
#	title
#	date
#	user_id
#	transaction_type




