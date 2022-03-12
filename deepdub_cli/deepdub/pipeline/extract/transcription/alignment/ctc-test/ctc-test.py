import torch, transformers, ctc_segmentation
import soundfile



# wav2vec2
model_file = 'jonatasgrosman/wav2vec2-large-xlsr-53-english'
vocab_dict = {"<pad>": 0, "<s>": 1, "</s>": 2, "<unk>": 3, "|": 4, "E": 5, "N": 6, "I": 7, "S": 8, "R": 9, "T": 10, "A": 11, "H": 12, "D": 13, "U": 14, "L": 15, "C": 16, "G": 17, "M": 18, "O": 19, "B": 20, "W": 21, "F": 22, "K": 23, "Z": 24, "V": 25, "Ü": 26, "P": 27, "Ä": 28, "Ö": 29, "J": 30, "Y": 31, "'": 32, "X": 33, "Q": 34, "-": 35}

processor = transformers.Wav2Vec2Processor.from_pretrained( model_file )
model = transformers.Wav2Vec2ForCTC.from_pretrained( model_file )

speech_array, sampling_rate = soundfile.read( 'test-16khz-mono.wav' )
assert sampling_rate == 16000
features = processor(speech_array,sampling_rate=16000, return_tensors="pt")
input_values = features.input_values
attention_mask = features.attention_mask
with torch.no_grad():
    logits = model(input_values).logits
predicted_ids = torch.argmax(logits, dim=-1)
transcription = processor.batch_decode(predicted_ids)[0]
transcription = transcription.lower().split()

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
    softmax = torch.nn.Softmax(dim = -1)
    lpz = softmax(logits)[0].cpu().numpy()
char_list = [x.lower() for x in vocab_dict.keys()]
ground_truth_mat, utt_begin_indices = ctc_segmentation.prepare_text(config, transcription,char_list)
timings, char_probs, state_list = ctc_segmentation.ctc_segmentation(config, lpz, ground_truth_mat)
segments = ctc_segmentation.determine_utterance_segments(config, utt_begin_indices, char_probs, timings, transcription)

# dump
for word, segment in zip(transcription, segments):  # note: removed split()
    print( f"{segment[0]:.2f} {segment[1]:.2f} {segment[2]:3.4f} {word}")
