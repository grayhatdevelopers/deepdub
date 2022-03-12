import paddle 
from paddlespeech.cli import TextExecutor

def run(
    input_raw_transcription,
    args,
):

    print("************************ Printing input raw transcriptions ************************")
    print(input_raw_transcription)   
    
    text_executor = TextExecutor()       
    result = text_executor(
                        # insert raw transcription in text
                        text=str(input_raw_transcription), 
                        task='punc',
                        # use args passed to modify parameters below 
                        model='ernie_linear_p7_wudao',
                        lang='zh',
                        config=None,
                        ckpt_path=None,
                        punc_vocab=None,
                        device=paddle.get_device())

    print('Text Result: \n{}'.format(result))

    return result