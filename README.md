# Deck of Many Things

## Overview
The **Deck of Many Things** is a graphical application simulating the iconic item from tabletop role-playing games. This program allows users to interact with a virtual deck, shuffle cards, and reveal their effects in a visually engaging way.

## Features
- **Full-Screen Mode**: The application opens in full-screen for an immersive experience.
- **Interactive UI**: Users can shuffle the deck, draw cards displayed in a semi-circle, and reveal their details.
- **Dynamic Layout**:
  - Cards are positioned in a large semi-circle, adjustable for different screen sizes.
  - The semi-circle is drawn closer to the bottom of the screen for better visibility.
- **Sound Effects**: Shuffle and special effects sounds enhance the experience.
- **Customizable Assets**:
  - JSON-based card definitions for easy customization.
  - Replaceable images and sound effects to match your theme.
- **Exit Options**:
  - Return to the main menu while picking cards.
  - Exit the application after finishing.
- **Card Sizes**:
  - Back cards: 400x700 pixels.
  - Revealed cards: 400x700 pixels.

## Requirements
- Python 3.8+
- Required libraries:
  - `tkinter`
  - `Pillow` (PIL)
  - `pygame`
- Assets folder structure:
  ```
  deck_app/
    assets/
      decks/
        major_arcana.json
        counter_label.txt
        drawn_cards_report.txt
      images/
        cards/
          card_back.png
          card_fronts/
            The_Fool.png
            The_Magician.png
            ...
      sounds/
        shuffle.wav
        draw.mp3
        spookymagic.mp3
    static/
      css/
        styles.css
      js/
        script.js
    templates/
      base.html
      index.html
  ```

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/deck-of-many-things.git
   ```
2. Install required Python packages:
   ```bash
   pip install pygame pillow
   ```
3. Ensure the `assets/` folder structure and files are in place.

## Usage
1. Run the application:
   ```bash
   python deck_app/main.py
   ```
2. Follow the on-screen instructions to shuffle and draw cards.
3. Use the "Exit Picking Cards" button to return to the main menu or "Finish and Exit" to close the application.

## File Structure
- **deck_app/**: Main application folder.
  - **assets/**: Contains decks, images, and sounds.
    - `decks/`: JSON files with card definitions and other textual data.
    - `images/`: Images for card backs, fronts, and UI elements.
    - `sounds/`: Audio files for shuffle and reveal effects.
  - **static/**: Contains static files such as CSS and JavaScript.
    - `css/`: Styling files.
    - `js/`: Scripts for frontend functionality.
  - **templates/**: HTML templates for Flask integration.
  - `main.py`: The core application logic.
  - `main_gui.py`: Handles the GUI logic.
  - `deck_gui.py`: Contains the logic for rendering the card GUI.
  - `card_logic.py`: Encapsulates card-related logic.

## Customization
- **Card Layout**:
  - Adjust the semi-circle radius or position in the `init_draw_all_ui` function.
  - Change card sizes in the `shuffle_deck` and `reveal_card` methods.
- **Assets**:
  - Replace images in the `assets/images/` folder to customize card visuals.
  - Update sound files in the `assets/sounds/` folder for different effects.
- **Card Definitions**:
  - Modify `assets/decks/major_arcana.json` to define new cards, effects, and themes.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contributing
Contributions are welcome! Please fork the repository and create a pull request for any enhancements or bug fixes.

## Acknowledgments
- Inspired by the *Deck of Many Things* from Dungeons & Dragons.
- Special thanks to open-source contributors for libraries and tools used in this project.
