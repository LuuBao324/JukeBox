import tkinter as tk
import tkinter.scrolledtext as tkst
import tkinter.ttk as ttk
import track_library as lib
import font_manager as fonts
import os
import json
import webbrowser
from tkinter import messagebox

def set_text(text_area, content):
    text_area.delete("1.0", tk.END)
    text_area.insert(1.0, content)

class ViewTrackTab:
    def __init__(self, parent):
        self.parent = parent
        self.create_widgets()

    def create_widgets(self):
        list_all_btn = tk.Button(self.parent, text="List All Tracks", command=self.list_tracks_clicked)
        list_all_btn.grid(row=0, column=0, padx=10, pady=10)

        self.list_txt_view = tkst.ScrolledText(self.parent, width=48, height=10, wrap="none")
        self.list_txt_view.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

        enter_lbl = tk.Label(self.parent, text="Enter Track Number:")
        enter_lbl.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        self.track_input = tk.Entry(self.parent, width=5)
        self.track_input.grid(row=0, column=2, padx=10, pady=10)

        view_btn = tk.Button(self.parent, text="View Track", command=self.view_track)
        view_btn.grid(row=0, column=3, padx=10, pady=10)

        self.track_txt = tk.Text(self.parent, width=24, height=4, wrap="none")
        self.track_txt.grid(row=1, column=3, sticky="NW", padx=10, pady=10)

    def list_tracks_clicked(self):
        track_list = lib.list_all()
        set_text(self.list_txt_view, track_list)

    def view_track(self):
        key = self.track_input.get()
        name = lib.get_name(key)
        if name is not None:
            artist = lib.get_artist(key)
            rating = lib.get_rating(key)
            play_count = lib.get_play_count(key)
            track_details = f"{name}\n{artist}\nRating: {rating}\nPlays: {play_count}"
            set_text(self.track_txt, track_details)
        else:
            messagebox.showerror("Error", f"Track {key} not found")


