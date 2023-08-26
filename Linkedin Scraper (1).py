from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import re
import pandas as pd
import random

# Create an instance of the Chrome web driver
driver = webdriver.Chrome()

# Navigate to a website
driver.get("https://www.linkedin.com/login")
# User Credentials
user_name = ''
password1 = ''

# Find the username and password fields and enter the login credentials
user = driver.find_element("id", "username")
user.send_keys(user_name)
password = driver.find_element("id", "password")
password.send_keys(password1)
# Click on the login button
log_in_button = driver.find_element("class name", "login__form_action_container")
log_in_button.click()

def find_name_location_description(driver=driver):
    try:
        name = driver.find_element(
            By.XPATH, "//h1[@class='text-heading-xlarge inline t-24 v-align-middle break-words']")
        location = driver.find_element(
            By.XPATH, "//span[@class='text-body-small inline t-black--light break-words']")
        description = driver.find_element(
            By.XPATH, "//div[@class='text-body-medium break-words']")
        return name.text, location.text, description.text
    except:
        return "No name, location or description found"

# find the current company through xpath using function and try and except


def find_current_company(driver=driver):
    try:
        company = []
        jobs = driver.find_element(
            By.CSS_SELECTOR, "ul.pv-text-details__right-panel")
        for job in jobs.find_elements(By.CSS_SELECTOR, "li"):
            company.append(job.text)
        return company
    except:
        return "No current company found"

# find the experience through xpath using function and try and except


def find_experience(driver=driver):
    try:
        experianceList = []
        experiance = driver.find_element("xpath", "//div[@id='experience']")
# get parent
        parent = experiance.find_element(By.XPATH, "..")
        li = parent.find_elements(
            By.CSS_SELECTOR, 'ul li .display-flex.flex-row.justify-space-between ')
        for i in li:
            experianceList.append(i.text.split("\n")[::2])
        return experianceList
    except:
        return "No experience found"


def find_about(driver=driver):
    try:
        about = driver.find_element("xpath", "//div[@id='about']")
        # get parent
        parent = about.find_element(By.XPATH, "..")
        span = parent.find_elements(By.TAG_NAME, "span")[2]

        return span.text
    except:
        return "No about found"
# find the education through xpath using function and try and except


def find_education(driver=driver):
    try:
        education = driver.find_element("xpath", "//div[@id='education']")
        # get parent
        parent = education.find_element(By.XPATH, "..")
        li = parent.find_elements(
            By.CSS_SELECTOR, 'ul li .display-flex.flex-row.justify-space-between ')
        educationList = []
        for i in li:
            educationList.append(i.text.split("\n")[::2])
        return educationList
    except:
        return "No education found"
# find the skills through xpath using function and try and except


def find_skills(driver=driver):
    try:
        skillList = []
        skills = driver.find_element("xpath", "//div[@id='skills']")
        # get parent
        parent = skills.find_element(By.XPATH, "..")
        li = parent.find_elements(
            By.CSS_SELECTOR, 'ul li .display-flex.flex-row.justify-space-between')
        for i in li:
            skillList.extend(i.text.split("\n")[::2])
        return skillList
    except:
        return []
# if profile has experience


def have_experience(driver=driver):
    try:
        experiance = driver.find_element("xpath", "//div[@id='experience']")
        return True
    except:
        return False

# find only university education through xpath using function and try and except


def find_university_education(driver=driver):
    try:
        educationList = []
        education = driver.find_element("xpath", "//div[@id='education']")
        parent = education.find_element(By.XPATH, "..")
        li = parent.find_elements(By.CSS_SELECTOR, 'span')
        university = li[2].text.split("\n")[::2]
        try:
            degree = li[5].text.split("\n")[::2]
            educationList.append(university[0])
            educationList.append(degree[0])
            return educationList
        except:
            try:
                university[0]!='None'
            except:
                return educationList.append(university[0])
            return []

    except:
        return []

# find the certifications through xpath using function and try and except


def find_certifications(driver=driver):
    try:
        certificationsList = []
        licenses = driver.find_element(
            "xpath", "//div[@id='licenses_and_certifications']")
# get parent
        parent = licenses.find_element(By.XPATH, "..")
        li = parent.find_elements(
            By.CSS_SELECTOR, 'ul li .display-flex.flex-row.justify-space-between')
        for i in li:
            certificationsList.extend(i.text.split("\n")[::2])
        return certificationsList
    except:
        return "No certifications found"


