from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
from fpdf import FPDF
from flask import Flask, render_template, request,jsonify
import pymongo
import requests
import logging
logging.basicConfig(filename="scrapper.log" ,format='%(asctime)s - %(message)s', level=logging.INFO)

app=Flask(__name__)

class Scrapper:
    def make_conection_to_mongo_db(self,data):
        try:
            client = pymongo.MongoClient("mongodb+srv://kiran:abcdef_kiran@cluster0.zmkp9hd.mongodb.net/?retryWrites=true&w=majority")
                
            db = client['eccommerce']
                    
            review_col = db['all']
        except Exception as e:
            logging.info(e)


        #data={"name":"Prakash","email":"gautamprakash@gmail.com","class":99}
        #data1={"name":"bitti","address":"betul","class":"first"}
        # review_col.insert_one(data)
        # review_col.insert_one(data1)
        #one=review_col.find_one()
        #monodata(one)
        #return all_table
        logging.info('selenium work')
 


    #this function is for saving course info into pdf 
    def save_to_pdf(self,dic_of_info):
        pdf = FPDF()

     # Add a page
        pdf.add_page()

    # set style and size of font
    # that you want in the pdf
        pdf.set_font("Arial", size=15)

    # create a cell
        pdf.cell(200, 10, txt="GeeksforGeeks", ln=1, align='C')

    # loop over the dictionary and add each key-value pair to the PDF
        ln = 2
        for key, value in dic_of_info.items():
            pdf.cell(200, 10, txt=key, ln=ln, align='C')
            ln += 1
            for v in value:
                pdf.cell(200, 10, txt=v, ln=ln, align='C')
                ln += 1

    # save the pdf with name .pdf
        pdf.output("k1.pdf")


#find element course tab and click on it then after course page display extract each course link and store it to list we are going to study
    def Course_link_from_corse_page(self):
        all_matches = driver.find_element("xpath", "//a[@href='/courses?source=navbar']")
        all_matches.click()
        time.sleep(5)

    #find the element of course then click on that
        matches = []
    #after the course page get comon xpath of all courses and store it in list ,iterate the xpath and get one xpath from list and get text and link in match list 
        xpath_list = ["//div[@class='Course_right-area__JqFFV']//a",]
        for xpath in xpath_list:
            elements = driver.find_elements("xpath",xpath)
            for element in elements:
                text = element.text
                href = element.get_attribute('href')
                print(f"Text: {text} - Href: {href}")
                matches.append(href)
                print("---------------------------------")
        print(matches)
        return matches

#extratting course detail
    def Store_all_link_in_dic(self,matches):
        do=[]

    # here get each link from matches then click i
        for link in matches:

        # Click the link to open it in the current tab
            driver.get(link)
            time.sleep(3)

        # Use the ActionChains class to open the link in a new tab
            ActionChains(driver).key_down(Keys.CONTROL).click().key_up(Keys.CONTROL).perform()
            time.sleep(10)

        #xpath of course name ,description under course name and list what we going to learn
            Course_NAme = driver.find_element("xpath", "//h3[@class='Hero_course-title__4JX81']")
            print(Course_NAme .text)
            description = driver.find_element("xpath", "//div[@class='Hero_course-desc__lcACM']")
            print(description.text)
            learn = driver.find_element("xpath", '//div[@class="CourseLearning_card__0SWov card"]//h4')
            print(learn.text)

        #list what we going to learn text and list content append to list
            elements = driver.find_elements("xpath", '//div[@class="CourseLearning_card__0SWov card"]//ul//li')
            for i in elements:
                print(i.text)
                do.append(i.text)

            Make_set=set(do) 
            make_list=list(Make_set) 

        #add to dic heading and all topic list
            dic_of_info = {Course_NAme.text : make_list}
            print(dic_of_info)   
        

        #call function to pdf
            self.save_to_pdf(dic_of_info)  
            self.make_conection_to_mongo_db(dic_of_info) 

            driver.switch_to.window(driver.window_handles[-1])
            do=[]
            time.sleep(5)
my_instance = Scrapper()
#my_instance.func1()
#define the path and excute 
logging.info('start')
website = 'https://ineuron.ai/'
path = 'chromedriver'

driver = webdriver.Chrome(path)
driver.maximize_window()
driver.get(website)
time.sleep(5)

key=[]
mongo_key_list1=[]
mongo_value_list1=[]
#table=make_conection_to_mongo_db()
@app.route("/",methods=['GET'])
def HomePage():
    
    # Connect to MongoDB and retrieve the data
    try:
        client = pymongo.MongoClient("mongodb+srv://kiran:abcdef_kiran@cluster0.zmkp9hd.mongodb.net/?retryWrites=true&w=majority")
        db = client['eccommerce']
        collection = db['all']
    except Exception as e:
          logging.info(e)    
    Data = collection.find()
    for data in Data:
        if data.keys() !='_id':
            mongo_key=data.keys()
            mongo_key_list=list(mongo_key)
            mongo_key_list1.append(mongo_key_list[1])

            mongo_value=data.values()
            mongo_value_list2=list(mongo_value)
            mongo_value_list1.append(mongo_value_list2[1])
            

    # Pass the data to the template for rendering
    return render_template('index.html',mongo_key_list1=mongo_key_list1,mongo_value_list1=mongo_value_list1)
    
#call function   
try:  
    matches=my_instance.Course_link_from_corse_page()    

    my_instance.Store_all_link_in_dic(matches)
except Exception as e:
                    logging.info(e)    

driver.quit()

if __name__ == "__main__":
     app.run(host="0.0.0.0") 