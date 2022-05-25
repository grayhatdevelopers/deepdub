import os

def run(
    audio_paths, 
    texts, 
    args,
    translated_audio_path="./translated/audio/"   
):

    translated_audio_paths = []

    for idx, (text, audio_path) in enumerate(zip(texts, audio_paths)):
        print("\n[ {} ] *************** Running YourTTS from Commandline ***************".format(idx))

        filename = os.path.join(translated_audio_path, "yourtts_output_%02d.wav" % idx)

        os.system("tts  --text \"{}\" --model_name tts_models/multilingual/multi-dataset/your_tts  --speaker_wav {} --language_idx \"en\" --out_path {}".format(text, audio_path, filename))

        print("\nSaved output as %s\n\n" % filename)

        translated_audio_paths.append (filename)

        print("\n[ {} ] *************** TTS complete ***************".format(idx))
    
    return translated_audio_paths