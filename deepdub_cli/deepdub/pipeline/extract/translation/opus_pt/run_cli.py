from transformers import AutoTokenizer, AutoModelForSeq2SeqLM



opus_supported_languages = {
	"German,English": "Helsinki-NLP/opus-mt-de-en",
	"Hindi,English": "Helsinki-NLP/opus-mt-hi-en",
    "Urdu,English": "Helsinki-NLP/opus-mt-ur-en",
    "Chinese,English": "Helsinki-NLP/opus-mt-zh-en",
}


# input_string = "RZEHNTICH BIN ÜBERZEUGT WIR HABEN GUTE GRÜNDE ZUVERSICHTLICH ZU SEIN DASS DIE IN WENIGEN STUNDEN BEGINNENDEN ZWANZIGER JAHRE DES EINUNDZWANZIGSTEN JAHRHUNDERTS GUTE JAHRE WERDEN KÖNNEN WENN WIR UNSERE STÄRKEN NUTZEN WENN WIR AUFT DAS SETZEN WAS UNS VERBINDET WENN WIR UNS DARAN ERINNERN WAS WIR IN DEN LETZTEN JAHRZEHNTEN GEMEINSAM ERREICHT HABENIM NÄCHSTEN JAHR WIRD DEUTSCHLAND SEIT DREISSIG JAHREN IN FRIEDEN UND FREIHEIT WIEDERVEREINT SEIN IN DIESEN DREISSIG JAHREN HABEN WIR GROSSARTIGES GESCHAFFT SO HATTEN ZUM BEISPIEL NOCH NIE SO VIELE MENSCHEN ARBEIT WIE HEUTE DENNOCH BLEIBT AUCH IM NÄCHSTEN JAHRZEHNTEN NOCH MEHR ZU TUN ALS WIR VOR DREISSIG JAHREN GEDACHT HABEN"



import srt

def run (
    subs_path,
    args,
):
    model_name = opus_supported_languages[','.join([
    args.translation_language_source, 
    args.translation_language_target
    ])]

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)


    subs = list(srt.parse(open(subs_path)))

    for s in subs:    
        input_string = s.content
	    
        input_ids = tokenizer(input_string, return_tensors='pt').input_ids
        outputs = model.generate(input_ids)

        output_string = tokenizer.decode(outputs[0], skip_special_tokens=True)

        print(input_string, "   --->   ", output_string)
        # Das Haus ist wunderbar.

        s.content = output_string
	    
    final_srt = srt.compose(list(subs))
    
    translation_srt_filepath = args.metadata_path + "/translation_sentences.srt" 
    
    text_file = open(translation_srt_filepath, "w")
    n = text_file.write(final_srt)
    text_file.close()  
    
    return translation_srt_filepath
