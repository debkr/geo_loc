# GEO Location Lookup 1.0.0
# 12June 2016

# Retrieving locations using Google GeoCoding API
# and storing in an SQL database


# import libraries
import json
import urllib
import sqlite3

# create database file connection
conn = sqlite3.connect('locations1.sqlite')
curs = conn.cursor()

# create database tables/fields if not already created
curs.executescript('''
CREATE TABLE IF NOT EXISTS Location (
    id   INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    addr TEXT UNIQUE,
    geo  TEXT,
    loc  TEXT,
    lat  FLOAT,
    lng  FLOAT
)
''')

# read address from file and check if already in database
serviceurl = 'http://maps.googleapis.com/maps/api/geocode/json?'
fname = 'where.data'
fhand = open(fname,'r')
print '\nReading addresses from a file (filename:', fname+')...'
count = 1
for line in fhand :
    if count > 10 : break   # only looks up 10 geodata at a time
    addr = line.rstrip()
    addr = addr.replace('.','')
    
    # check if address already in database
    print '\nChecking in database for:', addr
    try:
        curs.execute('SELECT addr FROM Location WHERE addr = ? ', (addr, ))
    except:
        new = 0
        print 'Cannot process:', new, addr
        continue
    
    try:
        result = curs.fetchone()[0]
        new = 0
        print 'Success:', new, result
    except:
        new = 1
        print 'Not in database:', new, addr

    # retrieve geodata for new addresses only (count to 10)
    if new == 1 :
        print 'Processing:', addr
        url = serviceurl + urllib.urlencode({'sensor':'false', 'address': addr})
        print '\nRetrieving:', url
        uhand = urllib.urlopen(url)
        data = uhand.read()
        print 'Retrieved:', len(data),'characters'
        count = count + 1
        
        try: 
            js = json.loads(str(data))
            #print js
        except: 
            continue

        # error handling: failed or empty JSON data
        # add address/geodata onlyto database
        if 'status' not in js or (js['status'] != 'OK' or js['status'] == 'ZERO_RESULTS') : 
            print 'Retrieve failed'
            print data
            print 'Adding address & failed geodata only'
            curs.execute('''INSERT OR IGNORE INTO Location (addr, geo ) 
                VALUES ( ?, ? )''', ( addr, data ) )
            conn.commit()
            continue
            
        print '\nAdding to database...'
        print 'ADDRESS:', addr
        geo = data
        #print data
        
        #error handling: unicode in location > err
        try:
            loc = js["results"][0]["formatted_address"]
            print 'LOCATION:', loc
        except:
            print 'LOC (err)'
            loc = 'err'
        
        lat = js["results"][0]["geometry"]["location"]["lat"]
        print 'LAT:', lat
        
        lng = js["results"][0]["geometry"]["location"]["lng"]
        print 'LONG:', lng
        
        #error handling: unicode in geodata > err
        try:
            curs.execute('''INSERT OR IGNORE INTO Location (addr, geo, loc, lat, lng) 
                VALUES ( ?, ?, ?, ?, ? )''', ( addr, geo, loc, lat, lng ) )
        except:
            print 'Error (unicode), geodata not added'
            curs.execute('''INSERT OR IGNORE INTO Location (addr, geo, loc, lat, lng) 
                VALUES ( ?, ?, ?, ?, ? )''', ( addr, 'err', loc, lat, lng ) )
    
        conn.commit()

quit()
