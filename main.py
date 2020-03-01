from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from pathlib import Path
import requests
import os
from selenium.common.exceptions import NoSuchElementException
import xlwt
import httplib2
import time

BASE_URL = 'https://www.avito.ru/sankt-peterburg/akvarium'
#driver = webdriver.Chrome('D:\\Python\\driver\\chromedriver.exe')
driver = webdriver.Chrome()

#create new workbook
MAIN_WORKBOOK = xlwt.Workbook()

#create new page(sheet)
MAIN_SHEET = MAIN_WORKBOOK.add_sheet('New sheet')
#.write(row, column, data)
MAIN_SHEET.write(0, 0, 'Link_on_image')
MAIN_SHEET.write(0, 1, 'Name')
MAIN_SHEET.write(0, 2, 'Price')

BASE_SAVE_PATH = Path('./pars')
if not os.path.exists(BASE_SAVE_PATH):
	os.makedirs(BASE_SAVE_PATH)

FOR_IMAGE_PRODUCT = Path('./pars/image')
if not os.path.exists(FOR_IMAGE_PRODUCT):
	os.makedirs(FOR_IMAGE_PRODUCT)

driver.get(BASE_URL)

#for name
number = 0

count_page = 1

#for __ xls
count_rows = 1

while True:

	#try find buttom
	if count_page != 1:
		try:
			time.sleep(3)
			next_page = driver.find_element_by_class_name("pagination-item-1WyVp.pagination-item_arrow-Sd9ID").find_element_by_xpath('//span[@data-marker="pagination-button/next"]')
			ActionChains(driver).move_to_element(next_page).click().perform()
		except NoSuchElementException:
			break
			
	print('page number: __________________________' + str(count_page))

	count_page += 1

	class_img = driver.find_elements_by_class_name('snippet-horizontal.item.item_table.clearfix.js-catalog-item-enum.item-with-contact.js-item-extended')
			
	#parsing image
	for id_img in class_img:
		number += 1
			
		http = httplib2.Http('.cache')
		response, content = http.request(id_img.find_element_by_class_name('large-picture-img').get_attribute('src'))

		#print in console for me
		name = id_img.find_element_by_class_name('snippet-link')
		price = id_img.find_element_by_class_name('price')
		print(name.text)
		print(price.text)

		full_name_product = str(number)
		link_on_one_product_image = full_name_product + '.jpg'

		#write a data
		MAIN_SHEET.write(count_rows, 0, full_name_product)#.write(row, column, data)
		MAIN_SHEET.write(count_rows, 1, name.text)
		MAIN_SHEET.write(count_rows, 2, price.text)

		MAIN_WORKBOOK.save('./pars/fish_house.xls')
					
		count_rows += 1

		#write an image
		out = open(FOR_IMAGE_PRODUCT / link_on_one_product_image, "wb")
		out.write(content)
		out.close()
		
driver.quit()

print('Download [' + str(number) + '] files')