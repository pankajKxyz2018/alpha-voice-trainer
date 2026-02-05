# ============================================
# 🎤 REAL LIVE STREAM ENGINE (BROWSER MIC)
# ============================================

import streamlit as st
import numpy as np
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase, WebRtcMode
import av


# --------------------------------------------
# AUDIO PROCESSOR (REAL VOICE ANALYSIS)
# --------------------------------------------
class AlphaAudioProcessor(AudioProcessorBase):

    def __init__(self):
        self.latest_result = None

    def recv(self, frame: av.AudioFrame):

        audio = frame.to_ndarray().flatten().astype(np.float32)

        # 🔴 Ignore silence
        if np.max(np.abs(audio)) < 0.01:
            return frame

        # ------------------------------------
        # SIMPLE REAL FREQUENCY ANALYSIS
        # ------------------------------------
        fft = np.abs(np.fft.rfft(audio))
        freqs = np.fft.rfftfreq(len(audio), 1 / 48000)

        total_energy = np.sum(fft) + 1e-10

        sub_100 = np.sum(fft[(freqs >= 50) & (freqs <= 95)])
        chest   = np.sum(fft[(freqs >= 150) & (freqs <= 350)])
        gravel  = np.sum(fft[(freqs >= 3000) & (freqs <= 5500)])
        belly   = np.sum(fft[(freqs >= 20) & (freqs <= 60)])

        # HARD MODE SCALING (NOT LENIENT)
        sub100_score = min(100, int((sub_100 / total_energy) * 2600))
        chest_score  = min(100, int((chest / total_energy) * 1700))
        gravel_score = min(100, int((gravel / total_energy) * 2800))
        belly_score  = min(100, int((belly / total_energy) * 4200))

        alpha_score = int(
            sub100_score * 0.5 +
            chest_score  * 0.3 +
            gravel_score * 0.2
        )

        self.latest_result = {
            "sub100": sub100_score,
            "chest": chest_score,
            "gravel": gravel_score,
            "belly": belly_score,
            "alpha": alpha_score
        }

        return frame


# --------------------------------------------
# STREAM STARTER FUNCTION
# --------------------------------------------
def start_live_stream():

    ctx = webrtc_streamer(
        key="alpha-live-stream",
        mode=WebRtcMode.SENDRECV,
        audio_processor_factory=AlphaAudioProcessor,
        media_stream_constraints={"audio": True, "video": False},
    )

    if ctx.audio_processor:
        return ctx.audio_processor.latest_result

    return None



