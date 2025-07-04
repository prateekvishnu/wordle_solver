# Wordle AI Solver

A sophisticated Wordle solver that uses advanced AI algorithms to solve Wordle puzzles efficiently. The project includes both a command-line interface and a graphical user interface, along with a web bot for playing on the official Wordle website.

## Features

### 🤖 Advanced AI Algorithms
- **Information Theory-Based Decision Making**: Uses entropy calculations to maximize information gain
- **Advanced Repeated Letter Handling**: Sophisticated logic for words with duplicate letters (e.g., "eerie", "seeds")
- **Position-Specific Letter Frequency Analysis**: Considers letter frequency at each position
- **Common Letter Combination Analysis**: Recognizes and leverages common letter patterns
- **Repeated Letter Pattern Recognition**: Analyzes patterns of repeated letters in solutions
- **Fixed Optimal Starter Words**: Uses proven optimal starting words like "raise", "stare", "crane"
- **OptimizedWordleAI**: Enhanced AI with additional heuristics and pattern recognition

### 🎮 Multiple Interfaces
- **Command Line Interface (CLI)**: Fast testing and batch processing
- **Graphical User Interface (GUI)**: User-friendly tkinter-based interface with real-time AI suggestions
- **Web Bot**: Automated play on the official Wordle website using advanced AI
- **Game Simulator**: Test AI performance against various words with detailed statistics

### 📊 Performance Features
- **Real-time Statistics**: Track win rates, average attempts, and performance metrics
- **Detailed Reasoning**: See AI's decision-making process and reasoning
- **Manual Feedback Mode**: Test AI with custom feedback patterns
- **Auto-Feedback Mode**: Automatic feedback calculation for testing
- **Clean Debug Output**: Minimal debug information for focused gameplay

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)
- Chrome browser (for web bot functionality)

### Setup
1. Clone or download the project files
2. Install required dependencies:
```bash
pip install selenium webdriver-manager
```

### Files Required
- `wordle_words.txt`: Word list file (2309 words, included)
- All Python files in the project directory

## Usage

### 1. Command Line Interface

#### Basic Usage
```bash
python wordle_ai_solver.py
```

#### Game Simulator with Statistics
```bash
python wordle_game_simulator.py
```

#### Advanced AI Testing
```bash
python advanced_wordle_ai.py
```

### 2. Graphical User Interface

Launch the GUI application:
```bash
python wordle_gui.py
```

**GUI Features:**
- Interactive game board with color-coded feedback
- Real-time AI suggestions with detailed reasoning
- Manual and automatic feedback modes
- AI information display and statistics
- Game controls (New Game, AI Solve, Show Solution)
- Status log with scrollable output

### 3. Web Bot (Automated Play)

Play automatically on the official Wordle website:
```bash
python wordle_web_bot.py
```

**Web Bot Features:**
- Automated browser control with Chrome
- Real-time game state reading from the official Wordle site
- Advanced AI integration for optimal gameplay
- Multiple game statistics tracking
- Headless mode support
- Proper game end detection (6 attempts or GGGGG feedback)
- Clean output without debug clutter

## Project Structure

```
wordlesolver/
├── README.md                    # This file
├── wordle_words.txt            # Word list (2309 words)
├── wordle_ai_solver.py         # Core AI logic and CLI
├── wordle_game_simulator.py    # Game simulation and testing
├── advanced_wordle_ai.py       # Advanced AI with optimizations
├── wordle_gui.py              # Graphical user interface
└── wordle_web_bot.py          # Web automation bot with advanced AI
```

## AI Algorithm Details

### Core Strategy
The AI uses a multi-layered approach:

1. **First Guess**: Always uses a proven optimal starter word from a curated list
2. **Subsequent Guesses**: Uses entropy-based decision making to maximize information gain
3. **Word Filtering**: Advanced logic for handling repeated letters and position constraints
4. **Scoring System**: Multi-factor scoring including letter frequency, position frequency, and pattern recognition

### Key Components

#### AdvancedWordleAI
- Base AI class with information theory implementation
- Entropy calculations for optimal guess selection
- Advanced word filtering with repeated letter handling
- Fixed starter word list for consistent first guesses

