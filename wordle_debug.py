import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def test_tile_reading():
    """Test script to debug tile reading from Wordle."""
    
    # Setup driver
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        # Open Wordle
        driver.get("https://www.nytimes.com/games/wordle/index.html")
        time.sleep(3)
        
        print("Wordle opened. Making a test guess...")
        
        # Make a test guess
        actions = webdriver.ActionChains(driver)
        actions.send_keys("ALERT")
        actions.send_keys(Keys.RETURN)
        actions.perform()
        
        # Wait for animation
        time.sleep(4)
        
        print("\n=== READING TILE STRUCTURE ===")
        
        # Find all rows
        rows = driver.find_elements(By.CSS_SELECTOR, "[role='group'][aria-label*='Row']")
        print(f"Found {len(rows)} rows")
        
        for i, row in enumerate(rows):
            print(f"\nRow {i+1}:")
            tiles = row.find_elements(By.CSS_SELECTOR, "[data-testid='tile']")
            print(f"  Found {len(tiles)} tiles")
            
            word = ""
            feedback = ""
            
            for j, tile in enumerate(tiles):
                aria_label = tile.get_attribute("aria-label")
                data_state = tile.get_attribute("data-state")
                text_content = tile.text
                
                print(f"    Tile {j+1}: aria-label='{aria_label}', data-state='{data_state}', text='{text_content}'")
                
                # Try to extract letter and state
                if aria_label:
                    parts = aria_label.split(", ")
                    if len(parts) >= 2:
                        letter = parts[1].strip()
                        word += letter
                        
                        # Determine feedback
                        if data_state == "correct":
                            feedback += "G"
                        elif data_state == "present":
                            feedback += "Y"
                        elif data_state == "absent":
                            feedback += "B"
                        else:
                            feedback += "?"
            
            if len(word) == 5:
                print(f"  Extracted word: {word}")
                print(f"  Extracted feedback: {feedback}")
        
        print("\n=== WAITING FOR USER INPUT ===")
        input("Press Enter to continue...")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        driver.quit()

if __name__ == "__main__":
    test_tile_reading() 