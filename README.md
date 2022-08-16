# Google Map Result Scraping

This app is used to collect all google search results up until 20 results.

To use this app:
1. go to google map and search for something
2. scroll the search results until you reach the end
3. open inspect and copy the "body" HTML element and past it in the "temp.txt" file
4. run the program
                
============================================================================

# TODO
- for some reason it don't get more than 13 result while it should get up to 20
- make the writer only open once and write
- eliminate duplicate rows
- make compromised rows point out in the error column
- give the user the ability to just enter the url. This must allow javascript to load and then access the HTML code.
