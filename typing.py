import tkinter as tk
import random
import time
from lexical import words_by_level

class TypingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Fast Typing")
        self.root.geometry("700x750")  # Adjusted window size
        self.root.configure(bg="#A0C878")  # Dark green background
        
        # Color scheme
        self.bg_color = "#DDEB9D"  # Main green background
        self.screen_color = "#FAF6E9"  # Cream screen
        self.frame_color = "#5A8F5E"  # Dark green outline
        self.highlight_color = "#E0B068"  # Yellow for highlight
        self.highlight_dark = "#D9A560"  # Darker yellow for outlines
        self.text_color = "#653F27"  # Dark brown text
        self.timer_color = "#FFFDF6"  # White for timer
        
        # Initialize variables
        self.words = []
        self.paragraphs = []
        self.leaderboard = []
        
        # Create main canvas with adjusted size
        self.canvas = tk.Canvas(
            root,
            width=650,
            height=700,
            bg=self.bg_color,
            highlightthickness=0
        )
        self.canvas.pack(pady=20)
        
        # Show home page initially
        self.show_home_page()
    
    def create_rounded_rectangle(self, canvas, x1, y1, x2, y2, radius=25, **kwargs):
        """Draw a rounded rectangle on canvas with outline"""
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
        # First draw the outline (darker color)
        outline_color = kwargs.pop('outline', self.frame_color)
        width = kwargs.pop('width', 3)
        canvas.create_polygon(points, outline=outline_color, width=width, smooth=True, **kwargs)
        # Then draw the fill
        return canvas.create_polygon(points, **kwargs, smooth=True)
    
    def create_rounded_button(self, canvas, x, y, text, command, radius=15, font_size=12, **kwargs):
        """Create a button with rounded corners and outline"""
        btn_frame = tk.Frame(canvas, bg=self.bg_color)
        btn_frame.place(x=x, y=y, anchor=tk.CENTER)
        
        btn = tk.Button(
            btn_frame,
            text=text,
            command=command,
            bg=self.highlight_color,
            fg=self.text_color,
            activebackground="#FCEFCB",
            relief="flat",
            padx=15,
            pady=8,
            bd=0,
            font=("Helvetica", font_size)
        )
        btn.pack()
        
        # Create rounded rectangle effect
        btn.update_idletasks()  # Update to get actual button size
        width = btn.winfo_width()
        height = btn.winfo_height()
        
        # Draw rounded rectangle outline
        self.create_rounded_rectangle(
            canvas,
            x-width//2, y-height//2,
            x+width//2, y+height//2,
            radius=radius,
            fill="",
            outline=self.highlight_dark,
            width=2
        )
        
        return btn
    
    def show_home_page(self):
        """Display the home page with welcome message and start button"""
        # Clear the canvas
        self.canvas.delete("all")
        
        # Draw main rounded rectangle (device screen)
        self.create_rounded_rectangle(
            self.canvas,
            25, 25, 625, 675,  # Adjusted dimensions
            radius=40,
            fill=self.bg_color,
            outline=self.frame_color,
            width=6
        )
        
        # Home page content
        title_label = tk.Label(
            self.canvas,
            text="Welcome to the Typing Speed Game", 
            font=("Helvetica", 20, "bold"),
            bg=self.bg_color,
            fg=self.text_color
        )
        self.canvas.create_window(325, 120, window=title_label)
        
        # Create rounded button
        self.create_rounded_button(
            self.canvas, 325, 250,
            "Start Typing Test",
            self.start_typing_test,
            font_size=14
        )
        
        subtitle = tk.Label(
            self.canvas,
            text="Test your typing speed in 1 minute\n\nHow fast can you type?", 
            font=("Helvetica", 12),
            bg=self.bg_color,
            fg=self.text_color
        )
        self.canvas.create_window(325, 350, window=subtitle)
    
    
    def start_typing_test(self):
        """Initialize and show the typing test interface"""
        # Clear the canvas
        self.canvas.delete("all")
        
        # Prepare word lists
        all_words = []
        for level, weight in {'A': 0.45, 'B': 0.40, 'C': 0.15}.items():
            level_words = random.choices(words_by_level[level], k=int(200 * weight))  # Reduced word count
            all_words.extend(level_words)
        
        random.shuffle(all_words)
        self.words = all_words
        # display 6 words per paragraph
        self.paragraphs = [self.words[i:i+6] for i in range(0, len(self.words), 6)]

        self.reset_test_vars()

        # Draw main rounded rectangle (device screen)
        self.create_rounded_rectangle(
            self.canvas,
            25, 25, 625, 675,  # Adjusted dimensions
            radius=40,
            fill=self.bg_color,
            outline=self.frame_color,
            width=6
        )
        
        # Create smaller canvas (text display area)
        self.small_canvas = tk.Canvas(
            self.canvas,
            width=550,
            height=300,  # Adjusted height
            bg=self.screen_color,
            highlightthickness=0
        )
        self.canvas.create_window(325, 250, window=self.small_canvas)
        
        # Create rounded rectangle for text display
        self.create_rounded_rectangle(
            self.small_canvas,
            10, 10, 540, 290,  # Adjusted dimensions
            radius=15,
            fill=self.screen_color,
            outline=self.frame_color,
            width=3
        )
        
        # Text display widget
        self.text_display = tk.Text(
            self.small_canvas,
            height=12,
            width=50,
            font=("Helvetica", 12),  # Smaller font
            wrap=tk.WORD,
            bg=self.screen_color,
            fg=self.text_color,  # Dark brown text
            padx=15,
            pady=15,
            highlightthickness=0,
            bd=0
        )
        self.text_display.place(x=25, y=25, width=500, height=240)
        self.text_display.config(state=tk.DISABLED)
        self.text_display.tag_config("highlight", background="yellow")
        
        # Countdown timer display
        self.time_label = tk.Label(
            self.canvas,
            text="01:00",
            font=("Helvetica", 20, "bold"),
            fg=self.timer_color,
            bg=self.bg_color
        )
        self.canvas.create_window(325, 120, window=self.time_label)
        
        # Input frame
        input_frame = tk.Frame(
            self.canvas,
            bg=self.bg_color
        )
        self.canvas.create_window(325, 450, window=input_frame)
        
        # Input entry with rounded corners
        self.input_entry = tk.Entry(
            input_frame,
            font=("Helvetica", 14),  # Smaller font
            bg="white",
            fg=self.text_color,
            relief="flat",
            bd=0,
            highlightthickness=2,
            highlightbackground=self.frame_color,
            highlightcolor=self.highlight_color
        )
        self.input_entry.pack(padx=15, pady=8, ipady=6, ipadx=15)
        self.input_entry.bind("<space>", self.check_word)
        self.input_entry.bind("<Return>", self.check_word)
        self.input_entry.bind("<Key>", self.start_timer_on_first_key)
        
        # Status label
        self.status_label = tk.Label(
            self.canvas,
            text="",
            font=("Helvetica", 10),
            bg=self.bg_color,
            fg=self.text_color
        )
        self.canvas.create_window(325, 500, window=self.status_label)
        
        # Initialize test
        self.update_paragraphs()
        self.input_entry.focus_set()

    def start_timer_on_first_key(self, event):
        """Start timer when first key is pressed"""
        if self.start_time is None and event.char and event.char.isalnum():
            self.start_time = time.time()
            self.update_timer()
            # Remove this binding after first key press
            self.input_entry.unbind("<Key>")

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
        
        # Clear any existing result displays
        if hasattr(self, 'result_label'):
            self.result_label.place_forget()
        if hasattr(self, 'score_label'):
            self.score_label.place_forget()

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
        
        self.text_display.insert(tk.END, current_p + "\n\n" + next_p)  # Added extra newline
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
        self.text_display.insert(tk.END, current_p + "\n\n" + next_p + "\n\n" + next_next_p)  # Added extra newlines
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
        # just in case user type too fast
        if self.current_paragraph_index >= len(self.paragraphs):
            return
            
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
        self.text_display.config(state=tk.DISABLED)

    def check_word(self, event):
        """Check if the typed word matches the current word"""
        if not self.test_running or self.animation_running:
            return
            
        typed = self.input_entry.get().strip()
        if not typed:  # Ignore empty input
            return

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

        # Clear previous result displays
        if hasattr(self, 'result_label'):
            self.result_label.place_forget()
        if hasattr(self, 'score_label'):
            self.score_label.place_forget()

        # Create new result displays
        self.result_label = tk.Label(
            self.canvas,
            text=f"Your WPM: {self.current_wpm}",
            font=("Helvetica", 20, "bold"),
            bg=self.bg_color,
            fg=self.text_color
        )
        self.canvas.create_window(325, 550, window=self.result_label)

        self.score_label = tk.Label(
            self.canvas,
            text=f"Correct: {self.correct_count} / {total_attempted} words",
            font=("Helvetica", 14),
            bg=self.bg_color,
            fg=self.text_color
        )
        self.canvas.create_window(325, 590, window=self.score_label)

        # Create action buttons with rounded corners
        self.create_rounded_button(
            self.canvas, 250, 630,
            "Add to Leaderboard",
            self.enter_leaderboard,
            font_size=12
        )
        
        self.create_rounded_button(
            self.canvas, 400, 630,
            "Try Again",
            self.reset_test,
            font_size=12
        )
        
        self.time_label.config(text="00:00")
        self.status_label.config(text="Time's up!")

    def enter_leaderboard(self):
        """Show dialog to enter name for leaderboard"""
        self.name_window = tk.Toplevel(self.root)
        self.name_window.title("Enter Name")
        self.name_window.geometry("300x150")
        self.name_window.resizable(False, False)
        self.name_window.configure(bg=self.bg_color)
        self.name_window.grab_set()  # Make it modal
        
        # Create rounded container
        lb_canvas = tk.Canvas(
            self.name_window,
            width=280,
            height=130,
            bg=self.bg_color,
            highlightthickness=0
        )
        lb_canvas.pack(pady=10)
        
        self.create_rounded_rectangle(
            lb_canvas,
            10, 10, 270, 120,
            radius=15,
            fill=self.screen_color,
            outline=self.frame_color,
            width=2
        )
        
        tk.Label(
            lb_canvas,
            text="Enter your name:",
            font=("Helvetica", 12),
            bg=self.screen_color,
            fg=self.text_color
        ).place(x=140, y=40, anchor=tk.CENTER)
        
        self.name_entry = tk.Entry(
            lb_canvas,
            font=("Helvetica", 12),
            bg="white",
            fg=self.text_color,
            highlightthickness=1,
            highlightcolor=self.frame_color
        )
        self.name_entry.place(x=140, y=70, anchor=tk.CENTER, width=200)
        self.name_entry.focus_set()
        
        # Submit button - fixed the font parameter issue
        submit_btn = tk.Button(
            lb_canvas,
            text="Submit",
            command=self.submit_leaderboard_name,
            font=("Helvetica", 10),
            bg=self.highlight_color,
            fg=self.text_color,
            activebackground="#FCEFCB",
            relief="flat",
            padx=10,
            pady=5,
            bd=0
        )
        submit_btn.place(x=140, y=100, anchor=tk.CENTER)

        self.warning_label = tk.Label(
            lb_canvas,
            text="",
            font=("Helvetica", 10),
            fg="red",
            bg=self.screen_color
        )
        self.warning_label.place(x=140, y=115, anchor=tk.CENTER)

    def submit_leaderboard_name(self):
        """Handle leaderboard name submission"""
        name = self.name_entry.get().strip()
        # check duplicate names
        if name in [entry[0] for entry in self.leaderboard]:
            self.warning_label.config(text="Please use another name.")
            return
        self.warning_label.config(text="")
        
        if name:
            self.leaderboard.append((name, self.current_wpm))
            self.leaderboard.sort(key=lambda x: x[1], reverse=True)
            self.show_leaderboard()
            self.name_window.destroy()

    def show_leaderboard(self):
        """Display the leaderboard"""
        # Clear previous leaderboard display
        self.canvas.delete("leaderboard")
        
        # Create rounded container
        self.create_rounded_rectangle(
            self.canvas,
            50, 100, 600, 500,
            radius=15,
            fill=self.screen_color,
            outline=self.frame_color,
            width=2,
            tags="leaderboard"
        )
        
        # Create scrollable frame for leaderboard
        lb_frame = tk.Frame(
            self.canvas,
            bg=self.screen_color
        )
        self.canvas.create_window(325, 300, window=lb_frame, tags="leaderboard")
        
        # Add title
        tk.Label(
            lb_frame,
            text="Leaderboard",
            font=("Helvetica", 16, "bold"),
            bg=self.screen_color,
            fg=self.text_color
        ).pack(pady=5)
        
        # Add entries
        for idx, (name, wpm) in enumerate(self.leaderboard[:10], 1):
            entry_frame = tk.Frame(lb_frame, bg=self.screen_color)
            entry_frame.pack(fill=tk.X, padx=15, pady=2)
            
            tk.Label(
                entry_frame,
                text=f"#{idx}",
                font=("Helvetica", 12),
                bg=self.screen_color,
                fg=self.text_color,
                width=3,
                anchor=tk.W
            ).pack(side=tk.LEFT)
            
            tk.Label(
                entry_frame,
                text=name,
                font=("Helvetica", 12),
                bg=self.screen_color,
                fg=self.text_color,
                width=15,
                anchor=tk.W
            ).pack(side=tk.LEFT)
            
            tk.Label(
                entry_frame,
                text=f"{wpm} WPM",
                font=("Helvetica", 12),
                bg=self.screen_color,
                fg=self.text_color,
                width=8,
                anchor=tk.E
            ).pack(side=tk.RIGHT)

    def reset_test(self):
        """Reset the test to start again"""
        # Clear the canvas except the main background
        self.canvas.delete("all")
        self.start_typing_test()

if __name__ == "__main__":
    root = tk.Tk()
    app = TypingApp(root)
    root.mainloop()
