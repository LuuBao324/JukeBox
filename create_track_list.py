import tkinter as tk
import tkinter.scrolledtext as tkst
import track_library as lib
import font_manager as fonts
import os
import json


def set_text(text_area, content):
    text_area.delete("1.0", tk.END)
    text_area.insert(1.0, content)

class CreateTrackList():
    def __init__(self, window):
        window.geometry("1150x600")
        window.title("Manage Playlists")

        self.playlists = {}
        self.current_playlist = None
        self.script_dir = os.path.dirname(__file__)
        self.playlists_file = os.path.join(self.script_dir, "playlists.json")
        
        self.load_playlists()

        # Playlist Name
        self.playlist_name_label = tk.Label(window, text="Playlist Name:")
        self.playlist_name_label.grid(row=0, column=0, padx=10, pady=10)

        self.playlist_name_entry = tk.Entry(window, width=20)
        self.playlist_name_entry.grid(row=0, column=1, padx=10, pady=10)

        self.new_playlist_btn = tk.Button(window, text="New Playlist", command=self.create_new_playlist)
        self.new_playlist_btn.grid(row=0, column=2, padx=10, pady=10)

        # Tracks
        self.list_tracks_btn = tk.Button(window, text="List All Tracks", command=self.list_tracks_clicked)
        self.list_tracks_btn.grid(row=1, column=0, padx=10, pady=10)

        self.list_txt = tkst.ScrolledText(window, width=50, height=15, wrap="none")
        self.list_txt.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

        self.track_number_label = tk.Label(window, text="Enter Track Number")
        self.track_number_label.grid(row=1, column=1, padx=10, pady=10)

        self.track_number_entry = tk.Entry(window, width=10)
        self.track_number_entry.grid(row=1, column=2, padx=10, pady=10)

        self.add_track_btn = tk.Button(window, text="Add Track", command=self.add_track)
        self.add_track_btn.grid(row=1, column=3, padx=10, pady=10)

        # Playlist Display
        self.playlist_lbl = tk.Label(window, text="Current Playlist:")
        self.playlist_lbl.grid(row=2, column=2, columnspan=2, padx=10, pady=10)

        self.playlist_display = tkst.ScrolledText(window, width=50, height=15, wrap="none")
        self.playlist_display.grid(row=3, column=3, columnspan=3, padx=10, pady=10)

        # Controls
        self.play_btn = tk.Button(window, text="Play Playlist", command=self.play_playlist)
        self.play_btn.grid(row=4, column=0, padx=10, pady=10)

        self.save_btn = tk.Button(window, text="Save Playlist", command=self.save_playlists)
        self.save_btn.grid(row=4, column=1, padx=10, pady=10)

        self.load_btn = tk.Button(window, text="Load Playlist", command=self.load_playlist)
        self.load_btn.grid(row=4, column=2, padx=10, pady=10)

        self.reset_btn = tk.Button(window, text="Reset Playlist", command=self.reset_playlist)
        self.reset_btn.grid(row=4, column=3, padx=10, pady=10)

        self.status_lbl = tk.Label(window, text="", font=("Helvetica", 10))
        self.status_lbl.grid(row=5, column=0, columnspan=4, sticky="W", padx=10, pady=10)

    def list_tracks_clicked(self):
        track_list = lib.list_all()
        set_text(self.list_txt, track_list)
    
    def create_new_playlist(self):
        name = self.playlist_name_entry.get().strip()
        if name:
            if name not in self.playlists:
                self.playlists[name] = []
                self.current_playlist = name
                self.update_playlist_display()
                self.status_lbl.configure(text=f"New playlist '{name}' created.")
            else:
                self.status_lbl.configure(text=f"Playlist '{name}' already exists.")
        else:
            self.status_lbl.configure(text="Enter a valid playlist name.")

    def load_playlist(self):
        name = self.playlist_name_entry.get().strip()
        if name in self.playlists:
            self.current_playlist = name
            self.update_playlist_display()
            self.status_lbl.configure(text=f"Playlist '{name}' loaded.")
        else:
            self.status_lbl.configure(text=f"Playlist '{name}' not found.")

    def add_track(self):
        if self.current_playlist is None:
            self.status_lbl.configure(text="No playlist selected.")
            return

        key = self.track_number_entry.get()
        name = lib.get_name(key)
        if name:
            self.playlists[self.current_playlist].append(key)
            self.update_playlist_display()
            self.track_number_entry.delete(0, tk.END)
            self.status_lbl.configure(text=f"Track {key} added to playlist '{self.current_playlist}'.")
        else:
            self.status_lbl.configure(text=f"Track {key} not found.")

    def play_playlist(self):
        if self.current_playlist is None:
            self.status_lbl.configure(text="No playlist selected.")
            return

        for key in self.playlists[self.current_playlist]:
            lib.increment_play_count(key)
        self.update_playlist_display()
        self.status_lbl.configure(text=f"Playlist '{self.current_playlist}' played.")
        lib.save_library(os.path.join(self.script_dir, 'song_data.csv'))

    def reset_playlist(self):
        if self.current_playlist:
            self.playlists[self.current_playlist].clear()
            self.update_playlist_display()
            self.status_lbl.configure(text=f"Playlist '{self.current_playlist}' reset.")
        else:
            self.status_lbl.configure(text="No playlist selected.")

    def save_playlists(self):
        try:
            with open(self.playlists_file, 'w') as f:
                json.dump(self.playlists, f, indent=4)
            self.status_lbl.configure(text="Playlists saved.")
        except Exception as e:
            self.status_lbl.configure(text=f"Error saving playlists: {e}")

    def load_playlists(self):
        try:
            with open(self.playlists_file, 'r') as f:
                self.playlists = json.load(f)
        except FileNotFoundError:
            self.playlists = {}

    def update_playlist_display(self):
        self.playlist_display.delete("1.0", tk.END)
        if self.current_playlist:
            for key in self.playlists[self.current_playlist]:
                name = lib.get_name(key)
                artist = lib.get_artist(key)
                play_count = lib.get_play_count(key)
                self.playlist_display.insert(tk.END, f"{key}: {name} - {artist} (Play Count: {play_count})\n")


if __name__ == "__main__":
    window = tk.Tk()
    fonts.configure()
    CreateTrackList(window)
    window.mainloop()