def separate(df, colName):
    df = df.join(pd.DataFrame(df[colName].tolist()).add_prefix(colName))
    df.drop(colName, axis=1, inplace=True)
    return df
    #get company name using function and try and except
def get_company_name(driver=driver):
    try:
        ompany_name = driver.find_element(By.CSS_SELECTOR, ".jobs-unified-top-card__company-name")
        return ompany_name.text
    except:
        return "Not found"
def get_location(driver=driver):
    try:
        location = driver.find_element(By.CSS_SELECTOR, ".jobs-unified-top-card__bullet")
        return location.text
    except:
        return "Not found"
def get_type(driver=driver):
    try:
        type = driver.find_element(By.CSS_SELECTOR, ".jobs-unified-top-card__workplace-type")
        return type.text
    except:
        return "Not found"
    
def get_description(driver=driver):
    try:
        parent= driver.find_element(By.CSS_SELECTOR, ".jobs-box--fadein")
        button=parent.find_element(By.CSS_SELECTOR, "button")
        time.sleep(2)
        #click on button
        button.click()
        description = driver.find_element(By.CSS_SELECTOR, ".jobs-description__content")
        return description.text
    except:
        return "Not found"
def get_industry(driver=driver):
    try:
        div = driver.find_element(By.CSS_SELECTOR, "div .mt5.mb2")
        ul= div.find_element(By.CSS_SELECTOR, "ul")
        company=ul.find_element(By.XPATH, "//li-icon[@type='company']")
        parent=company.find_element(By.XPATH, "../../../..")
        return parent.text.split(" · ")[1] 
    except:
        return "Not found"
    
def get_type_work(driver=driver):
    try:
        div = driver.find_element(By.CSS_SELECTOR, "div .mt5.mb2")
        ul= div.find_element(By.CSS_SELECTOR, "ul")
        company=ul.find_element(By.XPATH, "//li-icon[@type='job']")
        parent=company.find_element(By.XPATH, "../../../..")
        return parent.text.split(" · ")[0] 
    except:
        return "Not found"

def get_skills(driver=driver):
    try:
        time.sleep(3)
        button=driver.find_element(By.CSS_SELECTOR, ".mv5")
        button.click()
        time.sleep(3)
        ulSkill=driver.find_element(By.CSS_SELECTOR, "ul.job-details-skill-match-status-list")
        return ulSkill.text.split("\n")[::2]
    except:
        return []    

def get_jobTitle(driver=driver):
    try:
        jobTitle=driver.find_element(By.CSS_SELECTOR, "h1")
        return jobTitle.text
    except:
        return "Not found"

def extract_degree_requirement(job_description):
    pattern = r"(?i).*\b(degree)\b.*?(?=\n)"

    match = re.search(pattern, job_description)
    if match:
        degree_requirement_line = match.group()
        return degree_requirement_line.strip()
    else:
        return ' '
print("Select the Scrape")
print("1. Scrape Profiles")
print("2. Scrape jobs")
scrape = int(input("Enter your scrape \n"))

if scrape == 1:
  #choice which country to scrape
  print("Select the Country to scrape")
  print("1. India")
  print("2. USA")
  print("3. Lebanon")
  
  country=str(input("Enter your country Link \n"))

        #choice number of profiles to scrape
  print("Select the number of profiles to scrape")
  number_of_profiles=int(input("Enter the number of profiles to scrape \n"))
  profilesFile=pd.read_csv("profiles.csv")
  Links=[]
  num1 = random.randint(2, 50)
  num2 = random.randint(2, 50)
  minn=min(num1,num2)
  maxn=max(num1,num2)
  print(minn,maxn)
  for page in range(2,3):
    try:
        l=country+"&start="+str(page)+""
      # Navigate to a website
        driver.get(l)
        time.sleep(3)
        ul = driver.find_element(By.XPATH, "//ul[@class='reusable-search__entity-result-list list-style-none']")
        li=ul.find_elements(By.TAG_NAME,"li")
        for i in li:
          link=i.find_element(By.TAG_NAME,"a")
          Links.append(link.get_attribute("href"))
    except:
      continue
  info=[]
  counter = len(info)+1
  for i in range(0, number_of_profiles):
      driver.get(Links[i])
      time.sleep(2)
      name, location, description = find_name_location_description()
      about=find_about()
      have_exp=have_experience()
      university=find_university_education()
      skillsList = find_skills()
      print(counter)
      counter += 1
      print("-------------------")
      info.append({"name": name, "location": location, "description": description,"about":about,
                  "experiance": have_exp, "university": university, "skills": skillsList})
  df=pd.DataFrame(info)



  skills_seprate= separate(df,'skills')
  education_seprate= separate(skills_seprate,'university')      
  education_seprate[['degree', 'magor']] = education_seprate['university1'].str.split(',',1, expand=True)
  education_seprate.drop('university1', axis=1, inplace=True)
  
  education_seprate.loc[education_seprate['description'].str.contains('Data Analyst '), 'description'] = 'Data Analyst'
  education_seprate.loc[education_seprate['description'].str.contains('Data Engineer '), 'description'] = 'Data Engineer'
  education_seprate.loc[education_seprate['description'].str.contains('Data Scientist '), 'description'] = 'Data Scientist'
  education_seprate.loc[education_seprate['description'].str.contains('Software'), 'description'] = 'Software Engineer'
  education_seprate.loc[education_seprate['location'].str.contains('Lebanon'), 'location'] = 'Lebanon'

  pd.concat([profilesFile, education_seprate], axis=0).to_csv('profiles.csv', index=False)
