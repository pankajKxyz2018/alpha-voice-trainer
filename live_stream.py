import numpy as np
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase, WebRtcMode
import streamlit as st

# ---------------------------------------
# REAL AUDIO PROCESSOR
# ---------------------------------------
class VoiceProcessor(AudioProcessorBase):

    def __init__(self):
        self.alpha = 0
        self.deep = 0
        self.chest = 0
        self.belly = 0
        self.tone = 0

    def recv(self, frame):

        audio = frame.to_ndarray()

        # Convert stereo → mono
        if len(audio.shape) > 1:
            audio = audio.mean(axis=1)

        volume = np.abs(audio).mean()

        # 👉 REAL SIGNAL ENERGY ANALYSIS
        self.deep = int(min(100, volume * 2))
        self.chest = int(min(100, volume * 1.8))
        self.belly = int(min(100, volume * 1.5))
        self.tone = int(min(100, volume * 1.2))

        self.alpha = int(
            self.deep * 0.4 +
            self.chest * 0.3 +
            self.belly * 0.2 +
            self.tone * 0.1
        )

        return frame

# ---------------------------------------
# START LIVE STREAM FUNCTION
# ---------------------------------------
def start_live_stream():

    ctx = webrtc_streamer(
        key="alpha-live",
        mode=WebRtcMode.SENDRECV,
        audio_processor_factory=VoiceProcessor,
        media_stream_constraints={"audio": True, "video": False},
        async_processing=True,
    )

    if ctx.audio_processor:
        return {
            "alpha": ctx.audio_processor.alpha,
            "deep": ctx.audio_processor.deep,
            "chest": ctx.audio_processor.chest,
            "belly": ctx.audio_processor.belly,
            "tone": ctx.audio_processor.tone,
        }

    return {
        "alpha":0,
        "deep":0,
        "chest":0,
        "belly":0,
        "tone":0,
    }

