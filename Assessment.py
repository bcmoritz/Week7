import requests
from bs4 import BeautifulSoup
import json
from dataclasses import dataclass, field
import datetime
import sys
from datetime import date

url = "https://api.tomorrow.io/v4/timelines"

querystring = {
"location":"43, 87",
"fields":["temperature", "cloudCover"],
"units":"imperial",
"timesteps":"1d",
"apikey":"xYyT5Ke7qRr3XOn9l7bBItUyprXFJxdq"}

response = requests.request("GET", url, params=querystring)
response

with open('holidays.json', 'w', encoding = "utf-8") as file:
    file.write('{\n}')
@dataclass
class Holiday:
    date : date
    name : str
    '''Holiday Class'''
    def print():
        return(self._date , self._name)
    def jsonprint(spaghetti_fn):
        def inner_fn(*args):
            HolidayTemp = spaghetti_fn(*args)
            HolidayJSON = json.dumps(HolidayTemp, indent=4, sort_keys=True, default=str)
            with open('holidays.json', 'a', encoding = "utf-8") as file:
                file.write(str(HolidayJSON) + '\n')
            print(HolidayJSON)
            return HolidayJSON
        return inner_fn   
    @jsonprint
    def getDetails(self):
        return [{'date': self.date, 'name': self.name}]
    def __gt__(self, other):
        if self.date > other.date:
            return self.date > other.date
        else:
            return False
    def __eq__(self, other):
        if self.date == other.date:
            return self.unit == other.date
        else:
            return False
    def __ge__(self, other):
        if self.date == other.date:
            return self.date >= other.amount
        else:
            return False
    def getHTML(url):
        response = requests.get(url)
        return response.text



url = 'https://www.timeanddate.com/holidays/us/'


Holidaydict = []
Holidayobjects = []
with open('holidays.json', newline = '') as jsonfile:
    reader = json.load(jsonfile)
    for row in reader:
        Holidaydict.append(row)

for item in Holidaydict:
    Holidayobjects.append(Holiday(item[0], item[1]))

HolidayList = []
for i in range(0, 5):
    html = getHTML('https://www.timeanddate.com/holidays/us/202' + str(i))
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table',attrs = {'id':'holidays-table'}, )


    for row in table.find_all_next('tr')[1:]:
        if row is not None:
            if (row.find_next('th') is None) or (row.find_next('a') is None):
                break
            else:
                tempYear = ('202' + str(i))
                tempMonth, tempDay = row.find_next('th').get_text().split(' ')
                tempMonth = datetime.datetime.strptime(tempMonth, '%b')
                tempMonth = tempMonth.month
                HolidayList.append(Holiday(date(int(tempYear), int(tempMonth), int(tempDay)), row.find_next('a').get_text()))
                # HolidayList.append(Holiday(('202' + str(i) + ' ' + row.find_next('th').get_text()) , row.find_next('a').get_text()))
                
runTime = 0
while runTime is not None:

    runTimeValid = True
    if (runTimeValid):
        print('\n===========\nHoliday Menu\n\n===========\n\n1. Add a Holiday\n2. Remove a Holiday\n3. Save Holidays List\n4. View Holidays\n5. Exit\n\n')   
        runTime = input()
    try:
        int(runTime)
    except ValueError:
        runTimeValid = False
    if(runTimeValid):
        runTime = int(runTime)

    while runTime == 1:
    
        inputName = input('Enter Holiday Name: ')
        inputDate = input('Enter Holiday Date mm/dd/yyyy: ')
        ValidSplit = True
        ValidDate = True
        month, day, year = 0, 0, 0
        try:
            month, day, year = inputDate.split('/')
        except ValueError:
            ValidSplit = False
        if(ValidSplit):
            month, day, year = inputDate.split('/')
            try:
                date(int(year), int(month), int(day))
            except ValueError:
                ValidDate = False
        
        if(ValidDate and ValidSplit):
            ##HolidayDate = datetime.datetime(int(year), int(month), int(day))
            DateTemp = date(int(year), int(month), int(day))
            HolidayAdd = Holiday(DateTemp, inputName)
            HolidayList.append(HolidayAdd)
        else:
            print('Invalid date please try again.')

        inputName = ''
        inputDate = ''
        runTime = 0
        ##addholiday
    while runTime == 2:
        ##RemoveHoliday
        updatedList = []
        holidayToRemove = input('What is the name of the holiday you would like to remove: ')
        for item in HolidayList:
            if (item not in updatedList) and (item.name != holidayToRemove):
                updatedList.append(item)
        print('You have removed' , (len(HolidayList) - len(updatedList)) ,  'item(s) from the list')
        HolidayList = updatedList
        runTime = 0
            
    while runTime == 3:
        noDuplicates = []
        for item in HolidayList:
            if item not in noDuplicates:
                noDuplicates.append(item)
        for item in noDuplicates:
            item.getDetails()
        ##SaveList
        print('Current List Saved to JSon')
        runTime = 0
    
    while runTime == 4:
        ##ViewList
        inputYear = input('Please input Year you would like to see: ')
        inputWeek = input('Please enter which week you would like 1-52: ')
        printWeather = True
        tempPrint = input('Would you like to know the weather(Y/N): ')
        if tempPrint.upper() == 'N':
            printWeather = False
        
        YearValid = True
        WeekValid = True
        try:
            int(inputYear)
        except ValueError:
            YearValid = False
        if YearValid:
            if (int(inputYear) < 10000) and (int(inputYear) > 0):
                inputYear = int(inputYear)
            else:
                YearValid = False
        try:
            int(inputWeek)
        except ValueError:
            WeekValid = False
        if WeekValid:
            if (int(inputWeek) > 0) and (int(inputWeek) < 53):
                inputWeek = int(inputWeek)
            else:
                WeekValid = False
        if WeekValid and YearValid:
            for i in range(0, len(HolidayList)):
                inWeek = (lambda x, y, z: x.year == y and x.isocalendar().week == z)(HolidayList[i].date, inputYear, inputWeek)
                if inWeek == True:
                    print(HolidayList[i].name , HolidayList[i].date )
            if printWeather:
                results = response.json()['data']['timelines'][0]['intervals']
                numTemp = 0
                for item in results:
                    date = item['startTime'][0:10]
                    temp = round(item['values']['temperature'])
                    print('ON the date of' , date , 'the termperature will be' ,  temp)
                    if numTemp == 7:
                        break
                    numTemp = numTemp + 1
            runTime = 0
    while runTime == 5:
    ##exit
        print('Have a nice day, goodbye.')
        print(type(HolidayList[0]))
        sys.exit()
    runTime = 0
