#!/usr/bin/env python
# coding=utf-8

from aeneas.exacttiming import TimeValue
from aeneas.executetask import ExecuteTask
from aeneas.language import Language
from aeneas.syncmap import SyncMapFormat
from aeneas.task import Task
from aeneas.task import TaskConfiguration
from aeneas.textfile import TextFileFormat
import aeneas.globalconstants as gc




from pydub import AudioSegment
from pydub.silence import detect_nonsilent


import json

#adjust target amplitude
def match_target_amplitude(sound, target_dBFS):
    change_in_dBFS = target_dBFS - sound.dBFS
    return sound.apply_gain(change_in_dBFS)


def find_nonsilent_chunks(wav_file):
    #Convert wav to audio_segment
    audio_segment = AudioSegment.from_wav(wav_file)

    #normalize audio_segment to -20dBFS 
    normalized_sound = match_target_amplitude(audio_segment, 0.0)
    print("length of audio_segment={} seconds".format(len(normalized_sound)/1000))

    #Print detected non-silent chunks, which in our case would be spoken words.
    nonsilent_data = detect_nonsilent(normalized_sound, min_silence_len=500, silence_thresh=-20, seek_step=1)

    #convert ms to seconds
    print("start,Stop")
    for chunks in nonsilent_data:
        print( [chunk/1000 for chunk in chunks])

    return nonsilent_data


def run (
	input_audio_path,
	transcription,
	args,
	):
	
	transcription = "\n".join(item for item in transcription)
	
	print ("Transcription in Aeneas is:", transcription)
	
	transcription_path = args.metadata_path + "/transcription.txt" 
    
	text_file = open(transcription_path, "w")
	n = text_file.write(transcription)
	text_file.close()   
	
	# create Task object
	config_string = u"task_language=de|is_text_type=plain|os_task_file_format=json"
	task = Task(config_string=config_string)
	task.audio_file_path_absolute = input_audio_path
	task.text_file_path_absolute = transcription_path

	task.sync_map_file_path_absolute = args.metadata_path + "aeneas_aligned_output.json"

	# process Task
	ExecuteTask(task).execute()

	# Find nonsilent portions (we assume little to no background noise)
	nonsilent_data = find_nonsilent_chunks(input_audio_path)

	# print produced sync map
	print(task.sync_map)
	word_level_alignment_filepath = task.output_sync_map_file()

	sync_map_json = json.load(open(word_level_alignment_filepath))

	print (sync_map_json)

	speech_brackets = find_nonsilent_chunks(input_audio_path)
	
	for speech in speech_brackets:
		speech[0] = float("{:.3f}".format(speech[0] / 1000))
		speech[1] = float("{:.3f}".format(speech[1] / 1000))
	
	
	for idx, item in enumerate(sync_map_json["fragments"]):

		for jdx, speech in enumerate(speech_brackets):
			print ("Begin: ", float(item["begin"]), ", Speech 0: ", speech[0])
			print ("End: ", float(item["end"]), ", Speech 1: ", speech[1])
			if float(item["begin"]) > speech[0] and (float(item["end"]) - speech[1] < 0.2 and float(item["end"]) - speech[1] >=0) and float(item["begin"]) < speech[1]:
				item["end"] = str(speech[1])
				print("in the following bracket:")
				break
		print ("Item #", idx, ":", item)

	

	return word_level_alignment_filepath

	
#print ( run(
#		u"./test.wav",
#		u"./sample_output.txt",
#		args=None
#	))


#print ("==============================================")

#print (find_nonsilent_chunks("./test.wav"))




