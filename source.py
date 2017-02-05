#!/usr/bin/env python
import urllib
import string
import json
import subprocess
import os
import csv
from bs4 import BeautifulSoup
from time import sleep
from requests import session 

#after login : http://placement.iitk.ac.in/pas/student
#before login : http://placement.iitk.ac.in/pas/login
#in source action: /pas/userlogin_sessions

url = 'http://placement.iitk.ac.in/pas/login'

with session() as c:
	html = c.get(url)
	soup = BeautifulSoup(html.content)
	csrftoken  = soup.find("input")['value']
	print(csrftoken)
	
	payload = {
	'action' : 'login',
	'authenticity_token': csrftoken,
	'userlogin_session[login]': '<username>',
	'userlogin_session[password]': '<password>'
	}
		
	c.post('http://placement.iitk.ac.in/pas/userlogin_sessions', data = payload, headers= {"Referer": "http://placement.iitk.ac.in"})
	page = c.get('http://placement.iitk.ac.in/pas/')
	page = c.get('http://placement.iitk.ac.in/pas/student')
	page = c.get('http://placement.iitk.ac.in/student/company_profiles')
#	print page.content

	soup = BeautifulSoup(page.content)
	companies = soup.find_all("a")
	print(len(companies))
	k = 0;

	file_total = open('PlacementData.csv','w')
	writer = csv.writer(file_total)
	writer.writerow(('NameOfTheCompany', 'NatureOfBusiness', 'JobDesignation','Eligibility', 'CTC'))

	for company in companies:
		print(k)
		k = k+1
		if k>10:
			com_name = company.string	
			com_link = 'http://placement.iitk.ac.in' + company['href']
			print(com_link)
			page = c.get(com_link)

			if not os.path.exists(os.path.dirname('Companies/'+ com_name + '.html')):
   				os.makedirs(os.path.dirname('Companies/'+ com_name + '.html' ))
			file = open('Companies/'+ com_name + '.html', 'w')
			file.write(page.content)
			file.close()

			soup_page = BeautifulSoup(page.content,"lxml")
			td_list = soup_page.find_all('td')
			i = 0
			for elem in td_list:
				if elem.text == 'Name of the Company':
					ind = i
					#break
				i += 1

			NameOfTheCompany= td_list[ind+2].text
			NatureOfBusiness=td_list[ind+5].text
			JobDesignation= td_list[ind+8].text
      
			i = 0
			for elem in td_list:
				if elem.text == 'Eligibility':
					ind = i
					#break
				i += 1

			# Eligibility=(td_list[ind+2].contents[0])+(td_list[ind+2].contents[1])+(td_list[ind+2].contents[2])
			Eligibility=td_list[ind+2].text

			i = 0
			for elem in td_list:
				if elem.text == 'Total cost to Company':
					ind = i
					#break
			i += 1

			CTC = td_list[ind+7].text
			try:
				writer.writerow((NameOfTheCompany, NatureOfBusiness, JobDesignation, Eligibility, CTC))
			except:
				pass

file_total.close()

