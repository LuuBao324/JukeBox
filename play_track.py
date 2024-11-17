import tkinter as tk
from tkinter import messagebox
import track_library as lib
import webbrowser
import font_manager as fonts




class PlayTrack:
    def __init__(self, window):
        window.geometry('750x350')
        window.title('Play Track List')

        frame = tk.Frame(window)
        frame.pack(pady=10)

        # Create a listbox to display tracks
        self.track_listbox = tk.Listbox(window, width=100)
        self.track_listbox.pack(pady=10)


        # Populate the listbox with tracks from the library
        self.update_track_list()

        # Create a button to play the selected track
        play_button = tk.Button(window, text="Play Track", command=self.play_selected_track)
        play_button.pack()

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
            # Open the youtube link in the web browser
            youtube_link = lib.get_youtube_link(key)  # Fetch link using new function
            youtube_link = str(youtube_link)

            if youtube_link:
                webbrowser.open(youtube_link)
            else:
                messagebox.showerror("Error", "YouTube link not found for this track.")
            self.update_track_list()  # Update the listbox after playing


if __name__ == "__main__":
    window = tk.Tk()
    fonts.configure()
    PlayTrack(window)
    window.mainloop()




    