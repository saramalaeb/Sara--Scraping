import time
import pandas as pd     
import selenium
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
print("PLEASE INSTALL FOLLOWING LIBRARIES")
print("pip install pandas")
print("pip install selenium")
print("pip install beautifulsoup4")
path = 'chromedriver.exe'
driver = webdriver.Chrome(path)  


driver.maximize_window() 
driver.minimize_window()  
driver.maximize_window()  
driver.switch_to.window(driver.current_window_handle)
driver.implicitly_wait(10)

driver.get('https://www.linkedin.com/login');
time.sleep(1)


# User Credentials
user_name = ''
password = ''
driver.find_element_by_xpath('//*[@id="username"]').send_keys(user_name)
driver.find_element_by_xpath('//*[@id="password"]').send_keys(password)
time.sleep(1)


driver.find_element_by_xpath('//*[@id="organic-div"]/form/div[3]/button').click()
driver.implicitly_wait(10)

print("Select the Scrape")
print("1. Scrape Country Jobs")
print("2. Scrape Country People")
choice = int(input("Enter your Choice \n"))




country_link = input("Enter the link of country you wish to scrape\n")
driver.get(country_link)
time.sleep(1)

links = []
total_pages = int(input("Enter total no. of Job pages to be Scraped: \n"))
t_page = total_pages + 1
print('Collecting links.')

for page in range(2,t_page):
    src = driver.page_source
    soup = BeautifulSoup(src, 'lxml')
    time.sleep(2)
    jobs_block = driver.find_element_by_class_name('jobs-search-results-list')
    jobs_list= jobs_block.find_elements(By.CSS_SELECTOR, '.jobs-search-results-list-item')
        
    for link in soup.findAll('a'):
        #print(link.get('href'))
        links.append(link.get('href'))
    for job in jobs_list:    
        driver.execute_script("arguments[0].scrollIntoView();", job)
        
    print(f'Collecting the links in the page: {page-1}')
        
    driver.find_element_by_xpath(f"//button[@aria-label='Page {page}']").click()
    time.sleep(1)



links1 = []
for j in range(len(links)):
    if links[j].startswith("/jobs/view"):
        links1.append(links[j])
#print(links1)
#print('Found ' + str(len(links1)) + ' links for job offers')
links2 = ['https://www.linkedin.com'+ item for item in links1]

job_titles = []
company_names = []
company_locations = []
work_methods = []
post_dates = []
work_times = [] 
job_desc = []

i = 0
j = 1

print('Visiting the links and scrapping data')
for i in range(len(links2)):
    try:
        driver.get(links2[i])
        i=i+1
        time.sleep(2)
    except:
        pass

    contents = driver.find_elements_by_class_name('p5')
    for content in contents:
            try:
                job_titles.append(content.find_element_by_tag_name("h1").text)
            except:
                job_titles.append("NA")
            try:
                company_names.append(content.find_element_by_class_name("jobs-unified-top-card__company-name").text)
            except:
                company_names.append("NA")
            try:
                company_locations.append(content.find_element_by_class_name("jobs-unified-top-card__bullet").text)
            except:
                company_locations.append("NA")
            try:
                work_methods.append(content.find_element_by_class_name("jobs-unified-top-card__workplace-type").text)
            except:
                work_methods.append("NA")
            try:
                post_dates.append(content.find_element_by_class_name("jobs-unified-top-card__posted-date").text)
            except:
                post_dates.append("NA")
            try:
                work_times.append(content.find_element_by_class_name("jobs-unified-top-card__job-insight").text)
            except:
                work_times.append("NA")
            print(f'Scraping the Job {j} DONE.')
            j+= 1
            time.sleep(1)
        
    # Scraping the job description
    job_description = driver.find_elements_by_class_name('jobs-description__content')
    for description in job_description:
        job_desc.append(description.find_element_by_class_name("jobs-box__html-content").text)
        time.sleep(1)  


job1_desc = []
for sub in job_desc:
    job1_desc.append(re.sub('\n', '', sub))

# Creating the dataframe 
df = pd.DataFrame(list(zip(job_titles,company_names,
                    company_locations,work_methods,
                    post_dates,work_times,job1_desc)),
                    columns =['job_title', 'company_name',
                           'company_location','work_method',
                           'post_date','work_time','job_decription'])

df.to_csv('data.csv', index=False)

df = pd.read_csv('data.csv')

df['work_method'] = df['work_method'].astype(str)

df['work_time'] = df['work_time'].astype(str)


df.to_csv('data_final.csv', index=False)
