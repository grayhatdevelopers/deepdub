
import srt
from time import strftime
from time import gmtime

# importing the module
import json

import datetime

def run (alignments_path, args):

    # Opening JSON file
    with open(alignments_path) as json_file:
        data = json.load(json_file)

        # Print the type of data variable
        print("Type:", type(data))

        print ("All Data: ", data)

        # Print the data of dictionary
        print("\nfragments:\n", data['words'])

    subtitles = []

    line_index = 0
    line_start_sec = line_end_sec = data['words'][0]['start']
    line_content = ""

    for idx, fragment in enumerate(data['words']): 
        try:
            print ("Fragment is ", fragment)

            if fragment['start'] - line_end_sec > 0.5:

                line_index += 1
                line_start = datetime.timedelta(0, line_start_sec, 0)
                line_end = datetime.timedelta(0, line_end_sec, 0)
                subtitles.append(srt.Subtitle(
                    index=line_index, 
                    start=line_start, 
                    end=line_end, 
                    content=line_content, 
                    proprietary=''
                    )
                )
                line_start_sec = fragment['start']
                line_content = ""
            line_end_sec = fragment['end']
            if line_content != "":
                line_content += " "
            line_content += fragment['alignedWord']

        except Exception as e:
            print ("Could not parse this into the subtitles. Reason:", str(e))


    parsed_subtitles = subtitles

    print (parsed_subtitles)
    for s in parsed_subtitles:
        print (s.content)

    final_srt = srt.compose(parsed_subtitles)

    transcription_srt_filepath = "transcription_sentences.srt" 
    
    text_file = open(transcription_srt_filepath, "w")
    n = text_file.write(final_srt)
    text_file.close()    
    

    return transcription_srt_filepath

print (run("./align_output.json", None))

# print (find_silent_chunks("./test.wav"))
