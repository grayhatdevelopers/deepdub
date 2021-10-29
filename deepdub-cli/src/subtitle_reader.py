
import srt

from pytimeparse.timeparse import timeparse


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

def reintegrate (
    original_video_filename,
    subtitles,
    translated_video_paths
):
    print ("[EXTRACTOR] Reintegrating clips into video...")
    


def extract_audio_and_video (
    subs_path, 
    video_path, 
    extracted_audio_path="./extracted/audio/",
    extracted_video_path="./extracted/video/",
    start_time="00:00:00", 
    end_time=None, 
    minimum_length=1.5
):

    print ("[EXTRACTOR] Starting audio and video extraction...")
    subs = list(srt.parse(open(subs_path)))

    texts       = []
    audio_paths = []
    video_paths = []

    num_generated = 0

    for s in subs:
        if s.start > timedelta_parse(start_time):
            start_seconds = float(s.start.total_seconds())
            end_seconds = float(s.end.total_seconds())


            if end_seconds - start_seconds < minimum_length:
                continue

            print ("")
            print (s.index)
            print (s.content)


            video_filename = r"{}{}cut_srt.mp4".format(extracted_video_path,str(s.index))
            audio_filename = r"{}{}audio_srt.mp3".format(extracted_audio_path,str(s.index))

            ffmpeg_extract_subclip("C:\squidgames\ep1.mp4", start_seconds, end_seconds, targetname=video_filename)		
            my_clip = mp.VideoFileClip(video_filename)
            my_clip.audio.write_audiofile(audio_filename)

            texts.append(s)
            audio_paths.append(audio_filename)
            video_paths.append(video_filename)

            num_generated+=1

        if end_time and s.start > timedelta_parse(end_time):
            break
    
    print ("[EXTRACTOR] Extracted {} clips and audios.".format(num_generated))

    return texts, audio_paths, video_paths

