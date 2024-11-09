import tkinter as tk
import tkinter.scrolledtext as tkst


import track_library as lib
import font_manager as fonts
import os


class CreateTrackList():
    def __init__(self, window):
        window.geometry("750x500")
        window.title("Create Track List")
        self.playlist = []

        #Input for Track numbers
        self.track_number_label = tk.Label(window, text="Enter Track Number")
        self.track_number_label.grid(row=0, column=0, padx=10, pady=10)

        self.track_number_entry = tk.Entry(window, width=5)
        self.track_number_entry.grid(row=0, column=1, padx=10, pady=10)

        #Button to Add track to playlist
        self.add_track_btn = tk.Button(window, text="Add Track", command=self.add_track)
        self.add_track_btn.grid(row=0, column=2, padx=10, pady=10)

        # Display Playlist 
        self.playlist_lbl = tk.Label(window, text="Playlist:")
        self.playlist_lbl.grid(row=1, column=0, padx=10, pady=10)
        
        self.playlist_display = tkst.ScrolledText(window, width=48, height=15, wrap="none")
        self.playlist_display.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

        #Button to play the Playlist
        self.play_btn = tk.Button(window, text="Play Playlist", command=self.play_playlist)
        self.play_btn.grid(row=3, column=0, padx=10, pady=10)

        #Button to reset the Playlist
        self.reset_btn = tk.Button(window, text="Reset Playlist", command=self.reset_playlist)
        self.reset_btn.grid(row=3, column=1, padx=10, pady=10)

        #Status Label
        self.status_lbl = tk.Label(window, text="", font=("Helvetica", 10))
        self.status_lbl.grid(row=4, column=0, columnspan=4, sticky="W", padx=10, pady=10)

    def add_track(self):
        key = self.track_number_entry.get()
        name = lib.get_name(key)
        if name is not None:
            self.playlist.append(key)
            self.update_playlist_display()
            self.track_number_entry.delete(0, tk.END)
            self.status_lbl.configure(text=f"Track {key} added to playlist.")
        else:
            self.status_lbl.configure(tk.END, text=f"ERROR, the track number {key} not found. \n")

    def play_playlist(self):
        for key in self.playlist:
            lib.increment_play_count(key)
            self.update_playlist_display()
        self.status_lbl.configure(text="Playlist played.")
        current_dir = os.path.dirname(__file__)  # Gets the directory of the script
        csv_path = os.path.join(current_dir, 'songs.csv')
        lib.save_library(csv_path) #Save the changes to library back to CSV file

    
        

    def reset_playlist(self):
        self.playlist.clear()
        self.playlist_display.delete("1.0", tk.END)
        self.update_playlist_display()
        self.status_lbl.configure(text="Playlist reset.")

    def update_playlist_display(self):
        self.playlist_display.delete("1.0", tk.END)
        for key in self.playlist:
            name = lib.get_name(key) 
            artist = lib.get_artist(key)
            play_count = lib.get_play_count(key)
            self.playlist_display.insert(tk.END, f"{key}: {name} - {artist} (Play Count: {play_count})\n")

if __name__ == "__main__":
    window = tk.Tk()
    fonts.configure()
    CreateTrackList(window)
    window.mainloop()