import tkinter as tk
import tkinter.scrolledtext as tkst

# Import necessary modules
import track_library as lib  # Assumed to contain functions for interacting with a track database
import font_manager as fonts # Assumed to contain functions for configuring fonts


def set_text(text_area, content):
    """
    Clears the existing text in a text area and inserts new content.

    Args:
        text_area: The tkinter Text widget to modify.
        content: The text string to insert.
    """
    text_area.delete("1.0", tk.END)  # Delete all text from the beginning (1.0) to the end (tk.END)
    text_area.insert(1.0, content)  # Insert the new content at the beginning (1.0)


class TrackViewer():
    """
    A graphical user interface (GUI) for viewing track information from a library.
    """
    def __init__(self, window):
        """
        Initializes the TrackViewer GUI.

        Args:
            window: The main tkinter window.
        """
        window.geometry("750x350")  # Set window size
        window.title("View Tracks")  # Set window title

        # Create and place the "List All Tracks" button
        list_tracks_btn = tk.Button(window, text="List All Tracks", command=self.list_tracks_clicked)
        list_tracks_btn.grid(row=0, column=0, padx=10, pady=10)

        # Create and place a label for track number input
        enter_lbl = tk.Label(window, text="Enter Track Number")
        enter_lbl.grid(row=0, column=1, padx=10, pady=10)

        # Create and place an entry field for track number input
        self.input_txt = tk.Entry(window, width=3)
        self.input_txt.grid(row=0, column=2, padx=10, pady=10)

        # Create and place the "View Track" button
        check_track_btn = tk.Button(window, text="View Track", command=self.view_tracks_clicked)
        check_track_btn.grid(row=0, column=3, padx=10, pady=10)

        # Create and place a scrolled text area to display the list of tracks
        self.list_txt = tkst.ScrolledText(window, width=48, height=12, wrap="none") 
        self.list_txt.grid(row=1, column=0, columnspan=3, sticky="W", padx=10, pady=10)

        # Create and place a text area to display individual track details
        self.track_txt = tk.Text(window, width=24, height=4, wrap="none")
        self.track_txt.grid(row=1, column=3, sticky="NW", padx=10, pady=10)

        # Create and place a label to display status messages
        self.status_lbl = tk.Label(window, text="", font=("Helvetica", 10))
        self.status_lbl.grid(row=2, column=0, columnspan=4, sticky="W", padx=10, pady=10)

        # Initially display the list of all tracks
        self.list_tracks_clicked()

    def view_tracks_clicked(self):
        """
        Handles the "View Track" button click event.  Retrieves and displays track details.
        """
        key = self.input_txt.get() # Get the track number from the entry field
        name = lib.get_name(key)    # Get track name using the track library function
        if name is not None:        # Check if track exists
            artist = lib.get_artist(key)  # Get artist
            rating = lib.get_rating(key)  # Get rating
            play_count = lib.get_play_count(key) # Get play count
            track_details = f"{name}\n{artist}\nrating: {rating}\nplays: {play_count}" #Format track details
            set_text(self.track_txt, track_details) # Update track details text area
        else:
            set_text(self.track_txt, f"Track {key} not found") # Display "not found" message if track doesn't exist
        self.status_lbl.configure(text="View Track button was clicked!") # Update status label

    def list_tracks_clicked(self):
        """
        Handles the "List All Tracks" button click event. Displays all tracks from the library.
        """
        track_list = lib.list_all()  # Get the list of all tracks from the track library
        set_text(self.list_txt, track_list)  # Update list text area
        self.status_lbl.configure(text="List Tracks button was clicked!")  # Update status label


if __name__ == "__main__":  # only runs when this file is run as a standalone
    window = tk.Tk()        # create a TK object
    fonts.configure()       # configure the fonts (using a custom function from font_manager.py)
    TrackViewer(window)     # create and open the TrackViewer GUI
    window.mainloop()       # run the window main loop, reacting to button presses, etc