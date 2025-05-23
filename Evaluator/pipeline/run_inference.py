from segmenter import segment_audio
from feature_extractor import generate_feature_file
from predictor import load_model, predict_and_aggregate
from transcriber import transcribe_all_audios
from live_recording import record_audio, save_audio
import shutil
import os

def clear_input_folders():
    """
    Method to clean input folders before running the evaluation
    """
    folders_to_clear = ["input/segments", "input/transcripts"]
    for folder in folders_to_clear:
        if os.path.exists(folder):
            shutil.rmtree(folder)
            print(f"🧹 Cleared: {folder}")
        os.makedirs(folder)

# Cleaning the input folders
clear_input_folders()

# Record audio via mic
recording, sr = record_audio(duration=10)
if recording is not None:
    recorded_path = save_audio(recording, sr, filename="live_input.wav")
    audio_files = [recorded_path] 
else:
    audio_files = []

#Paths
audio_path = recorded_path
segment_dir = "input/segments"
transcript_dir = "input/transcripts"

# segment the audio and save in the segment_dir
segment_paths = segment_audio(audio_path, segment_dir)

# generating the transcripts
transcribe_all_audios(audio_base_dir=segment_dir, transcript_base_dir="input/transcripts")

# Feature extraction
X = generate_feature_file(audio_dir=segment_dir, transcript_dir=transcript_dir)

# Model prediction and aggregation
model, top_features = load_model()
final_label, segment_labels = predict_and_aggregate(X, segment_paths, model, top_features)


# Final result
print(f"\n---- Final predicted fluency level ----: {final_label}\n")