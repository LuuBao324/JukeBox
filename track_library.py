from library_item import LibraryItem
import csv


library = {}
def load_library(filename):
    """Load library data from a CSV file
    
    Args:
        filename: songs.csv
    """
    with open (filename,'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            key = row['key']
            name = row['name']
            artist = row['artist']
            rating =int(row['rating'])
            play_count = int(row['play count'])
            library[key] = LibraryItem(name, artist, rating, play_count )

def save_library(filename):
    """Save library data to a CSV file
    
    Args:
            filename: songs.csv
    """
    with open (filename, 'w', newline='') as csvfile:
        fieldnames = ['key', 'name', 'artist', 'rating', 'play count']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for key, item in library.items():
            writer.writerow({
                'key': key,
                'name': item.name,
                'artist': item.artist,
                'rating': item.rating,
                'play count': item.play_count
            })

#Load library data from CSV file

load_library('songs.csv')


    


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
    
#Save the changes to library back to CSV file
save_library('songs.csv')