class CreatePlaylistTab:
    def __init__(self, parent, music_manager):
        self.parent = parent
        self.music_manager = music_manager
        self.playlists_file = music_manager.playlists_file
        self.create_widgets()

    def create_widgets(self):
        # Playlist Name
        self.playlist_name_label = tk.Label(self.parent, text="Playlist Name:")
        self.playlist_name_label.grid(row=0, column=0, padx=10, pady=5)

        self.playlist_name_entry = tk.Entry(self.parent, width=20)
        self.playlist_name_entry.grid(row=0, column=1, padx=10, pady=5)

        self.new_playlist_btn = tk.Button(self.parent, text="New Playlist", command=self.create_new_playlist)
        self.new_playlist_btn.grid(row=0, column=2, padx=10, pady=5)

        # Tracks
        self.list_tracks_btn = tk.Button(self.parent, text="List All Tracks", command=lambda: self.list_tracks_clicked(self.list_txt))
        self.list_tracks_btn.grid(row=1, column=0, padx=10, pady=5)

        self.list_txt = tkst.ScrolledText(self.parent, width=40, height=10, wrap="none")
        self.list_txt.grid(row=2, column=0, columnspan=3, padx=10, pady=5)

        self.track_number_label = tk.Label(self.parent, text="Enter Track Number:")
        self.track_number_label.grid(row=0, column=3, padx=10, pady=5)

        self.track_number_entry = tk.Entry(self.parent, width=10)
        self.track_number_entry.grid(row=0, column=4, padx=10, pady=5)

        self.add_track_btn = tk.Button(self.parent, text="Add Track", command=self.add_track_to_playlist)
        self.add_track_btn.grid(row=0, column=5, padx=10, pady=5)


        # Playlist Display
        self.playlist_lbl = tk.Label(self.parent, text="Current Playlist:")
        self.playlist_lbl.grid(row=1, column=2, columnspan=3, padx=10, pady=5)

        self.playlist_display = tkst.ScrolledText(self.parent, width=40, height=10, wrap="none")
        self.playlist_display.grid(row=2, column=3, columnspan=3, padx=10, pady=5)

        # Controls
        self.save_btn = tk.Button(self.parent, text="Save Playlist", command=self.save_playlists)
        self.save_btn.grid(row=3, column=3, padx=10, pady=5)

        self.load_btn = tk.Button(self.parent, text="Load Playlist", command=self.load_playlist_from_file)
        self.load_btn.grid(row=3, column=4, padx=10, pady=5)

        self.reset_btn = tk.Button(self.parent, text="Reset Playlist", command=self.reset_playlist)
        self.reset_btn.grid(row=3, column=5, padx=10, pady=5)

        self.status_lbl = tk.Label(self.parent, text="", font=("Helvetica", 10))
        self.status_lbl.grid(row=4, column=0, columnspan=3, sticky="W", padx=10, pady=5)

    def list_tracks_clicked(self, text_widget):
        track_list = lib.list_all()
        set_text(text_widget, track_list)

    def create_new_playlist(self):
        name = self.playlist_name_entry.get().strip()
        if name:
            if name not in self.music_manager.playlists:
                self.music_manager.playlists[name] = []
                self.music_manager.current_playlist_name = name
                self.update_playlist_display()
                self.status_lbl.config(text=f"New playlist '{name}' created.")
            else:
                self.status_lbl.config(text=f"Playlist '{name}' already exists.")
        else:
            self.status_lbl.config(text="Enter a valid playlist name.")

    def add_track_to_playlist(self):
        if self.music_manager.current_playlist_name is None:
            self.status_lbl.config(text="No playlist selected.")
            return

        key = self.track_number_entry.get()
        name = lib.get_name(key)
        if name:
            self.music_manager.playlists[self.music_manager.current_playlist_name].append(key)
            self.update_playlist_display()
            self.track_number_entry.delete(0, tk.END)
            self.status_lbl.config(text=f"Track {key} added to playlist '{self.music_manager.current_playlist_name}'.")
        else:
            self.status_lbl.config(text=f"Track {key} not found.")

    def save_playlists(self):
        try:
            with open(self.playlists_file, 'w') as f:
                json.dump(self.music_manager.playlists, f, indent=4)
            self.status_lbl.config(text="Playlists saved.")
        except Exception as e:
            self.status_lbl.config(text=f"Error saving playlists: {e}")

    def load_playlist_from_file(self):
        name = self.playlist_name_entry.get().strip()
        if name in self.music_manager.playlists:
            self.music_manager.current_playlist_name = name
            self.update_playlist_display()
            self.status_lbl.config(text=f"Playlist '{name}' loaded.")
        else:
            self.status_lbl.config(text=f"Playlist '{name}' not found.")

    def update_playlist_display(self):
        self.playlist_display.delete("1.0", tk.END)
        if self.music_manager.current_playlist_name:
            for key in self.music_manager.playlists[self.music_manager.current_playlist_name]:
                name = lib.get_name(key)
                artist = lib.get_artist(key)
                play_count = lib.get_play_count(key)
                self.playlist_display.insert(tk.END, f"{key}: {name} - {artist} (Play Count: {play_count})\n")

    def reset_playlist(self):
        if self.music_manager.current_playlist_name:
            self.music_manager.playlists[self.music_manager.current_playlist_name].clear()
            self.playlist_display.delete("1.0", tk.END)
            self.update_playlist_display()
            self.status_lbl.config(text=f"Playlist '{self.music_manager.current_playlist_name}' reset.")
        else:
            self.status_lbl.config(text="No playlist selected.")


