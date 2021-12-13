import torch, transformers, ctc_segmentation
import soundfile

from asrecognition import ASREngine

asr = ASREngine("en", model_path="jonatasgrosman/wav2vec2-large-xlsr-53-english")

audio_paths = ["/path/to/file.mp3", "/path/to/another_file.wav"]
transcriptions = asr.transcribe(audio_paths)

print ("TRANSCRIPTION:\n", transcription)


#filename = "./sample_output.txt"

#with open(filename) as file:
 #   lines = file.readlines()
  #  lines = [line.rstrip() for line in lines]

#transcription = lines


# ctc-segmentation
config = ctc_segmentation.CtcSegmentationParameters()

config.index_duration = 0.0200  # or: speech_array.shape[0] / lpz.shape[0] / sampling_rate

with torch.no_grad():
    softmax = torch.nn.LogSoftmax(dim = -1)
    lpz = softmax(logits)[0].cpu().numpy()
char_list = [x.lower() for x in vocab_dict.keys()]
ground_truth_mat, utt_begin_indices = ctc_segmentation.prepare_text(config, transcription,char_list)
timings, char_probs, state_list = ctc_segmentation.ctc_segmentation(config, lpz, ground_truth_mat)
segments = ctc_segmentation.determine_utterance_segments(config, utt_begin_indices, char_probs, timings, transcription)

# dump
for word, segment in zip(transcription, segments):  # note: removed split()
    print( f"{segment[0]:.2f} {segment[1]:.2f} {segment[2]:3.4f} {word}")
