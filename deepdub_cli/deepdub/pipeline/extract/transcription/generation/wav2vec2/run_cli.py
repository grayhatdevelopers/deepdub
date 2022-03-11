import torch, transformers, ctc_segmentation
import soundfile

import os
import subprocess

from transformers.models import wav2vec2

wav2vec2_supported_languages = {
	"English": 'jonatasgrosman/wav2vec2-large-xlsr-53-english',
	"Hindi": 'theainerd/Wav2Vec2-large-xlsr-hindi',
	"German": 'jonatasgrosman/wav2vec2-large-xlsr-53-german',
	"Urdu": 'addy88/wav2vec2-urdu-stt',
}

def run (
	input_audio_file, 
	args
	):
	# wav2vec2
	model_file = wav2vec2_supported_languages[args.translation_language_source]
	# vocab_dict = {"<pad>": 0, "<s>": 1, "</s>": 2, "<unk>": 3, "|": 4, "E": 5, "N": 6, "I": 7, "S": 8, "R": 9, "T": 10, "A": 11, "H": 12, "D": 13, "U": 14, "L": 15, "C": 16, "G": 17, "M": 18, "O": 19, "B": 20, "W": 21, "F": 22, "K": 23, "Z": 24, "V": 25, "Ü": 26, "P": 27, "Ä": 28, "Ö": 29, "J": 30, "Y": 31, "'": 32, "X": 33, "Q": 34, "-": 35}

	processor = transformers.Wav2Vec2Processor.from_pretrained( model_file )
	model = transformers.Wav2Vec2ForCTC.from_pretrained( model_file )

	speech_array, sampling_rate = soundfile.read( input_audio_file )
	if sampling_rate != 16000:

		head, tail = os.path.split(input_audio_file)

		new_input_audio_file = head+"/16khz_"+tail+".wav"
		subprocess.run(["sox", input_audio_file, "-c 1", "-r 16000", new_input_audio_file])
		speech_array, sampling_rate = soundfile.read( new_input_audio_file )

		# Check just to be sure
		assert sampling_rate == 16000
	features = processor(speech_array,sampling_rate=16000, return_tensors="pt")
	input_values = features.input_values
	try:
	    attention_mask = features.attention_mask
	except:
	    print ("Cannot obtain attention mask in this model.")
	with torch.no_grad():
	    logits = model(input_values).logits
	predicted_ids = torch.argmax(logits, dim=-1)
	transcription = processor.batch_decode(predicted_ids)[0]
	newline_transcription = transcription.lower().split()

	print ("TRANSCRIPTION:\n", transcription)
	
	return transcription, newline_transcription

# args = {}
# args["translation_language_source"] = "Hindi"
# print(run("./test_urdu.wav", None))
# print(run("./german_new_year_speech_30s_16khz.wav", None))
# print (run("./hindi_16k.wav", args))
