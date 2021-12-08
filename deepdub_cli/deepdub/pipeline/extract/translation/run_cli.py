from transformers import T5Tokenizer, T5ForConditionalGeneration 

tokenizer = T5Tokenizer.from_pretrained("t5-large")
model = T5ForConditionalGeneration.from_pretrained("t5-large")

def run (
    input_string,
    args,
):

    _prefix = "translate {} to {}: ".format("English", "German")

    input_ids = tokenizer(_prefix + input_string, return_tensors='pt').input_ids
    outputs = model.generate(input_ids)

    output_string = tokenizer.decode(outputs[0], skip_special_tokens=True)
    print(output_string)
    # Das Haus ist wunderbar.
    
    return output_string
