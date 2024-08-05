
# https://huggingface.co/learn/cookbook/en/information_extraction_haystack_nuextract
# https://llama-cpp-python.readthedocs.io/en/stable/api-reference/#llama_cpp.Llama.create_completion
# https://numind.ai/blog/nuextract-a-foundation-model-for-structured-extraction
# https://huggingface.co/numind/NuExtract-tiny
# GGUF repo https://huggingface.co/Felladrin/gguf-NuExtract-tiny
# https://www.geeksforgeeks.org/json-loads-in-python/

import json
from llama_cpp import Llama
from rich.markdown import Markdown
import warnings
warnings.filterwarnings(action='ignore')
import datetime
from rich.console import Console
console = Console(width=90)

print('loading NuExtract-tiny.gguf with LlamaCPP...')
nCTX = 12000
sTOPS = ['<|end-output|>']
client = Llama(
            model_path='model/NuExtract-tiny.gguf',
            #n_gpu_layers=0,
            temperature=0.24,
            n_ctx=nCTX,
            max_tokens=600,
            repeat_penalty=1.176,
            stop=sTOPS,
            verbose=False,
            )
print('Done...')

prompt = """<|input|>\n### Template:
{
    "Car": {
        "Name": "",
        "Manufacturer": "",
        "Designers": [],
        "Number of units produced": "",
    }
}
### Text:
The Fiat Panda is a city car manufactured and marketed by Fiat since 1980, currently in its third generation. The first generation Panda, introduced in 1980, was a two-box, three-door hatchback designed by Giorgetto Giugiaro and Aldo Mantovani of Italdesign and was manufactured through 2003 — receiving an all-wheel drive variant in 1983. SEAT of Spain marketed a variation of the first generation Panda under license to Fiat, initially as the Panda and subsequently as the Marbella (1986–1998).

The second-generation Panda, launched in 2003 as a 5-door hatchback, was designed by Giuliano Biasio of Bertone, and won the European Car of the Year in 2004. The third-generation Panda debuted at the Frankfurt Motor Show in September 2011, was designed at Fiat Centro Stilo under the direction of Roberto Giolito and remains in production in Italy at Pomigliano d'Arco.[1] The fourth-generation Panda is marketed as Grande Panda, to differentiate it with the third-generation that is sold alongside it. Developed under Stellantis, the Grande Panda is produced in Serbia.

In 40 years, Panda production has reached over 7.8 million,[2] of those, approximately 4.5 million were the first generation.[3] In early 2020, its 23-year production was counted as the twenty-ninth most long-lived single generation car in history by Autocar.[4] During its initial design phase, Italdesign referred to the car as il Zero. Fiat later proposed the name Rustica. Ultimately, the Panda was named after Empanda, the Roman goddess and patroness of travelers.
<|output|>
"""

nCTX = 12000
sTOPS = ['<|end-output|>']

start =  datetime.datetime.now()


output = client.create_completion(
                prompt =prompt,
                temperature=0.1,
                repeat_penalty= 1.11,
                stop=sTOPS,
                max_tokens=500,              
                stream=False)
delta = datetime.datetime.now() - start
result = output['choices'][0]['text']
console.print(result)
console.print('---')
console.print(f'Completed in {delta}')

replies = [result]
import json
from haystack.components.converters import OutputAdapter


adapter = result.replace("'",'"')
final = json.loads(adapter)
console.print('---')
console.print(final)