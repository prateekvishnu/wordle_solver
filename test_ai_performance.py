import unittest
import random
import time
from collections import defaultdict
from wordle_ai_solver import load_word_list, WordleGame, WordleAI

class TestAIPerformance(unittest.TestCase):
    """Test suite for AI performance across multiple words."""
    
    @classmethod
    def setUpClass(cls):
        """Load word list once for all tests."""
        cls.word_list = load_word_list()
        print(f"Loaded {len(cls.word_list)} words for testing")
    
    def test_ai_solves_random_words(self):
        """Test AI performance on 100 random words."""
        print("\n" + "="*60)
        print("AI PERFORMANCE TEST - 100 RANDOM WORDS")
        print("="*60)
        
        # Select 1000 random words
        test_words = random.sample(self.word_list, 1000)
        
        # Statistics tracking
        stats = {
            'total_words': len(test_words),
            'solved': 0,
            'failed': 0,
            'attempts_distribution': defaultdict(int),
            'avg_attempts': 0,
            'max_attempts': 0,
            'min_attempts': float('inf'),
            'failed_words': [],
            'performance_by_attempts': defaultdict(list)
        }
        
        start_time = time.time()
        
        for i, solution in enumerate(test_words, 1):
            print(f"\nTest {i}/100: Testing word '{solution.upper()}'")
            
            # Create game with specific solution
            game = WordleGame(self.word_list)
            game.solution = solution  # Override random selection
            
            # Create AI
            ai = WordleAI(self.word_list)
            
            # Play the game
            attempts_made = 0
            solved = False
            
            while not game.is_over() and attempts_made < 6:
                # Get AI's best guess
                guess, reasoning = ai.get_best_guess()
                
                if not guess:
                    print(f"  ❌ AI cannot find valid guess after {attempts_made} attempts")
                    break
                
                # Make the guess
                feedback, error = game.guess(guess)
                if error:
                    print(f"  ❌ Error making guess: {error}")
                    break
                
                attempts_made += 1
                print(f"  Attempt {attempts_made}: {guess.upper()} -> {feedback} | {reasoning}")
                
                # Update AI with feedback
                ai.update_with_feedback(guess, feedback)
                
                # Check if solved
                if game.solved:
                    solved = True
                    break
            
            # Record results
            if solved:
                stats['solved'] += 1
                stats['attempts_distribution'][attempts_made] += 1
                stats['performance_by_attempts'][attempts_made].append(solution)
                
                if attempts_made < stats['min_attempts']:
                    stats['min_attempts'] = attempts_made
                if attempts_made > stats['max_attempts']:
                    stats['max_attempts'] = attempts_made
                
                print(f"  ✅ SOLVED in {attempts_made} attempts!")
            else:
                stats['failed'] += 1
                stats['failed_words'].append(solution)
                print(f"  ❌ FAILED to solve '{solution.upper()}'")
        
        # Calculate final statistics
        end_time = time.time()
        total_time = end_time - start_time
        
        if stats['solved'] > 0:
            total_attempts = sum(attempts * count for attempts, count in stats['attempts_distribution'].items())
            stats['avg_attempts'] = total_attempts / stats['solved']
        
        # Print comprehensive results
        self.print_performance_report(stats, total_time)
        
        # Assertions for minimum performance
        self.assertGreaterEqual(stats['solved'], 90, f"AI should solve at least 90% of words, but only solved {stats['solved']}%")
        self.assertLessEqual(stats['avg_attempts'], 4.5, f"AI should average 4.5 or fewer attempts, but averaged {stats['avg_attempts']:.2f}")
    
    def test_ai_handles_edge_cases(self):
        """Test AI on edge cases like repeated letters, rare words."""
        print("\n" + "="*60)
        print("AI EDGE CASE TESTING")
        print("="*60)
        
        # Test words with repeated letters
        repeated_letter_words = ['eerie', 'seeds', 'speed', 'steer', 'wheel']
        
        for word in repeated_letter_words:
            if word in self.word_list:
                print(f"\nTesting repeated letters: '{word.upper()}'")
                self.test_single_word(word)
        
        # Test some common first guesses
        common_starts = ['stare', 'crane', 'slate', 'audio', 'raise']
        
        for word in common_starts:
            if word in self.word_list:
                print(f"\nTesting common start word: '{word.upper()}'")
                self.test_single_word(word)
    
    def test_single_word(self, solution):
        """Test AI on a single word and return results."""
        game = WordleGame(self.word_list)
        game.solution = solution
        
        ai = WordleAI(self.word_list)
        attempts = []
        
        while not game.is_over():
            guess, reasoning = ai.get_best_guess()
            
            if not guess:
                print(f"  ❌ AI cannot find valid guess")
                return False
            
            feedback, error = game.guess(guess)
            if error:
                print(f"  ❌ Error: {error}")
                return False
            
            attempts.append((guess, feedback))
            print(f"  {guess.upper()} -> {feedback}")
            
            ai.update_with_feedback(guess, feedback)
            
            if game.solved:
                print(f"  ✅ Solved in {len(attempts)} attempts!")
                return True
        
        print(f"  ❌ Failed to solve '{solution.upper()}'")
        return False
    
    def print_performance_report(self, stats, total_time):
        """Print a comprehensive performance report."""
        print("\n" + "="*60)
        print("PERFORMANCE REPORT")
        print("="*60)
        
        print(f"Total Words Tested: {stats['total_words']}")
        print(f"Successfully Solved: {stats['solved']}")
        print(f"Failed to Solve: {stats['failed']}")
        print(f"Success Rate: {(stats['solved']/stats['total_words'])*100:.1f}%")
        
        if stats['solved'] > 0:
            print(f"\nAttempts Statistics:")
            print(f"  Average Attempts: {stats['avg_attempts']:.2f}")
            print(f"  Minimum Attempts: {stats['min_attempts']}")
            print(f"  Maximum Attempts: {stats['max_attempts']}")
            
            print(f"\nAttempts Distribution:")
            for attempts in sorted(stats['attempts_distribution'].keys()):
                count = stats['attempts_distribution'][attempts]
                percentage = (count / stats['solved']) * 100
                print(f"  {attempts} attempts: {count} words ({percentage:.1f}%)")
        
        if stats['failed_words']:
            print(f"\nFailed Words ({len(stats['failed_words'])}):")
            for word in stats['failed_words'][:10]:  # Show first 10
                print(f"  {word.upper()}")
            if len(stats['failed_words']) > 10:
                print(f"  ... and {len(stats['failed_words']) - 10} more")
        
        print(f"\nPerformance by Attempts:")
        for attempts in sorted(stats['performance_by_attempts'].keys()):
            words = stats['performance_by_attempts'][attempts]
            print(f"  {attempts} attempts: {', '.join(words[:5])}{'...' if len(words) > 5 else ''}")
        
        print(f"\nTotal Test Time: {total_time:.2f} seconds")
        print(f"Average Time per Word: {total_time/stats['total_words']:.2f} seconds")
        print("="*60)

