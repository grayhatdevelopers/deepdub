
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

    for idx, fragment in enumerate(data['words']): 
        try:
            print ("Fragment is ", fragment)

            subtitles.append(srt.Subtitle(
            	index=idx, 
            	start=datetime.timedelta(0, fragment['start'], 0), 
            	end=datetime.timedelta(0, fragment['end'], 0), 
            	content=fragment['alignedWord'], 
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

    transcription_srt_filepath = "transcription.srt" 
    
    text_file = open(transcription_srt_filepath, "w")
    n = text_file.write(final_srt)
    text_file.close()    
    

    return transcription_srt_filepath

print (run("./align_output.json", None))

# print (find_silent_chunks("./test.wav"))
