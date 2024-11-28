import tkinter as tk
from tkinter import messagebox
import track_library as lib
import webbrowser
import font_manager as fonts
import json
import os

class PlayTrack:
    def __init__(self, window):
        window.geometry('1200x400')
        window.title('Play Tracks and Playlists')
        self.script_dir = os.path.dirname(__file__)
        self.playlists_file = os.path.join(self.script_dir, "playlists.json")
        self.current_playlist = []

        # Song Library Section
        self.library_label = tk.Label(window, text="Song Library:")
        self.library_label.grid(row=0, column=0, padx=10, pady=5)

        self.library_listbox = tk.Listbox(window, width=40, height=10)
        self.library_listbox.grid(row=1, column=0, padx=10, pady=5)

        self.play_library_button = tk.Button(window, text="Play Selected Song", command=self.play_library_song)
        self.play_library_button.grid(row=2, column=0, padx=10, pady=5)

        # Playlist Selection Section
        self.playlist_label = tk.Label(window, text="Playlists:")
        self.playlist_label.grid(row=0, column=1, padx=10, pady=5)

        self.playlist_dropdown = tk.StringVar(window)
        self.playlist_menu = tk.OptionMenu(window, self.playlist_dropdown, "")
        self.playlist_menu.grid(row=1, column=1, padx=10, pady=5)

        self.load_playlists_button = tk.Button(window, text="Load Playlist", command=self.load_selected_playlist)
        self.load_playlists_button.grid(row=2, column=1, padx=10, pady=5)

        # Playlist Tracks Section
        self.playlist_tracks_label = tk.Label(window, text="Playlist Tracks:")
        self.playlist_tracks_label.grid(row=0, column=2, padx=10, pady=5)

        self.playlist_listbox = tk.Listbox(window, width=40, height=10)
        self.playlist_listbox.grid(row=1, column=2, padx=10, pady=5)

        self.play_playlist_song_button = tk.Button(window, text="Play Selected Playlist Song", command=self.play_selected_playlist_song)
        self.play_playlist_song_button.grid(row=2, column=2, padx=10, pady=5)

        self.play_entire_playlist_button = tk.Button(window, text="Play Entire Playlist", command=self.play_playlist)
        self.play_entire_playlist_button.grid(row=3, column=2, padx=10, pady=5)

        # Load Initial Data
        self.update_library_list()
        self.update_playlist_menu()

    def update_library_list(self):
        """Populate the Song Library Listbox with all available songs."""
        self.library_listbox.delete(0, tk.END)
        for key, item in lib.library.items():
            self.library_listbox.insert(tk.END, f"{key} - {item.name} - {item.artist}")

    def update_playlist_menu(self):
        """Populate the Playlist Dropdown with available playlists."""
        try:
            with open(self.playlists_file, 'r') as f:
                playlists = json.load(f)
                self.playlist_dropdown.set("")
                menu = self.playlist_menu['menu']
                menu.delete(0, 'end')  # Clear previous entries
                for playlist_name in playlists.keys():
                    menu.add_command(label=playlist_name, command=lambda name=playlist_name: self.playlist_dropdown.set(name))
        except (FileNotFoundError, json.JSONDecodeError):
            messagebox.showerror("Error", "No playlists found or file is corrupted.")

    def load_selected_playlist(self):
        """Load tracks from the selected playlist into the Playlist Listbox."""
        playlist_name = self.playlist_dropdown.get()
        if not playlist_name:
            messagebox.showwarning("Warning", "No playlist selected!")
            return

        try:
            with open(self.playlists_file, 'r') as f:
                playlists = json.load(f)
                if playlist_name in playlists:
                    self.current_playlist = playlists[playlist_name]
                    self.update_playlist_list()
                    messagebox.showinfo("Success", f"Playlist '{playlist_name}' loaded successfully.")
                else:
                    messagebox.showerror("Error", f"Playlist '{playlist_name}' not found.")
        except (FileNotFoundError, json.JSONDecodeError):
            messagebox.showerror("Error", "Failed to load playlists.")

    def update_playlist_list(self):
        """Populate the Playlist Listbox with tracks from the current playlist."""
        self.playlist_listbox.delete(0, tk.END)
        for key in self.current_playlist:
            item = lib.library.get(key, None)
            if item:
                self.playlist_listbox.insert(tk.END, f"{key} - {item.name} - {item.artist}")

    def play_library_song(self):
        """Play the selected song from the Song Library."""
        selection = self.library_listbox.curselection()
        if selection:
            selected_track_text = self.library_listbox.get(selection[0])
            key = str(selected_track_text.split(" - ")[0])
            self.play_track_by_key(key)
        else:
            messagebox.showwarning("Warning", "No song selected!")

    def play_selected_playlist_song(self):
        """Play the selected song from the Playlist."""
        selection = self.playlist_listbox.curselection()
        if selection:
            selected_track_text = self.playlist_listbox.get(selection[0])
            key = str(selected_track_text.split(" - ")[0])
            self.play_track_by_key(key)
        else:
            messagebox.showwarning("Warning", "No song selected!")

    def play_playlist(self):
        """Play all tracks in the current playlist."""
        if not self.current_playlist:
            messagebox.showwarning("Warning", "No playlist loaded!")
            return

        for key in self.current_playlist:
            self.play_track_by_key(key)

    def play_track_by_key(self, key):
        """Play a track by its key."""
        youtube_link = lib.get_youtube_link(key)
        if youtube_link:
            webbrowser.open(youtube_link)
            lib.increment_play_count(key)
            self.update_library_list()  # Update library list with updated play counts
        else:
            messagebox.showerror("Error", "YouTube link not found for this track!")

if __name__ == "__main__":
    window = tk.Tk()
    fonts.configure()
    PlayTrack(window)
    window.mainloop()
