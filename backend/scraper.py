"""
Scraper file to fetch and clean content from Wikipedia articles.
"""
import requests
from bs4 import BeautifulSoup
import re

def scrape_wikipedia(url: str) -> tuple[str | None, str | None]:
    """
    Scrapes a Wikipedia article for its title and clean main-body text.

    It strips out:
    - Reference links ([1], [2], etc.)
    - Tables
    - Infoboxes
    - Image captions (thumbnails)
    - "See also," "References," "External links" sections
    - Other navigation and edit-link boilerplate

    Args:
        url: The full URL of the Wikipedia article to scrape.

    Returns:
        A tuple of (title, clean_text).
        Returns (None, None) if the scrape fails.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        # 1. Fetch the URL content
        response = requests.get(url, headers=headers, timeout=10)
        # Raise an exception for bad status codes (4xx or 5xx)
        response.raise_for_status()

        # 2. Parse with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # --- Extract Title ---
        title_tag = soup.find('h1', id='firstHeading')
        title = title_tag.get_text(strip=True) if title_tag else "No Title Found"

        # --- Identify Main Content Body ---
        # The main content is inside a div with class 'mw-parser-output'
        # 1. Scrape the page
        main_content = soup.find('div', class_='mw-parser-output')

        # 2. CHECK if it was successful
        if main_content:
          text = main_content.get_text()
        else:
        # 3. Handle the failure
           print("Error: Could not find main content on this page.")
        # We could also check for a disambiguation class here
           disambiguation = soup.find('div', id='disambigbox')
           if disambiguation:
              print("This is a disambiguation page.")
        # Return None or raise an error

        # --- 3. Clean Content ---
        
        # Select all tags to be removed
        junk_selectors = [
            'sup',                   # Reference links (e.g., [1])
            'table',                 # All tables
            '.infobox',              # Infoboxes (side tables)
            '.navbox',               # Navigation boxes (bottom)
            '.metadata',             # Metadata boxes
            'span.mw-editsection',   # "edit" links
            'div.thumb',             # Image thumbnails
            '.noprint',              # Printer-hidden content
            '.reflist',              # Reference list sections
            '.reference'             # Individual references
        ]

        for selector in junk_selectors:
            for tag in main_content.select(selector):
                tag.decompose() # Remove the tag completely

        # Now, get all the text from the remaining elements (mostly <p>, <ul>, <li>)
        # We use a newline as a separator to maintain paragraph breaks.
        clean_text = main_content.get_text(separator='\n', strip=True)
        
        # --- Final Cleanup ---
        # Find the "References" or "See also" section and cut off everything after it.
        # These are usually in <h2> tags.
        stop_keywords = [
            'References',
            'See also',
            'Notes',
            'External links',
            'Further reading'
        ]
        
        # Regex to find any of the stop keywords as a whole line
        # This is more robust than a simple split
        stop_pattern = re.compile(r'^(' + '|'.join(re.escape(k) for k in stop_keywords) + r')$', re.MULTILINE)
        match = stop_pattern.search(clean_text)
        
        if match:
            # Cut off the text from the point where the stop keyword was found
            clean_text = clean_text[:match.start()]

        # Remove excessive blank lines
        clean_text = re.sub(r'\n\s*\n', '\n\n', clean_text).strip()

        return title, clean_text

    except requests.exceptions.RequestException as e:
        print(f"Error during request: {e}")
        return None, None
    except Exception as e:
        print(f"An error occurred during parsing: {e}")
        return None, None

# --- Example Usage ---
if __name__ == "__main__":
    # Test with a complex article
    test_url = "https://en.wikipedia.org/wiki/Python_(programming_language)"
    
    print(f"Scraping {test_url}...")
    
    article_title, article_text = scrape_wikipedia(test_url)
    
    if article_title and article_text:
        print("\n" + "="*30)
        print(f"SCRAPE SUCCESSFUL")
        print(f"TITLE: {article_title}")
        print("="*30)
        print(f"\n--- CLEANED TEXT (first 800 characters) ---\n")
        print(article_text[:800] + "...")
        print(f"\n\nTotal characters scraped: {len(article_text)}")
    else:
        print("\n" + "="*30)
        print("SCRAPE FAILED")
        print("="*30)