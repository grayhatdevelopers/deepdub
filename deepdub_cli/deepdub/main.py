# ------ RELATIVE-FIX START
if __name__ != "__main__":
	# to prevent the relative import issue, add this folder to the syspath
	import os
	import sys
	parent_dir_name = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
	sys.path.append(parent_dir_name + "/deepdub")
# ------ RELATIVE-FIX END

import argparse
import subprocess
import sys

from pathlib import Path
import os

## Info about this script
parser = argparse.ArgumentParser(
    description="Deepdub dubs videos to a language of your choosing (out of the ones we support, of course).",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter
)


## Arguments for this script
parser.add_argument("-vd", "--video", type=Path, 
                    required=True,
                    help="Input video to process.")

parser.add_argument("-tn", "--translation", type=Path, 
                    required=False,
                    help="Translation file (.srt) to use as reference.")
parser.add_argument("-dds", "--deepdubstart", type=str, 
                    default="00:00:00",
                    help="Starting point from where deepdub should start dubbing."
                    )
parser.add_argument("-dde", "--deepdubend", type=str, 
                    default=None,
                    help="Ending point from where deepdub should end dubbing."
                    )
parser.add_argument("-cml", "--clipminlength", type=float, 
                    default=1.5,
                    help="Minimum duration of a clip of dubbed video."
                    )                    

parser.add_argument("-tls", "--translation_language_source", type=str, 
                    required=False,
                    help="Language in which the original video is in.")
parser.add_argument("-tlt", "--translation_language_target", type=str, 
                    required=False,
                    help="Language in which to output the video.")


parser.add_argument("-ep", "--extracted_path", type=str, 
                    default="./extracted",
                    help="Directory in which temporary extracted files are saved."
)
parser.add_argument("-tp", "--translated_path", type=str, 
                    default="./translated",
                    help="Directory in which temporary translated files are saved."
)
parser.add_argument("-rp", "--results_path", type=str, 
                    default="./results",
                    help="Directory in which result files are saved."
)
parser.add_argument("-sp", "--samples_path", type=str, 
                    default="./samples",
                    help="Directory in which sample mp3 files exist."
)
parser.add_argument("-mp", "--metadata_path", type=str, 
                    default="./metadata",
                    help="Directory in which preprocessing metadata is saved."
)


## Arguments from pipeline/audio/real_time_voice_cloning

parser.add_argument("-e", "--enc_model_fpath", type=Path, 
                    default="encoder/saved_models/pretrained.pt",
                    help="Path to a saved encoder")
parser.add_argument("-s", "--syn_model_fpath", type=Path, 
                    default="synthesizer/saved_models/pretrained/pretrained.pt",
                    help="Path to a saved synthesizer")
parser.add_argument("-v", "--voc_model_fpath", type=Path, 
                    default="vocoder/saved_models/pretrained/pretrained.pt",
                    help="Path to a saved vocoder")
parser.add_argument("--cpu", action="store_true", help=\
    "If True, processing is done on CPU, even when a GPU is available.")
parser.add_argument("--no_sound", action="store_true", help=\
    "If True, audio won't be played.")
parser.add_argument("--seed", type=int, default=None, help=\
    "Optional random number seed value to make toolbox deterministic.")
parser.add_argument("--no_mp3_support", action="store_true", help=\
    "If True, disallows loading mp3 files to prevent audioread errors when ffmpeg is not installed.")



## Arguments from pipeline/lipsync/wav2lip
lipsyncer_path = "pipeline/lipsync/wav2lip/"

parser.add_argument('--checkpoint_path', type=str, 
					help='Name of saved checkpoint to load weights from', required=True)

parser.add_argument('--outfile', type=str, help='Video path to save result. See default for an e.g.', 
								default='results/result_voice.mp4')

parser.add_argument('--static', type=bool, 
					help='If True, then use only first video frame for inference', default=False)
parser.add_argument('--fps', type=float, help='Can be specified only if input is a static image (default: 25)', 
					default=25., required=False)

parser.add_argument('--pads', nargs='+', type=int, default=[0, 10, 0, 0], 
					help='Padding (top, bottom, left, right). Please adjust to include chin at least')

