import random
import os

modules = {
    "arjun_das": [
        "The ground beneath me vibrates with my voice.",
        "Deep shadows move in the silence of the night.",
        "A heavy stone rolls slowly across the floor.",
        "The thunder rumbles in the distance, low and steady.",
        "My command is absolute, quiet, and profound."
    ],
    "neutral_accent": [
        "Stability is the mark of a true leader.",
        "I maintain a flat and consistent tone.",
        "There is no urgency in the way I speak.",
        "Every word carries the same weight and power.",
        "I am calm, composed, and entirely neutral."
    ],
    "chest_involvement": [
        "I push the sound from the center of my chest.",
        "Resonance builds within my ribcage now.",
        "The diaphragm is the engine of my authority.",
        "My voice is a physical force in this room.",
        "I feel the buzz in my sternum as I speak."
    ]
}

all_sentences = []
keys = list(modules.keys())

for i in range(1000):
    category = keys[i % len(keys)]
    base = random.choice(modules[category])
    suffix = random.choice([".", "...", " today.", " now."])
    all_sentences.append(f"{base.rstrip('.')}{suffix}")

with open("sentences.txt", "w", encoding="utf-8") as f:
    for s in all_sentences:
        f.write(s + "\n")

print("Success! 1,000 Arjun Das style sentences created.")
