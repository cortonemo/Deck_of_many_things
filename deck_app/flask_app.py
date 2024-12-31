from flask import Flask, render_template, jsonify
import os
import json
import random

app = Flask(__name__)

# Paths to deck files
decks_folder = os.path.join("assets", "decks")
working_deck_path = os.path.join(decks_folder, "workingDeck.json")
major_arcana_path = os.path.join(decks_folder, "major_arcana.json")

# Load the appropriate deck
def load_deck():
    if os.path.exists(working_deck_path):
        with open(working_deck_path, 'r') as f:
            data = json.load(f)
            return data.get("MajorArcana", [])
    elif os.path.exists(major_arcana_path):
        with open(major_arcana_path, 'r') as f:
            data = json.load(f)
            return data.get("MajorArcana", [])
    else:
        return []

deck = load_deck()

@app.route('/')
def home():
    return "Welcome to the Deck of Many Things Flask Web GUI!"

@app.route('/api/draw-card', methods=['GET'])
def draw_card():
    if not deck:
        return jsonify({"error": "The deck is empty or could not be loaded."}), 404
    card = random.choice(deck)
    return jsonify(card)

if __name__ == "__main__":
    app.run(debug=True)
