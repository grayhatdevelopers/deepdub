
import srt

# importing the module
import json


def run (alignments_path, args):

    # Opening JSON file
    with open(alignments_path) as json_file:
        data = json.load(json_file)

        # Print the type of data variable
        print("Type:", type(data))

        print ("All Data: ", data)

        # Print the data of dictionary
        print("\nfragments:\n", data['fragments'])

    subtitles = ""

    for idx, fragment in enumerate(data['fragments']): 
        subtitles += '''{}
{},200 --> {},300
{}
'''.format(idx+1, fragment['begin'], fragment['end'], fragment['lines'])

    parsed_subtitles = srt.parse(subtitles)

    print (parsed_subtitles)
    for s in parsed_subtitles:
        print (s.content)

    return None

print (run("./output.json", None))