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


def run (
	input_audio_path,
	raw_transcription_audio_path,
	args,
	):
	# create Task object
	config_string = u"task_language=eng|is_text_type=plain|os_task_file_format=json"
	task = Task(config_string=config_string)
	task.audio_file_path_absolute = input_audio_path
	task.text_file_path_absolute = raw_transcription_audio_path

	task.sync_map_file_path_absolute = u"./output.json"

	# process Task
	ExecuteTask(task).execute()

	# print produced sync map
	print(task.sync_map)
	word_level_alignment_filepath = task.output_sync_map_file()
	
	return word_level_alignment_filepath

	
#run(	u"./final_result.wav",
#	u"./transcription2.txt",
#	args=None
#	)

