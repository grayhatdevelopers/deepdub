
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
        print("\nfragments:\n", data['fragments'])

    subtitles = []

    line_index = 0
    line_start_sec = line_end_sec = float(data['fragments'][0]['begin'])
    line_content = ""

    for idx, fragment in enumerate(data['fragments']): 
        try:
            print ("Fragment is ", fragment)

            if float(fragment['begin']) - line_end_sec > 0:
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
                line_start_sec = float(fragment['begin'])
                line_content = ""
            line_end_sec = float(fragment['end'])
            if line_content != "":
                line_content += " "
            line_content += fragment['lines'][0]

        except Exception as e:
            print ("Could not parse this into the subtitles. Reason:", str(e))

    if len (subtitles) == 0:
        for idx, fragment in enumerate(data['fragments']): 
            try:
                print ("Fragment is ", fragment)

                if float(fragment['begin']) - line_end_sec >= 0:
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
                    line_start_sec = float(fragment['begin'])
                    line_content = ""
                line_end_sec = float(fragment['end'])
                if line_content != "":
                    line_content += " "
                line_content += fragment['lines'][0]

            except Exception as e:
                print ("Could not parse this into the subtitles. Reason:", str(e))    	

    parsed_subtitles = subtitles

    print (parsed_subtitles)
    for s in parsed_subtitles:
        print (s.content)

    final_srt = srt.compose(parsed_subtitles)

    print ("Final SRT is", final_srt)

    transcription_srt_filepath = args.metadata_path + "/transcription.srt" 
    
    text_file = open(transcription_srt_filepath, "w")
    n = text_file.write(final_srt)
    text_file.close()    
    

    return transcription_srt_filepath

# print (run("./align_output.json", None))
# print (run("./output.json", None))
# print (find_silent_chunks("./test.wav"))
