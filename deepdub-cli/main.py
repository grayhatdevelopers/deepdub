

import argparse
from pathlib import Path
# from utils.argutils import print_args


import src.subtitle_reader as extractor

import src.audio.real_time_voice_cloning.run_cli as vocoder

if __name__ == "__main__":
    ## Info & args
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )


    parser.add_argument("-v", "--video", type=Path, 
                        required=True,
                        # default="encoder/saved_models/pretrained.pt",
                        help="Input video to process.")

    parser.add_argument("-tn", "--translation", type=Path, 
                        required=True,
                        # default="encoder/saved_models/pretrained.pt",
                        help="Translation file (.srt) to use as reference.")

    # parser.add_argument("-e", "--enc_model_fpath", type=Path, 
    #                     default="encoder/saved_models/pretrained.pt",
    #                     help="Path to a saved encoder")
    # parser.add_argument("-s", "--syn_model_fpath", type=Path, 
    #                     default="synthesizer/saved_models/pretrained/pretrained.pt",
    #                     help="Path to a saved synthesizer")
    # parser.add_argument("-v", "--voc_model_fpath", type=Path, 
    #                     default="vocoder/saved_models/pretrained/pretrained.pt",
    #                     help="Path to a saved vocoder")
    # parser.add_argument("--cpu", action="store_true", help=\
    #     "If True, processing is done on CPU, even when a GPU is available.")
    # parser.add_argument("--no_sound", action="store_true", help=\
    #     "If True, audio won't be played.")
    # parser.add_argument("--seed", type=int, default=None, help=\
    #     "Optional random number seed value to make toolbox deterministic.")
    # parser.add_argument("--no_mp3_support", action="store_true", help=\
    #     "If True, disallows loading mp3 files to prevent audioread errors when ffmpeg is not installed.")



    args = parser.parse_args()
    # print_args(args, parser)


    # 1.
    # First extract audio and video bytes and store in a folder 
    # called extracted/audio and extracted/video 
    # (Subtitle_Reader)
    texts, extracted_audio_paths, extracted_video_paths = extractor.extract_audio_and_video(args["translation"], args["video"])

    # 2.
    # Pass files to speech vocoder 
    # (Real-Time-Voice-Cloning)
    translated_audio_paths = vocoder.run(extracted_audio_paths, texts, args)

    # 3.
    # Pass files to Lip Syncer
    # (Wav2Lip)
    # lip_syncer
