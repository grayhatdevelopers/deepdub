import os
import srt
from pathlib import Path

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
    original_video_path,
    subtitles,
    translated_video_paths
):
    print ("[EXTRACTOR] Reintegrating clips into video...")

    subclips = []

    original_video = mp.VideoFileClip(str(original_video_path))

    start_seconds = float(subtitles[0].start.total_seconds()) # Start from 0 second before the dub

    for s, translated_video_path in zip(subtitles, translated_video_paths):

        end_seconds = float(s.start.total_seconds())

        subclip = original_video.subclip(start_seconds, end_seconds)

        subclips.append(subclip)
        subclips.append(mp.VideoFileClip(str(translated_video_path)))

        start_seconds = float(s.end.total_seconds())

    ## Get the remaining part of the video after the last subtitle
    # subclip = original_video.subclip(start_seconds, original_video.end.total_seconds())
    # subclips.append(subclip)
    print ("[EXTRACTOR] Writing final video to disk...")

    final_clip = mp.concatenate_videoclips(subclips)
    to_return = final_clip.write_videofile("./results/final_result.mp4")

    print ("[EXTRACTOR] Reintegration complete.")

    return to_return

def extract_audio_and_video (
    subs_path, 
    video_path, 
    extracted_audio_path=r"./extracted/audio/",
    extracted_video_path=r"./extracted/video/",
    start_time="00:00:00", 
    end_time=None, 
    minimum_length=1.5
):

    print ("[EXTRACTOR] Starting audio and video extraction...")
    subs = list(srt.parse(open(subs_path)))

    subtitles   = []
    audio_paths = []
    video_paths = []

    original_video = mp.VideoFileClip(str(video_path))

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


            #video_filename = os.path.join(extracted_video_path, "{}cut_srt.mp4".format(str(s.index)))
            #audio_filename = os.path.join(extracted_audio_path, "{}audio_srt.mp3".format(str(s.index)))


            #video_filename = Path(extracted_video_path + "\\{}cut_srt.mp4".format(str(s.index)))
            #audio_filename = Path(extracted_audio_path + "\\{}audio_srt.mp3".format(str(s.index)))

		

            #video_filename = Path("C:\deepdub\deepdub_server\deepdub_server\user_uploads\wooey_scripts\extracted\video\{}cut_srt.mp4".format(str(s.index)))
            #audio_filename = Path("\\{}audio_srt.mp3".format(str(s.index)))


            video_filename = Path(r"{}{}cut_srt.mp4".format(extracted_video_path, str(s.index)))
            audio_filename = Path(r"{}{}audio_srt.mp3".format(extracted_audio_path, str(s.index)))
		
            print ("Video will be loaded from", video_path)
            print ("Video will be saved at", video_filename)

            #ffmpeg_extract_subclip(str(video_path), start_seconds, end_seconds, targetname=video_filename)	

            extracted_video_clip = original_video.subclip(start_seconds, end_seconds).write_videofile(str(video_filename))
	
            my_clip = mp.VideoFileClip(str(video_filename))
            my_clip.audio.write_audiofile(str(audio_filename))


            print ("[EXTRACTOR] Saving the current extracted subtitle and its audio & video...")
            subtitles.append(s)
            audio_paths.append(audio_filename)
            video_paths.append(video_filename)

            num_generated+=1

        if end_time and s.start > timedelta_parse(end_time):
            break
    
    print ("[EXTRACTOR] Extracted {} clips and audios.".format(num_generated))

    return subtitles, audio_paths, video_paths

