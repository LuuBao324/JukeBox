from library_item import LibraryItem
import csv
import os


library = {}
def load_library(filename):
    global library
    library = {}   
    with open (filename,'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            key = row[reader.fieldnames[0]]
            name = row[reader.fieldnames[1]]
            artist = row[reader.fieldnames[2]]
            rating = int(row[reader.fieldnames[3]])
            play_count = int(row[reader.fieldnames[4]])
            youtube_link = str(row[reader.fieldnames[5]])
            library[key] = LibraryItem(name, artist, rating, play_count, youtube_link)
            


def save_library(filename):
    
    with open (filename, 'w', newline='') as csvfile:
        fieldnames = ['key', 'name', 'artist', 'rating', 'play count', 'youtube_link']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for key, item in library.items():
            writer.writerow({
                'key': key,
                'name': item.name,
                'artist': item.artist,
                'rating': item.rating,
                'play count': item.play_count,
                'youtube_link':item.youtube_link
            })

#Load library data from CSV file

current_dir = os.path.dirname(__file__)  # Gets the directory of the script
csv_path = os.path.join(current_dir, 'songs.csv')
load_library(csv_path)



    


def list_all():
    output = ""
    for key in library:
        item = library[key]
        output += f"{key} {item.info()}\n"
    return output


def get_name(key):
    try:
        item = library[key]
        return item.name
    except KeyError:
        return None


def get_artist(key):
    try:
        item = library[key]
        return item.artist
    except KeyError:
        return None


def get_rating(key):
    try:
        item = library[key]
        return item.rating
    except KeyError:
        return -1


def set_rating(key, rating):
    try:
        item = library[key]
        item.rating = rating
    except KeyError:
        return


def get_play_count(key):
    try:
        item = library[key]
        return item.play_count
    except KeyError:
        return -1


def increment_play_count(key):
    try:
        item = library[key]
        item.play_count += 1
    except KeyError:
        return
    

def get_youtube_link(key):
    try:
        item = library[key] 
        return item.youtube_link
    except KeyError:
        return None
    
def get_track_data(key):
    try:
        return library[key]
    except KeyError:
        return None



    

