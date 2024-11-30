import pytest
from library_item import LibraryItem

def test_library_item_creation():
    item = LibraryItem("Song Title", "Artist Name")
    assert item.name == "Song Title"
    assert item.artist == "Artist Name"
    assert item.rating == 0
    assert item.play_count == 0
    assert item.youtube_link == ""

def test_library_item_with_attributes():
    item = LibraryItem("Another Song", "Another Artist", rating=4, play_count=10, youtube_link="https://www.youtube.com/watch?v=example")
    assert item.name == "Another Song"
    assert item.artist == "Another Artist"
    assert item.rating == 4
    assert item.play_count == 10
    assert item.youtube_link == "https://www.youtube.com/watch?v=example"

def test_library_item_info():
    item = LibraryItem("Test Song", "Test Artist", rating=3)
    assert item.info() == "Test Song - Test Artist ***"

def test_library_item_stars():
    item = LibraryItem("Song", "Artist", rating=5)
    assert item.stars() == "*****"
    item.rating = 0
    assert item.stars() == ""
    item.rating = 2
    assert item.stars() == "**"

def test_library_item_zero_rating():
    item = LibraryItem("Zero Rating Song", "Zero Rating Artist", rating=0)
    assert item.info() == "Zero Rating Song - Zero Rating Artist "
    assert item.stars() == ""

def test_library_item_max_rating():
    item = LibraryItem("Max Rating Song", "Max Rating Artist", rating=5)
    assert item.info() == "Max Rating Song - Max Rating Artist *****"
    assert item.stars() == "*****"