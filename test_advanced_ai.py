import time
import random
from collections import defaultdict
from wordle_ai_solver import load_word_list, WordleGame, WordleAI
from advanced_wordle_ai import OptimizedWordleAI

def compare_ai_performance(num_words=1000):
    """Compare original AI vs advanced AI performance."""
    print("="*80)
    print("AI PERFORMANCE COMPARISON - 1000 WORDS")
    print("="*80)
    
    word_list = load_word_list()
    test_words = random.sample(word_list, num_words)
    
    # Test original AI
    print("\nTesting ORIGINAL AI...")
    original_stats = test_ai_performance_detailed(test_words, WordleAI, "Original")
    
    # Test advanced AI
    print("\nTesting ADVANCED AI...")
    advanced_stats = test_ai_performance_detailed(test_words, OptimizedWordleAI, "Advanced")
    
    # Compare results
    print("\n" + "="*80)
    print("PERFORMANCE COMPARISON SUMMARY")
    print("="*80)
    
    print(f"{'Metric':<20} {'Original AI':<15} {'Advanced AI':<15} {'Improvement':<15}")
    print("-" * 80)
    
    # Success rate
    orig_success = (original_stats['solved'] / original_stats['total_words']) * 100
    adv_success = (advanced_stats['solved'] / advanced_stats['total_words']) * 100
    improvement = adv_success - orig_success
    print(f"{'Success Rate':<20} {orig_success:<15.1f}% {adv_success:<15.1f}% {improvement:<15.1f}%")
    
    # Average attempts
    orig_avg = original_stats['avg_attempts']
    adv_avg = advanced_stats['avg_attempts']
    improvement_avg = orig_avg - adv_avg
    print(f"{'Avg Attempts':<20} {orig_avg:<15.2f} {adv_avg:<15.2f} {improvement_avg:<15.2f}")
    
    # Max attempts
    print(f"{'Max Attempts':<20} {original_stats['max_attempts']:<15} {advanced_stats['max_attempts']:<15}")
    
    # Failed words
    print(f"{'Failed Words':<20} {len(original_stats['failed_words']):<15} {len(advanced_stats['failed_words']):<15}")
    
    print("\n" + "="*80)

def test_ai_performance_detailed(test_words, ai_class, ai_name):
    """Test a specific AI class and return detailed statistics."""
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
        if i % 50 == 0:
            print(f"  Progress: {i}/{len(test_words)}")
        
        # Create game with specific solution
        game = WordleGame(test_words)
        game.solution = solution
        
        # Create AI
        ai = ai_class(test_words)
        
        # Play the game
        attempts_made = 0
        solved = False
        
        while not game.is_over() and attempts_made < 6:
            # Get AI's best guess
            guess, reasoning = ai.get_best_guess()
            
            if not guess:
                break
            
            # Make the guess
            feedback, error = game.guess(guess)
            if error:
                break
            
            attempts_made += 1
            
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
        else:
            stats['failed'] += 1
            stats['failed_words'].append(solution)
    
    # Calculate final statistics
    end_time = time.time()
    total_time = end_time - start_time
    
    if stats['solved'] > 0:
        total_attempts = sum(attempts * count for attempts, count in stats['attempts_distribution'].items())
        stats['avg_attempts'] = total_attempts / stats['solved']
    
    # Print detailed results
    print_detailed_performance_report(stats, total_time, ai_name)
    
    return stats

def print_detailed_performance_report(stats, total_time, ai_name):
    """Print a comprehensive performance report similar to test_ai_performance.py."""
    print(f"\n{ai_name} AI - DETAILED PERFORMANCE REPORT")
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

def test_ai_performance(test_words, ai_class, ai_name):
    """Test a specific AI class and return statistics."""
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
        if i % 10 == 0:
            print(f"  Progress: {i}/{len(test_words)}")
        
        # Create game with specific solution
        game = WordleGame(test_words)
        game.solution = solution
        
        # Create AI
        ai = ai_class(test_words)
        
        # Play the game
        attempts_made = 0
        solved = False
        
        while not game.is_over() and attempts_made < 6:
            # Get AI's best guess
            guess, reasoning = ai.get_best_guess()
            
            if not guess:
                break
            
            # Make the guess
            feedback, error = game.guess(guess)
            if error:
                break
            
            attempts_made += 1
            
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
        else:
            stats['failed'] += 1
            stats['failed_words'].append(solution)
    
    # Calculate final statistics
    end_time = time.time()
    total_time = end_time - start_time
    
    if stats['solved'] > 0:
        total_attempts = sum(attempts * count for attempts, count in stats['attempts_distribution'].items())
        stats['avg_attempts'] = total_attempts / stats['solved']
    
    # Print results
    print(f"\n{ai_name} AI Results:")
    print(f"  Success Rate: {(stats['solved']/stats['total_words'])*100:.1f}%")
    print(f"  Average Attempts: {stats['avg_attempts']:.2f}")
    print(f"  Failed Words: {len(stats['failed_words'])}")
    print(f"  Test Time: {total_time:.2f} seconds")
    
    return stats

def test_specific_words():
    """Test both AIs on specific challenging words."""
    print("\n" + "="*80)
    print("TESTING SPECIFIC CHALLENGING WORDS")
    print("="*80)
    
    word_list = load_word_list()
    
    # Challenging words that might be difficult
    challenging_words = [
        'eerie', 'seeds', 'speed', 'steer', 'wheel', 'queen', 'quick',
        'jumbo', 'zebra', 'xenon', 'vivid', 'puppy', 'mamma', 'daddy'
    ]
    
    for word in challenging_words:
        if word not in word_list:
            continue
            
        print(f"\nTesting word: {word.upper()}")
        
        # Test original AI
        print("  Original AI:")
        test_single_word(word, WordleAI, word_list)
        
        # Test advanced AI
        print("  Advanced AI:")
        test_single_word(word, OptimizedWordleAI, word_list)

def test_single_word(solution, ai_class, word_list):
    """Test a single word with a specific AI."""
    game = WordleGame(word_list)
    game.solution = solution
    
    ai = ai_class(word_list)
    attempts = []
    
    while not game.is_over():
        guess, reasoning = ai.get_best_guess()
        
        if not guess:
            print(f"    ❌ Cannot find valid guess")
            return False
        
        feedback, error = game.guess(guess)
        if error:
            print(f"    ❌ Error: {error}")
            return False
        
        attempts.append((guess, feedback))
        print(f"    {guess.upper()} -> {feedback}")
        
        ai.update_with_feedback(guess, feedback)
        
        if game.solved:
            print(f"    ✅ Solved in {len(attempts)} attempts!")
            return True
    
    print(f"    ❌ Failed to solve")
    return False

def run_comprehensive_test():
    """Run a comprehensive test of both AIs."""
    print("Running comprehensive AI comparison...")
    
    # Test on 1000 words for detailed comparison
    compare_ai_performance(1000)
    
    # Test specific challenging words
    test_specific_words()

if __name__ == "__main__":
    run_comprehensive_test() 