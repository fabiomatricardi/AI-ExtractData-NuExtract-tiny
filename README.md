# AI-ExtractData-NuExtract-tiny
NuExtract-tiny GGUF for data extraction in json format

### How to go from this to this

##### JSON schema template:
```
{
    "Car": {
        "Name": "",
        "Manufacturer": "",
        "Designers": [],
        "Number of units produced": "",
    }
}
```
##### original text
```
The Fiat Panda is a city car manufactured and marketed by Fiat since 1980, currently in its third generation. The first generation Panda,
introduced in 1980, was a two-box, three-door hatchback designed by Giorgetto Giugiaro and Aldo Mantovani of Italdesign and was manufactured
through 2003 — receiving an all-wheel drive variant in 1983. SEAT of Spain marketed a variation of the first generation Panda under license
to Fiat, initially as the Panda and subsequently as the Marbella (1986–1998).

The second-generation Panda, launched in 2003 as a 5-door hatchback, was designed by Giuliano Biasio of Bertone, and won the European Car
of the Year in 2004. The third-generation Panda debuted at the Frankfurt Motor Show in September 2011, was designed at Fiat Centro Stilo under
the direction of Roberto Giolito and remains in production in Italy at Pomigliano d'Arco.[1] The fourth-generation Panda is marketed as Grande
Panda, to differentiate it with the third-generation that is sold alongside it. Developed under Stellantis, the Grande Panda is produced in Serbia.

In 40 years, Panda production has reached over 7.8 million,[2] of those, approximately 4.5 million were the first generation.[3] In early
2020, its 23-year production was counted as the twenty-ninth most long-lived single generation car in history by Autocar.[4]
During its initial design phase, Italdesign referred to the car as il Zero. Fiat later proposed the name Rustica. Ultimately,
the Panda was named after Empanda, the Roman goddess and patroness of travelers.

```

##### extracted JSON:
```
{
    'Car': {
        'Name': 'Fiat Panda',
        'Manufacturer': 'Fiat',
        'Designers': ['Giorgetto Giugiaro', 'Aldo Mantovani'],
        'Number of units produced': '7.8 million'
    }
}
```

### Create venv and install packages
```
python -m venv venv
venv\Scripts\activate

pip install llama-cpp-python==0.2.85 tiktoken streamlit==1.36.0
```

### download he GGUF file
download from HugginFace into `model` subfolder file NuExtract-tiny.gguf (fp16 quantization)

```
GGUF repo [https://huggingface.co/Felladrin/gguf-NuExtract-tiny](https://huggingface.co/Felladrin/gguf-NuExtract-tiny)
```

Original model card: https://huggingface.co/numind/NuExtract-tiny
```
NuExtract_tiny is a version of Qwen1.5-0.5, fine-tuned on a private high-quality synthetic dataset for information extraction. To use the model, provide an input text (less than 2000 tokens) and a JSON template describing the information you need to extract.

Note: This model is purely extractive, so all text output by the model is present as is in the original text. You can also provide an example of output formatting to help the model understand your task more precisely.

Note: While this model provides good 0 shot performance, it is intended to be fine-tuned on a specific task (>=30 examples).
```

Run everything with
```
python singleExtract.py
```

### Hyperparameters
```
temperature=0.1,
repeat_penalty= 1.11,
stop=['<|end-output|>'],
```



### Additional resources
```
# https://huggingface.co/learn/cookbook/en/information_extraction_haystack_nuextract
# https://llama-cpp-python.readthedocs.io/en/stable/api-reference/#llama_cpp.Llama.create_completion
# https://numind.ai/blog/nuextract-a-foundation-model-for-structured-extraction
# https://huggingface.co/numind/NuExtract-tiny
# GGUF repo https://huggingface.co/Felladrin/gguf-NuExtract-tiny
# https://www.geeksforgeeks.org/json-loads-in-python/
```



