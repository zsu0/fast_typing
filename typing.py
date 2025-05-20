import tkinter as tk
import random
import time
from lexical import words_by_level

class TypingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Fast Typing")
        self.root.geometry("800x600")
        
        # Initialize variables
        self.words = []
        self.paragraphs = []
        self.leaderboard = []
        
        # Create container frame
        self.container = tk.Frame(root)
        self.container.pack(fill="both", expand=True)
        
        # Animation variables
        self.animation_step = 0
        self.animation_running = False
        self.animation_direction = 0  # 0=no animation, 1=up, -1=down
        
        # Show home page initially
        self.show_home_page()
    
    def show_home_page(self):
        """Display the home page with welcome message and start button"""
        # Clear the container
        for widget in self.container.winfo_children():
            widget.destroy()
        
        # Home page widgets
        title_label = tk.Label(
            self.container, 
            text="Welcome to the Typing Speed Game", 
            font=("Helvetica", 24, "bold"),
            pady=50
        )
        title_label.pack()
        
        start_button = tk.Button(
            self.container,
            text="Start Typing Test",
            command=self.start_typing_test,
            font=("Helvetica", 16),
            padx=20,
            pady=10
        )
        start_button.pack()
        
        tk.Label(self.container, text="Test your typing speed in 1 minute", font=("Helvetica", 14)).pack(pady=20)
        tk.Label(self.container, text="How many words per minute can you type?", font=("Helvetica", 12)).pack()
    
    def start_typing_test(self):
        """Initialize and show the typing test interface"""
        # Clear the container
        for widget in self.container.winfo_children():
            widget.destroy()
        
        # Prepare word lists
        all_words = []
        for level, weight in {'A': 0.45, 'B': 0.40, 'C': 0.15}.items():
            level_words = random.choices(words_by_level[level], k=int(300 * weight))
            all_words.extend(level_words)
        
        random.shuffle(all_words)
        self.words = all_words
        self.paragraphs = [self.words[i:i+10] for i in range(0, len(self.words), 10)]

        self.reset_test_vars()

        # Create typing test widgets
        self.text_frame = tk.Frame(self.container)
        self.text_frame.pack(pady=10)
        
        self.text_display = tk.Text(
            self.text_frame, 
            height=10, 
            width=80, 
            font=("Helvetica", 14),
            wrap=tk.WORD
        )
        self.text_display.pack()
        self.text_display.config(state=tk.DISABLED)

        self.input_entry = tk.Entry(self.container, font=("Helvetica", 14))
        self.input_entry.pack()
        self.input_entry.bind("<space>", self.check_word)
        self.input_entry.bind("<Return>", self.check_word)

        self.status_label = tk.Label(self.container, text="", font=("Helvetica", 12))
        self.status_label.pack(pady=10)

        # Result labels (initially hidden)
        self.result_label = tk.Label(self.container, text="", font=("Helvetica", 14))
        self.score_label = tk.Label(self.container, text="", font=("Helvetica", 12))

        # Buttons (initially hidden)
        self.try_again_button = tk.Button(
            self.container, 
            text="Try Again", 
            command=self.reset_test, 
            font=("Helvetica", 12)
        )
        self.leaderboard_button = tk.Button(
            self.container, 
            text="Enter Leaderboard", 
            command=self.enter_leaderboard, 
            font=("Helvetica", 12)
        )
        self.back_to_home_button = tk.Button(
            self.container,
            text="Back to Home",
            command=self.show_home_page,
            font=("Helvetica", 12)
        )
        
        self.leaderboard_display = tk.Label(
            self.container, 
            text="", 
            font=("Helvetica", 12), 
            justify="left"
        )

        self.update_paragraphs()
        self.input_entry.focus_set()

    def reset_test_vars(self):
        """Reset all test variables to initial state"""
        self.current_paragraph_index = 0
        self.current_word_index = 0
        self.correct_count = 0
        self.incorrect_count = 0
        self.start_time = None
        self.test_running = True
        self.timer_id = None
        self.animation_step = 0
        self.animation_running = False
        self.animation_direction = 0

    def update_paragraphs(self, animate=False):
        """Update the displayed paragraphs with optional animation"""
        if self.current_paragraph_index >= len(self.paragraphs):
            self.end_test()
            return

        if animate:
            self.animate_paragraph_transition()
            return

        self.text_display.config(state=tk.NORMAL)
        self.text_display.delete("1.0", tk.END)
        
        # Show current and next paragraph
        current_p = " ".join(self.paragraphs[self.current_paragraph_index])
        next_p = " ".join(self.paragraphs[self.current_paragraph_index+1]) if self.current_paragraph_index+1 < len(self.paragraphs) else ""
        
        self.text_display.insert(tk.END, current_p + "\n" + next_p)
        self.text_display.config(state=tk.DISABLED)
        self.highlight_current_word()

    def animate_paragraph_transition(self):
        """Animate the paragraph scrolling up"""
        if self.animation_running:
            return
            
        self.animation_running = True
        self.animation_step = 0
        self.animation_direction = 1  # Up direction
        
        # Get the paragraphs to display
        current_p = " ".join(self.paragraphs[self.current_paragraph_index])
        next_p = " ".join(self.paragraphs[self.current_paragraph_index+1]) if self.current_paragraph_index+1 < len(self.paragraphs) else ""
        next_next_p = " ".join(self.paragraphs[self.current_paragraph_index+2]) if self.current_paragraph_index+2 < len(self.paragraphs) else ""
        
        self.text_display.config(state=tk.NORMAL)
        self.text_display.delete("1.0", tk.END)
        self.text_display.insert(tk.END, current_p + "\n" + next_p + "\n" + next_next_p)
        self.text_display.config(state=tk.DISABLED)
        
        self.perform_animation()

    def perform_animation(self):
        """Perform the scrolling animation step by step"""
        if not self.animation_running:
            return
            
        self.animation_step += 1
        scroll_amount = 0.2  # Smaller steps for smoother animation
        
        # Get current first line position
        first_line_pos = float(self.text_display.index("1.0").split('.')[0])
        
        # Scroll up
        self.text_display.yview_moveto(first_line_pos + scroll_amount)
        
        if self.animation_step < 5:  # Adjust number of steps for animation duration
            self.root.after(50, self.perform_animation)
        else:
            # Animation complete
            self.animation_running = False
            self.current_paragraph_index += 1
            self.current_word_index = 0
            self.update_paragraphs(animate=False)

    def highlight_current_word(self):
        """Highlight the current word that needs to be typed"""
        self.text_display.config(state=tk.NORMAL)
        self.text_display.tag_remove("highlight", "1.0", tk.END)

        full_text = self.text_display.get("1.0", tk.END).split()
        if self.current_word_index >= len(full_text):
            return

        word_pos = sum(len(word)+1 for word in full_text[:self.current_word_index])
        word_len = len(full_text[self.current_word_index])

        start_index = f"1.0 + {word_pos} chars"
        end_index = f"1.0 + {word_pos + word_len} chars"
        self.text_display.tag_add("highlight", start_index, end_index)
        self.text_display.tag_config("highlight", background="yellow")
        self.text_display.config(state=tk.DISABLED)

    def check_word(self, event):
        """Check if the typed word matches the current word"""
        if not self.test_running or self.animation_running:
            return
            
        if self.start_time is None:
            self.start_time = time.time()
            self.timer_id = self.root.after(1000, self.update_timer)

        typed = self.input_entry.get().strip()
        current_word = self.paragraphs[self.current_paragraph_index][self.current_word_index]

        if typed == current_word:
            self.correct_count += 1
        else:
            self.incorrect_count += 1
            
        self.input_entry.delete(0, tk.END)
        self.current_word_index += 1

        if self.current_word_index >= len(self.paragraphs[self.current_paragraph_index]):
            # Start paragraph transition animation
            if self.current_paragraph_index + 1 < len(self.paragraphs):
                self.update_paragraphs(animate=True)
            else:
                self.end_test()
        else:
            self.highlight_current_word()

    def update_timer(self):
        """Update the timer and check if time is up"""
        if not self.test_running or not self.start_time:
            return
            
        elapsed = time.time() - self.start_time
        if elapsed >= 60:
            self.end_test()
        else:
            remaining = 60 - int(elapsed)
            self.status_label.config(text=f"Time remaining: {remaining} seconds")
            self.timer_id = self.root.after(1000, self.update_timer)

    def end_test(self):
        """Handle test completion"""
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            
        self.test_running = False
        self.input_entry.config(state='disabled')
        elapsed = max(1, time.time() - self.start_time)
        self.current_wpm = int((self.correct_count / elapsed) * 60)
        total_attempted = self.correct_count + self.incorrect_count

        self.result_label.config(text=f"Your WPM: {self.current_wpm}")
        self.result_label.pack(pady=10)

        self.score_label.config(text=f"Correct: {self.correct_count} / {total_attempted} words in 1 minute")
        self.score_label.pack(pady=5)

        self.leaderboard_button.pack(pady=5)
        self.try_again_button.pack(pady=5)
        self.back_to_home_button.pack(pady=5)
        self.status_label.config(text="Time's up!")

    def enter_leaderboard(self):
        """Show dialog to enter name for leaderboard"""
        name_window = tk.Toplevel(self.root)
        name_window.title("Enter Name")
        tk.Label(name_window, text="Enter your name:").pack()
        name_entry = tk.Entry(name_window)
        name_entry.pack()

        def submit_name():
            name = name_entry.get().strip()
            if name:
                self.leaderboard.append((name, self.current_wpm))
                self.leaderboard.sort(key=lambda x: x[1], reverse=True)
                self.show_leaderboard()
            name_window.destroy()

        tk.Button(name_window, text="Submit", command=submit_name).pack()

    def show_leaderboard(self):
        """Display the leaderboard"""
        text = "Leaderboard:\n"
        for idx, (name, wpm) in enumerate(self.leaderboard[:10], 1):
            text += f"#{idx} {name} - {wpm} WPM\n"
        self.leaderboard_display.config(text=text)
        self.leaderboard_display.pack()

    def reset_test(self):
        """Reset the test to start again"""
        self.reset_test_vars()
        random.shuffle(self.words)
        self.paragraphs = [self.words[i:i+10] for i in range(0, len(self.words), 10)]

        self.input_entry.config(state=tk.NORMAL)
        self.input_entry.delete(0, tk.END)

        self.result_label.pack_forget()
        self.score_label.pack_forget()
        self.leaderboard_button.pack_forget()
        self.try_again_button.pack_forget()
        self.back_to_home_button.pack_forget()
        self.leaderboard_display.pack_forget()
        self.status_label.config(text="")

        self.update_paragraphs()
        self.input_entry.focus_set()

if __name__ == "__main__":
    root = tk.Tk()
    app = TypingApp(root)
    root.mainloop()
