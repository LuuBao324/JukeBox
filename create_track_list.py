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
        window.geometry("1050x500")
        window.title("Create Track List")
        self.playlist = []
        self.script_dir = os.path.dirname(__file__)  # Get the directory of the script
        self.playlist_file = os.path.join(self.script_dir, "playlist.json") # Construct the full path

        list_tracks_btn = tk.Button(window, text="List All Tracks", command=self.list_tracks_clicked)
        list_tracks_btn.grid(row=0, column=0, padx=10, pady=10)

        #Input for Track numbers
        self.track_number_label = tk.Label(window, text="Enter Track Number")
        self.track_number_label.grid(row=0, column=1, padx=10, pady=10)

        self.track_number_entry = tk.Entry(window, width=5)
        self.track_number_entry.grid(row=0, column=2, padx=10, pady=10)

        #Button to Add track to playlist
        self.add_track_btn = tk.Button(window, text="Add Track", command=self.add_track)
        self.add_track_btn.grid(row=0, column=3, padx=10, pady=10)

        # Display Playlist 
        self.playlist_lbl = tk.Label(window, text="Playlist:")
        self.playlist_lbl.grid(row=1, column=3, padx=10, pady=10)
        
        self.list_txt = tkst.ScrolledText(window, width=48, height=15, wrap="none")
        self.list_txt.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

        self.playlist_display =tkst.ScrolledText(window, width=48, height=15, wrap="none")
        self.playlist_display.grid(row=2, column=3, columnspan=3, padx=10, pady=10)

        #Button to play the Playlist
        self.play_btn = tk.Button(window, text="Play Playlist", command=self.play_playlist)
        self.play_btn.grid(row=3, column=0, padx=10, pady=10)

        #Button to reset the Playlist
        self.reset_btn = tk.Button(window, text="Reset Playlist", command=self.reset_playlist)
        self.reset_btn.grid(row=3, column=1, padx=10, pady=10)

        #Button to save the Playlist to JSON
        self.save_btn = tk.Button(window, text="Save Playlist", command=self.save_playlist)
        self.save_btn.grid(row=3, column=2, padx=10, pady=10)

        #Status Label
        self.status_lbl = tk.Label(window, text="", font=("Helvetica", 10))
        self.status_lbl.grid(row=4, column=0, columnspan=4, sticky="W", padx=10, pady=10)

        self.load_playlist()

    def list_tracks_clicked(self):
        track_list = lib.list_all()
        set_text(self.list_txt, track_list)

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
        csv_path = os.path.join(current_dir, 'song_data.csv')
        lib.save_library(csv_path) #Save the changes to library back to CSV file

    def save_playlist(self):
        try:  
            with open(self.playlist_file, 'w') as f:
                json.dump(self.playlist, f, indent=4)
            self.status_lbl.configure(text=f"Playlist saved to {self.playlist_file}")
        except Exception as e:
            self.status_lbl.configure(text=f"Error saving playlist: {e}")

    def load_playlist(self):
        try:
            with open(self.playlist_file, 'r') as f:
                self.playlist = json.load(f)
                self.update_playlist_display()
                self.status_lbl.configure(text=f"Playlist loaded from {self.playlist_file}")
        except FileNotFoundError:
            pass #Ignore if file doesn't exist
        except json.JSONDecodeError:
             self.status_lbl.configure(text=f"Error loading playlist: Invalid JSON format")
        except Exception as e:
            self.status_lbl.configure(text=f"Error loading playlist: {e}")

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