import xml.etree.ElementTree as ET
import sqlite3

conn = sqlite3.connect("trackdb.sqlite")
cur = conn.cursor()

cur.executescript("""
DROP TABLE IF EXISTS Artist;
DROP TABLE IF EXISTS Album;
DROP TABLE IF EXISTS Genre;
DROP TABLE IF EXISTS Track;

CREATE TABLE Artist (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name TEXT UNIQUE
);

CREATE TABLE Album (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    title TEXT UNIQUE,
    artist_id INTEGER
);

CREATE TABLE Genre (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name TEXT UNIQUE
);

CREATE TABLE Track (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    title TEXT UNIQUE,
    len INTEGER,
    rating INTEGER,
    count INTEGER,
    album_id INTEGER,
    genre_id INTEGER
);
""")

fname = input("Please input the file name: ")
if (len(fname) < 1): 
    fname = "Library.xml"

def lookup(entry, key):
    found = False
    for child in entry:
        if found == True: return child.text
        if child.tag == "key" and child.text == key:
            found = True
    return None

stuff = ET.parse(fname)
dicts = stuff.findall("dict/dict/dict")
print("All dict is:", len(dicts))
for entry in dicts:
    if (lookup(entry, "Track ID") is None):
        continue
        
    name = lookup(entry, "Name")
    artist = lookup(entry, "Artist")
    album = lookup(entry, "Album")
    genre = lookup(entry, "Genre")
    count = lookup(entry, "Play Count")
    rating = lookup(entry, "Rating")
    length = lookup(entry, "Total Time")
        
    if name is None or artist is None or album is None or genre is None:
        continue
    
    print(name, artist, album, genre, count, rating, length)
        
    cur.execute("INSERT OR IGNORE INTO Artist(name) VALUES (?)", (artist,))
    cur.execute("SELECT id FROM Artist WHERE name = ?", (artist,))
    artist_id = cur.fetchone()[0]
    
    cur.execute("INSERT OR IGNORE INTO Album(title, artist_id) VALUES (?, ?)", (album, artist_id))
    cur.execute("SELECT id FROM Album WHERE title = ?", (album,))
    album_id = cur.fetchone()[0]
    
    cur.execute("INSERT OR IGNORE INTO Genre(name) VALUES (?)", (genre,))
    cur.execute("SELECT id FROM Genre WHERE name = ?", (genre,))
    genre_id = cur.fetchone()[0]
    
    cur.execute("INSERT OR REPLACE INTO Track(title, len, rating, count, album_id, genre_id) VALUES (?, ?, ?, ?, ?, ?)", (name, length, rating, count, album_id, genre_id))
    
    conn.commit()
