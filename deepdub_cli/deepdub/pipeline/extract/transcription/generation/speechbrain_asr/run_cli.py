from speechbrain.pretrained import EncoderDecoderASR

asr_model = EncoderDecoderASR.from_hparams(source="speechbrain/asr-crdnn-rnnlm-librispeech", savedir="pretrained_model")

def run (
	input_audio_file, 
	args
	):

	print ("[GENERATING TRANSCRIPTION]")
	transcription = asr_model.transcribe_file(input_audio_file)

	print (transcription)
	newline_transcription = transcription.replace(" ", "\n")

	return transcription, newline_transcription


# print (run ("./test.wav", None)[1])