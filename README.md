# AI-ExtractData-NuExtract-tiny
NuExtract-tiny GGUF for data extraction in json format


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

