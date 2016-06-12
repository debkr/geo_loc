# GEO Location Lookup 1.0.0
A simple Python program to retrieve locations using Google GeoCoding API

12 June 2016

## Description

This program retireves location data using Google's Geocoding API and saves it in a database for later use in data visualisation on a Google Map. (Note: The Geocoding T's and C's require that this free service may only be used where the data is going to be displayed on a Google Map, not visualised through some other format.)

Simple walkthrough of the process:
1. Retrieve addresses of placenames from a file of location data.These might be a list of companies, holiday destinations, locations (town/city, country) of visitors to a website, or planned stop-offs en route during a road trip;
1. Look up each of the address locations to check if they're already in an SQL database;
1. If not already in the database, retrieve the location geodata from the Google GeoCoding API, extract the formatted address and lat/long data and append the following to the database:
  - address
  - raw geodata
  - location
  - latitude
  - longitude
1. Save all changes to the database ready for another program to extract the geodata and plot it on a Google Map (e.g. for output to a web page via HTML).

Some points to note:
* The geodata retrieval itself runs in batches of 10, to allow for testing and error handling, and to prevent it running on for ages. This can easily be changed/increased by changing the loop count parameter;
* Several kinds of error-handling have been added to the program to account for Unicode data within the JSON data returned - SQLite does not like these and won't allow them to be inserted into the database. To get around this problem the program simply returns 'err' instead (to either/both the geodat and location fields) and continues the program as normal.

Further improvements required:
* To research and include a way to convert Unicode (special characters) to read normally so they can be added to the SQL database;
* It may be better to read all addresses (from file) into the database at one go - adding the 'new' indicator (0/1) set to 0 to indicate this is a new address whose geodata has not yet been looked up. The program could be amended to run the geodata lookup in batches of n (e.g. n=10 as used here) on the next n data rows selected from the database where new = 0.