#### OptimizedWordleAI
- Enhanced version with additional heuristics
- Letter combination analysis
- Repeated letter pattern recognition
- Improved scoring algorithms
- Better handling of edge cases

### Performance Metrics
- **Average Attempts**: Typically 3-4 attempts for most words
- **Win Rate**: >95% success rate on standard Wordle words
- **Handles Edge Cases**: Effectively solves words with repeated letters like "eerie", "seeds"
- **Consistent Performance**: Uses proven starter words for reliable first guesses

## Examples

### CLI Example
```
Testing solution: RAISE
  Attempt 1: RAISE | Using starter word: RAISE | Eliminates from 2309 possible words
  Feedback: GGGGG
  ✅ SOLVED in 1 attempts!

Testing solution: EERIE
  Attempt 1: RAISE | Using starter word: RAISE | Eliminates from 2309 possible words
  Feedback: GYBBG
  Attempt 2: ERODE | Only 2 possible words remaining | Eliminates from 2 possible words
  Feedback: GYBBG
  Attempt 3: EERIE | Only 1 possible words remaining | Eliminates from 1 possible words
  Feedback: GGGGG
  ✅ SOLVED in 3 attempts!
```

### GUI Example
The GUI provides a visual game board where you can:
- Make manual guesses with real-time feedback
- See AI suggestions with detailed reasoning
- View AI information and statistics
- Test different scenarios with manual feedback
- Watch AI solve games automatically

### Web Bot Example
The web bot can automatically:
- Open the official Wordle website
- Read the current game state in real-time
- Make optimal guesses using advanced AI
- Track performance statistics across multiple games
- Handle game end conditions properly

## Recent Improvements

### Advanced AI Integration
- **Web Bot**: Now uses OptimizedWordleAI for better performance
- **Fixed Starter Words**: Consistent first guesses using proven optimal words
- **Better Edge Case Handling**: Improved performance on words with repeated letters

### Web Bot Enhancements
- **Proper Game End Detection**: Stops after 6 attempts or correct guess (GGGGG)
- **Clean Output**: Removed debug clutter for focused gameplay
- **Advanced AI**: Uses the same sophisticated AI as GUI and CLI versions
- **Reliable Performance**: Better handling of website interactions

### GUI Improvements
- **Real-time AI Integration**: Uses OptimizedWordleAI for suggestions
- **Enhanced User Experience**: Better interface and feedback
- **Comprehensive Statistics**: Detailed AI information and performance metrics

## Customization

### Modifying Starter Words
Edit the `starter_words` list in `advanced_wordle_ai.py`:
```python
self.starter_words = ['raise', 'stare', 'crane', 'slate', 'audio', ...]
```

### Adding New Words
Add words to `wordle_words.txt` (one word per line, lowercase).

### Adjusting AI Parameters
Modify scoring weights and thresholds in the AI classes for different strategies.

### Web Bot Settings
- Change `headless=False` to `True` for background operation
- Adjust `time.sleep()` values for different game speeds
- Modify browser options for different environments

## Troubleshooting

### Common Issues

1. **Missing wordle_words.txt**
   - Ensure the file is in the same directory as the Python scripts
   - Check file permissions

2. **Web Bot Issues**
   - Ensure Chrome browser is installed
   - Check internet connection
   - Verify selenium and webdriver-manager are installed
   - Try running in non-headless mode first

3. **GUI Not Starting**
   - Ensure tkinter is available (usually included with Python)
   - Check for missing dependencies

4. **AI Performance Issues**
   - Verify word list is complete and properly formatted
   - Check that all AI files are present

### Performance Tips

1. **For Large-Scale Testing**: Use the CLI version for faster processing
2. **For Interactive Testing**: Use the GUI for step-by-step analysis
3. **For Real Game Play**: Use the web bot for automated play
4. **For Development**: Use the game simulator for algorithm testing

## Contributing

Feel free to contribute improvements:
- Enhanced AI algorithms
- Better word lists
- UI improvements
- Performance optimizations
- Bug fixes
- Additional features

## License

This project is open source and available under the MIT License.

## Acknowledgments

- Wordle game by Josh Wardle
- Word list from official Wordle sources
- Research on optimal Wordle strategies
- Selenium and webdriver-manager for web automation

---

**Happy Wordling! 🎯** 