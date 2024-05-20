import tkinter as tk
from tkinter import filedialog, ttk
import pygame
import time

class MusicPlayer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Music Player")
        self.geometry("600x500")
        self.configure(bg="#1a1a1a")

        # Initialize Pygame Mixer
        pygame.mixer.init()

        # Create UI elements
        self.create_menu()
        self.create_playlist()
        self.create_controls()
        self.create_progress_bar()
        self.create_volume_controls()

        # Bind events
        self.bind_events()

        # Start progress bar update
        self.update_progress_bar()

    def create_menu(self):
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        file_menu = tk.Menu(menubar)
        file_menu.add_command(label="Add Songs", command=self.add_songs)
        file_menu.add_command(label="Remove Selected", command=self.remove_song)
        menubar.add_cascade(label="File", menu=file_menu)

    def create_playlist(self):
        playlist_frame = tk.Frame(self, bg="#1a1a1a")
        playlist_frame.pack(padx=20, pady=20)

        self.playlist = tk.Listbox(playlist_frame, bg="#2c2c2c", fg="#ffffff", font=("Arial", 12), selectbackground="#4c4c4c", selectforeground="#ffffff", height=10, width=50)
        self.playlist.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(playlist_frame, orient=tk.VERTICAL, command=self.playlist.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.playlist.config(yscrollcommand=scrollbar.set)

    def create_controls(self):
        controls_frame = tk.Frame(self, bg="#1a1a1a")
        controls_frame.pack(pady=20)

        self.previous_button = tk.Button(controls_frame, text="Previous", bg="#000000", fg="#000000", font=("Arial", 12), width=10, command=self.previous_song)
        self.previous_button.grid(row=0, column=0, padx=10)

        self.play_button = tk.Button(controls_frame, text="Play", bg="#000000", fg="#000000", font=("Arial", 12), width=10, command=self.play_song)
        self.play_button.grid(row=0, column=1, padx=10)

        self.pause_button = tk.Button(controls_frame, text="Pause", bg="#000000", fg="#000000", font=("Arial", 12), width=10, command=self.pause_song)
        self.pause_button.grid(row=0, column=2, padx=10)

        self.stop_button = tk.Button(controls_frame, text="Stop", bg="#000000", fg="#000000", font=("Arial", 12), width=10, command=self.stop_song)
        self.stop_button.grid(row=0, column=3, padx=10)

        self.next_button = tk.Button(controls_frame, text="Next", bg="#000000", fg="#000000", font=("Arial", 12), width=10, command=self.next_song)
        self.next_button.grid(row=0, column=4, padx=10)

    def create_progress_bar(self):
        progress_bar_frame = tk.Frame(self, bg="#1a1a1a")
        progress_bar_frame.pack(padx=20, pady=10)

        self.progress_bar = ttk.Progressbar(progress_bar_frame, length=400, mode="determinate")
        self.progress_bar.pack(pady=10)

    def create_volume_controls(self):
        volume_frame = tk.Frame(self, bg="#1a1a1a")
        volume_frame.pack(padx=20, pady=10)

        self.volume_label = tk.Label(volume_frame, text="Volume", bg="#1a1a1a", fg="#ffffff", font=("Arial", 12))
        self.volume_label.grid(row=0, column=0, padx=10)

        self.volume_scale = tk.Scale(volume_frame, from_=0, to=100, orient=tk.HORIZONTAL, bg="#2c2c2c", fg="#ffffff", length=200, command=self.set_volume)
        self.volume_scale.set(50)
        self.volume_scale.grid(row=0, column=1, padx=10)

    def bind_events(self):
        self.playlist.bind("<<ListboxSelect>>", self.on_song_select)

    def add_songs(self):
        songs = filedialog.askopenfilenames(title="Select Songs", filetypes=[("Audio Files", "*.mp3 *.wav *.ogg")])
        for song in songs:
            self.playlist.insert(tk.END, song)

    def remove_song(self):
        selected_song = self.playlist.curselection()
        if selected_song:
            self.playlist.delete(selected_song[0])

    def on_song_select(self, event):
        selected_song = self.playlist.curselection()
        if selected_song:
            song_path = self.playlist.get(selected_song[0])
            pygame.mixer.music.load(song_path)

    def play_song(self):
        pygame.mixer.music.play()

    def pause_song(self):
        pygame.mixer.music.pause()

    def stop_song(self):
        pygame.mixer.music.stop()
        self.progress_bar["value"] = 0

    def previous_song(self):
        current_index = self.playlist.curselection()
        if current_index:
            new_index = (current_index[0] - 1) % self.playlist.size()
            self.playlist.selection_clear(0, tk.END)
            self.playlist.selection_set(new_index)
            self.playlist.activate(new_index)
            self.on_song_select(None)
            self.play_song()

    def next_song(self):
        current_index = self.playlist.curselection()
        if current_index:
            new_index = (current_index[0] + 1) % self.playlist.size()
            self.playlist.selection_clear(0, tk.END)
            self.playlist.selection_set(new_index)
            self.playlist.activate(new_index)
            self.on_song_select(None)
            self.play_song()

    def set_volume(self, value):
        volume = int(value) / 100
        pygame.mixer.music.set_volume(volume)

    def update_progress_bar(self):
        try:
            selected_song = self.playlist.curselection()
            if selected_song:
                current_time = pygame.mixer.music.get_pos() / 1000
                song_path = self.playlist.get(selected_song[0])
                song_length = pygame.mixer.Sound(song_path).get_length()
                progress = (current_time / song_length) * 100
                self.progress_bar["value"] = progress
                self.progress_bar.after(1000, self.update_progress_bar)
        except pygame.error:
            pass

if __name__ == "__main__":
    app = MusicPlayer()
    app.mainloop()