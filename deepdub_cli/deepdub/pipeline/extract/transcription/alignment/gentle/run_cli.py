import argparse
import logging
import multiprocessing
import os
import sys

import gentle

parser = argparse.ArgumentParser(
        description='Align a transcript to audio by generating a new language model.  Outputs JSON')
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
parser.add_argument(
        '--log', default="INFO",
        help='the log level (DEBUG, INFO, WARNING, ERROR, or CRITICAL)')
parser.add_argument(
        'audiofile', type=str,
        help='audio file')
parser.add_argument(
        'txtfile', type=str,
        help='transcript text file')
args = parser.parse_args()

log_level = args.log.upper()
logging.getLogger().setLevel(log_level)

disfluencies = set(['uh', 'um'])

def on_progress(p):
    for k,v in p.items():
        logging.debug("%s: %s" % (k, v))


resources = gentle.Resources()

def run (
	input_audio_path,
	transcription_path,
	args,
	):


	with open(transcription_path, encoding="utf-8") as fh:
	    transcript = fh.read()


	logging.info("converting audio to 8K sampled wav")

	with gentle.resampled(input_audio_path) as wavfile:
	    logging.info("starting alignment")
	    aligner = gentle.ForcedAligner(resources, transcript, nthreads=args.nthreads, disfluency=args.disfluency, conservative=args.conservative, disfluencies=disfluencies)
	    result = aligner.transcribe(wavfile, progress_cb=on_progress, logging=logging)

	word_level_alignment_filepath = args.metadata_path + "/aligned_transcription.json"

	fh = open(word_level_alignment_filepath, 'w', encoding="utf-8")	
	fh.write(result.to_json(indent=2))
	logging.info("output written to %s" % (word_level_alignment_filepath))

	return word_level_alignment_filepath
