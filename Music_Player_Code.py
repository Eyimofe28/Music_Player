from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from mutagen.mp3 import MP3
import time
from tkinter import ttk
import pygame
import os


#  Comments are added to this code to make it more understandable.


def exit_code():
    exit()


class MusicPlayer:
    def __init__(self):
        pygame.mixer.init()
        self.stopped = False
        self.paused = False
        self.song_length = 0
        self.window = Tk()
        self.window.geometry("450x450")
        Icon = PhotoImage(file="music.png")
        self.window.iconphoto(True, Icon)
        self.window.title("MP3 MUSIC PLAYER")
        self.window.resizable(False, False)
        self.window.configure(bg="#200e38")

        self.menu_bar = Menu(self.window)
        self.window.config(menu=self.menu_bar)
        self.menu = Menu(self.menu_bar, tearoff=0, font=("MV Boli", 8))
        self.menu_bar.add_cascade(label="MENU", menu=self.menu)
        self.menu.add_command(label="Add Songs", command=self.add_song)
        self.menu.add_command(label="Delete Song", command=self.delete_song)
        self.menu.add_command(label="Clear Playlist", command=self.clear)
        self.menu.add_separator()
        self.menu.add_command(label="EXIT", foreground="red", command=exit_code)

        self.list_frame = Frame(self.window, bg="#200e38", highlightcolor="#200e38")
        self.list_frame.pack(pady=15)

        self.volume_frame = LabelFrame(self.list_frame, text='VOLUME', bg="#200e38", font=("MV Boli", 8),
                                       foreground='white', highlightcolor="#200e38")
        self.volume_frame.pack(side=LEFT, pady=5)
        self.volume_control = ttk.Scale(self.volume_frame, from_=1, to=0, orient=VERTICAL, state=DISABLED, length=130,
                                        cursor="dot", value=1, command=lambda value: self.volume())
        self.volume_control.pack(fill=Y)

        self.music_frame = Frame(self.list_frame, bg="#200e38", highlightcolor="#200e38")
        self.music_frame.pack(side=LEFT, padx=20)

        self.up_scroll = Scrollbar(self.music_frame, orient=VERTICAL)
        self.Music_box = Listbox(self.music_frame, fg="white", bg="black", width=65, height=13,
                                 selectbackground="#3c1869", yscrollcommand=self.up_scroll.set)
        self.up_scroll.pack(side=RIGHT, fill=Y)
        self.up_scroll.config(command=self.Music_box.yview)
        self.Music_box.pack(side=RIGHT)

        self.music_slider_label = Frame(self.window, bg="#200e38")
        self.music_slider_label.pack(pady=30)

        self.current_song = Label(self.window, bg="#200e38", fg="white")
        self.current_song.pack(side=TOP)

        self.song_position = Label(self.music_slider_label, bg="#200e38", fg="white")
        self.song_position.pack(side=LEFT)

        self.music_slider = ttk.Scale(self.music_slider_label, from_=0, to=100, orient=HORIZONTAL, state=DISABLED,
                                      length=365, command=lambda value: self.slide(), cursor="dot", value=0)
        self.music_slider.configure(style="")
        self.music_slider.pack(side=LEFT, padx=10)

        self.current_song_time = Label(self.music_slider_label, bg="#200e38", fg="white")
        self.current_song_time.pack(side=RIGHT)

        self.prev_image = PhotoImage(file="rewind.png")
        self.pause_image = PhotoImage(file="pause.png")
        self.play_image = PhotoImage(file="play.png")
        self.unpause_image = PhotoImage(file="resume.png")
        self.stop_image = PhotoImage(file="stop.png")
        self.next_image = PhotoImage(file="next.png")

        self.button_frame = Frame(self.window, bg="#200e38")
        self.button_frame.pack(pady=10)

        self.prev_button = Button(self.button_frame, image=self.prev_image, command=self.prev)
        self.pause_button = Button(self.button_frame, image=self.pause_image, command=self.pause)
        self.play_button = Button(self.button_frame, image=self.play_image, command=self.play)
        self.stop_button = Button(self.button_frame, image=self.stop_image, command=self.stop)
        self.next_button = Button(self.button_frame, image=self.next_image, command=self.nex)

        self.prev_button.grid(row=0, column=0, padx=9, pady=5)
        self.pause_button.grid(row=0, column=1, padx=9, pady=5)
        self.play_button.grid(row=0, column=2, padx=9, pady=5)
        self.stop_button.grid(row=0, column=4, padx=9, pady=5)
        self.next_button.grid(row=0, column=5, padx=9, pady=5)

    def add_song(self):
        path = filedialog.askdirectory()
        if path:
            os.chdir(path)
            songs = os.listdir(path)
            for song in songs:
                if song.endswith(".mp3"):
                    self.Music_box.insert(END, song)

    def delete_song(self):
        current_sng = self.Music_box.curselection()
        if current_sng:
            options = messagebox.askokcancel(message="This will delete your song permanently,"
                                                     " would you like to proceed?")
            if options:
                self.stop()
                self.Music_box.delete(current_sng)
        else:
            messagebox.showerror(title="ERROR", message="Please select a song to delete.")

    def clear(self):
        if self.Music_box.index(END) == 0:
            messagebox.showinfo(message="ALL CLEAR!")
        else:
            options = messagebox.askyesno(message="This will permanently clear your Music Player,"
                                                  " would you like to proceed?")
            if options:
                self.stop()
                self.Music_box.delete(0, END)
                self.play_button.config(state=ACTIVE)

    def len_of_song(self):
        song = self.Music_box.get(ACTIVE)
        mp3_song = MP3(song)
        self.song_length = mp3_song.info.length  # Gets length of song being played
        song_length_time_format = time.strftime("%M:%S", time.gmtime(int(self.song_length)))
        self.current_song_time.config(text=song_length_time_format)
        self.current_song_time.config(fg="white")
        self.song_position.config(fg="white")

    def play_time(self):
        if self.stopped:
            return
        current_sng = self.Music_box.get(ACTIVE)
        if current_sng == "":
            pass
        else:
            current_time = pygame.mixer.music.get_pos() / 1000  # get song time in seconds
            conv_current_time = time.strftime("%M:%S", time.gmtime(current_time))  # convert it to time format (Min:Sec)

            current_time += 1  # to make slider position time and current time equal

            if int(self.music_slider.get()) == int(self.song_length):
                self.current_song_time.config(fg="#200e38")
                self.song_position.config(fg="#200e38")
            elif self.music_slider.get() == int(current_time):
                self.song_position.config(text=conv_current_time)
                self.music_slider.config(to=int(self.song_length), value=int(current_time))
            elif self.paused:
                conv_current_time = time.strftime("%M:%S", time.gmtime(self.music_slider.get()))
                self.song_position.config(text=conv_current_time)
                pass
            else:
                self.music_slider.config(to=int(self.song_length), value=int(self.music_slider.get()))
                # Configures the value of the current song position to slider and makes it end where the song ends
                conv_current_time = time.strftime("%M:%S", time.gmtime(int(self.music_slider.get())))
                self.song_position.config(text=conv_current_time)
                slider_mover = int(self.music_slider.get()) + 1
                self.music_slider.config(value=slider_mover)

            self.song_position.after(1000, self.play_time)  # Updates current song position per second

    def play(self):
        self.stopped = False
        self.paused = False
        self.pause_button.config(image=self.pause_image)
        song = self.Music_box.curselection()
        if song:
            self.music_slider.config(value=0, state=ACTIVE)
            self.volume_control.config(state=ACTIVE)
            song = song[0]
            Song_name = self.Music_box.get(song)
            pygame.mixer.music.load(Song_name)
            pygame.mixer.music.play(loops=0, start=int(self.music_slider.get()))
            self.len_of_song()
            self.play_button.config(state=DISABLED)

            self.current_song.config(text=f"Song Playing: {self.Music_box.get(ACTIVE)}")
            # Displays the name of the song being played

            self.play_time()
        else:
            messagebox.showinfo(title="ERROR", message="No song selected. Please select a song to play.")

    def nex(self):
        try:
            self.stopped = False
            self.paused = False
            self.pause_button.config(image=self.pause_image)
            current_sng = self.Music_box.curselection()
            # curselection() returns a tuple of the position of the song being played in the list : (position,)

            next_song_index = current_sng[0] + 1
            next_song = self.Music_box.get(next_song_index)
            if next_song == "":
                self.stop()
                messagebox.showinfo(title="ERROR", message="No more songs to play.")
            else:
                self.music_slider.config(value=0, state=ACTIVE)
                pygame.mixer_music.load(next_song)
                pygame.mixer_music.play(loops=0)
                self.len_of_song()
                self.play_button.config(state=DISABLED)
                self.volume_control.config(state=ACTIVE)
                self.Music_box.selection_clear(0, END[0])  # CLEARS ACTIVE BAR FROM LIST BOX
                self.Music_box.activate(next_song_index)  # SETS ACTIVE BAR TO THE SONG BEING PLAYED

                self.Music_box.selection_set(next_song_index, last=None)
                # 'last = None' sets highlight to the current played song being played only

                self.current_song.config(text=f"Song Playing: {self.Music_box.get(ACTIVE)}")

                self.play_time()
        except IndexError:
            messagebox.showerror(title="ERROR", message="Please play a song first.")

    def prev(self):
        try:
            self.stopped = False
            self.paused = False
            self.pause_button.config(image=self.pause_image)
            current_sng = self.Music_box.curselection()
            next_song_index = current_sng[0] - 1
            next_song = self.Music_box.get(next_song_index)
            if next_song == "":
                self.stop()
                messagebox.showinfo(title="ERROR", message="No more songs to play.")
            else:
                self.music_slider.config(value=0, state=ACTIVE)
                pygame.mixer_music.load(next_song)
                pygame.mixer_music.play(loops=0)
                self.len_of_song()
                self.play_button.config(state=DISABLED)
                self.music_slider.config(to=int(self.song_length), value=0)
                self.volume_control.config(state=ACTIVE)
                self.Music_box.selection_clear(0, END[0])
                self.Music_box.activate(next_song_index)
                self.Music_box.selection_set(next_song_index, last=None)
                self.current_song.config(text=f"Song Playing: {self.Music_box.get(ACTIVE)}")

                self.play_time()
        except IndexError:
            messagebox.showerror(title="ERROR", message="Please play a song first.")

    def pause(self):
        song = self.Music_box.get(ACTIVE)
        if song:
            if self.paused:
                pygame.mixer.music.unpause()
                self.pause_button.config(image=self.pause_image)
                self.music_slider.config(state=ACTIVE)
                self.paused = False
            else:
                pygame.mixer.music.pause()
                self.pause_button.config(image=self.unpause_image)
                self.music_slider.config(state=DISABLED)
                self.paused = True
        else:
            pass

    def stop(self):
        pygame.mixer.music.stop()
        self.current_song_time.config(fg="#200e38")
        self.song_position.config(fg="#200e38")
        self.current_song.config(text='')
        self.play_button.config(state=ACTIVE)
        self.music_slider.config(value=0, state=DISABLED)
        self.volume_control.config(state=DISABLED)
        self.stopped = True

    def slide(self):
        try:
            song = self.Music_box.curselection()
            if song:
                song = song[0]
                Song_name = self.Music_box.get(song)
                pygame.mixer.music.load(Song_name)
                pygame.mixer.music.play(loops=0, start=int(self.music_slider.get()))
                self.current_song.config(text=f"Song Playing: {self.Music_box.get(ACTIVE)}")
                self.len_of_song()
        except TypeError:
            pass

    def volume(self):
        pygame.mixer.music.set_volume(self.volume_control.get())

    def run(self):
        try:
            self.window.mainloop()
        except KeyboardInterrupt:
            pass


MusicPlayer().run()
