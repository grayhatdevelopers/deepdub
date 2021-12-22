
# from typing import final
import srt
from time import strftime
from time import gmtime

# importing the module
import json

import datetime


from pydub import AudioSegment
from pydub.silence import detect_nonsilent

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



def run (alignments_path, input_audio_path, args):

    # Opening JSON file
    with open(alignments_path) as json_file:
        data = json.load(json_file)

        # Print the type of data variable
        print("Type:", type(data))

        print ("All Data: ", data)

        # Print the data of dictionary
        print("\nfragments:\n", data['fragments'])


    # Find nonsilent portions (we assume little to no background noise)
    speech_brackets = find_nonsilent_chunks(input_audio_path)

    fragments_list = data["fragments"]

    for frag in fragments_list:
        frag["added"] = False
        frag["begin"] = float(frag["begin"])
        frag["end"] = float(frag["end"])

    final_bucket = []

    for speech in speech_brackets:
        speech[0] = float("{:.3f}".format(speech[0] / 1000))
        speech[1] = float("{:.3f}".format(speech[1] / 1000))
        
        sentence = []
        for word in fragments_list:
            if (word["added"] == False):
                if (word["begin"] >= speech[0] and word["end"] <= speech[1]):
                    sentence.append(word)
                    word['added'] = True
        
        print (sentence)
        final_bucket.append({
            "begin": speech[0],
            "end": speech[1],
            "sentence": sentence,
        })

    included_words = [frag["added"] for frag in fragments_list]

    print ("Number of included words:", sum(included_words))
    print ("Number of discarded words:", len(included_words) - sum(included_words))

    print ("Discarded words:")
    discarded_word_objects = [frag if frag["added"] == False else "" for frag in fragments_list]


    # Re-adjust discarded words into sentences
    for word in discarded_word_objects:
        print ("WORD is: \n", word)
        print ("Type: ", type(word))
        
        if type(word) == str:
            continue

        for idx, bucket in enumerate(final_bucket):
            penalty = 0

            if word["begin"] <= bucket["end"] and word["begin"] >= bucket["begin"]:
                bucket["sentence"].append(word)
                word["added"] = True
                break

            # Treating words which appeared in silent parts
            elif idx + 1 != len(final_bucket):
                if word["begin"] >= final_bucket[idx]["end"] and word["begin"] <= final_bucket[idx+1]["begin"]:
                    silent_range = final_bucket[idx+1]["begin"] - final_bucket[idx]["end"]
                    
                    if word["end"] > final_bucket[idx+1]["begin"]:
                        penalty = 0.2
                    else:
                        penalty = 0.5

                    word_range = word["end"] - word["begin"]

                    time_to_add = word_range*penalty

                    # Add the word to the sentence (back only)
                    bucket["sentence"].append(word)

                    # Add the length of the word to the end (penalized)
                    if bucket["end"] + time_to_add < final_bucket[idx+1]["begin"]:
                        bucket["end"] += time_to_add
    
                    word["added"] = True


                    break
                    
            elif word["begin"] > final_bucket[idx]["end"]:

                bucket["sentence"].append(word)
                word["added"] = True

                break


    print ("Discarded words (again):")
    print([frag if frag["added"] == False else "" for frag in fragments_list])



    subtitles = []

    line_index = 0
    line_start_sec = line_end_sec = float(final_bucket[0]['begin'])
    line_content = ""

    for idx, fragment in enumerate(final_bucket): 
        try:
            print ("Fragment is ", fragment)

            line_index += 1
            line_start = datetime.timedelta(0, fragment["begin"], 0)
            line_end = datetime.timedelta(0, fragment["end"], 0)
            line_content = " ".join([word["lines"][0] for word in fragment["sentence"]])
            if line_content[-1] != ".":
                line_content += "."

            subtitles.append(srt.Subtitle(
                index=line_index, 
                start=line_start, 
                end=line_end, 
                content=line_content, 
                proprietary=''
                )
            )

        except Exception as e:
            print ("Could not parse this into the subtitles. Reason:", str(e))
            
    parsed_subtitles = subtitles

    print (parsed_subtitles)
    for s in parsed_subtitles:
        print (s.content)

    final_srt = srt.compose(parsed_subtitles)

    print ("Final SRT is", final_srt)

    # transcription_srt_filepath = "./test-transcription.srt" 
    transcription_srt_filepath = args.metadata_path + "/transcription.srt" 
    
    text_file = open(transcription_srt_filepath, "w")
    n = text_file.write(final_srt)
    text_file.close()    
    
    return transcription_srt_filepath

# print (run("./align_output.json", None))
# print (run("./output_de.json", "./test-16khz.wav", None))
# print (find_silent_chunks("./test.wav"))
