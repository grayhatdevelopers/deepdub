import soundfile
from espnet_model_zoo.downloader import ModelDownloader
from espnet2.bin.asr_align import CTCSegmentation
d = ModelDownloader(cachedir="./modelcache")
wsjmodel = d.download_and_unpack("kamo-naoyuki/wsj")
speech, rate = soundfile.read("./test.wav")
aligner = CTCSegmentation( **wsjmodel , kaldi_style_text=False )
#text = ["THE SALE OF THE HOTELS",
 #       "IS PART OF HOLIDAY'S STRATEGY",
  #      "TO SELL OFF ASSETS",
   #     "AND CONCENTRATE ON PROPERTY MANAGEMENT"]

filename = "./sample_output.txt"

with open(filename) as file:
    lines = file.readlines()
    lines = [line.rstrip() for line in lines]

text = lines

segments = aligner(speech, text)
print(segments)
# utt_0000 utt 0.26 1.73 -0.0154 THE SALE OF THE HOTELS
# utt_0001 utt 1.73 3.19 -0.7674 IS PART OF HOLIDAY'S STRATEGY
# utt_0002 utt 3.19 4.20 -0.7433 TO SELL OFF ASSETS
# utt_0003 utt 4.20 6.02 -0.9003 AND CONCENTRATE ON PROPERTY MANAGEMENTimport soundfile
from espnet_model_zoo.downloader import ModelDownloader
from espnet2.bin.asr_align import CTCSegmentation
d = ModelDownloader(cachedir="./modelcache")
wsjmodel = d.download_and_unpack("kamo-naoyuki/wsj")
speech, rate = soundfile.read("./test.wav")
aligner = CTCSegmentation( **wsjmodel , kaldi_style_text=False )
#text = ["THE SALE OF THE HOTELS",
 #       "IS PART OF HOLIDAY'S STRATEGY",
  #      "TO SELL OFF ASSETS",
   #     "AND CONCENTRATE ON PROPERTY MANAGEMENT"]

filename = "./sample_output.txt"

with open(filename) as file:
    lines = file.readlines()
    lines = [line.rstrip() for line in lines]

text = lines

segments = aligner(speech, text)
print(segments)
# utt_0000 utt 0.26 1.73 -0.0154 THE SALE OF THE HOTELS
# utt_0001 utt 1.73 3.19 -0.7674 IS PART OF HOLIDAY'S STRATEGY
# utt_0002 utt 3.19 4.20 -0.7433 TO SELL OFF ASSETS
# utt_0003 utt 4.20 6.02 -0.9003 AND CONCENTRATE ON PROPERTY MANAGEMENT
