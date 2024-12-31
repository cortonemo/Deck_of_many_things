# Deck of Many Things

## Overview
The **Deck of Many Things** is a graphical application simulating the iconic item from tabletop role-playing games. This program allows users to interact with a virtual deck, shuffle cards, and reveal their effects in a visually engaging way.

## Features
- **Full-Screen Mode**: The application opens in full-screen for an immersive experience.
- **Interactive UI**: Users can shuffle the deck, draw cards displayed in a semi-circle, and reveal their details.
- **Dynamic Layout**:
  - Cards are positioned in a large semi-circle, adjustable for different screen sizes.
  - The semi-circle is drawn closer to the bottom of the screen for better visibility.
- **Exit Options**:
  - Return to the main menu while picking cards.
  - Exit the application after finishing.
- **Custom Card Sizes**:
  - Back cards: 400x700 pixels.
  - Revealed cards: 400x700 pixels.
- **Sound Effects**: Shuffle and special effects sounds enhance the experience.

## Requirements
- Python 3.8+
- Required libraries:
  - `tkinter`
  - `Pillow` (PIL)
  - `pygame`
- Assets folder structure:
  ```
  assets/
    decks/
      major_arcana.json
    images/
      deck_of_many_things.png
    sounds/
      shuffle.wav
      spookymagic.mp3
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
   python main.py
   ```
2. Follow the on-screen instructions to shuffle and draw cards.
3. Use the "Exit Picking Cards" button to return to the main menu or "Finish and Exit" to close the application.

## File Structure
- **main.py**: The core application logic.
- **assets/**: Contains the decks, images, and sounds.
  - `decks/`: JSON files with card definitions.
  - `images/`: Images for the card backs and fronts.
  - `sounds/`: Audio files for sound effects.

## Customization
- **Card Layout**:
  - Adjust the semi-circle radius or position in `init_draw_all_ui`.
  - Change card sizes in the `shuffle_deck` and `reveal_card` methods.
- **Assets**:
  - Replace images in the `images/` folder to customize card visuals.
  - Update sound files in the `sounds/` folder for different effects.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contributing
Contributions are welcome! Please fork the repository and create a pull request for any enhancements or bug fixes.

## Acknowledgments
- Inspired by the *Deck of Many Things* from Dungeons & Dragons.
- Special thanks to open-source contributors for libraries and tools used in this project.