class UpdateTrackTab:
    def __init__(self, parent):
        self.parent = parent
        self.create_widgets()

    def create_widgets(self):
        list_all_btn = tk.Button(self.parent, text="List All Tracks", command=lambda: self.list_tracks_clicked(self.list_txt_update))
        list_all_btn.grid(row=0, column=0, padx=10, pady=10)

        self.list_txt_update = tkst.ScrolledText(self.parent, width=48, height=10, wrap="none")
        self.list_txt_update.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

        self.track_number_lbl_update = tk.Label(self.parent, text="Enter Track Number:")
        self.track_number_lbl_update.grid(row=2, column=0, padx=5, pady=5)

        self.track_number_entry_update = tk.Entry(self.parent, width=5)
        self.track_number_entry_update.grid(row=2, column=1, padx=5, pady=5)

        self.rating_lbl = tk.Label(self.parent, text="Enter New Rating:")
        self.rating_lbl.grid(row=3, column=0, padx=5, pady=5)

        self.rating_entry = tk.Entry(self.parent, width=5)
        self.rating_entry.grid(row=3, column=1, padx=5, pady=5)

        self.update_btn = tk.Button(self.parent, text="Update Track", command=self.update_track)
        self.update_btn.grid(row=4, column=0, columnspan=2, pady=10)

    def list_tracks_clicked(self, text_widget):
        track_list = lib.list_all()
        set_text(text_widget, track_list)

    def update_track(self):
        key = self.track_number_entry_update.get()
        new_rating = self.rating_entry.get()
        try:
            new_rating = int(new_rating)
            if 0 <= new_rating <= 5:
                lib.set_rating(key, new_rating)
                name = lib.get_name(key)
                artist = lib.get_artist(key)
                play_count = lib.get_play_count(key)
                messagebox.showinfo("Success", f"Track {key} ({name} - {artist}) updated with rating {new_rating}, play count: {play_count}")
                current_dir = os.path.dirname(__file__)
                csv_path = os.path.join(current_dir, 'song_data.csv')
                lib.save_library(csv_path)
                track_list = lib.list_all()
                set_text(self.list_txt_update, track_list)
            else:
                messagebox.showerror("Error", "Rating must be between 0 and 5.")
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter integers for rating.")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")



class PlayTrackTab:
    def __init__(self, parent, music_manager):
        self.parent = parent
        self.music_manager = music_manager
        self.playlist = [] # Initialize playlist
        self.create_widgets()
        
        # Bind the FocusIn event to refresh playlists
        window.bind("<FocusIn>", lambda event: self.update_playlist_menu())


    def create_widgets(self):
        # Song Library Section
        self.library_label = tk.Label(self.parent, text="Song Library:")
        self.library_label.grid(row=0, column=0, padx=10, pady=5)

        self.library_listbox = tk.Listbox(self.parent, width=40, height=10)
        self.library_listbox.grid(row=1, column=0, padx=10, pady=5)

        self.play_library_button = tk.Button(self.parent, text="Play Selected Song", command=self.play_library_song)
        self.play_library_button.grid(row=2, column=0, padx=10, pady=5)

        # Playlist Selection Section
        self.playlist_label = tk.Label(self.parent, text="Playlists:")
        self.playlist_label.grid(row=0, column=1, padx=10, pady=5)

        self.playlist_dropdown = tk.StringVar(self.parent)
        self.playlist_menu = tk.OptionMenu(self.parent, self.playlist_dropdown, "")
        self.playlist_menu.grid(row=1, column=1, padx=10, pady=5)

        self.load_playlists_button = tk.Button(self.parent, text="Load Playlist", command=self.load_selected_playlist)
        self.load_playlists_button.grid(row=2, column=1, padx=10, pady=5)

        # Playlist Tracks Section
        self.playlist_tracks_label = tk.Label(self.parent, text="Playlist Tracks:")
        self.playlist_tracks_label.grid(row=0, column=2, padx=10, pady=5)

        self.playlist_listbox = tk.Listbox(self.parent, width=40, height=10)
        self.playlist_listbox.grid(row=1, column=2, padx=10, pady=5)

        self.play_playlist_song_button = tk.Button(self.parent, text="Play Selected Playlist Song", command=self.play_selected_playlist_song)
        self.play_playlist_song_button.grid(row=2, column=2, padx=10, pady=5)

        self.play_entire_playlist_button = tk.Button(self.parent, text="Play Entire Playlist", command=self.play_playlist)
        self.play_entire_playlist_button.grid(row=3, column=2, padx=10, pady=5)

        self.update_library_list()
        self.update_playlist_menu()

    def update_library_list(self):
        self.library_listbox.delete(0, tk.END)
        for key, item in lib.library.items():
            self.library_listbox.insert(tk.END, f"{key} - {item.name} - {item.artist}")

    def update_playlist_menu(self):
        try:
            with open(self.music_manager.playlists_file, 'r') as f:
                playlists = json.load(f)
                self.playlist_dropdown.set("")
                menu = self.playlist_menu['menu']
                menu.delete(0, 'end')
                for playlist_name in playlists.keys():
                    menu.add_command(label=playlist_name, command=lambda name=playlist_name: self.playlist_dropdown.set(name))
        except (FileNotFoundError, json.JSONDecodeError):
            messagebox.showerror("Error", "No playlists found or file is corrupted.")

    def load_selected_playlist(self):
        playlist_name = self.playlist_dropdown.get()
        if not playlist_name:
            messagebox.showwarning("Warning", "No playlist selected!")
            return

        try:
            with open(self.music_manager.playlists_file, 'r') as f:
                playlists = json.load(f)
                if playlist_name in playlists:
                    self.playlist = playlists[playlist_name]
                    self.update_playlist_list()
                    messagebox.showinfo("Success", f"Playlist '{playlist_name}' loaded successfully.")
                else:
                    messagebox.showerror("Error", f"Playlist '{playlist_name}' not found.")
        except (FileNotFoundError, json.JSONDecodeError):
            messagebox.showerror("Error", "Failed to load playlists.")

    def update_playlist_list(self):
        self.playlist_listbox.delete(0, tk.END)
        for key in self.playlist:
            item = lib.library.get(key, None)
            if item:
                self.playlist_listbox.insert(tk.END, f"{key} - {item.name} - {item.artist}")

    def play_library_song(self):
        selection = self.library_listbox.curselection()
        if selection:
            selected_track_text = self.library_listbox.get(selection[0])
            key = selected_track_text.split(" - ")[0]
            self.play_track_by_key(key)
        else:
            messagebox.showwarning("Warning", "No song selected!")

    def play_selected_playlist_song(self):
        selection = self.playlist_listbox.curselection()
        if selection:
            selected_track_text = self.playlist_listbox.get(selection[0])
            key = selected_track_text.split(" - ")[0]
            self.play_track_by_key(key)
        else:
            messagebox.showwarning("Warning", "No song selected!")

    def play_playlist(self):
        if not self.playlist:
            messagebox.showwarning("Warning", "No playlist loaded!")
            return

        for key in self.playlist:
            self.play_track_by_key(key)

    def play_track_by_key(self, key):
        youtube_link = lib.get_youtube_link(key)
        if youtube_link:
            webbrowser.open(youtube_link)
            lib.increment_play_count(key)
            self.update_library_list()
        else:
            messagebox.showerror("Error", "YouTube link not found for this track!")
    


