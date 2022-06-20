import requests
import lxml
from bs4 import BeautifulSoup
from time import sleep
# from xlwt import *
import csv

base_url = "https://scholar.google.com"
label_to_search="edge_intelligence"
search_query="/citations?view_op=search_authors&hl=en&mauthors=label:"+label_to_search

headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
}

no_of_pages = 2
profiles_csv_file = label_to_search+"_profiles_pp_1_to_"+str(no_of_pages)+".csv"

csv_file = open(profiles_csv_file,'w', encoding='UTF8')
csv_writer = csv.writer(csv_file)
profile_header = ['author_name','citedby','affiliation','author_url','other_labels']
csv_writer.writerow(profile_header)

for counter in range(no_of_pages):
	f = requests.get(base_url+search_query, headers = headers)
	soup = BeautifulSoup(f.content,'lxml')
	profiles = soup.find_all('div',{'class':'gs_ai gs_scl gs_ai_chpr'})
	print("      Page "+str(counter)+"      ")
	
	for p in  profiles:
		profile_full_data = []
		profile_full_data.append(p.find('h3').text.split(',')[0]) # Get the name
		profile_full_data.append(p.find('div',{'class':'gs_ai_cby'}).text.split(' ')[2]) # Get the citation number 
		profile_full_data.append(p.find('div',{'class':'gs_ai_aff'}).text) # get the affiliation
		profile_full_data.append(base_url+p.find('h3').find('a')['href']) #get the url of the author		
		other_labels = []
		labels = p.find('div',{'class':'gs_ai_int'}).find_all('a')
		for l in labels:
			other_labels.append(l.text.replace(" ","_"))
		# print(name+" \t"+name_url+"  \t"+citedby)
		profile_full_data.append(other_labels)

		# Write data to csv
		csv_writer.writerow(profile_full_data)

	next_page = soup.find('button',{'class':'gs_btnPR gs_in_ib gs_btn_half gs_btn_lsb gs_btn_srt gsc_pgn_pnx'})
	next_page = next_page['onclick'].split('=')[1]
	next_page = next_page.replace("'","")
	next_page = next_page.replace("\\x3d","=")
	next_page = next_page.replace("\\x26","&")

	sleep(1)
	print("           ")
	search_query = next_page

csv_file.close()

