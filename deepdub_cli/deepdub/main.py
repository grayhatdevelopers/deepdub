# ------ RELATIVE-FIX START
if __name__ != "__main__":
	# to prevent the relative import issue, add this folder to the syspath
	import os
	import sys
	parent_dir_name = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
	sys.path.append(parent_dir_name + "/deepdub")
# ------ RELATIVE-FIX END

import argparse
import sys

from pathlib import Path

## Info about this script
parser = argparse.ArgumentParser(
    description="Deepdub dubs videos to a language of your choosing (according to a file you provide, of course).",
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



args = parser.parse_args()

def main():
    import pipeline.extract.subtitles.subtitle_reader as extractor
    import pipeline.audio.real_time_voice_cloning.run_cli as vocoder
    import pipeline.lipsync.wav2lip.run_cli as lip_syncer



    ## -------------------------------------------
    ## DeepDub pipeline 0
    ## Authors:
    ## 1. AbdurRehman Subhani
    ## 2. Saad Ahmed Bazaz
    ## -------------------------------------------


    # 0.
    # Preprocess the video. Here, if a translation file is not provided, we try to make it ourselves.
    if args.translation:
        translation_filepath = args.translation
    else:
        # import pipeline.extract.transcription.generation.speechbrain_asr.run_cli as transcription_generator
        import pipeline.extract.transcription.generation.wav2vec2.run_cli as transcription_generator
        # import pipeline.extract.transcription.alignment.gentle.run_cli as transcription_aligner
        import pipeline.extract.transcription.alignment.aeneas__pydub.run_cli as transcription_aligner
        import pipeline.extract.transcription.clustering.run_cli as transcription_clusterer
        import pipeline.extract.translation.opus_pt.run_cli as translator

        # Extract the audio from the original video (we will use it for all transcription tasks)
        import moviepy.editor as mp
        original_video = mp.VideoFileClip(str(args.video))
        original_audio_path = args.metadata_path + "/original_audio.wav"
        original_video.audio.write_audiofile(original_audio_path)

        # 0.1.
        # Generate the transcription
        raw_transcription, newline_transcription = transcription_generator.run(original_audio_path, args)

        # 0.2.
        # Align the words in the transcription to the original audio
        alignment_path = transcription_aligner.run(original_audio_path, newline_transcription, args)


        # 0.3. 
        # Cluster the words according to their timestamps, form sentences and create a .SRT file out of that
        transcription_srt_filepath = transcription_clusterer.run(alignment_path, original_audio_path, args)

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
    translated_video_paths = lip_syncer.run(translated_audio_paths, extracted_video_paths, args)

    # 4.
    # Finally, reintegrate the translated videos back into the original video
    extractor.reintegrate(args.video, subtitles, translated_video_paths)

    print ("Thank you for using deepdub.")

    return 0

if __name__ == "__main__":
    sys.exit(main())
