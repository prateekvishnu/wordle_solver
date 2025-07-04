import tkinter as tk
from tkinter import ttk, messagebox
import random
from collections import Counter
import os
import threading
import time

# Import the core logic from the existing solver
from wordle_ai_solver import load_word_list, WordleGame, WordleAI
from advanced_wordle_ai import OptimizedWordleAI

class WordleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Wordle AI Solver")
        self.root.geometry("800x700")
        self.root.configure(bg='#f0f0f0')
        
        # Load word list and initialize AI
        self.word_list = load_word_list()
        self.ai = OptimizedWordleAI(self.word_list)
        
        # Game state
        self.current_word = None
        self.attempts = 0
        self.max_attempts = 6
        self.game_over = False
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the user interface."""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Wordle AI Solver", 
                               font=('Arial', 24, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Game controls frame
        controls_frame = ttk.LabelFrame(main_frame, text="Game Controls", padding="10")
        controls_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # New game button
        self.new_game_btn = ttk.Button(controls_frame, text="New Game", 
                                      command=self.new_game)
        self.new_game_btn.grid(row=0, column=0, padx=(0, 10))
        
        # AI solve button
        self.ai_solve_btn = ttk.Button(controls_frame, text="AI Solve", 
                                      command=self.ai_solve)
        self.ai_solve_btn.grid(row=0, column=1, padx=(0, 10))
        
        # Show solution button
        self.show_solution_btn = ttk.Button(controls_frame, text="Show Solution", 
                                           command=self.show_solution)
        self.show_solution_btn.grid(row=0, column=2, padx=(0, 10))
        
        # AI info button
        self.ai_info_btn = ttk.Button(controls_frame, text="AI Info", 
                                     command=self.show_ai_info)
        self.ai_info_btn.grid(row=0, column=3)
        
        # Game board frame
        board_frame = ttk.LabelFrame(main_frame, text="Game Board", padding="10")
        board_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # Create game board
        self.board_labels = []
        for row in range(6):
            row_labels = []
            for col in range(5):
                label = tk.Label(board_frame, text="", width=4, height=2, 
                               font=('Arial', 16, 'bold'), relief='solid', borderwidth=2)
                label.grid(row=row, column=col, padx=2, pady=2)
                row_labels.append(label)
            self.board_labels.append(row_labels)
        
        # Input frame
        input_frame = ttk.LabelFrame(main_frame, text="Make a Guess", padding="10")
        input_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # Word input
        ttk.Label(input_frame, text="Enter 5-letter word:").grid(row=0, column=0, padx=(0, 10))
        self.word_var = tk.StringVar()
        self.word_entry = ttk.Entry(input_frame, textvariable=self.word_var, width=10, 
                                   font=('Arial', 14))
        self.word_entry.grid(row=0, column=1, padx=(0, 10))
        self.word_entry.bind('<Return>', lambda e: self.make_guess())
        
        # Submit button
        self.submit_btn = ttk.Button(input_frame, text="Submit Guess", 
                                    command=self.make_guess)
        self.submit_btn.grid(row=0, column=2, padx=(0, 10))
        
        # Clear button
        self.clear_btn = ttk.Button(input_frame, text="Clear", 
                                   command=self.clear_input)
        self.clear_btn.grid(row=0, column=3)
        
        # Feedback frame
        feedback_frame = ttk.LabelFrame(main_frame, text="Feedback", padding="10")
        feedback_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # Feedback input
        ttk.Label(feedback_frame, text="Enter feedback (G=Green, Y=Yellow, B=Black):").grid(row=0, column=0, padx=(0, 10))
        self.feedback_var = tk.StringVar()
        self.feedback_entry = ttk.Entry(feedback_frame, textvariable=self.feedback_var, 
                                       width=10, font=('Arial', 14))
        self.feedback_entry.grid(row=0, column=1, padx=(0, 10))
        self.feedback_entry.bind('<Return>', lambda e: self.submit_feedback())
        
        # Submit feedback button
        self.submit_feedback_btn = ttk.Button(feedback_frame, text="Submit Feedback", 
                                             command=self.submit_feedback)
        self.submit_feedback_btn.grid(row=0, column=2, padx=(0, 10))
        
        # Auto-feedback button
        self.auto_feedback_btn = ttk.Button(feedback_frame, text="Auto Feedback", 
                                           command=self.auto_feedback)
        self.auto_feedback_btn.grid(row=0, column=3)
        
        # Status frame
        status_frame = ttk.LabelFrame(main_frame, text="Status & AI Info", padding="10")
        status_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 20))
        
        # Status text
        self.status_text = tk.Text(status_frame, height=8, width=80, 
                                  font=('Consolas', 10), wrap=tk.WORD)
        status_scrollbar = ttk.Scrollbar(status_frame, orient=tk.VERTICAL, 
                                        command=self.status_text.yview)
        self.status_text.configure(yscrollcommand=status_scrollbar.set)
        
        self.status_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        status_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Configure status frame grid weights
        status_frame.columnconfigure(0, weight=1)
        status_frame.rowconfigure(0, weight=1)
        
        # Initialize game
        self.new_game()
        
    def new_game(self):
        """Start a new game."""
        self.current_word = random.choice(self.word_list)
        self.attempts = 0
        self.game_over = False
        
        # Reset AI
        self.ai = OptimizedWordleAI(self.word_list)
        
        # Clear board
        for row in self.board_labels:
            for label in row:
                label.config(text="", bg='white', fg='black')
        
        # Clear input
        self.clear_input()
        
        # Update status
        self.log_message(f"New game started! Target word: {self.current_word.upper()}")
        self.log_message(f"AI optimal first word: {self.ai.optimal_first_word.upper()}")
        self.log_message(f"Total possible words: {len(self.ai.possible_words)}")
        
    def make_guess(self):
        """Make a guess."""
        if self.game_over:
            messagebox.showwarning("Game Over", "Game is already over. Start a new game.")
            return
        
        guess = self.word_var.get().strip().lower()
        
        if len(guess) != 5:
            messagebox.showerror("Invalid Input", "Please enter a 5-letter word.")
            return
        
        if guess not in self.word_list:
            messagebox.showerror("Invalid Word", "Word not in dictionary.")
            return
        
        # Display guess on board
        for i, letter in enumerate(guess):
            self.board_labels[self.attempts][i].config(text=letter.upper())
        
        # Get feedback
        feedback = self.get_feedback(guess, self.current_word)
        
        # Update board colors
        for i, (letter, color) in enumerate(zip(guess, feedback)):
            if color == 'G':
                self.board_labels[self.attempts][i].config(bg='green', fg='white')
            elif color == 'Y':
                self.board_labels[self.attempts][i].config(bg='yellow', fg='black')
            else:
                self.board_labels[self.attempts][i].config(bg='gray', fg='white')
        
        # Update AI
        ai_update = self.ai.update_with_feedback(guess, feedback)
        
        # Log results
        self.log_message(f"Guess {self.attempts + 1}: {guess.upper()} | Feedback: {feedback}")
        self.log_message(f"AI update: {ai_update}")
        
        # Check win condition
        if guess == self.current_word:
            self.game_over = True
            self.log_message(f"🎉 CONGRATULATIONS! You solved it in {self.attempts + 1} attempts!")
            messagebox.showinfo("Success!", f"You solved it in {self.attempts + 1} attempts!")
        else:
            self.attempts += 1
            if self.attempts >= self.max_attempts:
                self.game_over = True
                self.log_message(f"❌ Game Over! The word was {self.current_word.upper()}")
                messagebox.showinfo("Game Over", f"The word was {self.current_word.upper()}")
        
        # Clear input
        self.clear_input()
        
    def get_feedback(self, guess, solution):
        """Get Wordle feedback for a guess."""
        feedback = ['B'] * 5
        solution_counter = Counter(solution)
        
        # First pass: greens
        for i in range(5):
            if guess[i] == solution[i]:
                feedback[i] = 'G'
                solution_counter[guess[i]] -= 1
        
        # Second pass: yellows
        for i in range(5):
            if feedback[i] == 'B' and guess[i] in solution and solution_counter[guess[i]] > 0:
                feedback[i] = 'Y'
                solution_counter[guess[i]] -= 1
        
        return ''.join(feedback)
    
    def submit_feedback(self):
        """Submit manual feedback."""
        feedback = self.feedback_var.get().strip().upper()
        
        if len(feedback) != 5:
            messagebox.showerror("Invalid Input", "Please enter 5 characters (G/Y/B).")
            return
        
        if not all(c in 'GYB' for c in feedback):
            messagebox.showerror("Invalid Input", "Feedback must contain only G, Y, or B.")
            return
        
        # Update AI with feedback
        ai_update = self.ai.update_with_feedback(self.last_guess, feedback)
        self.log_message(f"Manual feedback: {feedback} | AI update: {ai_update}")
        
        # Clear feedback input
        self.feedback_var.set("")
        
    def auto_feedback(self):
        """Automatically calculate and submit feedback for the last guess."""
        if not hasattr(self, 'last_guess') or not self.current_word:
            messagebox.showwarning("No Guess", "Make a guess first.")
            return
        
        feedback = self.get_feedback(self.last_guess, self.current_word)
        self.feedback_var.set(feedback)
        self.submit_feedback()
    
    def ai_solve(self):
        """Let AI solve the current game."""
        if not self.current_word:
            messagebox.showwarning("No Game", "Start a new game first.")
            return
        
        # Reset AI
        self.ai = OptimizedWordleAI(self.word_list)
        
        self.log_message("🤖 AI solving...")
        
        attempts = 0
        while attempts < 6:
            guess, reasoning = self.ai.get_best_guess()
            
            if not guess:
                self.log_message("❌ AI failed to find a valid guess")
                break
            
            # Display guess on board
            for i, letter in enumerate(guess):
                self.board_labels[attempts][i].config(text=letter.upper())
            
            # Get feedback
            feedback = self.get_feedback(guess, self.current_word)
            
            # Update board colors
            for i, (letter, color) in enumerate(zip(guess, feedback)):
                if color == 'G':
                    self.board_labels[attempts][i].config(bg='green', fg='white')
                elif color == 'Y':
                    self.board_labels[attempts][i].config(bg='yellow', fg='black')
                else:
                    self.board_labels[attempts][i].config(bg='gray', fg='white')
            
            # Update AI
            ai_update = self.ai.update_with_feedback(guess, feedback)
            
            # Log results
            self.log_message(f"AI Guess {attempts + 1}: {guess.upper()} | {reasoning}")
            self.log_message(f"Feedback: {feedback} | {ai_update}")
            
            if guess == self.current_word:
                self.log_message(f"🎉 AI solved it in {attempts + 1} attempts!")
                break
            
            attempts += 1
        
        if attempts >= 6:
            self.log_message(f"❌ AI failed to solve {self.current_word.upper()}")
    
    def show_solution(self):
        """Show the current solution."""
        if self.current_word:
            self.log_message(f"🔍 Solution: {self.current_word.upper()}")
        else:
            messagebox.showwarning("No Game", "Start a new game first.")
    
    def show_ai_info(self):
        """Show AI information and statistics."""
        info = f"""
🤖 AI Information:
• Optimal first word: {self.ai.optimal_first_word.upper()}
• Total words in dictionary: {len(self.word_list)}
• Current possible words: {len(self.ai.possible_words)}
• AI type: OptimizedWordleAI with advanced heuristics

📊 AI Features:
• Information theory-based decision making
• Advanced repeated letter handling
• Position-specific letter frequency analysis
• Common letter combination analysis
• Repeated letter pattern recognition
• Dynamic first word optimization

🎯 AI Strategy:
• Uses entropy to maximize information gain
• Considers both possible solutions and good guess words
• Handles repeated letters with sophisticated logic
• Balances exploration vs exploitation
        """
        
        self.log_message(info)
    
    def clear_input(self):
        """Clear input fields."""
        self.word_var.set("")
        self.feedback_var.set("")
        self.word_entry.focus()
    
    def log_message(self, message):
        """Add message to status log."""
        self.status_text.insert(tk.END, message + "\n")
        self.status_text.see(tk.END)
        self.root.update_idletasks()

def main():
    root = tk.Tk()
    app = WordleGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 