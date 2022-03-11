#!/usr/bin/env python
# coding=utf-8

from aeneas.exacttiming import TimeValue
from aeneas.executetask import ExecuteTask
from aeneas.language import Language
from aeneas.syncmap import SyncMapFormat
from aeneas.task import Task
from aeneas.task import TaskConfiguration
from aeneas.runtimeconfiguration import RuntimeConfiguration
from aeneas.textfile import TextFileFormat
import aeneas.globalconstants as gc

import json

aeneas_supported_languages = {
	"English": "eng",
	"German": "de",
	"Hindi": "hin",
	"Urdu": "ur",
}

def run (
	input_audio_path,
	transcription,
	args,
	):
	


	transcription = "\n".join(item for item in transcription)

	if args.translation_language_source == "Urdu":
		transcription = transcription.replace("<s>","")

	print ("Transcription in Aeneas is:", transcription)
	
	transcription_path = args.metadata_path + "/transcription.txt" 
    
	text_file = open(transcription_path, "w", encoding='utf-8')
	n = text_file.write(transcription)
	text_file.close()   
	
	# create Task object
	config_string = u"task_language={}|is_text_type=plain|os_task_file_format=json".format(aeneas_supported_languages[args.translation_language_source])
	
	if args.translation_language_source == "Urdu":

		rconf_string = u"tts=espeak-ng|allow_unlisted_languages=True" 
		
		rconf = RuntimeConfiguration(rconf_string)
		rconf[RuntimeConfiguration.ALLOW_UNLISTED_LANGUAGES] = True
		rconf[RuntimeConfiguration.TTS] = "espeak-ng"

		task = Task(config_string=config_string, rconf=rconf)
	else:
		task = Task(config_string=config_string)

	task.audio_file_path_absolute = input_audio_path
	task.text_file_path_absolute = transcription_path

	task.sync_map_file_path_absolute = args.metadata_path + "/aeneas_aligned_output.json"

	# process Task
	if args.translation_language_source == "Urdu":
		ExecuteTask(task, rconf=rconf).execute()
	else:
		ExecuteTask(task).execute()

	# print produced sync map
	print(task.sync_map)
	word_level_alignment_filepath = task.output_sync_map_file()

	sync_map_json = json.load(open(word_level_alignment_filepath))

	print (sync_map_json)



	return word_level_alignment_filepath

	
#print ( run(
#		u"./test.wav",
#		u"./sample_output.txt",
#		args=None
#	))


#print ("==============================================")

#print (find_nonsilent_chunks("./test.wav"))




