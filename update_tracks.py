import tkinter as tk


import track_library as lib
import font_manager as fonts


class UpdateTracks():
    def __init__(self, window):
        window.geometry("750x350")
        window.title("Update Tracks")

        #Track number entry
        self.track_number_lbl = tk.Label(window, text="Enter Track Number")
        self.track_number_lbl.grid(row=0, column=0, padx=10, pady=10)

        self.track_number_entry = tk.Entry(window, width=5)
        self.track_number_entry.grid(row=0, column=1, padx=10, pady=10)

        #Rating Entry
        self.rating_lbl = tk.Label(window, text="Enter New Rating")
        self.rating_lbl.grid(row=1, column=0, padx=10, pady=10)

        self.rating_entry = tk.Entry(window, width=5)
        self.rating_entry.grid(row=1, column=1, padx=10, pady=10)

        #Update Button
        self.update_btn = tk.Button(window, text="Update Track", command=self.update_track)
        self.update_btn.grid(row=2, column=0, columnspan=2, pady=10)

        #Status Label
        self.status_lbl = tk.Label(window, text="", font=("Helvetica", 10))
        self.status_lbl.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    def update_track(self):
        track_number = self.track_number_entry.get()
        new_rating = self.rating_entry.get()
        try:
            new_rating = int(new_rating)
            if 0 <= new_rating <=5:
                lib.set_rating(track_number, new_rating)
                track_name = lib.get_name(track_number)
                play_count = lib.get_play_count(track_number)
                self.status_lbl.configure(text= f"Track {track_number} ({track_name}) updated with rating {new_rating}, play count: {play_count}")
            else:
                self.status_lbl.configure(text="Rating must be between 0 and 5.")
        except ValueError:
            self.status_lbl.configure(text="Invalid rating input. Please enter a number.")
            

if __name__ == "__main__":
    window = tk.Tk()
    fonts.configure()
    UpdateTracks(window)
    window.mainloop()




    