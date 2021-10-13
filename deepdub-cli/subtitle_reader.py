
import srt

from pytimeparse.timeparse import timeparse

subs = list(srt.parse(open("C:\squidgames\subtitles\ep1.srt")))

#from datetime import datetime, timedelta
# we specify the input and the format...
#t1 = datetime.strptime("00:14:00","%H:%M:%S")
# ...and use datetime's hour, min and sec properties to build a timedelta
#delta1 = timedelta(hours=t1.hour, minutes=t1.minute, seconds=t1.second)



import re
from datetime import timedelta


regex = re.compile(r'((?P<hours>\d+?)hr)?((?P<minutes>\d+?)m)?((?P<seconds>\d+?)s)?')


def parse_time(time_str):
    parts = regex.match(time_str)
    if not parts:
        return
    parts = parts.groupdict()
    time_params = {}
    for name, param in parts.items():
        if param:
            time_params[name] = int(param)
    return timedelta(**time_params)



def timedelta_parse(value):
    """
    convert input string to timedelta
    """
    value = re.sub(r"[^0-9:]", "", value)
    if not value:
        return

    return timedelta(**{key:float(val)
                        for val, key in zip(value.split(":")[::-1], 
                                            ("seconds", "minutes", "hours", "days"))
               })

import moviepy.editor as mp
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

for s in subs:
	#print (s.start)
	#print (timedelta_parse("00:14:00"))
	if s.start > timedelta_parse("00:14:00"):
		start_seconds = float(s.start.total_seconds())
		end_seconds = float(s.end.total_seconds())


		if end_seconds - start_seconds < 1.5:
			continue

		print ("")
		print (s.index)
		print (s.content)


		video_filename = r"C:\squidgames\cut_srt{}.mp4".format(str(s.index))
		audio_filename = r"C:\squidgames\audio_srt{}.mp3".format(str(s.index))

		ffmpeg_extract_subclip("C:\squidgames\ep1.mp4", start_seconds, end_seconds, targetname=video_filename)		
		my_clip = mp.VideoFileClip(video_filename)
		my_clip.audio.write_audiofile(audio_filename)
	
	if s.start > timedelta_parse("00:14:20"):
		break


