import math
from collections import Counter, defaultdict
from wordle_ai_solver import load_word_list

class AdvancedWordleAI:
    """Advanced AI solver using information theory and entropy-based decision making."""
    
    def __init__(self, word_list):
        self.word_list = word_list
        self.possible_words = word_list.copy()
        self.letter_frequency = self._calculate_letter_frequency(word_list)
        self.position_frequency = self._calculate_position_frequency(word_list)
        self.word_scores = self._calculate_word_scores(word_list)
        # Fixed list of common optimal starter words
        self.starter_words = ['raise', 'stare', 'crane', 'slate', 'audio', 'roate', 'soare', 'arise', 'irate', 'orate', 'least', 'steal', 'tears']
        
    def _calculate_letter_frequency(self, words):
        """Calculate letter frequency across all positions."""
        frequency = {}
        for word in words:
            for i, letter in enumerate(word):
                if letter not in frequency:
                    frequency[letter] = [0] * 5
                frequency[letter][i] += 1
        return frequency
    
    def _calculate_position_frequency(self, words):
        """Calculate letter frequency for each position specifically."""
        position_freq = [defaultdict(int) for _ in range(5)]
        for word in words:
            for i, letter in enumerate(word):
                position_freq[i][letter] += 1
        return position_freq
    
    def _calculate_word_scores(self, words):
        """Pre-calculate scores for all words based on multiple factors."""
        scores = {}
        for word in words:
            score = 0
            unique_letters = set(word)
            
            # Letter frequency score
            for letter in unique_letters:
                score += sum(self.letter_frequency.get(letter, [0]))
            
            # Position-specific frequency bonus
            for i, letter in enumerate(word):
                score += self.position_frequency[i].get(letter, 0) * 2
            
            # Unique letter bonus
            score += len(unique_letters) * 50
            
            # Vowel/consonant balance bonus
            vowels = sum(1 for letter in word if letter in 'aeiou')
            if 1 <= vowels <= 3:  # Optimal vowel count
                score += 100
            
            # Common letter combinations bonus
            common_patterns = ['th', 'er', 'on', 'an', 're', 'he', 'in', 'ed', 'nd', 'ha']
            for pattern in common_patterns:
                if pattern in word:
                    score += 20
            
            scores[word] = score
        return scores
    
    def _calculate_entropy(self, word, possible_words):
        """Calculate the information entropy of a word based on possible outcomes."""
        if not possible_words:
            return 0
        
        # Simulate all possible feedback patterns for this word
        feedback_counts = defaultdict(int)
        
        for solution in possible_words:
            feedback = self._simulate_feedback(word, solution)
            feedback_counts[feedback] += 1
        
        # Calculate entropy
        entropy = 0
        total_words = len(possible_words)
        
        for count in feedback_counts.values():
            probability = count / total_words
            if probability > 0:
                entropy -= probability * math.log2(probability)
        
        return entropy
    
    def _simulate_feedback(self, guess, solution):
        """Simulate Wordle feedback for a guess against a solution."""
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
    
    def _filter_words_by_feedback(self, guess, feedback):
        """Filter possible words based on feedback using advanced logic."""
        filtered_words = []
        
        for word in self.possible_words:
            if self._word_matches_advanced_feedback(word, guess, feedback):
                filtered_words.append(word)
        
        return filtered_words
    
    def _word_matches_advanced_feedback(self, word, guess, feedback):
        """Advanced word matching with improved handling of repeated letters."""
        # Create copies to track used letters
        word_chars = list(word)
        guess_chars = list(guess)
        
        # Track letter counts in solution
        solution_letter_counts = Counter(word)
        
        # First pass: check greens (exact matches)
        for i in range(5):
            if feedback[i] == 'G':
                if word[i] != guess[i]:
                    return False
                # Mark as used
                word_chars[i] = None
                guess_chars[i] = None
                solution_letter_counts[guess[i]] -= 1
        
        # Second pass: check yellows and grays with improved repeated letter logic
        for i in range(5):
            if guess_chars[i] is None:  # Already processed
                continue
            
            if feedback[i] == 'Y':
                # Letter must be in word but not at this position
                if guess[i] not in word_chars or solution_letter_counts[guess[i]] <= 0:
                    return False
                # Remove the first occurrence of this letter
                for j in range(5):
                    if word_chars[j] == guess[i]:
                        word_chars[j] = None
                        solution_letter_counts[guess[i]] -= 1
                        break
            elif feedback[i] == 'B':
                # For repeated letters, be more careful
                guess_letter = guess[i]
                guess_count = guess.count(guess_letter)
                
                # Count how many of this letter we've already accounted for
                accounted_for = 0
                for j in range(5):
                    if j != i and guess[j] == guess_letter:
                        if feedback[j] in ['G', 'Y']:
                            accounted_for += 1
                
                # If we have more of this letter in the guess than accounted for,
                # and this position is black, then this letter shouldn't be in the word
                if guess_count > accounted_for:
                    if guess_letter in word_chars and solution_letter_counts[guess_letter] > 0:
                        return False
        
        return True
    
    def _get_optimal_guess(self):
        """Get the optimal guess using entropy and information theory."""
        if not self.possible_words:
            return None, "No possible words remaining"
        
        # For first guess, use the first available starter word
        if len(self.possible_words) == len(self.word_list):
            for word in self.starter_words:
                if word in self.word_list and word in self.possible_words:
                    return word, f"Using starter word: {word.upper()}"
            # Fallback if none found
            return self.possible_words[0], "Fallback: first word in list"
        
        # If we have very few possible words, pick the best one
        if len(self.possible_words) <= 3:
            best_word = max(self.possible_words, key=lambda w: self.word_scores.get(w, 0))
            return best_word, f"Only {len(self.possible_words)} possible words remaining"
        
        # Calculate entropy for all possible guesses
        best_entropy = -1
        best_word = None
        best_reasoning = ""
        
        # Consider both possible solutions and good guess words
        candidate_words = list(set(self.possible_words + self.word_list[:100]))  # Top 100 words as candidates
        
        for word in candidate_words:
            entropy = self._calculate_entropy(word, self.possible_words)
            
            # Bonus for words that are possible solutions
            if word in self.possible_words:
                entropy += 0.5
            
            # Bonus for high-scoring words
            score_bonus = self.word_scores.get(word, 0) / 1000
            entropy += score_bonus
            
            if entropy > best_entropy:
                best_entropy = entropy
                best_word = word
                best_reasoning = f"Entropy: {entropy:.3f}, Score: {self.word_scores.get(word, 0)}"
        
        return best_word, best_reasoning
    
    def get_best_guess(self):
        """Get the best guess using advanced AI logic."""
        guess, reasoning = self._get_optimal_guess()
        
        if not guess:
            return None, "No valid guess found"
        
        # Generate detailed reasoning
        unique_letters = set(guess)
        reasoning_parts = [
            f"Chose '{guess.upper()}' with {len(unique_letters)} unique letters",
            f"Information gain: {reasoning}",
            f"Eliminates from {len(self.possible_words)} possible words"
        ]
        
        # Add position-specific reasoning
        position_info = []
        for i, letter in enumerate(guess):
            freq = self.position_frequency[i].get(letter, 0)
            position_info.append(f"{letter}({freq})")
        reasoning_parts.append(f"Position scores: {' '.join(position_info)}")
        
        return guess, " | ".join(reasoning_parts)
    
    def update_with_feedback(self, guess, feedback):
        """Update AI state with new guess and feedback."""
        remaining_count = len(self.possible_words)
        self.possible_words = self._filter_words_by_feedback(guess, feedback)
        new_count = len(self.possible_words)
        
        return f"Filtered from {remaining_count} to {new_count} possible words"

