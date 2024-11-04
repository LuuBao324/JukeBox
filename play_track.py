import tkinter as tk
import track_library as lib
import webbrowser

class PlayTrackViewer:
    def __init__(self, window):
        window.geometry('750x350')
        window.title('Play Track List')

    def web_open()