class TestAILogic(unittest.TestCase):
    """Test specific AI logic components."""
    
    @classmethod
    def setUpClass(cls):
        """Load word list once for all tests."""
        cls.word_list = load_word_list()
    
    def test_word_filtering(self):
        """Test that AI correctly filters words based on feedback."""
        ai = WordleAI(self.word_list)
        
        # Test with a simple case
        initial_count = len(ai.possible_words)
        
        # Simulate guessing "stare" and getting feedback "GGBBB"
        ai.update_with_feedback("stare", "GGBBB")
        
        # Should have fewer possible words
        self.assertLess(len(ai.possible_words), initial_count)
        
        # All remaining words should start with "st"
        for word in ai.possible_words:
            self.assertTrue(word.startswith("st"))
    
    def test_frequency_calculation(self):
        """Test that letter frequency is calculated correctly."""
        ai = WordleAI(self.word_list)
        
        # Check that frequency data exists
        self.assertIsNotNone(ai.letter_frequency)
        self.assertGreater(len(ai.letter_frequency), 0)
        
        # Check that common letters have higher frequency
        if 'e' in ai.letter_frequency and 'q' in ai.letter_frequency:
            e_freq = sum(ai.letter_frequency['e'])
            q_freq = sum(ai.letter_frequency['q'])
            self.assertGreater(e_freq, q_freq)
    
    def test_reasoning_generation(self):
        """Test that AI generates reasonable explanations."""
        ai = WordleAI(self.word_list)
        
        guess, reasoning = ai.get_best_guess()
        
        self.assertIsNotNone(guess)
        self.assertIsNotNone(reasoning)
        self.assertEqual(len(guess), 5)
        self.assertIn("Chose", reasoning)

def run_performance_test():
    """Run the performance test standalone."""
    print("Running AI Performance Test...")
    
    # Create test instance
    test_instance = TestAIPerformance()
    test_instance.setUpClass()
    
    # Run the performance test
    test_instance.test_ai_solves_random_words()

if __name__ == "__main__":
    # Run the performance test directly
    run_performance_test()
    
    # Or run all unit tests
    # unittest.main(verbosity=2) 