class MusicManager:
    def __init__(self, window):
        window.geometry("1100x450")
        window.title("Music Manager")
        self.playlists = {}
        self.script_dir = os.path.dirname(__file__)
        self.playlists_file = os.path.join(self.script_dir, "playlists.json")
        self.current_playlist_name = None
        self.notebook = ttk.Notebook(window)
        self.notebook.pack(expand=True, fill="both")
        self.create_tabs(self.notebook)
        self.load_playlist()


    def create_tabs(self, notebook):
        view_tab = ttk.Frame(notebook)
        notebook.add(view_tab, text="View Track")
        self.view_tab = ViewTrackTab(view_tab)

        create_tab = ttk.Frame(notebook)
        notebook.add(create_tab, text="Create Playlist")
        self.create_tab = CreatePlaylistTab(create_tab, self)

        update_tab = ttk.Frame(notebook)
        notebook.add(update_tab, text="Update Track")
        self.update_tab = UpdateTrackTab(update_tab)

        play_tab = ttk.Frame(notebook)
        notebook.add(play_tab, text="Play Track")
        self.play_tab = PlayTrackTab(play_tab, self)

    def load_playlist(self):
        try:
            with open(self.playlists_file, 'r') as f:
                self.playlists = json.load(f)
        except FileNotFoundError:
            pass  # Ignore if file doesn't exist
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Error loading playlist: Invalid JSON format")
        except Exception as e:
            messagebox.showerror("Error", f"Error loading playlist: {e}")



if __name__ == "__main__":
    window = tk.Tk()
    fonts.configure()
    MusicManager(window)
    window.mainloop()