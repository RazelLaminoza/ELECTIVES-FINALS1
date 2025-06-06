import sounddevice as sd
import numpy as np
import tkinter as tk

# Parameters
samplerate = 44100  # Standard audio sample rate
delay_samples = int(0.2 * samplerate)  # 200ms delay
effect_type = None  # Stores the selected effect
stream = None  # Audio stream instance

# Audio effect functions
def apply_echo(input_signal, delay_samples):
    output_signal = np.zeros_like(input_signal)
    for i in range(len(input_signal)):
        output_signal[i] = input_signal[i]
        if i >= delay_samples:
            output_signal[i] += 0.5 * input_signal[i - delay_samples]  # Echo effect
    return output_signal

def apply_delay(input_signal, delay_samples):
    output_signal = np.zeros_like(input_signal)
    output_signal[delay_samples:] = input_signal[:-delay_samples]  # Delay effect
    return output_signal

def apply_distortion(input_signal):
    return np.tanh(5 * input_signal)  # Distortion effect

def apply_reverb(input_signal):
    output_signal = np.convolve(input_signal, np.ones(500)/500, mode="same")  # Reverb effect
    return output_signal

# Callback function for real-time processing
def audio_callback(indata, outdata, frames, time, status):
    global effect_type
    if status:
        print(status)
    
    processed_audio = indata[:, 0]  # Get input signal
    if effect_type == "Echo":
        processed_audio = apply_echo(processed_audio, delay_samples)
    elif effect_type == "Delay":
        processed_audio = apply_delay(processed_audio, delay_samples)
    elif effect_type == "Distortion":
        processed_audio = apply_distortion(processed_audio)
    elif effect_type == "Reverb":
        processed_audio = apply_reverb(processed_audio)

    outdata[:, 0] = processed_audio  # Send processed audio to output

# Start audio processing
def start_audio(eff):
    global stream, effect_type
    effect_type = eff
    stream = sd.Stream(callback=audio_callback, samplerate=samplerate, channels=1)
    stream.start()
    status_label.config(text=f"Processing {eff} effect... Speak now!")

# Stop audio processing
def stop_audio():
    global stream
    if stream:
        stream.stop()
        stream.close()
        status_label.config(text="Stopped")

# Create GUI
root = tk.Tk()
root.title("Real-Time Audio Effects")

status_label = tk.Label(root, text="Press a button to start an effect", font=("Arial", 12))
status_label.pack()

tk.Button(root, text="Yellow: Echo", bg="yellow", command=lambda: start_audio("Echo")).pack()
tk.Button(root, text="Red: Delay", bg="red", command=lambda: start_audio("Delay")).pack()
tk.Button(root, text="Blue: Distortion", bg="blue", command=lambda: start_audio("Distortion")).pack()
tk.Button(root, text="Brown: Reverb", bg="brown", command=lambda: start_audio("Reverb")).pack()
tk.Button(root, text="Stop", bg="gray", command=stop_audio).pack()

root.mainloop()
