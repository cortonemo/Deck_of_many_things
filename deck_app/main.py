import tkinter as tk
from tkinter import messagebox
import json
import random
import os
from math import sin, cos, radians
from PIL import Image, ImageTk
import pygame
from threading import Thread
from flask_app import app  # Import the Flask app

class DeckOfManyThingsApp:
    def __init__(self, root):
        """Initialize the application and its components."""
        self.root = root
        self.root.title("Deck of Many Things")
        self.root.attributes('-fullscreen', True)  # Set fullscreen mode
        self.root.resizable(True, True)  # Allow resizing if needed

        # Asset folders
        self.assets_folder = "assets"
        self.decks_folder = os.path.join(self.assets_folder, "decks")
        self.images_folder = os.path.join(self.assets_folder, "images")
        self.sounds_folder = os.path.join(self.assets_folder, "sounds")

        # Ensure required folders exist
        os.makedirs(self.decks_folder, exist_ok=True)
        os.makedirs(self.images_folder, exist_ok=True)
        os.makedirs(self.sounds_folder, exist_ok=True)

        self.deck = []
        self.deck_saved = False  # Track if the deck is ready for drawing

        # Initialize pygame for sound
        pygame.mixer.init()

        # Create the status label at the root level and make it persistent
        self.status_label = tk.Label(self.root, text="", relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)

        # Validate assets
        self.validate_assets()

        # Check for an existing deck
        if self.get_last_deck():
            if messagebox.askyesno("Deck Found", "An existing deck was found. Do you want to use it?"):
                self.load_existing_deck()
                self.init_draw_all_ui()  # Go directly to card choice
            else:
                self.init_first_menu()
        else:
            self.init_first_menu()

    def validate_assets(self):
        """Validate that all required assets are present."""
        required_files = [
            os.path.join(self.decks_folder, "major_arcana.json"),
            os.path.join(self.images_folder, "deck_of_many_things.png"),
            os.path.join(self.sounds_folder, "shuffle.wav"),
            os.path.join(self.sounds_folder, "spookymagic.mp3")
        ]
        missing_files = [f for f in required_files if not os.path.exists(f)]
        if missing_files:
            messagebox.showerror(
                "Missing Assets",
                f"The following required files are missing:\n" + "\n".join(missing_files)
            )
            self.root.quit()

    def init_first_menu(self):
        """Initialize the first menu with New Deck and Exit options."""
        for widget in self.root.winfo_children():
            if widget is not self.status_label:  # Avoid destroying the status label
                widget.destroy()

        new_deck_button = tk.Button(self.root, text="New Deck", command=self.load_new_deck)
        new_deck_button.pack(pady=10)

        exit_button = tk.Button(self.root, text="Exit", command=self.save_and_exit)
        exit_button.pack(pady=10)

        self.status_label.config(text="Welcome to the Deck of Many Things")

    def init_shuffle_ui(self):
        """Initialize the shuffle UI."""
        for widget in self.root.winfo_children():
            if widget is not self.status_label:  # Avoid destroying the status label
                widget.destroy()

        shuffle_button = tk.Button(self.root, text="Shuffle Deck", command=self.shuffle_deck)
        shuffle_button.pack(pady=10)

        self.status_label.config(text="Shuffle the deck to proceed.")

    def shuffle_deck(self):
        """Perform the shuffle animation and transition to the draw all UI."""
        try:
            pygame.mixer.Sound(os.path.join(self.sounds_folder, "shuffle.wav")).play()
        except Exception as e:
            messagebox.showwarning("Warning", f"Shuffle sound could not be played: {e}")

        for widget in self.root.winfo_children():
            if widget is not self.status_label:  # Avoid destroying the status label
                widget.destroy()

        canvas_width = self.root.winfo_screenwidth()
        canvas_height = self.root.winfo_screenheight()
        canvas = tk.Canvas(self.root, width=canvas_width, height=canvas_height)
        canvas.pack(fill=tk.BOTH, expand=True)

        back_image_path = os.path.join(self.images_folder, "deck_of_many_things.png")
        try:
            back_image = Image.open(back_image_path).resize((400, 700))
            self.back_photo = ImageTk.PhotoImage(back_image)  # Store reference as a class attribute
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load back image: {e}")
            return

        card = canvas.create_image(canvas_width // 2, canvas_height // 2, image=self.back_photo, anchor=tk.CENTER)

        def animate_shuffle():
            for _ in range(10):
                x_offset = random.randint(-20, 20)
                y_offset = random.randint(-20, 20)
                canvas.move(card, x_offset, y_offset)
                canvas.update()
                self.root.after(100)
                canvas.move(card, -x_offset, -y_offset)

            canvas.destroy()
            self.init_draw_all_ui()

        self.root.after(100, animate_shuffle)
        random.shuffle(self.deck)  # Shuffle the deck
        self.save_deck()

    def init_draw_all_ui(self):
        """Initialize the UI for displaying all cards in a semi-circle and allowing selection."""
        for widget in self.root.winfo_children():
            if widget is not self.status_label:  # Avoid destroying the status label
                widget.destroy()

        if not self.deck:
            if messagebox.askyesno("Deck Depleted", "No cards left in the deck. Do you want to load a new deck?"):
                self.init_first_menu()
            else:
                self.save_and_exit()
            return

        canvas_width = self.root.winfo_width()
        canvas_height = self.root.winfo_height()
        canvas = tk.Canvas(self.root, width=canvas_width, height=canvas_height)
        canvas.pack()

        back_image_path = os.path.join(self.images_folder, "deck_of_many_things.png")
        try:
            back_image = Image.open(back_image_path).resize((100, 175))
            back_photo = ImageTk.PhotoImage(back_image)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load back image: {e}")
            return

        self.card_images = []  # Store image references to prevent garbage collection

        # Calculate semi-circle positions
        center_x = canvas_width // 2
        center_y = canvas_height // 2 + 100
        radius = 480
        angle_step = 180 // (len(self.deck) - 1) if len(self.deck) > 1 else 0  # Spread evenly in a semi-circle

        for i, card in enumerate(self.deck):
            angle = 180 + i * angle_step  # Rotated semi-circle (90° left)
            x = center_x + int(radius * cos(radians(angle))) - 50
            y = center_y + int(radius * sin(radians(angle))) - 75

            card_id = canvas.create_image(x, y, image=back_photo, anchor=tk.CENTER)
            self.card_images.append(back_photo)

            # Bind click event to each card
            canvas.tag_bind(card_id, "<Button-1>", lambda e, c=card: self.reveal_card(c, canvas))

        finish_button = tk.Button(self.root, text="Finish and Exit", command=self.save_and_exit)
        finish_button.pack(pady=10)

        exit_button = tk.Button(self.root, text="Exit Picking Cards", command=self.init_first_menu)
        exit_button.pack(pady=10)

        self.status_label.config(text="Click on a card to reveal it or finish to exit.")

    def reveal_card(self, card, canvas):
        """Reveal the selected card and display its details in the main window."""
        for widget in self.root.winfo_children():
            if widget is not self.status_label:  # Avoid destroying the status label
                widget.destroy()

        try:
            front_image_path = os.path.join(self.images_folder, card["image"].replace("images/", ""))
            front_image = Image.open(front_image_path).resize((400, 700))
            front_photo = ImageTk.PhotoImage(front_image)

            self.deck.remove(card)

            self.save_deck()

            card_image_label = tk.Label(self.root, image=front_photo)
            card_image_label.image = front_photo
            card_image_label.pack()

            card_details_label = tk.Label(
                self.root,
                text=f"Name: {card['name']}\nTheme: {card['theme']}\nEffect: {card['effect']}",
                font=("Arial", 14)
            )
            card_details_label.pack(pady=10)

            action_frame = tk.Frame(self.root)
            action_frame.pack(pady=10)

            draw_button = tk.Button(action_frame, text="Draw New Card", command=self.init_draw_all_ui)
            draw_button.pack(side=tk.LEFT, padx=5)

            finish_button = tk.Button(action_frame, text="Finish and Exit", command=self.save_and_exit)
            finish_button.pack(side=tk.RIGHT, padx=5)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to reveal card: {e}")

    def load_new_deck(self):
        """Load and shuffle a new deck."""
        default_deck_path = os.path.join(self.decks_folder, "major_arcana.json")
        if os.path.exists(default_deck_path):
            try:
                pygame.mixer.Sound(os.path.join(self.sounds_folder, "spookymagic.mp3")).play()
                messagebox.showinfo(
                    "New Discovery",
                    "You stumble upon a deck, its cards pristine and untouched. A whisper in your mind urges: 'Shuffle and awaken its power.'"
                )
                self.load_json(default_deck_path)
                self.init_shuffle_ui()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load the deck: {e}")
        else:
            messagebox.showerror("Error", "Default deck file major_arcana.json not found!")

    def load_existing_deck(self):
        """Load the existing workingDeck.json file."""
        save_path = self.get_last_deck()
        if save_path:
            try:
                self.load_json(save_path)
                self.update_status(f"Loaded existing deck with {len(self.deck)} cards.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load the existing deck: {e}")

    def load_json(self, file_path):
        """Load the deck from a JSON file."""
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                self.deck = data["MajorArcana"]
            self.update_status(f"Loaded {len(self.deck)} cards.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load deck: {e}")

    def get_last_deck(self):
        """Get the last saved deck."""
        save_path = os.path.join(self.decks_folder, "workingDeck.json")
        return save_path if os.path.exists(save_path) else None

    def save_deck(self):
        """Save the current deck to a JSON file."""
        save_path = os.path.join(self.decks_folder, "workingDeck.json")
        with open(save_path, 'w') as f:
            json.dump({"MajorArcana": self.deck}, f)

    def save_and_exit(self):
        """Save the drawn and remaining cards to a file and exit."""
        drawn_cards_file = os.path.join(self.decks_folder, "drawn_cards_report.txt")
        try:
            with open(drawn_cards_file, 'w') as f:
                f.write("Remaining Cards:\n")
                for card in self.deck:
                    f.write(f"- {card['name']}\n")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save remaining cards: {e}")
        finally:
            self.root.quit()

    def update_status(self, message):
        """Update the status message in the UI."""
        self.status_label.config(text=message)

    def start_web_gui(self):
        """Start the Flask app in a separate thread."""
        from flask_app import app as flask_app  # Import the Flask app explicitly here
        thread = Thread(target=flask_app.run, kwargs={'host': '127.0.0.1', 'port': 5000, 'debug': False})
        thread.daemon = True  # Ensure Flask exits when Tkinter exits
        thread.start()


if __name__ == "__main__":
    root = tk.Tk()
    app = DeckOfManyThingsApp(root)
    app.start_web_gui()  # Start the Flask web GUI
    root.mainloop()