elif scrape == 2:
    #choice which country to scrape
  print("Enter The Linke Country to scrape")

  
  country=str(input("Enter your country Link \n"))

      #choice number of profiles to scrape
  print("Select the number of Jobs to scrape")
  number_of_jobs=int(input("Enter the number of jobs to scrape \n"))
  
  jobFile=pd.read_csv("jobs.csv")
  #get all the job links
  link=[]
  for i in range(1,14,7):
      l=country+"&start="+str(i)+""  
      driver.get(l)
      # get ul 
      time.sleep(5)
      #scroll down in right side to get all the jobs
      driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

      ul = driver.find_element(By.CSS_SELECTOR, ".scaffold-layout__list-container")

      a= ul.find_elements(By.CSS_SELECTOR, "a")
      for i in a:
          link.append(i.get_attribute("href"))
  info=[]
  counter = len(info)+1
  for i in range(0, number_of_jobs):
      driver.get(link[i])
      time.sleep(2)
      jobTitle=get_jobTitle()
      company_name = get_company_name()
      location = get_location()
      type = get_type()
      description = get_description()
      degree=extract_degree_requirement(description)
      industry = get_industry()
      type_work = get_type_work()
      skills = get_skills()
      print(counter)
      print("skills: ", skills)
      counter += 1
      print("-------------------")
      info.append({"company_name": company_name, "jobTitle":jobTitle, "location": location, "type": type,
                  "degree": degree, "industry": industry, "type_work": type_work, "skills": skills})
  df=pd.DataFrame(info)
  df['jobTitle'] = df['jobTitle'].str.split().str[:3].str.join(' ')

  df.loc[df['degree'].str.contains('Computer'), "degree"] = 'degree in Computer Science'
  df.loc[df['degree'].str.contains('Engineering'), 'degree'] = 'degree in Engineering'
  df.loc[df['degree'].str.contains('Information Technology'), 'degree'] = 'degree in Information Technology'
  df.loc[df['degree'].str.contains('language'), 'degree'] = 'degree in language'
  df.loc[df['degree'].str.contains('Business'), 'degree'] = 'degree in Business'
  df.loc[df['degree'].str.contains('Arts'), 'degree'] = 'degree in Arts'
  df.loc[df['degree'].str.contains('Math'), 'degree'] = 'degree in Math'
  df.loc[df['degree'].str.contains('Statistics'), 'degree'] = 'degree in Statistics'
  df.loc[df['degree'].str.contains('Economics'), 'degree'] = 'degree in Economics'
  df.loc[df['degree'].str.contains('Finance'), 'degree'] = 'degree in Finance'
  df.loc[df['degree'].str.contains('Accounting'), 'degree'] = 'degree in Accounting'
  df.loc[df['degree'].str.contains('Marketing'), 'degree'] = 'degree in Marketing'
  df.loc[df['degree'].str.contains('Management'), 'degree'] = 'degree in Management'
  df.loc[df['degree'].str.contains('Science'), 'degree'] = 'degree in Computer Science'
  df.loc[df['location'].str.contains('Lebanon'), 'location'] = 'Lebanon'

                            
  def separate(df,colName):
    df = df.join(pd.DataFrame(df[colName].tolist()).add_prefix(colName))
    df.drop(colName, axis=1, inplace=True)
    return df

  skills_seprate= separate(df,'skills')
  #update jobs csv file by skills_seprate
  pd.concat([jobFile, skills_seprate], axis=0).to_csv('jobs.csv', index=False)
  #convert data in degree coulmns appreviation to full name
    
