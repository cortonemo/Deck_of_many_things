import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import pygame
import json
import random
import os


class DeckOfManyThingsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Deck of Many Things")
        self.deck = []

        # Initialize pygame for sound effects
        pygame.init()

        # Set default paths
        self.image_folder = os.path.join("deck_app", "assets", "images")
        self.sound_folder = os.path.join("deck_app", "assets", "sounds")

        # Initialize UI components before loading the deck
        self.init_ui()

        # Load the deck JSON file after UI is ready
        self.load_json("major_arcana.json")

    def load_json(self, file_path):
        """Load deck from a JSON file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.deck = data["MajorArcana"]
            self.update_status(f"Loaded {len(self.deck)} cards.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load deck: {e}")

    def shuffle_deck(self):
        """Shuffle the deck and play shuffle sound."""
        try:
            shuffle_sound = os.path.join(self.sound_folder, "shuffle.wav")
            if os.path.exists(shuffle_sound):
                pygame.mixer.Sound(shuffle_sound).play()
            else:
                print("Shuffle sound not found. Skipping sound.")
            random.shuffle(self.deck)
            self.update_status("Deck shuffled!")
        except Exception as e:
            print(f"Error playing shuffle sound: {e}")
            random.shuffle(self.deck)
            self.update_status("Deck shuffled!")

    def draw_card(self):
        """Draw a card from the deck."""
        if not self.deck:
            messagebox.showinfo("Info", "No cards left in the deck!")
            return
        card = self.deck.pop(0)
        self.display_card(card)

    def display_card(self, card):
        """Display the drawn card with its image."""
        card_name = card['name']
        card_info = f"Card: {card_name}\nTheme: {card['theme']}\nEffect: {card['effect']}"

        # Display card details
        self.card_label.config(text=card_info)

        # Load and display the card image
        image_path = os.path.join(self.image_folder, f"{card_name.replace(' ', '_')}.png")
        if os.path.exists(image_path):
            card_image = Image.open(image_path)
            card_image = card_image.resize((200, 300), Image.ANTIALIAS)
            card_image_tk = ImageTk.PhotoImage(card_image)
            self.card_image_label.config(image=card_image_tk)
            self.card_image_label.image = card_image_tk
        else:
            print(f"Image for {card_name} not found. Skipping image.")

    def save_deck(self):
        """Save the current deck to a JSON file."""
        file_path = filedialog.asksaveasfilename(defaultextension=".json",
                                                 filetypes=[("JSON Files", "*.json")])
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump({"MajorArcana": self.deck}, f, ensure_ascii=False, indent=4)
            self.update_status("Deck saved successfully!")

    def update_status(self, message):
        """Update the status bar."""
        self.status_label.config(text=message)

    def init_ui(self):
        """Initialize the user interface."""
        # Buttons
        shuffle_button = tk.Button(self.root, text="Shuffle Deck", command=self.shuffle_deck)
        shuffle_button.pack(pady=10)

        draw_button = tk.Button(self.root, text="Draw Card", command=self.draw_card)
        draw_button.pack(pady=10)

        save_button = tk.Button(self.root, text="Save Deck", command=self.save_deck)
        save_button.pack(pady=10)

        # Card display
        self.card_label = tk.Label(self.root, text="Drawn Card: None", font=("Arial", 14))
        self.card_label.pack(pady=10)

        # Card image display
        self.card_image_label = tk.Label(self.root)
        self.card_image_label.pack(pady=20)

        # Status bar
        self.status_label = tk.Label(self.root, text="Welcome to the Deck of Many Things", relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)


if __name__ == "__main__":
    root = tk.Tk()
    app = DeckOfManyThingsApp(root)
    root.mainloop()
