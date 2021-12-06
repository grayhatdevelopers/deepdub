from speechbrain.pretrained import EncoderDecoderASR

def run (input_audio_file, args):

	asr_model = EncoderDecoderASR.from_hparams(source="speechbrain/asr-crdnn-rnnlm-librispeech", savedir="pretrained_model")

	print ("[GENERATING TRANSCRIPTION]")
	transcription = asr_model.transcribe_file(audio_file )

	print (transcription)
	new_line_transcription = transcription.replace(" ", "\n")

	return new_line_transcription
