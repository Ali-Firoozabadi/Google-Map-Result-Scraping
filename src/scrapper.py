"""
============================================================================
Name        : Scrapper.py
Author      : Seyed Ali Firooz Abadi
Version     : 1.0
Description : This app is used to collect all google search results up until 20 results. To use this app:
                1. go to google map and search for something
                2. scroll the search results until you reach the end
                3. open inspect and copy the "body" HTML element and past it in the "temp.txt" file
                4. run the program
Copyright © 2022 Ali Firooz. All rights reserved.
============================================================================
TODO:
    - for some reason it don't get more than 13 result while it should get up to 20
    - make the writer only open once and write
    - eliminate duplicate rows
    - make compromised rows point out in the error column
    - give the user the ability to just enter the url. This must allow javascript to load and then access the HTML code.
"""

import csv
from bs4 import BeautifulSoup


def writeCSV(row):
    rowName = ['Name', 'URL', 'Rating', 'Users Num', 'Category', 'Address', 'Phone Num', 'Open/Close', 'Errors']
    writeData = False
    fileName = "../data/results.csv"
    try:
        # checking if the first line / file does exist
        try:
            with open(fileName, 'r') as tempFile:
                reader = csv.reader(tempFile)
                firstLine = []
                for line in reader:
                    firstLine.append(str(line))
                    break
                if firstLine[0] != str(rowName):
                    writeData = True

        # if file don't exist
        except:
            writeData = True

        # writing down the first line if needed
        finally:
            if writeData:
                with open(fileName, 'w', newline='') as firstLineFile:
                    writer = csv.writer(firstLineFile)
                    writer.writerow(rowName)

        # writing the data to file
        with open(fileName, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(cleanText(row))
    except:
        print("couldn't write statistics, a problem accrued")


def cleanText(row):
    newRow = []
    for i in row:
        newRow.append(str(i).strip("\n\r"))
    return newRow


if __name__ == '__main__':
    # trying to access the website URL and get the HTML code
    try:
        with open('../data/temp.txt', 'r') as html_file:
            local_copy = html_file.read()
            # soup = BeautifulSoup(local_copy, "lxml")
            soup = BeautifulSoup(local_copy, "html5lib")
    except:
        print("\n\nThe website HTML was not accessible")
        exit(0)

    # ----------------------------------------------------------------------

    # grabbing each search result in a list to later go through
    searchResult = soup.find_all(attrs={'class': 'Nv2PK tH5CWc THOPZb'})
    for result in searchResult:
        # a place to save each data retrieved to then add to the Excel file
        rowData = []

        # re-parsing each search result individually to get more specific data
        newSoup = BeautifulSoup(str(result), "html5lib")
        # list that hold name and url
        nameList = newSoup.find(attrs={'class': 'hfpxzc'})
        # Name
        try:
            rowData.append(nameList.get('aria-label'))
        except Exception as e:
            rowData.append('N/A')

        # URLs
        try:
            rowData.append(nameList.get('href'))
        except Exception as e:
            rowData.append('N/A')

        # rating
        try:
            rating = newSoup.find('span', attrs={'class': 'MW4etd'}).get_text(strip=True)
            rowData.append(rating)
        except Exception as e:
            rowData.append(0)

        # Number of users
        try:
            NumOfUsers = newSoup.find('span', attrs={'class': 'UY7F9'}).get_text(strip=True)
            NumOfUsers = NumOfUsers[1:-1].replace(',', '')
            rowData.append(NumOfUsers)
        except Exception as e:
            rowData.append(0)

        # list that hold category, address, phone number
        genList = newSoup.find_all('div', attrs={'class': 'W4Efsd'})[1].get_text(strip=True).strip('Â·').replace('â‹… ', ' - ').split('Â·')

        # A check to make sure the list have all attributes and if not, make if distinguishable by having the word "UnAccountedFor"
        addFlag = False
        while len(genList) < 4:
            addFlag = True
            genList.append('N/A')

        # Category
        try:
            cat = genList[0]
            if len(cat) == 0:
                raise Exception
            rowData.append(cat)
        except Exception as e:
            rowData.append('N/A')

        # address
        try:
            address = genList[1].strip(" \n\r")
            if len(address) == 0:
                raise Exception
            rowData.append(address)
        except Exception as e:
            rowData.append('N/A')

        # phone number
        try:
            phone = genList[3].strip("(").replace(') ', '').replace('-', '')
            # you can use this Excel formatting to get phone numbers formatted "_ * (000) 000 - 0000_ ;_ @_ ", or just comment the strip and replace above
            if len(phone) == 0:
                raise Exception
            rowData.append(phone)
        except Exception:
            rowData.append('N/A')

        # Open/Close time
        try:
            OCT = genList[2]
            if len(OCT) == 0:
                raise Exception
            rowData.append(OCT)
        except Exception:
            rowData.append('N/A')

        if addFlag:
            rowData.append('YES')
        # ----------------------------------------------------------------------

        # writing the row to CSV
        try:
            writeCSV(rowData)
        except Exception:
            print("Something went wrong. One row was compromised")

    print("Everything went well")
