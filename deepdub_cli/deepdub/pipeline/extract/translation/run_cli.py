from transformers import T5Tokenizer, T5ForConditionalGeneration 

tokenizer = T5Tokenizer.from_pretrained("t5-large")
model = T5ForConditionalGeneration.from_pretrained("t5-large")

import srt

def run (
    subs_path,
    args,
):

    subs = list(srt.parse(open(subs_path)))

    _prefix = "translate {} to {}: ".format(args.translation_language_source, args.translation_language_target)

    for s in subs:    
        input_string = s.content
	    
        input_ids = tokenizer(_prefix + input_string, return_tensors='pt').input_ids
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


#run("", None)
