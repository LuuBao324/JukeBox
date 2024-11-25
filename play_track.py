import tkinter as tk
from tkinter import messagebox
import track_library as lib
import webbrowser
import font_manager as fonts
import json
import os



class PlayTrack:
    def __init__(self, window):

        window.geometry('750x400')
        window.title('Play Track List')
        self.script_dir = os.path.dirname(__file__)
        self.playlist_file = os.path.join(self.script_dir, "playlist.json")

        frame = tk.Frame(window)
        frame.pack(pady=10)

        # Create a listbox to display tracks
        self.track_listbox = tk.Listbox(window, width=100)
        self.track_listbox.pack(pady=10)


        # Populate the listbox with tracks from the library
        self.update_track_list()

        # Create a button to play the selected track
        play_button = tk.Button(window, text="Play selected track", command=self.play_selected_track)
        play_button.pack()

        play_playlist_button = tk.Button(window, text="Play playlist", command=self.play_playlist)
        play_playlist_button.pack()

    def load_playlist(self):
        try:
            with open(self.playlist_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError,json.JSONDecodeError):
            messagebox.showerror("Error", "Playlist file not found or invalid.")
            return {}

    def update_track_list(self):
        self.track_listbox.delete(0, tk.END)  # Clear existing entries
        for key, item in lib.library.items():
            self.track_listbox.insert(tk.END, f"{key} - {item.name} - {item.artist}")
            

    def play_selected_track(self):
        selection = self.track_listbox.curselection()
        if selection:
            # Get the key of the selected track from the listbox
            selected_track_text = self.track_listbox.get(selection[0])
            key = str(selected_track_text.split(" - ")[0])
            self.play_track_by_key(key)
        else:
            messagebox.showwarning("Warning", "No track selected!")

    def play_track_by_key(self, key):
        youtube_link = lib.get_youtube_link(key)
        if youtube_link:
            webbrowser.open(youtube_link)
            lib.increment_play_count(key)
            self.update_track_list()
        else:
            messagebox.showerror("Error, your youtube link not found for this track!")

    def play_playlist(self):
        playlist = self.load_playlist()
        if playlist:
            for key in playlist:
                self.play_track_by_key(key)
        else:
            messagebox.showwarning("Warning", "Playlist is empty!")

if __name__ == "__main__":
    window = tk.Tk()
    fonts.configure()
    PlayTrack(window)
    window.mainloop()




    