import sqlite3
import json
import codecs

conn = sqlite3.connect("geodata.sqlite")
cur = conn.cursor()

cur.execute("SELECT * FROM Locations")
fh = codecs.open("where.js", "w", "utf-8")
fh.write("myData = [\n")

count = 0
for row in cur:
    data = str(row[1].decode())
    try:
        json_data = json.loads(data)
    except:
        continue
    
    if "status" not in json_data or json_data["status"] != "OK":
        continue
    
    lat = json_data["results"][0]["geometry"]["location"]["lat"]
    lng = json_data["results"][0]["geometry"]["location"]["lng"]
    if lat == 0 or lng == 0: 
        continue
    where = json_data["results"][0]["formatted_address"]
    where = where.replace("'", "")
    try:
        print(where, lat, lng)
        
        count = count + 1
        if count > 1:
            fh.write(",\n")
        output = "["+str(lat)+", "+str(lng)+", '"+where+"']"
        fh.write(output)
        
    except:
        continue
        
fh.write("\n];\n")
cur.close()
fh.close()
print(count, "records written to where.js")
print("Open where.html to view data in a browser")
    
            