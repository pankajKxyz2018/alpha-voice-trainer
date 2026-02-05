# HYBRID VOICE ENGINE
# Localhost = REAL MIC
# Streamlit Cloud = SIMULATION

import os
import random

# Detect cloud deployment
IS_CLOUD = os.getenv("STREAMLIT_SERVER_PORT") is not None

if not IS_CLOUD:
    try:
        import numpy as np
        import sounddevice as sd
        REAL_MODE = True
    except:
        REAL_MODE = False
else:
    REAL_MODE = False


def analyze_mic_input(duration=3):

    # -----------------------------------
    # 🌐 CLOUD MODE (Simulation)
    # -----------------------------------
    if not REAL_MODE:

        sub100 = random.randint(45, 85)
        chest  = random.randint(40, 90)
        gravel = random.randint(30, 80)
        belly  = random.randint(35, 75)

        alpha = int((sub100 * 0.5) +
                    (chest * 0.3) +
                    (gravel * 0.2))

        return {
            "sub100": sub100,
            "chest": chest,
            "gravel": gravel,
            "belly": belly,
            "alpha": alpha,
            "speech_detected": True
        }

    # -----------------------------------
    # 🖥 LOCAL REAL MIC MODE
    # -----------------------------------
    try:
        recording = sd.rec(int(duration * 44100),
                           samplerate=44100,
                           channels=1,
                           dtype='float32')
        sd.wait()
        audio_data = recording.flatten()

        energy = np.sqrt(np.mean(audio_data**2))
        if energy < 0.01:
            return {
                "sub100":0,
                "chest":0,
                "gravel":0,
                "belly":0,
                "alpha":0,
                "speech_detected":False
            }

        peak = np.max(np.abs(audio_data))
        if peak > 1e-5:
            audio_data = audio_data / peak

        fft_data = np.abs(np.fft.rfft(audio_data))
        freqs = np.fft.rfftfreq(len(audio_data), 1/44100)
        total_energy = np.sum(fft_data) + 1e-10

        sub_100 = np.sum(fft_data[(freqs >= 50) & (freqs <= 95)])
        chest_zone = np.sum(fft_data[(freqs >= 150) & (freqs <= 350)])
        clarity_zone = np.sum(fft_data[(freqs >= 3000) & (freqs <= 5500)])
        belly_zone = np.sum(fft_data[(freqs >= 20) & (freqs <= 60)])

        res = {
            'sub100': min(100, int((sub_100 / total_energy) * 2500)),
            'chest': min(100, int((chest_zone / total_energy) * 1500)),
            'gravel': min(100, int((clarity_zone / total_energy) * 3000)),
            'belly': min(100, int((belly_zone / total_energy) * 4000)),
            'speech_detected': True
        }

        res['alpha'] = int((res['sub100']*0.5) +
                           (res['chest']*0.3) +
                           (res['gravel']*0.2))

        return res

    except:
        return {
            "sub100":0,
            "chest":0,
            "gravel":0,
            "belly":0,
            "alpha":0,
            "speech_detected":False
        }
