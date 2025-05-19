import tkinter as tk
import random
import time
from lexical import words_by_level

class TypingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Fast Typing")
        self.root.geometry("800x400")

        self.level = 1
        self.words = words_by_level[self.level]
        self.paragraphs = [self.words[i:i+10] for i in range(0, len(self.words), 10)]
        self.current_paragraph_index = 0
        self.current_word_index = 0
        self.correct_words = 0
        self.start_time = None
        self.time_limit = 60  # 1 minute
        self.timer_running = False
        self.leaderboard = []

        self.create_widgets()
        self.load_paragraphs()

    def create_widgets(self):
        self.text_frame = tk.Frame(self.root)
        self.text_frame.pack(pady=10)

        self.paragraph_labels = [tk.Label(self.text_frame, text="", font=("Arial", 16)) for _ in range(2)]
        for label in self.paragraph_labels:
            label.pack(anchor="w")

        self.entry = tk.Entry(self.root, font=("Arial", 16))
        self.entry.pack(pady=10)
        self.entry.bind("<KeyRelease>", self.check_word)

        self.timer_label = tk.Label(self.root, text="Time: 60", font=("Arial", 14))
        self.timer_label.pack()

        self.result_label = tk.Label(self.root, text="", font=("Arial", 16))
        self.result_label.pack(pady=10)

        self.leaderboard_frame = tk.Frame(self.root)
        self.leaderboard_frame.pack(pady=10)

    def load_paragraphs(self):
        for i in range(2):
            idx = self.current_paragraph_index + i
            if idx < len(self.paragraphs):
                self.paragraph_labels[i].config(text=self.format_paragraph(self.paragraphs[idx]))
            else:
                self.paragraph_labels[i].config(text="")

    def format_paragraph(self, paragraph):
        words = paragraph.copy()
        if self.current_word_index < len(words) and self.current_paragraph_index == self.paragraphs.index(paragraph):
            words[self.current_word_index] = f"[{words[self.current_word_index]}]"
        return " ".join(words)

    def check_word(self, event):
        if not self.timer_running:
            self.start_timer()
            self.start_time = time.time()

        typed_word = self.entry.get().strip()
        current_paragraph = self.paragraphs[self.current_paragraph_index]
        current_word = current_paragraph[self.current_word_index]

        # Check for premature typing or wrong typing
        if not current_word.startswith(typed_word):
            self.entry.delete(len(typed_word)-1, tk.END)
            return

        if typed_word == current_word:
            self.correct_words += 1
            self.current_word_index += 1
            self.entry.delete(0, tk.END)

            if self.current_word_index == len(current_paragraph):
                self.current_paragraph_index += 1
                self.current_word_index = 0

            self.load_paragraphs()

    def start_timer(self):
        self.timer_running = True
        self.update_timer()

    def update_timer(self):
        elapsed = int(time.time() - self.start_time)
        remaining = self.time_limit - elapsed
        self.timer_label.config(text=f"Time: {remaining}")

        if remaining > 0:
            self.root.after(1000, self.update_timer)
        else:
            self.end_test()

    def end_test(self):
        self.timer_running = False
        wpm = self.correct_words
        self.result_label.config(text=f"Your WPM: {wpm}")
        self.entry.config(state="disabled")

        self.show_post_test_options(wpm)

    def show_post_test_options(self, wpm):
        self.leaderboard_frame.destroy()
        self.leaderboard_frame = tk.Frame(self.root)
        self.leaderboard_frame.pack(pady=10)

        tk.Button(self.leaderboard_frame, text="Enter name for leaderboard", command=lambda: self.prompt_leaderboard(wpm)).pack()
        tk.Button(self.leaderboard_frame, text="Try Again", command=self.try_again).pack(pady=5)

    def prompt_leaderboard(self, wpm):
        self.entry_window = tk.Toplevel(self.root)
        self.entry_window.title("Enter Name")

        tk.Label(self.entry_window, text="Enter your name:").pack()
        name_entry = tk.Entry(self.entry_window)
        name_entry.pack()
        tk.Button(self.entry_window, text="Submit", command=lambda: self.submit_leaderboard(name_entry.get(), wpm)).pack()

    def submit_leaderboard(self, name, wpm):
        name = name.strip()
        if not name or any(entry[0] == name for entry in self.leaderboard):
            return
        self.leaderboard.append((name, wpm))
        self.leaderboard.sort(key=lambda x: x[1], reverse=True)
        self.entry_window.destroy()
        self.show_leaderboard()

    def show_leaderboard(self):
        for widget in self.leaderboard_frame.winfo_children():
            widget.destroy()

        tk.Label(self.leaderboard_frame, text="Leaderboard:", font=("Arial", 14, "bold")).pack()
        for i, (name, wpm) in enumerate(self.leaderboard, 1):
            tk.Label(self.leaderboard_frame, text=f"#{i} {name} {wpm} wpm").pack()

        tk.Button(self.leaderboard_frame, text="Try Again", command=self.try_again).pack(pady=5)

    def try_again(self):
        self.words = words_by_level[self.level]
        self.paragraphs = [self.words[i:i+10] for i in range(0, len(self.words), 10)]
        self.current_paragraph_index = 0
        self.current_word_index = 0
        self.correct_words = 0
        self.start_time = None
        self.timer_running = False

        for label in self.paragraph_labels:
            label.config(text="")

        self.entry.config(state="normal")
        self.entry.delete(0, tk.END)
        self.result_label.config(text="")
        self.load_paragraphs()
        self.timer_label.config(text="Time: 60")

if __name__ == "__main__":
    root = tk.Tk()
    app = TypingApp(root)
    root.mainloop()
