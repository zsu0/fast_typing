import tkinter as tk
import random
import time
from lexical import words_by_level

class TypingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Fast Typing")
        self.root.geometry("800x400")

        level_weights = {'A': 0.45, 'B': 0.40, 'C': 0.15}
        self.level = random.choices(list(level_weights.keys()), weights=list(level_weights.values()), k=1)[0]
        self.words = words_by_level[self.level]
        random.shuffle(self.words)

        self.paragraphs = [self.words[i:i+10] for i in range(0, len(self.words), 10)]
        self.current_paragraph_index = 0
        self.current_word_index = 0
        self.correct_count = 0
        self.start_time = None

        self.text_display = tk.Text(root, height=10, width=80, font=("Helvetica", 14))
        self.text_display.pack(pady=10)
        self.text_display.config(state=tk.DISABLED)

        self.input_entry = tk.Entry(root, font=("Helvetica", 14))
        self.input_entry.pack()
        self.input_entry.bind("<space>", self.check_word)
        self.input_entry.bind("<Return>", self.check_word)

        self.status_label = tk.Label(root, text="", font=("Helvetica", 12))
        self.status_label.pack(pady=10)

        self.try_again_button = tk.Button(root, text="Try Again", command=self.reset, font=("Helvetica", 12))
        self.leaderboard_button = tk.Button(root, text="Enter Leaderboard", command=self.enter_leaderboard, font=("Helvetica", 12))
        self.leaderboard_display = tk.Label(root, text="", font=("Helvetica", 12), justify="left")

        self.leaderboard = []

        self.update_paragraphs()

    def update_paragraphs(self):
        self.text_display.config(state=tk.NORMAL)
        self.text_display.delete("1.0", tk.END)
        to_show = self.paragraphs[self.current_paragraph_index:self.current_paragraph_index+2]
        for p in to_show:
            self.text_display.insert(tk.END, " ".join(p) + "\n")
        self.text_display.config(state=tk.DISABLED)
        self.highlight_current_word()

    def highlight_current_word(self):
        self.text_display.config(state=tk.NORMAL)
        self.text_display.tag_remove("highlight", "1.0", tk.END)

        full_text = self.text_display.get("1.0", tk.END).split()
        word_pos = sum(len(word)+1 for word in full_text[:self.current_word_index])
        word_len = len(full_text[self.current_word_index])

        start_index = f"1.0 + {word_pos} chars"
        end_index = f"1.0 + {word_pos + word_len} chars"
        self.text_display.tag_add("highlight", start_index, end_index)
        self.text_display.tag_config("highlight", background="yellow")
        self.text_display.config(state=tk.DISABLED)

    def check_word(self, event):
        if self.start_time is None:
            self.start_time = time.time()
            self.root.after(1000, self.update_timer)

        typed = self.input_entry.get().strip()
        current_word = self.paragraphs[self.current_paragraph_index][self.current_word_index]

        if typed == current_word:
            self.correct_count += 1
        self.input_entry.delete(0, tk.END)
        self.current_word_index += 1

        if self.current_word_index >= len(self.paragraphs[self.current_paragraph_index]):
            self.current_paragraph_index += 1
            self.current_word_index = 0

            if self.current_paragraph_index >= len(self.paragraphs):
                self.end_test()
                return

            self.update_paragraphs()
        else:
            self.highlight_current_word()

    def update_timer(self):
        if self.start_time is None:
            return

        elapsed = time.time() - self.start_time
        if elapsed >= 60:
            self.end_test()
        else:
            self.root.after(1000, self.update_timer)

    def end_test(self):
        self.input_entry.config(state=tk.DISABLED)
        elapsed = max(1, time.time() - self.start_time)
        wpm = int(self.correct_count / (elapsed / 60))
        self.status_label.config(text=f"Test complete! WPM: {wpm}")

        self.try_again_button.pack()
        self.leaderboard_button.pack()
        self.current_wpm = wpm

    def enter_leaderboard(self):
        name_window = tk.Toplevel(self.root)
        name_window.title("Enter Name")
        tk.Label(name_window, text="Enter your name:").pack()
        name_entry = tk.Entry(name_window)
        name_entry.pack()

        def submit_name():
            name = name_entry.get()
            if name and all(n != name for n, _ in self.leaderboard):
                self.leaderboard.append((name, self.current_wpm))
                self.leaderboard.sort(key=lambda x: x[1], reverse=True)
                self.show_leaderboard()
            name_window.destroy()

        tk.Button(name_window, text="Submit", command=submit_name).pack()

    def show_leaderboard(self):
        text = "Leaderboard:\n"
        for idx, (name, wpm) in enumerate(self.leaderboard, 1):
            text += f"#{idx} {name} {wpm} wpm\n"
        self.leaderboard_display.config(text=text)
        self.leaderboard_display.pack()

    def reset(self):
        self.start_time = None
        self.current_paragraph_index = 0
        self.current_word_index = 0
        self.correct_count = 0

        random.shuffle(self.words)
        self.paragraphs = [self.words[i:i+10] for i in range(0, len(self.words), 10)]

        self.input_entry.config(state=tk.NORMAL)
        self.input_entry.delete(0, tk.END)
        self.status_label.config(text="")
        self.try_again_button.pack_forget()
        self.leaderboard_button.pack_forget()
        self.leaderboard_display.pack_forget()

        self.update_paragraphs()

if __name__ == "__main__":
    root = tk.Tk()
    app = TypingApp(root)
    root.mainloop()
