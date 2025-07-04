import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

# Import our AI logic
from wordle_ai_solver import load_word_list
from advanced_wordle_ai import OptimizedWordleAI

class WordleWebBot:
    def __init__(self, headless=False):
        """Initialize the Wordle web bot."""
        self.word_list = load_word_list()
        self.ai = OptimizedWordleAI(self.word_list)
        self.driver = None
        self.headless = headless
        self.wait = None
        
    def setup_driver(self):
        """Setup Chrome driver with automatic driver management."""
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        
        # Add user agent to avoid detection
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        
        # Use webdriver-manager to automatically download and manage ChromeDriver
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.wait = WebDriverWait(self.driver, 10)
        
        print("Chrome driver setup complete!")
        
    def open_wordle(self):
        """Open the Wordle website."""
        self.driver.get("https://www.nytimes.com/games/wordle/index.html")
        time.sleep(2)
        
        # Close any popups or modals
        try:
            # Look for and close any popup buttons
            close_buttons = self.driver.find_elements(By.XPATH, "//button[contains(text(), 'Close') or contains(text(), '×') or contains(text(), 'X')]")
            for button in close_buttons:
                if button.is_displayed():
                    button.click()
                    time.sleep(0.5)
        except:
            pass
        
        print("Wordle website opened successfully!")
        
    def get_game_state(self):
        """Read the current game state from the website."""
        try:
            # Wait a moment for any animations to complete
            time.sleep(1)
            
            # Find all tile rows
            rows = self.driver.find_elements(By.CSS_SELECTOR, "[role='group'][aria-label*='Row']")
            
            attempts = []
            for row in rows:
                tiles = row.find_elements(By.CSS_SELECTOR, "[data-testid='tile']")
                if not tiles or len(tiles) != 5:
                    continue
                    
                # Check if this row has been filled
                first_tile = tiles[0]
                first_state = first_tile.get_attribute("data-state")
                
                # Skip empty rows
                if first_state == "empty" or first_state == "tbd":
                    break
                
                # Read the word and feedback from this row
                word = ""
                feedback = ""
                
                for tile in tiles:
                    # Get the letter from aria-label
                    aria_label = tile.get_attribute("aria-label")
                    if not aria_label:
                        continue
                    
                    # Parse letter from aria-label (format: "1st letter, A" or "1st letter, A, correct")
                    parts = aria_label.split(", ")
                    if len(parts) >= 2:
                        letter = parts[1].strip()
                    else:
                        continue
                    
                    # Get the state
                    state = tile.get_attribute("data-state")
                    
                    word += letter
                    
                    # Map states to our feedback format
                    if state == "correct":
                        feedback += "G"
                    elif state == "present":
                        feedback += "Y"
                    elif state == "absent":
                        feedback += "B"
                    else:
                        # For unknown states, try to infer from aria-label
                        if "correct" in aria_label.lower():
                            feedback += "G"
                        elif "present" in aria_label.lower():
                            feedback += "Y"
                        else:
                            feedback += "B"
                
                # Only add if we have a complete 5-letter word
                if len(word) == 5 and len(feedback) == 5:
                    attempts.append((word.lower(), feedback))
                    print(f"Read attempt: {word.lower()} -> {feedback}")
            
            return attempts
            
        except Exception as e:
            print(f"Error reading game state: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def is_game_over(self):
        """Check if the game is over."""
        try:
            # Look for game over indicators
            game_over_indicators = [
                "//div[contains(text(), 'Not in word list')]",
                "//div[contains(text(), 'Game Over')]",
                "//div[contains(text(), 'Congratulations')]",
                "//div[contains(text(), 'You win')]"
            ]
            
            for xpath in game_over_indicators:
                try:
                    element = self.driver.find_element(By.XPATH, xpath)
                    if element.is_displayed():
                        return True
                except:
                    continue
            
            # Check if we've made 6 attempts
            attempts = self.get_game_state()
            return len(attempts) >= 6
            
        except Exception as e:
            print(f"Error checking game over: {e}")
            return False
    
    def is_game_won(self):
        """Check if the game was won."""
        try:
            # Look for win indicators
            win_indicators = [
                "//div[contains(text(), 'Congratulations')]",
                "//div[contains(text(), 'You win')]",
                "//div[contains(text(), 'Well done')]"
            ]
            
            for xpath in win_indicators:
                try:
                    element = self.driver.find_element(By.XPATH, xpath)
                    if element.is_displayed():
                        return True
                except:
                    continue
            
            return False
            
        except Exception as e:
            print(f"Error checking game won: {e}")
            return False
    
    def make_guess(self, word):
        """Make a guess by typing the word and pressing Enter."""
        try:
            # Type the word
            actions = webdriver.ActionChains(self.driver)
            actions.send_keys(word.upper())
            actions.send_keys(Keys.RETURN)
            actions.perform()
            
            # Wait for the animation to complete
            time.sleep(3)
            
            print(f"Made guess: {word.upper()}")
            return True
            
        except Exception as e:
            print(f"Error making guess: {e}")
            return False
    
    def reset_ai(self):
        """Reset the AI for a new game."""
        self.ai = OptimizedWordleAI(self.word_list)
    
    def debug_tile_structure(self):
        """Debug method to inspect the actual tile structure."""
        try:
            print("\n=== DEBUG: Inspecting tile structure ===")
            
            # Find all tile rows
            rows = self.driver.find_elements(By.CSS_SELECTOR, "[role='group'][aria-label*='Row']")
            print(f"Found {len(rows)} rows")
            
            for i, row in enumerate(rows):
                tiles = row.find_elements(By.CSS_SELECTOR, "[data-testid='tile']")
                
                # Check if this row is completely empty
                all_empty = True
                for tile in tiles:
                    data_state = tile.get_attribute("data-state")
                    if data_state != "empty" and data_state != "tbd":
                        all_empty = False
                        break
                
                # Skip printing if row is completely empty
                if all_empty:
                    continue
                
                print(f"\nRow {i+1}:")
                print(f"  Found {len(tiles)} tiles")
                
                for j, tile in enumerate(tiles):
                    aria_label = tile.get_attribute("aria-label")
                    data_state = tile.get_attribute("data-state")
                    text_content = tile.text
                    
                    print(f"    Tile {j+1}: aria-label='{aria_label}', data-state='{data_state}', text='{text_content}'")
            
            print("=== END DEBUG ===\n")
            
        except Exception as e:
            print(f"Debug error: {e}")

    def play_game(self):
        """Play a complete Wordle game using AI."""
        try:
            self.setup_driver()
            self.open_wordle()
            
            print("Starting AI Wordle game...")
            
            attempts_made = 0
            max_attempts = 6
            
            while attempts_made < max_attempts:
                # Get current game state
                attempts = self.get_game_state()
                print(f"Current attempts: {attempts}")
                
                # Check if we already won (GGGGG feedback)
                if attempts and attempts[-1][1] == 'GGGGG':
                    print(f"🎉 AI won in {len(attempts)} attempts!")
                    break
                
                # Check if we've reached max attempts
                if len(attempts) >= max_attempts:
                    print(f"😔 AI failed to solve the word in {max_attempts} attempts")
                    break
                
                # Update AI with all previous attempts
                for word, feedback in attempts:
                    self.ai.update_with_feedback(word, feedback)
                
                # Get AI's best guess
                guess, reasoning = self.ai.get_best_guess()
                if not guess:
                    print("AI cannot find a valid guess!")
                    break
                
                print(f"AI reasoning: {reasoning}")
                print(f"AI suggests: {guess.upper()}")
                
                # Make the guess
                if not self.make_guess(guess):
                    print("Failed to make guess!")
                    break
                
                attempts_made += 1
                
                # Wait a bit before next iteration
                time.sleep(2)
            
            # Check final result
            final_attempts = self.get_game_state()
            if final_attempts and final_attempts[-1][1] == 'GGGGG':
                print(f"🎉 AI won in {len(final_attempts)} attempts!")
            elif len(final_attempts) >= max_attempts:
                print(f"😔 AI failed to solve the word in {max_attempts} attempts")
            else:
                print("😔 AI failed to solve the word")
            
            # Wait a bit to see the result
            time.sleep(5)
            
        except Exception as e:
            print(f"Error during gameplay: {e}")
            import traceback
            traceback.print_exc()
        finally:
            if self.driver:
                self.driver.quit()
    
    def play_multiple_games(self, num_games=5):
        """Play multiple games and track statistics."""
        stats = {'games_played': 0, 'games_won': 0, 'attempts': []}
        
        for game_num in range(num_games):
            print(f"\n{'='*50}")
            print(f"Starting Game {game_num + 1}/{num_games}")
            print(f"{'='*50}")
            
            try:
                self.setup_driver()
                self.open_wordle()
                self.reset_ai()
                
                max_attempts = 6
                attempts_made = 0
                
                while attempts_made < max_attempts:
                    attempts = self.get_game_state()
                    
                    # Check if we already won (GGGGG feedback)
                    if attempts and attempts[-1][1] == 'GGGGG':
                        print(f"🎉 AI won in {len(attempts)} attempts!")
                        break
                    
                    # Check if we've reached max attempts
                    if len(attempts) >= max_attempts:
                        print(f"😔 AI failed to solve the word in {max_attempts} attempts")
                        break
                    
                    # Update AI with all previous attempts
                    for word, feedback in attempts:
                        self.ai.update_with_feedback(word, feedback)
                    
                    # Get AI's best guess
                    guess, reasoning = self.ai.get_best_guess()
                    if not guess:
                        print("AI cannot find a valid guess!")
                        break
                    
                    print(f"AI suggests: {guess.upper()} | Reasoning: {reasoning}")
                    
                    # Make the guess
                    if not self.make_guess(guess):
                        print("Failed to make guess!")
                        break
                    
                    attempts_made += 1
                    time.sleep(1)
                
                # Record result
                final_attempts = self.get_game_state()
                stats['games_played'] += 1
                
                if final_attempts and final_attempts[-1][1] == 'GGGGG':
                    stats['games_won'] += 1
                    stats['attempts'].append(len(final_attempts))
                    print(f"🎉 Won in {len(final_attempts)} attempts!")
                else:
                    print("😔 Failed to solve")
                
                time.sleep(3)
                
            except Exception as e:
                print(f"Error in game {game_num + 1}: {e}")
            finally:
                if self.driver:
                    self.driver.quit()
        
        # Print final statistics
        print(f"\n{'='*50}")
        print("FINAL STATISTICS")
        print(f"{'='*50}")
        print(f"Games Played: {stats['games_played']}")
        print(f"Games Won: {stats['games_won']}")
        if stats['games_played'] > 0:
            win_rate = (stats['games_won'] / stats['games_played']) * 100
            print(f"Win Rate: {win_rate:.1f}%")
        if stats['attempts']:
            avg_attempts = sum(stats['attempts']) / len(stats['attempts'])
            print(f"Average Attempts (wins): {avg_attempts:.1f}")
            print(f"Attempts distribution: {stats['attempts']}")

def main():
    """Main function to run the Wordle web bot."""
    print("Wordle Web Bot - AI Solver")
    print("=" * 40)
    print("Starting single game mode...")
    
    # Create and run the bot
    bot = WordleWebBot(headless=False)
    bot.play_game()

if __name__ == "__main__":
    main() 