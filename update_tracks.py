import tkinter as tk
import tkinter.scrolledtext as tkst

import track_library as lib
import font_manager as fonts

import os

def set_text(text_area, content):
    text_area.delete("1.0", tk.END)
    text_area.insert(1.0, content)

class UpdateTracks():
    def __init__(self, window):
        window.geometry("750x450")
        window.title("Update Tracks")

        list_tracks_btn = tk.Button(window, text="List All Tracks", command=self.list_tracks_clicked)
        list_tracks_btn.grid(row=0, column=0, padx=10, pady=10)
        
        self.list_txt = tkst.ScrolledText(window, width=48, height=12, wrap="none")
        self.list_txt.grid(row=1, column=0, columnspan=3, sticky="W", padx=10, pady=10)
        
        #Track number entry
        self.track_number_lbl = tk.Label(window, text="Enter Track Number")
        self.track_number_lbl.grid(row=0, column=4, padx=10, pady=10)

        self.track_number_entry = tk.Entry(window, width=5)
        self.track_number_entry.grid(row=0, column=5, padx=10, pady=10)

        #Rating Entry
        self.rating_lbl = tk.Label(window, text="Enter New Rating")
        self.rating_lbl.grid(row=1, column=4, padx=10, pady=10)

        self.rating_entry = tk.Entry(window, width=5)
        self.rating_entry.grid(row=1, column=5, padx=10, pady=10)

        #Update Button
        self.update_btn = tk.Button(window, text="Update Track", command=self.update_track)
        self.update_btn.grid(row=2, column=4, columnspan=2, pady=10)

        #Status Label
        self.status_lbl = tk.Label(window, text="", font=("Helvetica", 10))
        self.status_lbl.grid(row=3, column=4, columnspan=2, padx=10, pady=10)

        

    def list_tracks_clicked(self):
        track_list = lib.list_all()
        set_text(self.list_txt, track_list)
        
    
    def update_track(self):
        key = self.track_number_entry.get()
        new_rating = self.rating_entry.get()
        try:
            new_rating = int(new_rating)
            if 0 <= new_rating <=5:
                lib.set_rating(key, new_rating)
                name = lib.get_name(key)
                artist = lib.get_artist(key)
                play_count = lib.get_play_count(key)
                self.status_lbl.configure(text= f"Track {key} ({name} - {artist}) updated with rating {new_rating}, play count: {play_count}")
                
                current_dir = os.path.dirname(__file__)  # Gets the directory of the script
                csv_path = os.path.join(current_dir, 'song_data.csv')
                lib.save_library(csv_path) #Save the changes to library back to CSV file
                track_list = lib.list_all()
                set_text(self.list_txt, track_list)
            else:
                self.status_lbl.configure(text="Rating must be between 0 and 5.")
        except ValueError:
            self.status_lbl.configure(text="Invalid rating input. Please enter a number.")
            

if __name__ == "__main__":
    window = tk.Tk()
    fonts.configure()
    UpdateTracks(window)
    window.mainloop()




    