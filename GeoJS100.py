# GEO JavaScript Writer 1.0.0
# 12 June 2016

# Extracts location data from an SQL database
# and writes to a JavaScript output file


# import libraries
import sqlite3
import json
import codecs

# create database file connection
conn = sqlite3.connect('locations1.sqlite')
curs = conn.cursor()

# select all records from database
curs.execute('SELECT * FROM Location')
result = curs.fetchall()
print '\n\nRecords retrieved:', len(result)

# set up JavaScript output file
fhand = codecs.open('geoloc1.js','w', "utf-8")
fhand.write("geoData = [\n")

# loop through all records
count = 1 ; outrow = 0
for record in result :
    if count > 50 : break    # amend count criteria as required
    id = record[0] ; addr = record[1] ; loc = record[3]
    lat = record[4] ; lng = record[5]
    
    # ignore records without lat/long data
    if lat == None or lng == None :
        print '\nRecord number:', count, 'Error, ignored'
        count = count + 1
        continue
    
    # print all good records and write to JavaScript file
    else:
        print '\nRecord number:', count
        print 'ID:', id
        print 'Address:', addr
        #print 'GeoData:', record[2]
        print 'Location:', loc
        print 'LAT/LONG:', lat, lng
        count = count + 1
        outrow = outrow + 1
    
        if outrow > 1 : fhand.write(',\n')
        
        # if no location data, use address instead
        if loc == 'err' :
            output = "["+str(lat)+","+str(lng)+", '"+addr+"']"
        else:
            output = "["+str(lat)+","+str(lng)+", '"+loc+"']"
        
        fhand.write(output)

# finalise list of lists to .js file; close cursor & .js file
fhand.write("\n];\n")
curs.close()
fhand.close()

print '\n\n++Finished++'
print outrow, 'records written to: geoloc1.js'
quit()
