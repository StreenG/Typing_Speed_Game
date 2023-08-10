import csv
import random
import tkinter.messagebox
from tkinter import *
import time


# ------------- Screen making --------------
class speedtestgame():
    def __init__(self):
        self.screen = Tk()
        self.screen.title("Typing Speed Game")
        self.screen.geometry("330x200")
        self.screen.config(padx=20, pady=10, bg="#303030")

        # call start_screen
        self.start_screen()
        # call screen.mainloop so the screen wont close.
        self.screen.mainloop()

    # ------------- Function for starting game when the difficulty is pressed. --------------
    def start_game(self, difficulty):
        self.screen.geometry("510x500")
        self.random_words_list = []
        r_words_formatted = ""
        # opening the csv.data (words for the game) and adding them to a list, then taking a random line from it.
        with open("words.csv", "r") as csv_data:
            data = csv.reader(csv_data)
            game_script_words_list = [row for row in data]
            # for loop to get 20 random words and put them in a list, then write them on the label.
            for _ in range(25):
                r_words = random.choice(game_script_words_list)
                self.random_words_list.append(r_words)
                r_words_formatted += "".join(r_words) + " "
        self.timer_label = Label(self.screen, text="TIME: 0s", font=("Helvetica", 12, "bold"), fg="#FFC107", bg="#303030")
        self.timer_label.grid(row=0, column=0, sticky="nw")

        self.accuracy_label = Label(self.screen, text="Accuracy: 100% ", font=("Helvetica", 12, "bold"), fg="#FFC107",bg="#303030")
        self.accuracy_label.grid(row=0, column=0, sticky="ne")

        self.WPM_Label = Label(self.screen, text="WPM: 0 ", font=("Helvetica", 12, "bold"), fg="#FFC107", bg="#303030")
        self.WPM_Label.grid(row=0, column=0, sticky="n")

        self.text_box = Text(self.screen, width=30, height=10, font=("Helvetica", 22, "bold"), wrap="word")
        self.text_box.grid(row=1, column=0, pady=5)
        self.text_box.insert("end", r_words_formatted)
        #this is a way to put a tag on this Text so whenever it "matches" the color turns green, mismatch turns red.
        self.text_box.tag_configure("match", foreground="green")
        self.text_box.tag_configure("mismatch", foreground="red")

        self.enter_text_label = Label(self.screen, text="WRITE BELOW:", font=("Helvetica", 12, "bold"), bg="#303030",fg="#FFC107")
        self.enter_text_label.grid(row=2, column=0, sticky="nw")

        self.timer_help_label = Label(self.screen, text="Timer starts once you begin to write", font=("Helvetica", 10, "bold"), bg="#303030",fg="#D3D3D3")
        self.timer_help_label.grid(row=2, column=0, sticky="ne")

        self.user_entry_text = Entry(self.screen, width=32, font=("Helvetica", 20, "bold"))
        self.user_entry_text.grid(row=3, column=0)

        ## calling event to functions (key presses) - space, backspace, etc.
        self.user_entry_text.bind("<KeyRelease>",self.check_words)
        self.user_entry_text.bind("<space>", self.check_space)
        self.user_entry_text.bind("<BackSpace>", self.backspace)

        self.restart_btn = Button(self.screen, text="RESTART", fg="#D3D3D3", bg="#303030", font=("Helvetica", 12, "bold"), command=self.restart_game)
        self.restart_btn.grid(row=4, column=0, pady=5, sticky="se")


        # Game variables
        self.built_words_string = ""
        self.time_secs = 60
        self.start_countdown = False
        self.mistakes = 0
        self.WPM = 0
        self.accuracy = 0
        self.count = 0
        self.high_score = 0


        self.check_words()
    # ------------- The main function for checking the words, basically comparing the user input and the random words. -------------
    def check_words(self, event=None):
        self.start_timer()
        self.user_input = self.built_words_string + self.user_entry_text.get()
        text_content = self.text_box.get("1.0", "end-1c")
        # check if the characters in index 0 (user_input) match the characters in 1.0(text_content) if true, then they turn green, else, red.
        length = min(len(self.user_input), len(text_content))
        self.mistakes = 0
        for i in range(length):
            if self.user_input[i] == text_content[i]:
                self.text_box.tag_add("match", f"1.{i}", f"1.{i + 1}")


            elif self.user_input[i] != text_content[i]:
                self.text_box.tag_add("mismatch", f"1.{i}", f"1.{i + 1}")
                self.mistakes += 1
        # if player finishes the words, end game.
        if len(self.user_input) == len(text_content):
            self.start_countdown = False
            tkinter.messagebox.showinfo(title="Game Over", message=f"Score: {self.WPM} WPM! \n "
                                                                   f"Accuracy: {self.accuracy}%\n"
                                                                   f"In {self.count} Seconds!\n"
                                                                   f"With {self.mistakes} Mistakes")
            if self.WPM > self.high_score and self.accuracy > 80:
                with open("highscore.csv", "w") as csv_data:
                    csv_data.write(str(self.WPM))

    # function that reacts whenever the user presses space, clearing the entry_text and inserting the word that the user built before space is pressed
    def check_space(self, event):
        if event.keysym == 'space':
            # insert the built words to the user entry, thus enabling the user_entry not affect the length of the word and resetting the index.
            self.built_words_string += self.user_entry_text.get()
            self.user_entry_text.delete(0, 'end')


    #function that works whenever a user backspaces, it deletes and reinserts the word.
    def backspace(self, event):
        current_input = self.user_entry_text.get() + self.built_words_string
        length = len(current_input)
        text_content = self.text_box.get("1.0", "end-1c")
        char_to_insert = text_content[length - 1]
        self.text_box.delete(f"1.{length - 1}")
        self.text_box.insert(f"1.{length - 1}", char_to_insert)

    #function that does the count down from 60 to 0
    def count_down(self, count):
        if self.start_countdown == True:
            self.screen.after_id = self.screen.after(1000, self.count_down, count+1)
            self.timer_label.config(text=f"TIME: {count}s")
            self.calc_score(count=count)
    #function that starts the count_down if text isn't empty
    def start_timer(self):
        self.user_input = self.built_words_string + self.user_entry_text.get()
        if any(char.strip() for char in self.user_input) and not self.start_countdown:
            self.start_countdown = True
            self.count_down(0)
        elif len(self.user_input) == 0:
            self.start_countdown = False

    #function that calculates the words per minute
    def calc_score(self, count):
        self.count = count
        text_content = self.text_box.get("1.0", "end-1c")
        textlen = len(text_content)
        words_typed = len(self.built_words_string)
        if count > 0:
            self.WPM = (words_typed / 5) / (count / 60)
            self.WPM = int(self.WPM)
            self.accuracy = ((textlen - self.mistakes) / textlen) * 100
            self.WPM_Label.config(text=f"WPM: {self.WPM:.0f}")
            self.accuracy_label.config(text=f"Accuracy: {self.accuracy:.2f}%")

    def restart_game(self):
        elements_to_destroy = [
            self.timer_label,
            self.accuracy_label,
            self.WPM_Label,
            self.text_box,
            self.enter_text_label,
            self.timer_help_label,
            self.user_entry_text,
            self.restart_btn
        ]
        for e in elements_to_destroy:
            e.destroy()
        self.start_screen()
    # ------------- Starting Screen --------------
    def start_screen(self):
        self.screen.geometry("330x200")
        self.screen.config(padx=12, pady=10, bg="#303030")

        with open("highscore.csv", "r") as csv_data:
            data = csv.reader(csv_data)
            for row in data:
                self.high_score = ','.join(row)

        self.lbl = Label(self.screen, text="TYPING SPEED GAME", font=("Helvetica", 22, "bold"), bg="#303030",
                         fg="#FAFAFA")
        self.lbl.grid(row=0, column=0)
        self.other_lbl = Label(self.screen, text="Type as FAST as you can!", font=("Helvetica", 12, "bold"), bg="#303030",fg="#FFFFFF")
        self.other_lbl.grid(row=1, column=0, pady=10)

        self.high_score_lbl = Label(self.screen, text=f"Curent high score: {self.high_score} WPM!", font=("Helvetica", 16, "bold"), bg="#303030",fg="#FFD700")
        self.high_score_lbl.grid(row=2, column=0)


        self.start_game_btn = Button(self.screen,width=15,  text="START GAME!", bg="black", fg="#00A859",
                                     font=("Helvetica", 17, "bold"),
                                     command=lambda: [self.start_game("easy"), self.lbl.destroy(),
                                                      self.other_lbl.destroy(), self.start_game_btn.destroy(), self.high_score_lbl.destroy()])
        self.start_game_btn.grid(row=3, column=0, pady=10)

speedtestgame()