parser.add_argument('--face_det_batch_size', type=int, 
					help='Batch size for face detection', default=16)
parser.add_argument('--wav2lip_batch_size', type=int, help='Batch size for Wav2Lip model(s)', default=128)

parser.add_argument('--resize_factor', default=1, type=int, 
			help='Reduce the resolution by this factor. Sometimes, best results are obtained at 480p or 720p')

parser.add_argument('--crop', nargs='+', type=int, default=[0, -1, 0, -1], 
					help='Crop video to a smaller region (top, bottom, left, right). Applied after resize_factor and rotate arg. ' 
					'Useful if multiple face present. -1 implies the value will be auto-inferred based on height, width')

parser.add_argument('--box', nargs='+', type=int, default=[-1, -1, -1, -1], 
					help='Specify a constant bounding box for the face. Use only as a last resort if the face is not detected.'
					'Also, might work only if the face is not moving around much. Syntax: (top, bottom, left, right).')

parser.add_argument('--rotate', default=False, action='store_true',
					help='Sometimes videos taken from a phone can be flipped 90deg. If true, will flip video right by 90deg.'
					'Use if you get a flipped result, despite feeding a normal looking video')

parser.add_argument('--nosmooth', default=False, action='store_true',
					help='Prevent smoothing face detections over a short temporal window')



## Arguments from Gentle
import multiprocessing
parser.add_argument(
        '--nthreads', default=multiprocessing.cpu_count(), type=int,
        help='number of alignment threads')
parser.add_argument(
        '-o', '--output', metavar='output', type=str, 
        help='output filename')
parser.add_argument(
        '--conservative', dest='conservative', action='store_true',
        help='conservative alignment')
parser.set_defaults(conservative=False)
parser.add_argument(
        '--disfluency', dest='disfluency', action='store_true',
        help='include disfluencies (uh, um) in alignment')
parser.set_defaults(disfluency=False)


import os

# All arguments
deepdub_no_args = os.environ.get('DEEPDUB_NO_ARGS')
print ("deepdub_no_args =", deepdub_no_args)
args = None
if deepdub_no_args == None or deepdub_no_args == False:
	args = parser.parse_args()

# Only arguments which have a default
# all_defaults = {}
# for key in vars(args):
#	all_defaults[key] = parser.get_default(key)

# print("Default arguments", all_defaults)

