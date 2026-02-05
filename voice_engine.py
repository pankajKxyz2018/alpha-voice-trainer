# WEB DEPLOYMENT SAFE VOICE ENGINE
# This version simulates AI voice analysis
# because cloud servers cannot access microphones.

import random

def analyze_mic_input(duration=3):
    """
    Simulated Alpha Voice Analysis for Web Deployment.
    Generates realistic demo scores.
    """

    # Generate natural-looking changing values
    sub100 = random.randint(45, 85)
    chest  = random.randint(40, 90)
    gravel = random.randint(30, 80)
    belly  = random.randint(35, 75)

    alpha = int((sub100 * 0.5) + (chest * 0.3) + (gravel * 0.2))

    return {
        "sub100": sub100,
        "chest": chest,
        "gravel": gravel,
        "belly": belly,
        "alpha": alpha
    }
