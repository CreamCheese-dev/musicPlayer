import os
import tkinter as tk
from tkinter import ttk  # For the slider (volume control)
import pygame
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC
from PIL import Image, ImageTk
import io

class MusicPlayer:
    def __init__(self, window):
        window.geometry('1024x768')
        window.title('Music Player')
        self.current_song_playing = None
        self.music_file = False
        self.playing_state = False
        pygame.mixer.init()

        self.playlist_box = tk.Listbox(window, width=50, height=15, font=('Arial', 12))
        self.song_paths = {}

        # Album Art section
        self.album_art_frame = tk.Frame(window, height=200, width=200)
        self.album_art_frame.pack(side='top', fill='both', expand=True)
        self.album_art_label = tk.Label(self.album_art_frame)
        self.album_art_label.pack(side='top', fill='both', expand=True)

        # Song and Artist details section
        self.details_frame = tk.Frame(window)
        self.details_frame.pack(side='top', fill='x', expand=False)

        self.song_label = tk.Label(self.details_frame, text='Song Name: ')
        self.song_label.pack(side='top', fill='x')

        self.artist_label = tk.Label(self.details_frame, text='Artist: ')
        self.artist_label.pack(side='top', fill='x')

        # Load relative dir
        self.relative_dir = 'audio'
        for root, dirs, files in os.walk(self.relative_dir):
            for song in files:
                full_path = os.path.abspath(os.path.join(root, song))
                self.song_paths[song] = full_path
                self.playlist_box.insert(tk.END, song)

        self.playlist_box.pack(padx=10, pady=10)
        self.playlist_box.bind('<<ListboxSelect>>', self.on_select)

        # Buttons and Volume Control frame
        controls_frame = tk.Frame(window)
        controls_frame.pack(side=tk.BOTTOM, pady=10)

        # Buttons
        self.play_button = tk.Button(controls_frame, text='Play', width=10, font=('Arial', 14), command=self.play)
        self.play_button.pack(side=tk.LEFT, padx=10)

        self.pause_button = tk.Button(controls_frame, text='Pause', width=10, font=('Arial', 14), command=self.pause)
        self.pause_button.pack(side=tk.LEFT, padx=10)

        # Volume Control
        self.volume_slider = ttk.Scale(controls_frame, from_=0, to=1, orient=tk.HORIZONTAL, value=0.5, command=self.set_volume)
        self.volume_slider.pack(side=tk.LEFT, fill='x', padx=10)
        pygame.mixer.music.set_volume(0.5)  # Set the initial volume to 50%

    def set_volume(self, val):
        volume = float(val)
        pygame.mixer.music.set_volume(volume)

    def on_select(self, event):
        index = self.playlist_box.curselection()[0]
        selected_song = self.playlist_box.get(index)
        song_path = self.song_paths.get(selected_song)

        self.current_song_playing = song_path

        pygame.mixer.music.load(song_path)
        pygame.mixer.music.play(loops=0)
        self.playing_state = True

        filename = os.path.basename(song_path).replace('.mp3', '')
        if ' - ' in filename:
            artist, song = filename.split(' - ', 1)
        else:
            artist = 'Unknown'
            song = filename

        self.song_label.config(text=f'Song Name: {song}')
        self.artist_label.config(text=f'Artist: {artist}')

        try:
            audio_file = MP3(song_path, ID3=ID3)
            if 'APIC:' in audio_file:
                album_art = audio_file['APIC:'].data
                image = Image.open(io.BytesIO(album_art))
                image.thumbnail((200, 200), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                self.album_art_label.config(image=photo)
                self.album_art_label.image = photo  # Keep a reference
            else:
                self.album_art_label.config(image='')
                self.album_art_label.image = None
        except Exception as e:
            print(f"Error processing the MP3 file: {e}")
            self.album_art_label.config(image='')
            self.album_art_label.image = None

    def play(self):
        if not self.playing_state:
            pygame.mixer.music.play(loops=0)
            self.playing_state = True

    def pause(self):
        if self.playing_state:
            pygame.mixer.music.pause()
            self.playing_state = False
        else:
            pygame.mixer.music.unpause()
            self.playing_state = True

root = tk.Tk()
app = MusicPlayer(root)
root.mainloop()
