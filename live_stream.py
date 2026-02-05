# ==========================================================
# 🧠 ARJUN DAS RESONANCE AI V2
# Ultra Deep Bass + Chest Vibration Detector
# Real Browser Mic Streaming Engine
# ==========================================================

import numpy as np
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase, WebRtcMode
import av


# ----------------------------------------------------------
# 🎤 ULTRA PROCESSOR
# ----------------------------------------------------------
class AlphaResonanceProcessor(AudioProcessorBase):

    def __init__(self):
        self.latest_result = None
        self.prev_energy = 0

    def recv(self, frame: av.AudioFrame):

        audio = frame.to_ndarray().flatten().astype(np.float32)

        # --------------------------------------------------
        # 🛑 SILENCE GUARD (NO FAKE ANALYSIS)
        # --------------------------------------------------
        peak = np.max(np.abs(audio))
        if peak < 0.02:
            return frame

        # --------------------------------------------------
        # FFT ANALYSIS
        # --------------------------------------------------
        fft = np.abs(np.fft.rfft(audio))
        freqs = np.fft.rfftfreq(len(audio), 1 / 48000)

        total_energy = np.sum(fft) + 1e-10

        # --------------------------------------------------
        # 🎯 FREQUENCY ZONES (ARJUN DAS STYLE)
        # --------------------------------------------------

        # DEEP SUB BASS (throat depth)
        sub_zone = np.sum(fft[(freqs >= 50) & (freqs <= 95)])

        # CHEST RESONANCE CORE
        chest_zone = np.sum(fft[(freqs >= 120) & (freqs <= 300)])

        # BELLY SUPPORT / DIAPHRAGM FLOW
        belly_zone = np.sum(fft[(freqs >= 20) & (freqs <= 60)])

        # CLARITY / GRAVEL TEXTURE
        gravel_zone = np.sum(fft[(freqs >= 2500) & (freqs <= 5000)])

        # --------------------------------------------------
        # 🫀 CHEST VIBRATION DETECTOR (NEW)
        # --------------------------------------------------
        # Measures stability of low-frequency energy
        low_energy = sub_zone + chest_zone
        vibration_delta = abs(low_energy - self.prev_energy)
        self.prev_energy = low_energy

        # Stable vibration = deep masculine resonance
        vibration_score = max(0, 100 - int(vibration_delta * 8000))
        vibration_score = min(100, vibration_score)

        # --------------------------------------------------
        # 🔥 HARD MODE SCORING
        # --------------------------------------------------
        sub100 = min(100, int((sub_zone / total_energy) * 2500))
        chest  = min(100, int((chest_zone / total_energy) * 1700))
        belly  = min(100, int((belly_zone / total_energy) * 4200))
        gravel = min(100, int((gravel_zone / total_energy) * 2600))

        # ULTRA ALPHA SCORE
        alpha = int(
            (sub100 * 0.40) +
            (chest  * 0.30) +
            (vibration_score * 0.20) +
            (gravel * 0.10)
        )

        self.latest_result = {
            "sub100": sub100,
            "chest": chest,
            "belly": belly,
            "gravel": gravel,
            "alpha": alpha,
            "vibration": vibration_score
        }

        return frame


# ----------------------------------------------------------
# 🚀 START LIVE STREAM
# ----------------------------------------------------------
def start_live_stream():

    ctx = webrtc_streamer(
        key="alpha-resonance-v2",
        mode=WebRtcMode.SENDRECV,
        audio_processor_factory=AlphaResonanceProcessor,
        media_stream_constraints={"audio": True, "video": False},
    )

    if ctx.audio_processor:
        return ctx.audio_processor.latest_result

    return None




