import tkinter as tk
import random
import time
from lexical import words_by_level

class TypingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Fast Typing")
        self.root.geometry("900x700")
        self.root.configure(bg="#A0C878")
        
        # Color scheme
        self.bg_color = "#DDEB9D"  # Main background color
        self.screen_color = "#FAF6E9"  # Cream screen (small canvas)
        self.frame_color = "#555555"  # Dark frame color, canvas's frame
        self.highlight_color = "#F2C078"  # Yellow for highlights
        self.text_color = "#4B352A"  # Dark brown text
        self.timer_color = "#FFFDF6"  # White for timer
        
        # Initialize variables
        self.words = []
        self.paragraphs = []
        self.leaderboard = []
        
        # Create main container
        self.main_frame = tk.Frame(root, bg="#333333") 
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Show home page initially
        self.show_home_page()
    
    def create_rounded_rectangle(self, canvas, x1, y1, x2, y2, radius=25, **kwargs):
        """Draw a rounded rectangle on canvas"""
        points = [
            x1+radius, y1,
            x2-radius, y1,
            x2, y1,
            x2, y1+radius,
            x2, y2-radius,
            x2, y2,
            x2-radius, y2,
            x1+radius, y2,
            x1, y2,
            x1, y2-radius,
            x1, y1+radius,
            x1, y1
        ]
        return canvas.create_polygon(points, **kwargs, smooth=True)
    
    def show_home_page(self):
        """Display the home page with welcome message and start button"""
        # Clear the container
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
        # Create big canvas (device frame)
        self.big_canvas = tk.Canvas(
            self.main_frame,
            width=800,
            height=600,
            bg=self.frame_color,
            highlightthickness=0
        )
        self.big_canvas.pack()
        
        # Draw rounded rectangle for device screen
        self.create_rounded_rectangle(
            self.big_canvas,
            50, 50, 750, 550,
            radius=50,
            fill=self.bg_color,
            outline=self.frame_color,
            width=8
        )
        
        # Home page content
        title_label = tk.Label(
            self.big_canvas,
            text="Welcome to the Typing Speed Game", 
            font=("Helvetica", 24, "bold"),
            bg=self.bg_color,
            fg=self.text_color
        )
        self.big_canvas.create_window(400, 150, window=title_label)
        
        start_button = tk.Button(
            self.big_canvas,
            text="Start Typing Test",
            command=self.start_typing_test,
            font=("Helvetica", 16),
            bg=self.highlight_color,
            fg=self.text_color,
            relief="flat",
            padx=30,
            pady=10,
            bd=0
        )
        self.big_canvas.create_window(400, 300, window=start_button)
        
        subtitle = tk.Label(
            self.big_canvas,
            text="Test your typing speed in 1 minute", 
            font=("Helvetica", 14),
            bg=self.bg_color,
            fg=self.text_color
        )
        self.big_canvas.create_window(400, 400, window=subtitle)
        
        # Add decorative elements
        self.create_rounded_rectangle(
            self.big_canvas,
            300, 450, 500, 470,
            radius=10,
            fill=self.highlight_color,
            outline=self.frame_color
        )
    
    def start_typing_test(self):
        """Initialize and show the typing test interface"""
        # Clear the container
        for widget in self.main_frame.winfo_children():
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

        # Create big canvas (device frame)
        self.big_canvas = tk.Canvas(
            self.main_frame,
            width=800,
            height=600,
            bg=self.frame_color,
            highlightthickness=0
        )
        self.big_canvas.pack()
        
        # Draw rounded rectangle for device screen
        self.create_rounded_rectangle(
            self.big_canvas,
            50, 50, 750, 550,
            radius=50,
            fill=self.bg_color,
            outline=self.frame_color,
            width=8
        )
        
        # Create smaller canvas (text display area)
        self.small_canvas = tk.Canvas(
            self.big_canvas,
            width=600,
            height=300,
            bg=self.screen_color,
            highlightthickness=0
        )
        self.big_canvas.create_window(400, 250, window=self.small_canvas)
        
        # Create rounded rectangle for text display
        self.create_rounded_rectangle(
            self.small_canvas,
            10, 10, 590, 290,
            radius=20,
            fill=self.screen_color,
            outline=self.frame_color,
            width=4
        )
        
        # Text display widget
        self.text_display = tk.Text(
            self.small_canvas,
            height=12,
            width=50,
            font=("Helvetica", 14),
            wrap=tk.WORD,
            bg=self.screen_color,
            fg=self.text_color,
            padx=20,
            pady=20,
            highlightthickness=0,
            bd=0
        )
        self.text_display.place(x=30, y=30, width=540, height=240)
        self.text_display.config(state=tk.DISABLED)
        
        # Countdown timer display
        self.time_label = tk.Label(
            self.big_canvas,
            text="01:00",
            font=("Helvetica", 24, "bold"),
            fg=self.timer_color,
            bg=self.bg_color
        )
        self.big_canvas.create_window(400, 100, window=self.time_label)
        
        # Input frame
        input_frame = tk.Frame(
            self.big_canvas,
            bg=self.bg_color
        )
        self.big_canvas.create_window(400, 450, window=input_frame)
        
        # Input entry with rounded corners
        self.input_entry = tk.Entry(
            input_frame,
            font=("Helvetica", 16),
            bg="white",
            fg=self.text_color,
            relief="flat",
            bd=0,
            highlightthickness=2,
            highlightbackground=self.frame_color,
            highlightcolor=self.highlight_color
        )
        self.input_entry.pack(padx=20, pady=10, ipady=8, ipadx=20)
        self.input_entry.bind("<space>", self.check_word)
        self.input_entry.bind("<Return>", self.check_word)
        
        # Status label
        self.status_label = tk.Label(
            self.big_canvas,
            text="",
            font=("Helvetica", 12),
            bg=self.bg_color,
            fg=self.text_color
        )
        self.big_canvas.create_window(400, 500, window=self.status_label)
        
        # Result UI elements (initially hidden)
        self.result_label = tk.Label(
            self.big_canvas,
            text="",
            font=("Helvetica", 24, "bold"),
            bg=self.bg_color,
            fg=self.text_color
        )
        
        self.score_label = tk.Label(
            self.big_canvas,
            text="",
            font=("Helvetica", 16),
            bg=self.bg_color,
            fg=self.text_color
        )
        
        self.leaderboard_button = tk.Button(
            self.big_canvas,
            text="Add to Leaderboard",
            command=self.enter_leaderboard,
            font=("Helvetica", 14),
            bg=self.highlight_color,
            fg=self.text_color,
            relief="flat",
            padx=20,
            pady=5
        )
        
        self.try_again_button = tk.Button(
            self.big_canvas,
            text="Try Again",
            command=self.reset_test,
            font=("Helvetica", 14),
            bg=self.highlight_color,
            fg=self.text_color,
            relief="flat",
            padx=20,
            pady=5
        )
        
        self.back_to_home_button = tk.Button(
            self.big_canvas,
            text="Back to Home",
            command=self.show_home_page,
            font=("Helvetica", 14),
            bg=self.highlight_color,
            fg=self.text_color,
            relief="flat",
            padx=20,
            pady=5
        )
        
        self.leaderboard_display = tk.Label(
            self.big_canvas,
            text="",
            font=("Helvetica", 12),
            bg=self.bg_color,
            fg=self.text_color,
            justify=tk.LEFT
        )
        
        # Initialize test
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
        
        # Scroll up
        self.text_display.yview_scroll(1, tk.UNITS)
        
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
            self.update_timer()

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
            mins, secs = divmod(remaining, 60)
            self.time_label.config(text=f"{mins:02d}:{secs:02d}")
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
        self.big_canvas.create_window(400, 520, window=self.result_label)

        self.score_label.config(text=f"Correct: {self.correct_count} / {total_attempted} words in 1 minute")
        self.big_canvas.create_window(400, 560, window=self.score_label)

        self.big_canvas.create_window(400, 600, window=self.leaderboard_button)
        self.big_canvas.create_window(400, 640, window=self.try_again_button)
        self.big_canvas.create_window(400, 680, window=self.back_to_home_button)
        
        self.time_label.config(text="00:00")
        self.status_label.config(text="Time's up!")

    def enter_leaderboard(self):
        """Show dialog to enter name for leaderboard"""
        name_window = tk.Toplevel(self.root)
        name_window.title("Enter Name")
        name_window.geometry("300x150")
        name_window.resizable(False, False)
        
        tk.Label(name_window, text="Enter your name:", font=("Helvetica", 12)).pack(pady=10)
        name_entry = tk.Entry(name_window, font=("Helvetica", 12))
        name_entry.pack(pady=5)

        def submit_name():
            name = name_entry.get().strip()
            if name:
                self.leaderboard.append((name, self.current_wpm))
                self.leaderboard.sort(key=lambda x: x[1], reverse=True)
                self.show_leaderboard()
            name_window.destroy()

        submit_btn = tk.Button(
            name_window,
            text="Submit",
            command=submit_name,
            font=("Helvetica", 12),
            bg=self.highlight_color,
            fg=self.text_color
        )
        submit_btn.pack(pady=10)

    def show_leaderboard(self):
        """Display the leaderboard"""
        text = "Leaderboard:\n"
        for idx, (name, wpm) in enumerate(self.leaderboard[:10], 1):
            text += f"#{idx} {name} - {wpm} WPM\n"
        
        self.leaderboard_display.config(text=text)
        self.big_canvas.create_window(400, 720, window=self.leaderboard_display)

    def reset_test(self):
        """Reset the test to start again"""
        self.reset_test_vars()
        random.shuffle(self.words)
        self.paragraphs = [self.words[i:i+10] for i in range(0, len(self.words), 10)]

        self.input_entry.config(state=tk.NORMAL)
        self.input_entry.delete(0, tk.END)

        # Hide result elements
        self.big_canvas.delete(self.result_label)
        self.big_canvas.delete(self.score_label)
        self.big_canvas.delete(self.leaderboard_button)
        self.big_canvas.delete(self.try_again_button)
        self.big_canvas.delete(self.back_to_home_button)
        self.big_canvas.delete(self.leaderboard_display)
        
        self.time_label.config(text="01:00")
        self.status_label.config(text="")

        self.update_paragraphs()
        self.input_entry.focus_set()

if __name__ == "__main__":
    root = tk.Tk()
    app = TypingApp(root)
    root.mainloop()
