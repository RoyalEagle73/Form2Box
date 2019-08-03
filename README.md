# ***************** Form2Box ***************** 
### A Simple Auto-Responder Script which send message to users who fill in your google form via SMS using Fast2Sms service.
### Fast2SMS is a paid service so you'll have to add balance to wallet periodically, where Fast2Sms charges 20p/sms.

## FEATURES :
  1) Message is sent instantly.
  2) Message service is available between 9 AM to 9 PM, where all queries after 9 PM will be fulfilled next day in morning.
  3) A warning message for low balance is sent to form administrator at some checkpoint to remind for refilling in Fast2Sms service.
  4) Interactive console informs you for each step taken by script.
  5) You can deploy script for one time on deployment service of yours and all it needs is to refill the Fast2Sms wallet later.

## REQUIREMENTS :
  1) Python3
  2) Regex
  3) BeautifulSoup
  4) Requests
  5) ConfigParser

## HOW TO USE :
  1) Clone/Download the repository.
  2) Collect the below mentioned data and place it in it's right place in 'CONFIG.cfg' file and save the file.
  3) Run following command in terminal/command prompt.
      `python3 main.py`

## Data needed :
### 1) GOOGLE FORM SPREADSHEET URL
     Follow the following tutorial to collect Spreadsheet Url.

![](https://user-images.githubusercontent.com/34307370/62410481-b15f8700-b5d5-11e9-911e-5c774134fc0a.gif)

### 2) API TOKEN 
  A) Sign Up / Login on [Fast2Sms](www.fast2sms.com).
  
  B) Find the [DEV-API](https://www.fast2sms.com/dashboard/dev-api) dashboard and copy the API Key into config.cfg file.
  
### 3) PHONE INDEX
  Find the serial number at which phone number is asked from user. Let's Say your form asks data in following way :
      Name
      Address
      Phone Number
      Email-ID
      etc.
  Hence Phone Index of your form is 3.
