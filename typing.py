import tkinter as tk
import random
import time
from lexical import words_by_level

class TypingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Fast Typing")
        self.root.geometry("900x700")
        self.root.configure(bg="#A0C878")  # Dark green background
        
        # Color scheme
        self.bg_color = "#A0C878"  # Main green background
        self.screen_color = "#FAF6E9"  # Cream screen
        self.frame_color = "#5A8F5E"  # Dark green outline
        self.highlight_color = "#F2C078"  # Yellow for highlights
        self.highlight_dark = "#D9A560"  # Darker yellow for outlines
        self.text_color = "#4B352A"  # Dark brown text
        self.timer_color = "#FFFDF6"  # White for timer
        
        # Initialize variables
        self.words = []
        self.paragraphs = []
        self.leaderboard = []
        
        # Create main container (no frame needed, we'll use canvas directly)
        self.canvas = tk.Canvas(
            root,
            width=800,
            height=600,
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
    
    def create_rounded_button(self, canvas, x, y, text, command, radius=20, **kwargs):
        """Create a button with rounded corners and outline"""
        btn_frame = tk.Frame(canvas, bg=self.bg_color)
        btn_frame.place(x=x, y=y, anchor=tk.CENTER)
        
        btn = tk.Button(
            btn_frame,
            text=text,
            command=command,
            font=("Helvetica", 14),
            bg=self.highlight_color,
            fg=self.text_color,
            activebackground="#E0B068",
            relief="flat",
            padx=20,
            pady=10,
            bd=0,
            **kwargs
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
            50, 50, 750, 550,
            radius=50,
            fill=self.bg_color,
            outline=self.frame_color,
            width=8
        )
        
        # Home page content
        title_label = tk.Label(
            self.canvas,
            text="Welcome to the Typing Speed Game", 
            font=("Helvetica", 24, "bold"),
            bg=self.bg_color,
            fg=self.text_color
        )
        self.canvas.create_window(400, 150, window=title_label)
        
        # Create rounded button
        self.create_rounded_button(
            self.canvas, 400, 300,
            "Start Typing Test",
            self.start_typing_test
        )
        
        subtitle = tk.Label(
            self.canvas,
            text="Test your typing speed in 1 minute", 
            font=("Helvetica", 14),
            bg=self.bg_color,
            fg=self.text_color
        )
        self.canvas.create_window(400, 400, window=subtitle)
        
        # Add decorative elements
        self.create_rounded_rectangle(
            self.canvas,
            300, 450, 500, 470,
            radius=10,
            fill=self.highlight_color,
            outline=self.highlight_dark,
            width=2
        )
    
    def start_typing_test(self):
        """Initialize and show the typing test interface"""
        # Clear the canvas
        self.canvas.delete("all")
        
        # Prepare word lists
        all_words = []
        for level, weight in {'A': 0.45, 'B': 0.40, 'C': 0.15}.items():
            level_words = random.choices(words_by_level[level], k=int(300 * weight))
            all_words.extend(level_words)
        
        random.shuffle(all_words)
        self.words = all_words
        self.paragraphs = [self.words[i:i+10] for i in range(0, len(self.words), 10)]

        self.reset_test_vars()

        # Draw main rounded rectangle (device screen)
        self.create_rounded_rectangle(
            self.canvas,
            50, 50, 750, 550,
            radius=50,
            fill=self.bg_color,
            outline=self.frame_color,
            width=8
        )
        
        # Create smaller canvas (text display area)
        self.small_canvas = tk.Canvas(
            self.canvas,
            width=600,
            height=300,
            bg=self.screen_color,
            highlightthickness=0
        )
        self.canvas.create_window(400, 250, window=self.small_canvas)
        
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
            self.canvas,
            text="01:00",
            font=("Helvetica", 24, "bold"),
            fg=self.timer_color,
            bg=self.bg_color
        )
        self.canvas.create_window(400, 100, window=self.time_label)
        
        # Input frame
        input_frame = tk.Frame(
            self.canvas,
            bg=self.bg_color
        )
        self.canvas.create_window(400, 450, window=input_frame)
        
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
            self.canvas,
            text="",
            font=("Helvetica", 12),
            bg=self.bg_color,
            fg=self.text_color
        )
        self.canvas.create_window(400, 500, window=self.status_label)
        
        # Result UI elements (initially hidden)
        self.result_label = tk.Label(
            self.canvas,
            text="",
            font=("Helvetica", 24, "bold"),
            bg=self.bg_color,
            fg=self.text_color
        )
        
        self.score_label = tk.Label(
            self.canvas,
            text="",
            font=("Helvetica", 16),
            bg=self.bg_color,
            fg=self.text_color
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

        # Display results
        self.result_label.config(text=f"Your WPM: {self.current_wpm}")
        self.canvas.create_window(400, 520, window=self.result_label)

        self.score_label.config(text=f"Correct: {self.correct_count} / {total_attempted} words")
        self.canvas.create_window(400, 560, window=self.score_label)

        # Create action buttons with rounded corners
        self.create_rounded_button(
            self.canvas, 300, 600,
            "Add to Leaderboard",
            self.enter_leaderboard
        )
        
        self.create_rounded_button(
            self.canvas, 500, 600,
            "Try Again",
            self.reset_test
        )
        
        self.time_label.config(text="00:00")
        self.status_label.config(text="Time's up!")

    def enter_leaderboard(self):
        """Show dialog to enter name for leaderboard"""
        name_window = tk.Toplevel(self.root)
        name_window.title("Enter Name")
        name_window.geometry("300x150")
        name_window.resizable(False, False)
        name_window.configure(bg=self.bg_color)
        
        # Create rounded container
        lb_canvas = tk.Canvas(
            name_window,
            width=280,
            height=130,
            bg=self.bg_color,
            highlightthickness=0
        )
        lb_canvas.pack(pady=10)
        
        self.create_rounded_rectangle(
            lb_canvas,
            10, 10, 270, 120,
            radius=20,
            fill=self.screen_color,
            outline=self.frame_color,
            width=3
        )
        
        tk.Label(
            lb_canvas,
            text="Enter your name:",
            font=("Helvetica", 12),
            bg=self.screen_color
        ).place(x=140, y=30, anchor=tk.CENTER)
        
        name_entry = tk.Entry(
            lb_canvas,
            font=("Helvetica", 12),
            bg="white",
            highlightthickness=1,
            highlightcolor=self.frame_color
        )
        name_entry.place(x=140, y=60, anchor=tk.CENTER, width=200)
        
        submit_btn = self.create_rounded_button(
            lb_canvas, 140, 100,
            "Submit",
            lambda: self.submit_leaderboard_name(name_entry, name_window),
            radius=15,
            font=("Helvetica", 10),
            padx=15,
            pady=5
        )

    def submit_leaderboard_name(self, entry, window):
        """Handle leaderboard name submission"""
        name = entry.get().strip()
        if name:
            self.leaderboard.append((name, self.current_wpm))
            self.leaderboard.sort(key=lambda x: x[1], reverse=True)
            self.show_leaderboard()
        window.destroy()

    def show_leaderboard(self):
        """Display the leaderboard"""
        # Clear previous leaderboard display
        self.canvas.delete("leaderboard")
        
        # Create rounded container
        self.create_rounded_rectangle(
            self.canvas,
            200, 620, 600, 720,
            radius=20,
            fill=self.screen_color,
            outline=self.frame_color,
            width=3,
            tags="leaderboard"
        )
        
        text = "Leaderboard:\n"
        for idx, (name, wpm) in enumerate(self.leaderboard[:5], 1):
            text += f"#{idx} {name}: {wpm} WPM\n"
        
        tk.Label(
            self.canvas,
            text=text,
            font=("Helvetica", 12),
            bg=self.screen_color,
            fg=self.text_color,
            justify=tk.LEFT
        ).place(x=400, y=670, anchor=tk.CENTER)

    def reset_test(self):
        """Reset the test to start again"""
        # Clear the canvas except the main background
        self.canvas.delete("all")
        self.start_typing_test()

if __name__ == "__main__":
    root = tk.Tk()
    app = TypingApp(root)
    root.mainloop()
