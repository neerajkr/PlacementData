from mechanize import Browser
import cookielib
import csv
import sys


count=0
file = open('PlacementData.csv', 'w')
try:
    writer = csv.writer(file)
    writer.writerow( ('NameOfTheCompany', 'NatureOfBusiness', 'JobDesignation','Eligibility', 'CTC') )

    with open('Comapnies_links.csv', 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            print count
            count=count+1
            if count==5:
                break
            try:
                link=row[0]

                br = Browser()
                br.set_cookiejar(cookielib.LWPCookieJar())

                # Browser options
                br.set_handle_equiv(True)
                br.set_handle_redirect(True)
                br.set_handle_referer(True)

                br.open(link)

                # You need to spot the name of the form in source code
                br.select_form(nr=0)  

                # Spot the name of the inputs of the form that you want to fill, 
                # say "username" and "password"
                br.form["userlogin_session[login]"] = ""
                br.form["userlogin_session[password]"] = ""

                response = br.submit()
                myhtml=response.read()

                # print html

                #For downlaoding the html pages
                # filename=row[1]
                # Html_file= open(filename,"w")
                # Html_file.write(myhtml)
                # Html_file.close()

                from bs4 import BeautifulSoup
                soup = BeautifulSoup(myhtml,"lxml")

                td_list = soup.find_all('td')


                i = 0
                for elem in td_list:
                    if elem.text == 'Name of the Company':
                        ind = i
                    i += 1


                NameOfTheCompany= td_list[ind+2].text
                NatureOfBusiness=td_list[ind+5].text
                JobDesignation= td_list[ind+8].text

                i = 0
                for elem in td_list:
                    if elem.text == 'Eligibility':
                        ind = i
                    i += 1



                # Eligibility=(td_list[ind+2].contents[0])+(td_list[ind+2].contents[1])+(td_list[ind+2].contents[2])
                Eligibility=td_list[ind+2].text


                i = 0
                for elem in td_list:
                    if elem.text == 'Total cost to Company':
                        ind = i
                    i += 1

                CTC=td_list[ind+7].text

                writer.writerow( (NameOfTheCompany, NatureOfBusiness, JobDesignation,Eligibility,CTC) )

            
            
            except :
                pass


        
finally:
    file.close()
