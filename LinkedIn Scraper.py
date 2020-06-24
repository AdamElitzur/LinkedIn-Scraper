from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from csv import DictReader, DictWriter
import time

with open("names.csv", 'r', encoding='utf8', errors='ignore') as file:
    csv_reader = DictReader(file)
    driver = webdriver.Chrome()
    driver.get("https://www.linkedin.com/uas/login?session_redirect=https%3A%2F%2Fwww%2Elinkedin%2Ecom%2Ffeed%2F&fromSignIn=true&trk=cold_join_sign_in")

    email = 'email@gmail.com'
    password = 'password12'
    login = driver.find_element_by_xpath('//*[@id="username"]').send_keys(email)
    password = driver.find_element_by_xpath('//*[@id="password"]').send_keys(password)
    signin = driver.find_element_by_xpath('//*[@id="app__container"]/main/div[2]/form/div[3]/button').click()
    time.sleep(4)

    for row in csv_reader:
        searchBox = driver.find_element_by_xpath('//*[@id="ember41"]/input')
        searchBox.clear()
        searchBox.send_keys(row['Name'])
        searchBox.send_keys(Keys.RETURN)
        time.sleep(5)

        listNames = []
        listBios = []
        names = driver.find_elements_by_class_name('name.actor-name')
        bios = driver.find_elements_by_class_name("subline-level-1.t-14.t-black.t-normal.search-result__truncate")
        locations = driver.find_elements_by_class_name('subline-level-2.t-12.t-black--light.t-normal.search-result__truncate')
        indexes = []

        for n in names:
            count = 0
            if row['Name'].upper() in n.text.upper():
                indexes.append(names.index(n, count))
            count +=1

        for name in names:
            if names.index(name) in indexes:
                listNames.append(name.text)

        for bio in bios:
            if bios.index(bio) in indexes:
                listBios.append(bio.text)

        iterBios = iter(listBios)
        with open("info.csv", "a", newline = '', encoding='utf8', errors='ignore') as wfile:
            headers = ["Name", "1", "2", "3", "4", "5"]
            csv_writer = DictWriter(wfile, fieldnames = headers)
            if listNames:
                csv_writer.writerow({
                    "Name": listNames[0],
                    '1': next(iterBios, ''),
                    '2': next(iterBios, ''),
                    '3': next(iterBios, ''),
                    '4': next(iterBios, ''),
                    '5': next(iterBios, '')
                })
            else:
                csv_writer.writerow({
                    "Name": "N/A"
                })