class OptimizedWordleAI(AdvancedWordleAI):
    """Further optimized AI with additional heuristics."""
    
    def __init__(self, word_list):
        super().__init__(word_list)
        self.common_words = self._identify_common_words()
        self.letter_combinations = self._analyze_letter_combinations()
        self.repeated_letter_patterns = self._analyze_repeated_letter_patterns()
    
    def _identify_common_words(self):
        """Identify commonly used words for better first guesses."""
        # Words that are good starting words based on research
        common_starters = [
            'stare', 'crane', 'slate', 'audio', 'raise', 'roate', 'soare',
            'arise', 'irate', 'orate', 'stale', 'least', 'steal', 'tears'
        ]
        return set(common_starters)
    
    def _analyze_letter_combinations(self):
        """Analyze common letter combinations for better scoring."""
        combinations = defaultdict(int)
        for word in self.word_list:
            for i in range(4):
                combo = word[i:i+2]
                combinations[combo] += 1
        return combinations
    
    def _analyze_repeated_letter_patterns(self):
        """Analyze patterns of repeated letters in the word list."""
        patterns = defaultdict(int)
        for word in self.word_list:
            letter_counts = Counter(word)
            # Create pattern of repeated letters
            pattern = []
            for letter, count in letter_counts.items():
                if count > 1:
                    pattern.append(f"{letter}{count}")
            if pattern:
                pattern_str = "".join(sorted(pattern))
                patterns[pattern_str] += 1
        return patterns
    
    def _get_optimal_guess(self):
        """Enhanced optimal guess selection with additional heuristics."""
        if not self.possible_words:
            return None, "No possible words remaining"
        
        # For first guess, use the first available starter word
        if len(self.possible_words) == len(self.word_list):
            for word in self.starter_words:
                if word in self.word_list and word in self.possible_words:
                    return word, f"Using starter word: {word.upper()}"
            # Fallback if none found
            return self.possible_words[0], "Fallback: first word in list"
        
        # If we have very few possible words, pick the best one
        if len(self.possible_words) <= 2:
            best_word = max(self.possible_words, key=lambda w: self.word_scores.get(w, 0))
            return best_word, f"Only {len(self.possible_words)} possible words remaining"
        
        # Calculate entropy with additional heuristics
        best_entropy = -1
        best_word = None
        best_reasoning = ""
        
        # Consider possible solutions first, then good guess words
        candidate_words = list(self.possible_words) + [w for w in self.word_list[:200] if w not in self.possible_words]
        
        for word in candidate_words:
            entropy = self._calculate_entropy(word, self.possible_words)
            
            # Bonus for possible solutions
            if word in self.possible_words:
                entropy += 1.0
            
            # Bonus for high-scoring words
            score_bonus = self.word_scores.get(word, 0) / 2000
            entropy += score_bonus
            
            # Bonus for common letter combinations
            combo_bonus = 0
            for i in range(4):
                combo = word[i:i+2]
                combo_bonus += self.letter_combinations.get(combo, 0) / 1000
            entropy += combo_bonus
            
            # Bonus for words that handle repeated letters well
            letter_counts = Counter(word)
            repeated_letters = [letter for letter, count in letter_counts.items() if count > 1]
            if repeated_letters:
                # If this pattern is common in solutions, it's good
                pattern = []
                for letter in repeated_letters:
                    pattern.append(f"{letter}{letter_counts[letter]}")
                pattern_str = "".join(sorted(pattern))
                if pattern_str in self.repeated_letter_patterns:
                    entropy += self.repeated_letter_patterns[pattern_str] / 100
            
            if entropy > best_entropy:
                best_entropy = entropy
                best_word = word
                best_reasoning = f"Entropy: {entropy:.3f}, Score: {self.word_scores.get(word, 0)}"
        
        return best_word, best_reasoning

def test_advanced_ai():
    """Test the advanced AI performance."""
    print("Testing Advanced Wordle AI...")
    
    word_list = load_word_list()
    ai = OptimizedWordleAI(word_list)
    
    # Test on a few words
    test_words = ['stare', 'crane', 'slate', 'audio', 'raise', 'eerie', 'seeds']
    
    for word in test_words:
        print(f"\nTesting solution: {word.upper()}")
        
        # Reset AI
        ai.possible_words = word_list.copy()
        
        attempts = 0
        while attempts < 6:
            guess, reasoning = ai.get_best_guess()
            if not guess:
                print(f"  ❌ AI could not find a valid guess on attempt {attempts + 1}")
                break
            print(f"  Attempt {attempts + 1}: {guess.upper()} | {reasoning}")
            
            # Simulate feedback
            feedback = ai._simulate_feedback(guess, word)
            print(f"  Feedback: {feedback}")
            
            ai.update_with_feedback(guess, feedback)
            attempts += 1
            
            if guess == word:
                print(f"  ✅ SOLVED in {attempts} attempts!")
                break
        
        if guess != word:
            print(f"  ❌ Failed to solve {word.upper()}")

if __name__ == "__main__":
    test_advanced_ai() 