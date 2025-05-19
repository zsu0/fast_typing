import tkinter as tk
import random
import time
from lexical import words_by_level

# Word distribution based on drop rates
def generate_words(count=20):
    words = []
    for _ in range(count):
        rand = random.random()
        if rand < 0.45:
            level = 'A'
        elif rand < 0.85:
            level = 'B'
        else:
            level = 'C'
        words.append(random.choice(words_by_level[level]))
    return words

class TypeSpeedTester:
    def __init__(self, master):
        self.master = master
        self.master.title("Type Speed Tester")
        self.master.geometry("700x300")

        self.words = generate_words()
        self.current_word_index = 0
        self.start_time = None
        self.correct_count = 0

        self.title = tk.Label(master, text="Typing Speed Tester", font=("Arial", 20))
        self.title.pack(pady=10)

        self.words_display = tk.Label(master, text=" ".join(self.words), font=("Arial", 16), wraplength=680, justify="center")
        self.words_display.pack(pady=10)

        self.input_entry = tk.Entry(master, font=("Arial", 18))
        self.input_entry.pack(pady=10)
        self.input_entry.bind("<space>", self.check_word)
        self.input_entry.focus()

        self.result_label = tk.Label(master, text="", font=("Arial", 16))
        self.result_label.pack(pady=10)

        self.reset_button = tk.Button(master, text="Restart", font=("Arial", 14), command=self.reset)
        self.reset_button.pack(pady=10)

    def check_word(self, event):
        if self.start_time is None:
            self.start_time = time.time()

        typed_word = self.input_entry.get().strip()
        current_word = self.words[self.current_word_index]

        # Only proceed if the typed word exactly matches the current word
        if typed_word == current_word:
            self.correct_count += 1
            self.current_word_index += 1
            self.input_entry.delete(0, tk.END)
    
            if self.current_word_index >= len(self.words):
                elapsed_time = time.time() - self.start_time
                wpm = (self.correct_count / elapsed_time) * 60
                self.result_label.config(
                    text=f"Done!\nWPM: {wpm:.2f}\nCorrect words: {self.correct_count}/{len(self.words)}")
                self.input_entry.config(state='disabled')
            else:
                self.highlight_current_word()
        else:
            # Word is incorrect – do not allow advance
            self.input_entry.config(fg="red")
            self.master.after(150, lambda: self.input_entry.config(fg="black"))
    
        return "break"

    def highlight_current_word(self):
        highlighted_words = []
        for i, word in enumerate(self.words):
            if i == self.current_word_index:
                highlighted_words.append(f"[{word}]")
            else:
                highlighted_words.append(word)
        self.words_display.config(text=" ".join(highlighted_words))

    def reset(self):
        self.words = generate_words()
        self.current_word_index = 0
        self.start_time = None
        self.correct_count = 0
        self.input_entry.config(state='normal')
        self.input_entry.delete(0, tk.END)
        self.result_label.config(text="")
        self.highlight_current_word()
        self.input_entry.focus()

if __name__ == '__main__':
    root = tk.Tk()
    app = TypeSpeedTester(root)
    root.mainloop()