def main(func_args=None):

    global args

    if func_args != None:
        args = func_args
    
    import pipeline.extract.subtitles.subtitle_reader as extractor
    # import pipeline.audio.real_time_voice_cloning.run_cli as vocoder
    import pipeline.audio.yourtts.run_cli as vocoder
    import pipeline.lipsync.wav2lip.run_cli as lip_syncer

    ## -------------------------------------------
    ## DeepDub pipeline 2
    ## Authors:
    ## 1. AbdurRehman Subhani
    ## 2. Saad Ahmed Bazaz
    ## -------------------------------------------

    print("Args are = ", args)

    # 0.
    # Preprocess the video. Here, if a translation file is not provided, we try to make it ourselves.
    if args.translation:
        translation_filepath = args.translation
    else:
        # import pipeline.extract.transcription.generation.speechbrain_asr.run_cli as transcription_generator
        import pipeline.extract.transcription.generation.wav2vec2.run_cli as transcription_generator
        import pipeline.extract.transcription.pronunciation_correction.paddlespeech.text.run_cli as pronunciation_correction
        # import pipeline.extract.transcription.alignment.gentle.run_cli as transcription_aligner
        import pipeline.extract.transcription.alignment.aeneas__pydub.run_cli as transcription_aligner
        import pipeline.extract.transcription.clustering.run_cli as transcription_clusterer
        import pipeline.extract.transcription.pronounciation_correction.PaddleSpeech.paddlespeech.text.run_cli as pronounciation_correction
        import pipeline.extract.translation.opus_pt.run_cli as translator
        

        # Extract the audio from the original video (we will use it for all transcription tasks)
        import moviepy.editor as mp


        filename, file_extension = os.path.splitext(args.video)

        filename = Path(args.video).stem

        print ("Filename is", filename)


        converted_video = os.path.join(args.metadata_path, filename+".mp4")

        call = "ffmpeg -i {} {}".format(args.video, str(converted_video))        

        print ("System call is", call)
        os.system(call)

        args.video = converted_video

        try:
            original_video = mp.VideoFileClip(str(args.video))
        except:
            print("Video path is ", args.video)
            original_video = mp.VideoFileClip(args.video.path)

    #    original_video = mp.VideoFileClip(str(args.video))
     
        original_audio_path = args.metadata_path + "/original_audio.wav"
        original_video.audio.write_audiofile(original_audio_path)

        # 0.1.
        # Generate the transcription
        print("************************ \n Generating Transcriptions ************************")
        raw_transcription, newline_transcription = transcription_generator.run(original_audio_path, args)
        print("************************ \n Transcription generated ************************")
        
        # 0.1.2.
        # Add pronounciation correction here
        print("************************ \n Pronounciation Correction ************************")

        #punctuated = pronounciation_correction.run(raw_transcription,args)
        punctuated = raw_transcription
        punctuated = punctuated.replace(" ", "\n")

        print("************************ \n Pronounciation Correction Completed ************************")

        # 0.1.3.
        # Tranlsate 0.1.2.

        alignment_path = transcription_aligner.run(original_audio_path, newline_transcription, args)

        # 0.1.4.
        # Align Raw transcription here

        transcription_srt_filepath = transcription_clusterer.run(alignment_path, original_audio_path, args)

        # 0.1.5.
        # Cluster Raw transcription here

        # 0.1.6.
        # Extract percentage of words spoken in 0.1.5

        # 0.1.7.
        # Use 0.1.6. to extract percentage of words from translation


        # 0.2.
        # Align the words in the transcription to the original audio
        # alignment_path = transcription_aligner.run(original_audio_path, newline_transcription, args)


        # 0.3. 
        # Cluster the words according to their timestamps, form sentences and create a .SRT file out of that
        # transcription_srt_filepath = transcription_clusterer.run(alignment_path, original_audio_path, args)

        # 0.4.
        # Pass the .SRT file of the transcription to the Translator, so it can be translated (line by line) to a 
        # target language        
        translation_filepath = translator.run(transcription_srt_filepath, args)

    # 1.
    # First extract audio and video bytes and store in a folder 
    # called extracted/audio and extracted/video 
    # (Subtitle_Reader)
    subtitles, extracted_audio_paths, extracted_video_paths = extractor.extract_audio_and_video(
                                                                        translation_filepath, 
                                                                        args.video,
                                                                        args.extracted_path + "/audio/",
                                                                        args.extracted_path + "/video/",
                                                                        args.deepdubstart,
                                                                        args.deepdubend,
                                                                        args.clipminlength,
                                                                    )

    # 2.
    # Pass files to speech vocoder 
    # (Real-Time-Voice-Cloning)
    texts = [s.content for s in subtitles]
    translated_audio_paths = vocoder.run(extracted_audio_paths, texts, args, args.translated_path + "/audio/")

    # 3.
    # Pass files to Lip Syncer
    # (Wav2Lip)

    # 3a. check each translated audio file length, 
    # if it is more than the corresponding extracted video file, then 
    # extract a longer video from the original video! 

    # First update the subtitles
    from pydub import AudioSegment

    # Timedelta function demonstration 
    from datetime import timedelta

    import srt

    for idx, (s, translated_audio_path, extracted_video_path, extracted_audio_path) in enumerate(zip(subtitles, translated_audio_paths, extracted_video_paths, extracted_audio_paths)):

        # Load file
        audio_segment = AudioSegment.from_file(translated_audio_path)

        audio_duration = len(audio_segment) / 10000
        
        print ("Audio Duration is: ", audio_duration)
        print ("S.start is: ", s.start)
        
        new_end = s.start.total_seconds() + audio_duration 
        new_end = timedelta(0, new_end, 0)

        try:
            if idx+1 != len(subtitles) and new_end > subtitles[idx+1].start:
                # TODO: This is where some frames might have to be generated, because now it needs data which cannot be provided.
                print ("The new end time overlaps with the start time of the next clip.")
                print ("Setting the new end time as the start time of the next clip (to prevent overlaps).")
                new_end = subtitles[idx+1].start
        except Exception as e:
            print ("Couldn't check for overlaps. Reason: ", str(e))

        print ("New end is: ", new_end)
        print ("s.end is: ", s.end)  

        if new_end > s.end:
            s.end = new_end

            start_seconds = float(s.start.total_seconds())
            end_seconds = float(s.end.total_seconds())
            try:
                video_filename = Path(r"{}{}new_cut_srt.mp4".format(args.extracted_path + "/video/", str(s.index)))

                extracted_video_clip = original_video.subclip(start_seconds, end_seconds).write_videofile(str(video_filename))
	
                extracted_video_paths[idx] = video_filename
            except Exception as e:
                print ("Could not create the following subtitle:", s)
                print ("Reason:", str(e))
        elif new_end < s.end:
            # TODO: Check what happens when Wav2Lip receives a smaller video!
            # If it uses the length of video which is equal to length of audio, and discards the rest, then we have a
            # problem. We might have to generate frames to fill in the gap.
            # Or, we can try to ensure that all generated audio is at LEAST greater than the original video.
            # (in pre-hindsight, it should always try to be equal to the video, but mishaps happen :D )

            # Current fix: Fill in remaining duration with silence.
            # Reference: 
            # - https://github.com/Rudrabha/Wav2Lip/issues/274
            # - https://stackoverflow.com/questions/46757852/adding-silent-frame-to-wav-file-using-python
            print ("Generated audio is smaller than originally extracted video.")
            print ("Adding a silent part to compensate.")

            new_end_seconds = float(new_end.total_seconds())
            original_end_seconds = float(s.end.total_seconds())
            
            awkward_duration = (original_end_seconds - new_end_seconds) * 1000
            audio_in_file = translated_audio_path
            audio_out_file = Path(r"{}{}new_cut_srt.wav".format(args.translated_path + "/audio/", str(s.index)))

            # create silence audio segment of remaining time
            silent_segment = AudioSegment.silent(duration=awkward_duration)  #duration in milliseconds

            #read wav file to an audio segment
            speech = AudioSegment.from_wav(audio_in_file)

            #Add above two audio segments    
            final_translated_speech = speech + silent_segment

            #Sanity check: trim to match the original extracted audio
            original_audio_segment = AudioSegment.from_file(extracted_audio_path)
            final_translated_speech = final_translated_speech[0:len(original_audio_segment)-1]

            #Either save modified audio
            final_translated_speech.export(audio_out_file, format="wav")
            translated_audio_paths[idx] = audio_out_file

    final_srt = srt.compose(list(subtitles))
    
    translation_srt_filepath = args.metadata_path + "/new_translation_sentences.srt" 
    
    text_file = open(translation_srt_filepath, "w")
    n = text_file.write(final_srt)
    text_file.close()  

    #3b. Now you can pass the files 
    translated_video_paths = lip_syncer.run(translated_audio_paths, extracted_video_paths, args)

    # 4.
    # Finally, reintegrate the translated videos back into the original video
    final_file = extractor.reintegrate(args.video, subtitles, translated_video_paths, args)

    print("\n*************** Encoding video to mp4 ***************")

    os.system("ffmpeg -i {} -c:v libx264 -preset slow -crf 20 -c:a aac -b:a 160k -vf format=yuv420p -vf \"drawtext=text='deepdub':x=70:y=H-th-70:fontfile=../assets/fonts/RedHatDisplay-VariableFont_wght.ttf:fontsize=40:fontcolor=white:shadowcolor=black:shadowx=5:shadowy=5\" -movflags +faststart {}".format(final_file, final_file.split(".")[0] + "_iphonefixed.mp4"))

    print("\n*************** Encoding complete ***************")

    print ("Thank you for using deepdub.")

    if func_args != None:
        return final_file

    return 0

if __name__ == "__main__":
    sys.exit(main())
