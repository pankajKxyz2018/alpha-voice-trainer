# ==========================================================
# 🔥 PRO ULTRA ENGINE — ALPHA DEEP VOICE REAL STREAM ANALYSIS
# Designed for Deep Bass / Chest Resonance Training
# ==========================================================

import numpy as np
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase, WebRtcMode
import av


# ----------------------------------------------------------
# 🎤 PRO AUDIO PROCESSOR
# ----------------------------------------------------------
class AlphaUltraProcessor(AudioProcessorBase):

    def __init__(self):
        self.latest_result = None

    def recv(self, frame: av.AudioFrame):

        # Convert audio frame → numpy
        audio = frame.to_ndarray().flatten().astype(np.float32)

        # --------------------------------------------------
        # 🛑 SILENCE GUARD (NO FAKE SCORES)
        # --------------------------------------------------
        if np.max(np.abs(audio)) < 0.015:
            return frame

        # --------------------------------------------------
        # FFT ANALYSIS (REAL FREQUENCY BREAKDOWN)
        # --------------------------------------------------
        fft = np.abs(np.fft.rfft(audio))
        freqs = np.fft.rfftfreq(len(audio), 1 / 48000)

        total_energy = np.sum(fft) + 1e-10

        # --------------------------------------------------
        # 🎯 ULTRA BASS ZONES (ARJUN DAS STYLE)
        # --------------------------------------------------

        # SUB BASS (deep throat / vocal fry area)
        sub_zone = np.sum(fft[(freqs >= 50) & (freqs <= 95)])

        # CHEST RESONANCE
        chest_zone = np.sum(fft[(freqs >= 120) & (freqs <= 300)])

        # BELLY / DIAPHRAGM SUPPORT
        belly_zone = np.sum(fft[(freqs >= 20) & (freqs <= 60)])

        # CLARITY / GRAVEL TEXTURE
        gravel_zone = np.sum(fft[(freqs >= 2500) & (freqs <= 5000)])

        # --------------------------------------------------
        # 🔥 HARD MODE SCORING (STRICT)
        # --------------------------------------------------
        sub100 = min(100, int((sub_zone / total_energy) * 2400))
        chest  = min(100, int((chest_zone / total_energy) * 1600))
        belly  = min(100, int((belly_zone / total_energy) * 4200))
        gravel = min(100, int((gravel_zone / total_energy) * 2600))

        # ULTRA ALPHA SCORE (STRICT WEIGHTING)
        alpha = int(
            (sub100 * 0.45) +   # deep bass is primary
            (chest  * 0.35) +   # chest power important
            (gravel * 0.20)     # texture secondary
        )

        # Save latest result
        self.latest_result = {
            "sub100": sub100,
            "chest": chest,
            "belly": belly,
            "gravel": gravel,
            "alpha": alpha
        }

        return frame


# ----------------------------------------------------------
# 🚀 START LIVE STREAM FUNCTION
# ----------------------------------------------------------
def start_live_stream():

    ctx = webrtc_streamer(
        key="alpha-ultra-stream",
        mode=WebRtcMode.SENDRECV,
        audio_processor_factory=AlphaUltraProcessor,
        media_stream_constraints={"audio": True, "video": False},
    )

    if ctx.audio_processor:
        return ctx.audio_processor.latest_result

    return None



