import time,sys
import tkinter as tk
from tkinter.filedialog import askopenfilename
from Game import Game
from Definitions import Color,Direction
from Timeline import generate_timeline
from  MusicData import MusicData

def main():
    root = tk.Tk()
    root.withdraw()
    filename = askopenfilename()
    g = Game(filename)
    list_of_music_data = generate_timeline(filename)
    for one_set in list_of_music_data:
        g.add_music_data(one_set[0],one_set[1],one_set[2])
    g.game_intro()   

if __name__ == '__main__':
    main()      
sys.exit()
