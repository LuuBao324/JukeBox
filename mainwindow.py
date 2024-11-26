import tkinter as tk
import tkinter.scrolledtext as tkst
import tkinter.ttk as ttk
import track_library as lib #Make sure this file is in the same directory and correctly implemented.
import font_manager as fonts
import os
import json
import webbrowser
from tkinter import messagebox

def set_text(text_area, content):
    text_area.delete("1.0", tk.END)
    text_area.insert(1.0, content)

class MusicManager:
    def __init__(self, window):
        window.geometry("600x500")
        window.title("Music Manager")
        self.playlist = []
        self.script_dir = os.path.dirname(__file__)
        self.playlist_file = os.path.join(self.script_dir, "playlist.json")
        self.notebook = ttk.Notebook(window)
        self.notebook.pack(expand=True, fill="both")
        self.create_tabs(self.notebook)
        self.load_playlist()

    def create_tabs(self, notebook):
        self.create_view_tab(notebook)
        self.create_create_tab(notebook)
        self.create_update_tab(notebook)
        self.create_play_tab(notebook)

    def create_view_tab(self, notebook):
        view_tab = ttk.Frame(notebook)
        notebook.add(view_tab, text="View Track")
        
        enter_lbl = tk.Label(view_tab, text="Enter Track Number:")
        enter_lbl.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.track_input = tk.Entry(view_tab, width=5)
        self.track_input.grid(row=0, column=1, padx=10, pady=10)
        view_btn = tk.Button(view_tab, text="View Track", command=self.view_track)
        view_btn.grid(row=0, column=2, padx=10, pady=10)
        self.track_txt = tkst.ScrolledText(view_tab, width=48, height=10, wrap="none")
        self.track_txt.grid(row=1, column=0, columnspan=3, padx=10, pady=10)


    def create_create_tab(self, notebook):
        create_tab = ttk.Frame(notebook)
        notebook.add(create_tab, text="Create Playlist")

        self.track_number_label = tk.Label(create_tab, text="Enter Track Number:")
        self.track_number_label.grid(row=0, column=0, padx=5, pady=5)
        self.track_number_entry = tk.Entry(create_tab, width=5)
        self.track_number_entry.grid(row=0, column=1, padx=5, pady=5)
        self.add_track_btn = tk.Button(create_tab, text="Add Track", command=self.add_track)
        self.add_track_btn.grid(row=0, column=2, padx=5, pady=5)
        self.playlist_lbl = tk.Label(create_tab, text="Playlist:")
        self.playlist_lbl.grid(row=1, column=0, columnspan=3, padx=5, pady=5)

        self.playlist_display = tkst.ScrolledText(create_tab, width=48, height=10, wrap="none")
        self.playlist_display.grid(row=2, column=0, columnspan=3, padx=5, pady=5)
        self.play_btn = tk.Button(create_tab, text="Play Playlist", command=self.play_playlist)
        self.play_btn.grid(row=3, column=0, padx=5, pady=5)
        self.reset_btn = tk.Button(create_tab, text="Reset Playlist", command=self.reset_playlist)
        self.reset_btn.grid(row=3, column=1, padx=5, pady=5)
        self.save_btn = tk.Button(create_tab, text="Save Playlist", command=self.save_playlist)
        self.save_btn.grid(row=3, column=2, padx=5, pady=5)

    def create_update_tab(self, notebook):
        update_tab = ttk.Frame(notebook)
        notebook.add(update_tab, text="Update Track")
        list_all_btn = tk.Button(update_tab, text="List All Tracks", command=self.list_tracks_clicked)
        list_all_btn.grid(row=0, column=0, padx=10, pady=10)
        self.list_txt = tkst.ScrolledText(update_tab, width=48, height=10, wrap="none")
        self.list_txt.grid(row=1, column=0, columnspan=3, padx=10, pady=10)
        self.track_number_lbl_update = tk.Label(update_tab, text="Enter Track Number:")
        self.track_number_lbl_update.grid(row=2, column=0, padx=5, pady=5)
        self.track_number_entry_update = tk.Entry(update_tab, width=5)
        self.track_number_entry_update.grid(row=2, column=1, padx=5, pady=5)
        self.rating_lbl = tk.Label(update_tab, text="Enter New Rating:")
        self.rating_lbl.grid(row=3, column=0, padx=5, pady=5)
        self.rating_entry = tk.Entry(update_tab, width=5)
        self.rating_entry.grid(row=3, column=1, padx=5, pady=5)
        self.update_btn = tk.Button(update_tab, text="Update Track", command=self.update_track)
        self.update_btn.grid(row=4, column=0, columnspan=2, pady=10)


    def create_play_tab(self, notebook):
        play_tab = ttk.Frame(notebook)
        notebook.add(play_tab, text="Play Track")
        self.track_listbox = tk.Listbox(play_tab, width=100)
        self.track_listbox.pack(pady=10)
        self.update_track_list()
        play_button = tk.Button(play_tab, text="Play Selected Track", command=self.play_selected_track)
        play_button.pack()
        play_playlist_button = tk.Button(play_tab, text="Play Playlist", command=self.play_playlist)
        play_playlist_button.pack()
        

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
        else:
            messagebox.showerror("Error", f"Track {key} not found.")

    def play_playlist(self):
        for key in self.playlist:
            self.play_track_by_key(key)
        messagebox.showinfo("Playlist", "Playlist played.")
        current_dir = os.path.dirname(__file__)
        csv_path = os.path.join(current_dir, 'song_data.csv')
        lib.save_library(csv_path)

    def save_playlist(self):
        try:
            with open(self.playlist_file, 'w') as f:
                json.dump(self.playlist, f, indent=4)
            messagebox.showinfo("Success", f"Playlist saved to {self.playlist_file}")
        except Exception as e:
            messagebox.showerror("Error", f"Error saving playlist: {e}")

    def load_playlist(self):
        try:
            with open(self.playlist_file, 'r') as f:
                self.playlist = json.load(f)
                self.update_playlist_display()
        except FileNotFoundError:
            pass
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Error loading playlist: Invalid JSON format")
        except Exception as e:
            messagebox.showerror("Error", f"Error loading playlist: {e}")

    def reset_playlist(self):
        self.playlist.clear()
        self.playlist_display.delete("1.0", tk.END)
        self.update_playlist_display()
        messagebox.showinfo("Playlist", "Playlist reset.")

    def update_playlist_display(self):
        self.playlist_display.delete("1.0", tk.END)
        for key in self.playlist:
            name = lib.get_name(key)
            artist = lib.get_artist(key)
            play_count = lib.get_play_count(key)
            self.playlist_display.insert(tk.END, f"{key}: {name} - {artist} (Play Count: {play_count})\n")


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
                csv_path = os.path.join(current_dir, 'songs.csv')
                lib.save_library(csv_path)
                track_list = lib.list_all()
                set_text(self.list_txt, track_list)
            else:
                messagebox.showerror("Error", "Rating must be between 0 and 5.")
        except ValueError:
            messagebox.showerror("Error", "Invalid rating input. Please enter a number.")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    def play_track_by_key(self, key):
        youtube_link = lib.get_youtube_link(key)
        if youtube_link:
            webbrowser.open(youtube_link)
            lib.increment_play_count(key)
            self.update_playlist_display()
        else:
            messagebox.showerror("Error", "YouTube link not found for this track!")

    def update_track_list(self):
        self.track_listbox.delete(0, tk.END)
        for key, item in lib.library.items():
            self.track_listbox.insert(tk.END, f"{key} - {item.name} - {item.artist}")

    def play_selected_track(self):
        selection = self.track_listbox.curselection()
        if selection:
            selected_track_text = self.track_listbox.get(selection[0])
            key = str(selected_track_text.split(" - ")[0])
            self.play_track_by_key(key)
        else:
            messagebox.showwarning("Warning", "No track selected!")

if __name__ == "__main__":
    window = tk.Tk()
    fonts.configure()
    MusicManager(window)
    window.mainloop()