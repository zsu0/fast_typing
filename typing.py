import tkinter as tk
import random
import time
from lexical import words_by_level

PARAGRAPH_SIZE = 10
VISIBLE_PARAGRAPHS = 2
TEST_DURATION = 60  # seconds

def generate_words(total=100):
    words = []
    for _ in range(total):
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
        self.master.title("Fast Typing Speed Test")
        self.master.geometry("800x400")

        self.words = generate_words()
        self.paragraphs = [self.words[i:i+PARAGRAPH_SIZE] for i in range(0, len(self.words), PARAGRAPH_SIZE)]
        self.current_paragraph_index = 0
        self.current_word_index = 0
        self.correct_count = 0
        self.start_time = None
        self.timer_running = False

        self.title = tk.Label(master, text="Typing Speed Tester", font=("Arial", 20))
        self.title.pack(pady=10)

        self.display_frame = tk.Frame(master)
        self.display_frame.pack()

        self.text_labels = []
        for _ in range(VISIBLE_PARAGRAPHS):
            label = tk.Label(self.display_frame, text="", font=("Arial", 16), wraplength=750, justify="left", anchor="w")
            label.pack(anchor="w", pady=5)
            self.text_labels.append(label)

        self.input_entry = tk.Entry(master, font=("Arial", 18))
        self.input_entry.pack(pady=10)
        self.input_entry.bind("<space>", self.check_word)
        self.input_entry.focus()

        self.result_label = tk.Label(master, text="", font=("Arial", 14))
        self.result_label.pack(pady=10)

        self.try_again_btn = tk.Button(master, text="Try Again", font=("Arial", 14), command=self.reset, state="disabled")
        self.try_again_btn.pack(pady=5)

        self.update_display()

        self.master.after(1000, self.check_timer)

    def update_display(self):
        for i in range(VISIBLE_PARAGRAPHS):
            index = self.current_paragraph_index + i
            if index < len(self.paragraphs):
                paragraph = self.paragraphs[index]
                text = " ".join(paragraph)
                if index == self.current_paragraph_index:
                    text = f"[{text}]"
                self.text_labels[i].config(text=text)
            else:
                self.text_labels[i].config(text="")

    def check_word(self, event):
        if not self.timer_running:
            self.start_time = time.time()
            self.timer_running = True

        typed = self.input_entry.get().strip()
        self.input_entry.delete(0, tk.END)

        current_paragraph = self.paragraphs[self.current_paragraph_index]
        if self.current_word_index < len(current_paragraph):
            target_word = current_paragraph[self.current_word_index]
            if typed == target_word:
                self.correct_count += 1
            self.current_word_index += 1

        if self.current_word_index >= PARAGRAPH_SIZE:
            self.current_paragraph_index += 1
            self.current_word_index = 0
            self.update_display()

        return "break"

    def check_timer(self):
        if self.timer_running:
            elapsed = time.time() - self.start_time
            if elapsed >= TEST_DURATION:
                self.end_test()
        self.master.after(100)

    def end_test(self):
        self.timer_running = False
        self.input_entry.config(state="disabled")
        wpm = self.correct_count
        self.result_label.config(text=f"Time's up!\nWPM: {wpm}\nCorrect words: {self.correct_count}")
        self.try_again_btn.config(state="normal")
        self.prompt_name_and_record(wpm)

    def prompt_name_and_record(self, wpm):
        def save_name():
            name = name_entry.get().strip()
            if name and name not in self.load_leaderboard():
                with open("leaderboard.txt", "a") as f:
                    f.write(f"{name},{wpm}\n")
            top.destroy()

        top = tk.Toplevel(self.master)
        top.title("Save to Leaderboard")
        tk.Label(top, text="Enter your name for the leaderboard:").pack(pady=5)
        name_entry = tk.Entry(top, font=("Arial", 14))
        name_entry.pack(pady=5)
        tk.Button(top, text="Submit", command=save_name).pack(pady=5)

    def load_leaderboard(self):
        try:
            with open("leaderboard.txt", "r") as f:
                return set(line.split(",")[0] for line in f)
        except FileNotFoundError:
            return set()

    def reset(self):
        self.words = generate_words()
        self.paragraphs = [self.words[i:i+PARAGRAPH_SIZE] for i in range(0, len(self.words), PARAGRAPH_SIZE)]
        self.current_paragraph_index = 0
        self.current_word_index = 0
        self.correct_count = 0
        self.start_time = None
        self.timer_running = False
        self.input_entry.config(state="normal")
        self.input_entry.delete(0, tk.END)
        self.result_label.config(text="")
        self.try_again_btn.config(state="disabled")
        self.update_display()
        self.input_entry.focus()

if __name__ == "__main__":
    root = tk.Tk()
    app = TypeSpeedTester(root)
    root.mainloop()
