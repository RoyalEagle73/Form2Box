import requests
from bs4 import BeautifulSoup
import re
import configparser as cfg

# Taking out data from config file
parser = cfg.ConfigParser()														# Creating Object for parsing the config file
parser.read('config.cfg')														# Reading the config file
api_token = parser.get('creds', 'api_token')									# Reading Api Token from config file		
sms = parser.get('creds', 'sms')												# Reading the custom Sms saved in config file
wallet_url = parser.get('creds', 'wallet')										# Reading API URL for your Way2Sms wallet
your_number = parser.get('creds', 'your_number')								# Reading emergency contact number
spreadsheet = parser.get('creds', 'spreadsheet_url')							# Reading Link to your spreadsheet file
index = parser.get('creds', 'phone_index')										# Reading index of mobile number in main form
last_size =	int(parser.get('creds', 'last_size'))								# Reading last size of the list 

temp_list = []																	# Taking a temporary list to save garbage data 

## FUNCTION TO UPDATE LAST SIZE IN CONFIG FILE
def addLastIndex():
	global last_size
	temp = ""
	with open("config.cfg", 'r') as file:
		temp = file.read()
		index  = temp.find("last_size = ")
		temp = temp[:index]
		temp += "last_size = " + str(last_size)
	with open("config.cfg", 'w') as file:
		file.write(temp)



## FUNCTION TO SEND MESSAGE TO RETRIEVED NUMBER
def sendSms(message, number):
	url = "https://www.fast2sms.com/dev/bulk"
	payload = "sender_id=FSTSMS&message=%s&language=english&route=p&numbers=%s"%(message, number)
	headers = {'authorization': "%s"%(api_token),'Content-Type': "application/x-www-form-urlencoded",'Cache-Control': "no-cache",}
	response = requests.request("POST", url, data=payload, headers=headers)
	return response.json().get('return')

## FUNCTION TO CHECK BALANCE SO THAT API CAN INFORM OWNER IN CASE OF LOW BALANCE
def checkBalance():															
	global your_number
	global wallet_url
	global api_token
	headers = {
    'authorization': "%s"%(api_token),
    }
	response = requests.request("POST", wallet_url, headers=headers)
	if float(response.json().get('wallet')) in [5.0, 4.0, 3.0, 2.0, 1.6, 1.2, 1.0]:
		k = sendSms("Your wallet balance is low and soon people would be waiting for your response, Kindly recharge . Regards Way2Sms.", your_number)
		if k == True:
			print("Low Balance Error generted, SMS sent")
		else:
			print("Low Balance Detected but failed to generate SMS")

## TAKING DATA FROM THE SPREADSHEET 
def getData():
	global spreadsheet
	global index
	global temp_list
	# Getting data
	r = requests.get(spreadsheet)													# Loading URL
	soup = BeautifulSoup(r.content, 'html.parser')									# TAKING OUT HTML CONTENT OUT OF IT
	found = soup.find('meta', property="og:description")							# FINDING THE BLOCK CONTAINIG THE INFORMATION


	# Processing data
	garbage_data = str(found)
	try:
		final_list = garbage_data.split("\"")
		final_list = final_list[1].split("\n")
		final_list = final_list[3:]
		final_list = [i.split(",") for i in final_list]
		final_list = [i[index] for i in final_list]
		return final_list
	except Exception as e:
		final_list = [re.findall('\d{10}', str(i)) for i in final_list]
		for i in final_list:
			for j in i:
				if not j in temp_list:
					temp_list.append(j)
		return temp_list


## MAIN FUNCTION WORKING HERE
while True:
	print("Checking for new data....")									# TO KEEP AN EYE ON PROGRAM INDICATING IT'S WORKING STATE
	temp_list = getData()
	if len(temp_list) > last_size:
		for i in range(0, (len(temp_list)-last_size)):
			garbage = sendSms(sms, temp_list[last_size+i])
			checkBalance()
			if garbage == True:
				print("*** SUCCESS *** Sms sent at ", temp_list[last_size+i])
			else:
				print("!!! ERROR !!! Sms failed to send")
		last_size = len(temp_list)
		addLastIndex()
