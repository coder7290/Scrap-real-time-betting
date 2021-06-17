#!/usr/bin/env python
# coding: utf-8

# In[23]:


import os
import sys
import time
import json
import datetime
import random
from pymongo import MongoClient 
from threading import Thread


# In[24]:


from sys import platform
from bs4 import BeautifulSoup
from lxml import html
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


# In[25]:


from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


# In[26]:


from http_request_randomizer.requests.proxy.requestProxy import RequestProxy


# In[27]:



class Soccer24:
	def __init__(self):
		#self.searchkey = searchkey
		# self.first_driver = first_driver
		self.goodlist = []
		self.timeout = 30
		self.start_url = 'https://www.soccer24.com/'
		
		self.client = MongoClient("mongodb://localhost:27017/")
		database = 'efdbmain'
		collection = 's24fixtures'
		cursor = self.client[database]
		self.collection = cursor[collection]
        #self.data = data

		super(Soccer24, self).__init__()

	def scroller(self, timeout):
		last_height = self.first_driver.execute_script("return document.body.scrollHeight")
		new_height = 0
		while True:
			BeautifulSoup
			self.first_driver.execute_script(f"expand_collapse_league_load();")
			new_height +=100
			if new_height >= last_height:   break
		time.sleep(1)

	def run(self):
		self.first_driver = self.open_chrome()
		self.first_driver.delete_all_cookies()
		#chrome = self.first_driver.get(self.start_url + self.searchkey)
		#main_window = self.first_driver.window_handles[0]
		#self.first_driver.switch_to.window(main_window)
		chrome = self.first_driver.get(self.start_url)
		# if (chrome is None):
		#     self.first_driver.quit()
		#     print( "bestbut.com : Access Denied")
		#     return 

		time.sleep(3)
		dic = {}
		dicList = []
		while True:
			expand_tags = self.first_driver.find_elements_by_class_name('expand')
			#for expand_tag in expand_tags:
				#print (expand_tag)
				#BeautifulSoup(self.first_driver.page_source).click(expand_tag).perform()
				#expand_tag.click()
			#exit(0)

			soup = BeautifulSoup( self.first_driver.page_source, "html.parser")
			date = soup.find("div", "calendar__datepicker").text
			now = datetime.datetime.now()
			dic["match_date"] = date[0:5] + "/" + str(now.year)



			All_sportName = soup.find("div", "sportName soccer")
			children = All_sportName.findChildren("div", recursive=False)

			for child in children:
				all_divs = [child] + child.find_next_siblings('div')
				k = 0
				for item in all_divs:
					dic["match_id"] = ""
					dic["match_status"] = ""
					dic["match_referee"] = ""
					dic["match_stadium"] = ""
					dic["start_date"] = ""
					dic["match_last_update"] = ""
					dic["home_team"] = ""
					dic["away_team"] = ""
					dic["odds_1"] = ""
					dic["odds_2"] = ""
					dic["odds_x"] = ""
					dic["odds_1_status"] = ""
					dic["odds_2_status"] = ""
					dic["odds_3_status"] = ""
					dic["home_last_five_matches"] = ""
					dic["away_last_five_matches"] = ""
					dic["head_to_head_winner"] = ""
					dic["away_head_to_head"] = ""
					dic["home_rank"] = ""
					dic["home_goals_difference"] = ""

					k = k + 1
					_class = item.attrs['class'][0]
					if _class == "event__header":
						dic["venue_country"] = item.find_all('span', {'class': 'event__title--type'})[0].text
						legue = item.find_all('span', {'class': 'event__title--name'})[0].text
						dic["competition"] = dic["venue_country"] + " " + legue
						dic["federation"] = item.find_all('span', {'class': 'event__title--type'})[0].text
						dic["season"] = "2020/2021"


						tooltip = item.find_all('div', {'class': 'event__expander'})[0].get("title")
						if tooltip == "Display all matches of this league!":
							continue
							#item.find_all('div', {'class': 'event__expander'})[0].click() 
						continue
					

					_id = item['id']
					dic["match_id"] = _id[4:len(_id)]

					dic["match_status"] = self.first_driver.find_element_by_xpath("//*[@id='"+_id+"']//div[2]").text
					#dic["home_team"] = self.first_driver.find_element_by_xpath("//*[@id='"+_id+"']//div[3]").text
					#dic["away_team"] = self.first_driver.find_element_by_xpath("//*[@id='"+_id+"']//div[4]").text

					self.second_driver = self.open_chrome()
					self.second_driver.delete_all_cookies()
					self.second_driver.get("https://www.soccer24.com/match/"+ dic["match_id"] +"/#match-summary/match-summary")
					time.sleep(4)

					soup1 = BeautifulSoup( self.second_driver.page_source, "html.parser")
					expand_tags = soup1.find_all("div", {"class": "data___33slwBJ"})

					for div in expand_tags:
						if len(div.findChildren("span")) == 2:							
							referee = div.findChildren("span")[0].text
							stadium = div.findChildren("span")[1].text
							dic["match_referee"] = referee[9:len(referee)]
							dic["match_stadium"] = stadium[8:len(stadium)]
						elif len(div.findChildren("span")) == 1:
							temp = div.findChildren("span")[0].text
							if 'Referee' in temp:
								dic["match_referee"] = temp[9:len(temp)]
							elif 'Venue' in temp:
								dic["match_stadium"] = temp[8:len(temp)]
					#print (dic)

					time_tags = soup1.find_all("div", {"class": "startTime___2oy0czV"})

					for time_tag in time_tags:
						dic["start_date"] = time_tag.findChildren("div")[0].text
						dic["match_last_update"] = time_tag.findChildren("div")[0].text

					#soup1.find_all('div', {'class': 'participantName___3lRDM1i'})[0].text

					ii = 0
					for div in soup1.find_all('div', {'class': 'participantName___3lRDM1i'}):
						ii = ii + 1
						if ii == 1 :
							dic["home_team"] = div.findChildren("a")[0].text
						else:
							dic["away_team"] = div.findChildren("a")[0].text
						

					####################################################################
					#dic["match_status"] = item.find_all('div', {'class': _class_status})[0].text
					#dic["home_team"] = item.find_all('div', {'class': 'event__participant--home'})[0].text
					#dic["away_team"] = item.find_all('div', {'class': 'event__participant--away'})[0].text
					
					for div in item.findAll('div', {'class': 'event__scores'}):
						if len(div.findChildren("span")) == 0:
							dic["result"] = "null"
						else:
							dic["result"] = div.findChildren("span")[0].text + " - "+ div.findChildren("span")[1].text
					

					

					#mark1 = item.findChildren()[6].findChildren("span", recursive=False)[0]

					dic["odds_1"] = item.find_all('div', {'class': 'event__odd--odd1'})[0].text
					dic["odds_2"] = item.find_all('div', {'class': 'event__odd--odd2'})[0].text
					dic["odds_x"] = item.find_all('div', {'class': 'event__odd--odd3'})[0].text

					for div in item.findAll('div', {'class': 'event__odd--odd1'}):
						if dic["odds_1"] == "-":
							dic["odds_1_status"] = ""
						else:
							if len(div.find('span').attrs['class']) == 0:
								dic["odds_1_status"] = "flat"
							else:
								dic["odds_1_status"] = div.find('span').attrs['class'][0]
					
						
					for div in item.findAll('div', {'class': 'event__odd--odd2'}):
						if dic["odds_2"] == "-":
							dic["odds_2_status"] = ""
						else:
							if len(div.find('span').attrs['class']) == 0:
								dic["odds_2_status"] = "flat"
							else:
								dic["odds_2_status"] = div.find('span').attrs['class'][0]

					for div in item.findAll('div', {'class': 'event__odd--odd3'}):
						if dic["odds_x"] == "-":
							dic["odds_3_status"] = ""
						else:
							if len(div.find('span').attrs['class']) == 0:
								dic["odds_3_status"] = "flat"
							else:
								dic["odds_3_status"] = div.find('span').attrs['class'][0]

					#self.first_driver.find_element_by_xpath("//*[@class='sportName soccer']//div[" + str(i) + "]").click()

					
					#new_window = self.first_driver.window_handles[1]
					
					#self.first_driver.switch_to_window(new_window)

					#time.sleep(5)
					#self.first_driver.close()

					#main_window = self.first_driver.window_handles[0]


					#self.first_driver.switch_to_window(main_window)
							

					#print (dic)
					#print ("(##########################################)")
					#self.second_driver = self.open_chrome()
					#self.second_driver.delete_all_cookies()
					#self.second_driver.get("https://www.soccer24.com/match/"+ dic["match_id"] +"/#match-summary/match-summary")
					#time.sleep(4)

					#soup1 = BeautifulSoup( self.second_driver.page_source, "html.parser")
					#expand_tags = soup1.find_all("div", {"class": "data___33slwBJ"})

					#for div in expand_tags:
					#	referee = div.findChildren("span")[0].text
					#	stadium = div.findChildren("span")[1].text
					#	dic["match_referee"] = referee[9:len(referee)]
					#	dic["match_stadium"] = stadium[8:len(stadium)]
					

					#time_tags = soup1.find_all("div", {"class": "startTime___2oy0czV"})

					#for time_tag in time_tags:
					#	dic["start_date"] = time_tag.findChildren("div")[0].text
					#	dic["match_last_update"] = time_tag.findChildren("div")[0].text

					self.second_driver.get("https://www.soccer24.com/match/"+ dic["match_id"] +"/#h2h/overall")
					time.sleep(4)
					soup2 = BeautifulSoup( self.second_driver.page_source, "html.parser")
					away_tags = soup2.find_all("span", {"class": "icon___AM1IS3-"})
					#print (len(away_tags))
					#print (away_tags)

					home_last_five_matches = ""
					away_last_five_matches = ""
					i = 0

					for away_tag in away_tags:
						i = i + 1
						if i < 6:
							home_last_five_matches = home_last_five_matches + str(away_tag.findChildren("div")[0].text)
						else:
							away_last_five_matches = away_last_five_matches + str(away_tag.findChildren("div")[0].text)
					
					dic["home_last_five_matches"] = home_last_five_matches
					dic["away_last_five_matches"] = away_last_five_matches

					match_tags = soup2.find_all("div", {"class": "row___1EG6GCt"})
					j = 0
					home_mark = 0
					away_mark = 0

					for match_tag in match_tags:
						j = j + 1
						if j > 10:
							tempteam1 = match_tag.findChildren("span")[5].text
							tempteam2 = match_tag.findChildren("span")[6].text
							goals_result_temp = match_tag.findChildren("span")[8].text
							goals = goals_result_temp.split(":")
							#print (j)
							#print (tempteam1)
							#print (tempteam2)
							#print (goals_result_temp)
							#exit(0)

							if dic["away_team"] == tempteam1:
								if int(goals[0]) > int(goals[1]):
									away_mark = away_mark + 1
								elif int(goals[0]) < int(goals[1]):
									home_mark = home_mark + 1
							elif dic["away_team"] == tempteam2:
								if int(goals[0]) < int(goals[1]):
									away_mark = away_mark + 1
								elif int(goals[0]) > int(goals[1]):
									home_mark = home_mark + 1

					if home_mark - away_mark > 0:
						dic["head_to_head_winner"] = "1"
					elif home_mark - away_mark < 0:
						dic["head_to_head_winner"] = "2"
					else:
						dic["head_to_head_winner"] = "X"
					

					self.second_driver.get("https://www.soccer24.com/match/"+ dic["match_id"] +"/#h2h/away")
					time.sleep(3)
					soup2 = BeautifulSoup( self.second_driver.page_source, "html.parser")
					away_tags = soup2.find_all("span", {"class": "icon___AM1IS3-"})

					away_head_to_head = ""

					for away_tag in away_tags:
						away_head_to_head += str(away_tag.findChildren("div")[0].text)
					
					dic["away_head_to_head"] = away_head_to_head


					self.second_driver.get("https://www.soccer24.com/match/"+ dic["match_id"] +"/#standings/table/overall")
					time.sleep(3)
					soup2 = BeautifulSoup( self.second_driver.page_source, "html.parser")
					rank_tags = soup2.find_all("div", {"class": "selected___37fwRSu"})

					for rank_tag in rank_tags:
						rank = rank_tag.findChildren("div")[0].text
						team = rank_tag.findChildren("div")[1].text

						goals_result = rank_tag.findChildren("span")[4].text
						goals = goals_result.split(":")
						diff_goals = int(goals[0]) - int(goals[1])

						if team == dic["home_team"]:
							dic["home_rank"] = rank[0:1]
							dic["home_goals_difference"] = diff_goals
						elif team == dic["away_team"]:
							dic["away_rank"] = rank[0:1]
							dic["away_goals_difference"] = diff_goals

					dicList.append(dic)
					print (dic)
					
					self.second_driver.quit()
					dic["_id"] = str(random.randrange(3, 9999999999999999999999))
					query = {"match_id":{"$eq":dic["match_id"]}, "match_date":{"$eq":dic["match_date"]}}
					find_data = self.collection.find_one(query)

					if find_data is None:
						self.insert_data(dic)
					else:
						self.update_data(dic)
					#if k == 2:
					#	break

				self.first_driver.quit()
				break

			break

		#for data in dicList:
		#	query = {"match_id":{"$eq":data["match_id"]}, "match_date":{"$eq":data["match_date"]}}
		#	find_data = self.collection.find_one(query)
		#	if find_data is None:
		#		self.insert_data(data)
		#	else:
		#		update_data(data)


	def insert_data(self, data):
		#self.db.collection.getIndexes();
		#self.db.collection.dropIndex('_id');
		#self.db.collection.getIndexes();
		self.collection.insert_one(data)
		print ("insert_data ========== OK")

	def update_data(self, data):
		update_data = {}
		update_data["result"] = data["result"]
		update_data["match_status"] = data["match_status"]
		update_data["match_last_update"] = data["match_last_update"]
		update_data["odds_1"] = data["odds_1"]
		update_data["odds_1_status"] = data["odds_1_status"]
		update_data["odds_2"] = data["odds_2"]
		update_data["odds_2_status"] = data["odds_2_status"]
		update_data["odds_x"] = data["odds_x"]
		update_data["odds_3_status"] = data["odds_3_status"]

		new_data = {'$set':update_data}
		
		query = {"match_id":{"$eq":data["match_id"]}, "match_date":{"$eq":data["match_date"]}}
		present_data = self.collection.find_one(query)
		#filter["match_id"] = data["match_id"]
		#filter["match_date"] = data["match_date"]

		self.collection.update_one(present_data, new_data)
		print ("update_data ============ OK")


	def open_chrome(self):
		# options = webdriver.ChromeOptions()
		# options.add_argument('--incognito')
		# options.add_argument('--headless')
		# options.add_argument("--log-level=3")
		# options.add_argument('--disable-extensions')
		# # options.add_argument('start-maximized')
		# options.add_argument('disable-infobars')
		# options.add_argument('--disable-notifications')
		# options.add_argument('--ignore-certificate-errors')
		# options.add_argument('--ignore-ssl-errors')

		# # _driver = webdriver.Chrome(
		# #     options=options,
		# #     executable_path=self.input_dir,
		# # )
		# _driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
		# _driver.set_page_load_timeout(200)


		# chrome_options = webdriver.ChromeOptions()
		# chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
		# chrome_options.add_argument("--headless")
		# chrome_options.add_argument("--disable-dev-shm-usage")
		# chrome_options.add_argument("--no-sandbox")

		# proxy = {'address': 'smartproxy.com:1000',     'username': 'sp87694f0c',     'password': '824Qyb7m!!' }
		# capabilities = dict(DesiredCapabilities.CHROME)
		# capabilities['proxy'] = {'proxyType': 'MANUAL',
		#                  'httpProxy': proxy['address'],
		#                  'ftpProxy': proxy['address'],
		#                  'sslProxy': proxy['address'],
		#                  'noProxy': '',
		#                  'class': "org.openqa.selenium.Proxy",
		#                  'autodetect': False,
		#                  'socksUsername': proxy['username'],
		#                  'socksPassword': proxy['password']}
		# chrome_options.add_extension("./extension_2_0_0_0.crx")
		# _driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), desired_capabilities=capabilities, chrome_options=chrome_options)

		# _driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
		# _driver.set_page_load_timeout(500)

		# options = webdriver.ChromeOptions()
		# options.add_argument("--headless")
		# options.add_argument("--disable-gpu")
		# options.add_argument("--no-sandbox")
		# options.add_argument("enable-automation")
		# options.add_argument("--disable-infobars")
		# options.add_argument("--disable-dev-shm-usage")
		# _driver = webdriver.Chrome(executable_path = self.input_dir, options=options)

		_driver = webdriver.Chrome(ChromeDriverManager().install())


		return _driver


# In[28]:


if __name__ == '__main__':
	app = Soccer24()
	app.run()
	#goodslist = json.dumps(app.run())


# In[ ]:




