import tkinter as tk
import tkinter.scrolledtext as tkst


import track_library as lib
import font_manager as fonts



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
        track_number = self.track_number_entry.get()
        track_name = lib.get_name(track_number)
        if track_name is not None:
            self.playlist.append(track_name)
            self.update_playlist_display()
            self.track_number_entry.delete(0, tk.END)
            self.status_lbl.configure(text=f"Track {track_number} added to playlist.")
        else:
            self.status_lbl.configure(tk.END, text=f"ERROR, the track number {track_number} not found. \n")

    def play_playlist(self):
        
        for track_number in self.playlist:
            lib.increment_play_count(track_number)
        self.update_playlist_display()
        self.status_lbl.configure(text="Playlist played.")

    
        

    def reset_playlist(self):
        self.playlist.clear()
        self.playlist_display.delete("1.0", tk.END)
        self.update_playlist_display()
        self.status_lbl.configure(text="Playlist reset.")

    def update_playlist_display(self):
        self.playlist_display.delete("1.0", tk.END)
        for track_number in self.playlist:
            track_name = lib.get_name(track_number) 
            self.playlist_display.insert(tk.END, f"{track_number}: {track_name} \n")

if __name__ == "__main__":
    window = tk.Tk()
    fonts.configure()
    CreateTrackList(window)
    window.mainloop()