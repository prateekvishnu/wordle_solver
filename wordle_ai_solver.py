import os
import random
from collections import Counter

# ANSI color codes for better UI
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    GRAY = '\033[90m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    RESET = '\033[0m'
    CLEAR = '\033[2J\033[H'
    BLUE = '\033[94m'
    CYAN = '\033[96m'

WORD_LIST_PATH = "wordle_words.txt"

def load_word_list(path=WORD_LIST_PATH):
    """Load all five-letter words from the given file into a list."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"Word list file not found: {path}")
    with open(path, "r") as f:
        words = [line.strip().lower() for line in f if len(line.strip()) == 5]
    return words

class WordleGame:
    def __init__(self, word_list):
        self.word_list = word_list
        self.solution = random.choice(self.word_list)
        self.max_attempts = 6
        self.attempts = []
        self.solved = False
        self.start_time = None

    def guess(self, word):
        word = word.lower()
        if len(word) != 5 or word not in self.word_list:
            return None, "Invalid guess. Must be a valid five-letter word."
        feedback = self._generate_feedback(word)
        self.attempts.append((word, feedback))
        if word == self.solution:
            self.solved = True
        return feedback, None

    def _generate_feedback(self, guess):
        # Feedback: 'G' = green, 'Y' = yellow, 'B' = black/gray
        feedback = ['B'] * 5
        solution_counter = Counter(self.solution)
        # First pass: greens
        for i in range(5):
            if guess[i] == self.solution[i]:
                feedback[i] = 'G'
                solution_counter[guess[i]] -= 1
        # Second pass: yellows
        for i in range(5):
            if feedback[i] == 'B' and guess[i] in self.solution and solution_counter[guess[i]] > 0:
                feedback[i] = 'Y'
                solution_counter[guess[i]] -= 1
        return ''.join(feedback)

    def is_over(self):
        return self.solved or len(self.attempts) >= self.max_attempts

    def print_board(self):
        """Print a nicely formatted game board with colors."""
        print(f"\n{Colors.BOLD}WORDLE{Colors.RESET}")
        print("=" * 30)
        
        # Print the game grid
        for i in range(self.max_attempts):
            if i < len(self.attempts):
                word, feedback = self.attempts[i]
                colored_word = ""
                for j, letter in enumerate(word.upper()):
                    if feedback[j] == 'G':
                        colored_word += f"{Colors.GREEN}{Colors.BOLD}{letter}{Colors.RESET} "
                    elif feedback[j] == 'Y':
                        colored_word += f"{Colors.YELLOW}{Colors.BOLD}{letter}{Colors.RESET} "
                    else:
                        colored_word += f"{Colors.GRAY}{letter}{Colors.RESET} "
                print(f"  {colored_word}")
            else:
                print("  _ _ _ _ _")
        
        print("=" * 30)
        print(f"Attempts: {len(self.attempts)}/{self.max_attempts}")
        
        if self.solved:
            print(f"{Colors.GREEN}{Colors.BOLD}🎉 CONGRATULATIONS! 🎉{Colors.RESET}")
        elif self.is_over():
            print(f"{Colors.GRAY}Game Over. The word was: {Colors.BOLD}{self.solution.upper()}{Colors.RESET}")

class WordleAI:
    def __init__(self, word_list):
        self.word_list = word_list
        self.possible_words = word_list.copy()
        self.letter_frequency = self._calculate_letter_frequency(word_list)
        
    def _calculate_letter_frequency(self, words):
        """Calculate letter frequency across all positions in the word list."""
        frequency = {}
        for word in words:
            for i, letter in enumerate(word):
                if letter not in frequency:
                    frequency[letter] = [0] * 5
                frequency[letter][i] += 1
        return frequency
    
    def _filter_words(self, guess, feedback):
        """Filter possible words based on the guess and feedback."""
        filtered_words = []
        
        for word in self.possible_words:
            if self._word_matches_feedback(word, guess, feedback):
                filtered_words.append(word)
        
        self.possible_words = filtered_words
        return filtered_words
    
    def _word_matches_feedback(self, word, guess, feedback):
        """Check if a word matches the feedback from a guess."""
        # Create a copy of the word to track used letters
        word_chars = list(word)
        guess_chars = list(guess)
        
        # First pass: check greens (exact matches)
        for i in range(5):
            if feedback[i] == 'G':
                if word[i] != guess[i]:
                    return False
                # Mark as used
                word_chars[i] = None
                guess_chars[i] = None
        
        # Second pass: check yellows and grays
        for i in range(5):
            if guess_chars[i] is None:  # Already processed
                continue
                
            if feedback[i] == 'Y':
                # Letter must be in word but not at this position
                if guess[i] not in word_chars:
                    return False
                # Remove the first occurrence of this letter
                for j in range(5):
                    if word_chars[j] == guess[i]:
                        word_chars[j] = None
                        break
            elif feedback[i] == 'B':
                # Letter should not be in word (unless it's a yellow elsewhere)
                if guess[i] in word_chars:
                    return False
        
        return True
    
    def _calculate_word_score(self, word):
        """Calculate a score for a word based on letter frequency and coverage."""
        score = 0
        unique_letters = set(word)
        
        # Score based on letter frequency
        for letter in unique_letters:
            if letter in self.letter_frequency:
                # Sum frequency across all positions
                score += sum(self.letter_frequency[letter])
        
        # Bonus for words with more unique letters
        score += len(unique_letters) * 10
        
        return score
    
    def get_best_guess(self, game_state=None):
        """Get the best guess based on current possible words."""
        if not self.possible_words:
            return None, "No possible words remaining"
        
        # If we have very few possible words, pick the first one
        if len(self.possible_words) <= 2:
            return self.possible_words[0], f"Only {len(self.possible_words)} possible words remaining"
        
        # Calculate scores for all possible words
        word_scores = []
        for word in self.possible_words:
            score = self._calculate_word_score(word)
            word_scores.append((word, score))
        
        # Sort by score (highest first)
        word_scores.sort(key=lambda x: x[1], reverse=True)
        
        best_word = word_scores[0][0]
        best_score = word_scores[0][1]
        
        # Generate reasoning
        reasoning = self._generate_reasoning(best_word, word_scores[:5])
        
        return best_word, reasoning
    
    def _generate_reasoning(self, word, top_words):
        """Generate reasoning for why this word was chosen."""
        unique_letters = set(word)
        reasoning_parts = []
        
        # Letter coverage reasoning
        reasoning_parts.append(f"Chose '{word.upper()}' with {len(unique_letters)} unique letters")
        
        # Frequency reasoning
        total_freq = sum(sum(self.letter_frequency.get(letter, [0])) for letter in unique_letters)
        reasoning_parts.append(f"Total letter frequency score: {total_freq}")
        
        # Remaining words reasoning
        reasoning_parts.append(f"Eliminates from {len(self.possible_words)} possible words")
        
        # Alternative words
        if len(top_words) > 1:
            alternatives = [w[0].upper() for w in top_words[1:3]]
            reasoning_parts.append(f"Alternatives considered: {', '.join(alternatives)}")
        
        return " | ".join(reasoning_parts)
    
    def update_with_feedback(self, guess, feedback):
        """Update AI state with new guess and feedback."""
        remaining_count = len(self.possible_words)
        self._filter_words(guess, feedback)
        new_count = len(self.possible_words)
        
        return f"Filtered from {remaining_count} to {new_count} possible words"

class WordleUI:
    def __init__(self, word_list):
        self.word_list = word_list
        self.stats = {'games_played': 0, 'games_won': 0, 'current_streak': 0}
        self.ai = WordleAI(word_list)

    def show_help(self):
        """Display help information."""
        print(f"\n{Colors.BOLD}HOW TO PLAY:{Colors.RESET}")
        print("• Guess the 5-letter word in 6 attempts")
        print("• After each guess, you'll see:")
        print(f"  {Colors.GREEN}GREEN{Colors.RESET} = Letter is correct and in right position")
        print(f"  {Colors.YELLOW}YELLOW{Colors.RESET} = Letter is in the word but wrong position")
        print(f"  {Colors.GRAY}GRAY{Colors.RESET} = Letter is not in the word")
        print("\nCommands:")
        print("• Enter a 5-letter word to guess")
        print("• Type 'help' for this message")
        print("• Type 'quit' to exit")
        print("• Type 'new' to start a new game")
        print("• Type 'ai' to let AI play")
        print("• Type 'watch' to watch AI solve")

    def show_stats(self):
        """Display game statistics."""
        print(f"\n{Colors.BOLD}STATISTICS:{Colors.RESET}")
        print(f"Games Played: {self.stats['games_played']}")
        if self.stats['games_played'] > 0:
            win_rate = (self.stats['games_won'] / self.stats['games_played']) * 100
            print(f"Win Rate: {win_rate:.1f}%")
        print(f"Current Streak: {self.stats['current_streak']}")

    def ai_play_game(self, game):
        """Let AI play a complete game."""
        print(f"{Colors.BLUE}AI is playing...{Colors.RESET}")
        
        while not game.is_over():
            game.print_board()
            
            # Get AI's best guess
            guess, reasoning = self.ai.get_best_guess()
            if not guess:
                print(f"{Colors.GRAY}AI cannot find a valid guess{Colors.RESET}")
                break
            
            print(f"\n{Colors.CYAN}AI's guess: {Colors.BOLD}{guess.upper()}{Colors.RESET}")
            print(f"{Colors.GRAY}Reasoning: {reasoning}{Colors.RESET}")
            
            # Make the guess
            feedback, error = game.guess(guess)
            if error:
                print(f"{Colors.GRAY}AI error: {error}{Colors.RESET}")
                break
            
            # Update AI with feedback
            filter_info = self.ai.update_with_feedback(guess, feedback)
            print(f"{Colors.GRAY}{filter_info}{Colors.RESET}")
            
            # Small delay for readability
            import time
            time.sleep(1)
        
        # Game over
        game.print_board()
        
        if game.solved:
            print(f"\n{Colors.GREEN}AI solved it in {len(game.attempts)} attempts!{Colors.RESET}")
            return True
        else:
            print(f"\n{Colors.GRAY}AI failed to solve the word.{Colors.RESET}")
            return False

    def play_game(self):
        """Main game loop."""
        print(f"{Colors.CLEAR}{Colors.BOLD}Welcome to WORDLE!{Colors.RESET}")
        self.show_help()
        
        while True:
            print(f"\n{Colors.BOLD}Starting new game...{Colors.RESET}")
            game = WordleGame(self.word_list)
            self.stats['games_played'] += 1
            
            # Reset AI for new game
            self.ai = WordleAI(self.word_list)
            
            # Ask for play mode
            mode = input(f"\n{Colors.BOLD}Play mode (human/ai/watch): {Colors.RESET}").strip().lower()
            
            if mode == 'quit':
                print("Thanks for playing!")
                return
            elif mode == 'help':
                self.show_help()
                continue
            elif mode == 'stats':
                self.show_stats()
                continue
            elif mode == 'ai':
                # AI plays the game
                ai_won = self.ai_play_game(game)
                if ai_won:
                    self.stats['games_won'] += 1
                    self.stats['current_streak'] += 1
                else:
                    self.stats['current_streak'] = 0
            elif mode == 'watch':
                # Watch AI play
                ai_won = self.ai_play_game(game)
                # Don't count AI games in human stats
                self.stats['games_played'] -= 1
            else:
                # Human plays the game
                while not game.is_over():
                    game.print_board()
                    
                    guess = input(f"\n{Colors.BOLD}Enter your guess: {Colors.RESET}").strip().lower()
                    
                    if guess == 'quit':
                        print("Thanks for playing!")
                        return
                    elif guess == 'help':
                        self.show_help()
                        continue
                    elif guess == 'new':
                        break
                    elif guess == 'stats':
                        self.show_stats()
                        continue
                    elif guess == 'ai':
                        # Switch to AI mode mid-game
                        ai_won = self.ai_play_game(game)
                        if ai_won:
                            self.stats['games_won'] += 1
                            self.stats['current_streak'] += 1
                        else:
                            self.stats['current_streak'] = 0
                        break
                    
                    feedback, error = game.guess(guess)
                    if error:
                        print(f"{Colors.GRAY}{error}{Colors.RESET}")
                        continue
                
                # Game over for human play
                if not game.is_over():
                    game.print_board()
                    
                    if game.solved:
                        self.stats['games_won'] += 1
                        self.stats['current_streak'] += 1
                        print(f"\n{Colors.GREEN}You won in {len(game.attempts)} attempts!{Colors.RESET}")
                    else:
                        self.stats['current_streak'] = 0
                        print(f"\n{Colors.GRAY}Better luck next time!{Colors.RESET}")
            
            self.show_stats()
            
            play_again = input(f"\n{Colors.BOLD}Play again? (y/n): {Colors.RESET}").strip().lower()
            if play_again not in ['y', 'yes']:
                print("Thanks for playing!")
                break

if __name__ == "__main__":
    try:
        words = load_word_list()
        print(f"Loaded {len(words)} five-letter words.")
        
        ui = WordleUI(words)
        ui.play_game()
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Please ensure wordle_words.txt is in the same directory.")
    except KeyboardInterrupt:
        print(f"\n{Colors.GRAY}Game interrupted. Thanks for playing!{Colors.RESET}")
    except Exception as e:
        print(f"Unexpected error: {e}") 