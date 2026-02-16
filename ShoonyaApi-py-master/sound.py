import numpy as np
import pyaudio

# Audio parameters
SAMPLING_RATE = 44100  # samples per second
DURATION = 2  # seconds
FREQUENCY = 440 *2  # Hz (A4 note)

# Generate time array
t = np.linspace(0, DURATION, int(SAMPLING_RATE * DURATION), endpoint=False)

# Generate sine wave
amplitude = 0.5  # Adjust for volume
sine_wave = amplitude * np.sin(2 * np.pi * FREQUENCY * t)

# Convert to 16-bit integers for PyAudio
audio_data = (sine_wave * 32767).astype(np.int16)

# Initialize PyAudio
p = pyaudio.PyAudio()

# Open audio stream
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=SAMPLING_RATE,
                output=True)

# Play the audio
stream.write(audio_data.tobytes())

# Clean up
stream.stop_stream()
stream.close()
p.terminate()