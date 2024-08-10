import streamlit as st
from llama_cpp import Llama
import warnings
warnings.filterwarnings(action='ignore')
import datetime
import random
import string
from time import sleep
import tiktoken
import json

# for counting the tokens in the prompt and in the result
#context_count = len(encoding.encode(yourtext))
encoding = tiktoken.get_encoding("r50k_base") 

nCTX = 12000
sTOPS = ['<|end-output|>']
modelname = "NuExtract-tiny"
# Set the webpage title
st.set_page_config(
    page_title=f"Your LocalGPT ✨ with {modelname}",
    page_icon="🌟",
    layout="wide")

if "hf_model" not in st.session_state:
    st.session_state.hf_model = "NuExtract-tiny"
# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

if "repeat" not in st.session_state:
    st.session_state.repeat = 1.35

if "temperature" not in st.session_state:
    st.session_state.temperature = 0.1

if "maxlength" not in st.session_state:
    st.session_state.maxlength = 500

if "speed" not in st.session_state:
    st.session_state.speed = 0.0

def writehistory(filename,text):
    with open(filename, 'a', encoding='utf-8') as f:
        f.write(text)
        f.write('\n')
    f.close()

def genRANstring(n):
    """
    n = int number of char to randomize
    """
    N = n
    res = ''.join(random.choices(string.ascii_uppercase +
                                string.digits, k=N))
    return res

@st.cache_resource 
def create_chat():   
# Set HF API token  and HF repo
    from llama_cpp import Llama
    client = Llama(
                model_path='model/NuExtract-tiny.gguf',
                temperature=0.24,
                n_ctx=nCTX,
                max_tokens=600,
                repeat_penalty=1.176,
                stop=sTOPS,
                verbose=False,
                )
    print('loading NuExtract-tiny.gguf with LlamaCPP...')
    return client


# create THE SESSIoN STATES
if "logfilename" not in st.session_state:
## Logger file
    logfile = f'{genRANstring(5)}_log.txt'
    st.session_state.logfilename = logfile
    #Write in the history the first 2 sessions
    writehistory(st.session_state.logfilename,f'{str(datetime.datetime.now())}\n\nYour own LocalGPT with 🌀 {modelname}\n---\n🧠🫡: You are a helpful assistant.')    
    writehistory(st.session_state.logfilename,f'🌀: How may I help you today?')



### START STREAMLIT UI
# Create a header element
st.image('images/banner.png',use_column_width=True)
mytitle = f'> *Extract data with {modelname} into `JSON` format*'
st.markdown(mytitle, unsafe_allow_html=True)
#st.markdown('> Local Chat ')
#st.markdown('---')

# CREATE THE SIDEBAR
with st.sidebar:
    st.image('images/logo.png', use_column_width=True)
    st.session_state.temperature = st.slider('Temperature:', min_value=0.0, max_value=1.0, value=0.1, step=0.01)
    st.session_state.maxlength = st.slider('Length reply:', min_value=150, max_value=2000, 
                                           value=500, step=50)
    st.session_state.repeat = st.slider('Repeat Penalty:', min_value=0.0, max_value=2.0, value=1.11, step=0.02)
    st.markdown(f"**Logfile**: {st.session_state.logfilename}")
    statspeed = st.markdown(f'💫 speed: {st.session_state.speed}  t/s')
    btnClear = st.button("Clear History",type="primary", use_container_width=True)

llm = create_chat()

st.session_state.jsonformat = st.text_area('JSON Schema to be applied', value="", height=150,  
                     placeholder='here your schema', disabled=False, label_visibility="visible")
st.session_state.origintext = st.text_area('Source Document', value="", height=150,  
                     placeholder='here your text', disabled=False, label_visibility="visible")
extract_btn = st.button("Extract Data",type="primary", use_container_width=False)
st.markdown('---')
st.session_state.extractedJSON = st.empty()
st.session_state.onlyJSON = st.empty()



if extract_btn:
        prompt = f"""<|input|>\n### Template:
{st.session_state.jsonformat}

### Text:
{st.session_state.origintext}
<|output|>
"""
        print(prompt)
        with st.spinner("Thinking..."):
            start =  datetime.datetime.now()
            output = llm.create_completion(
                            prompt =prompt,
                            temperature=0.1,
                            repeat_penalty= 1.11,
                            stop=sTOPS,
                            max_tokens=500,              
                            stream=False)

        delta = datetime.datetime.now() -start
        result = output['choices'][0]['text']
        st.write(result)
        adapter = result.replace("'",'"')
        final = json.loads(adapter) 
        totalTokens = len(encoding.encode(prompt))+len(encoding.encode(result))
        totalseconds = delta.total_seconds()
        st.session_state.speed = totalTokens/totalseconds
        statspeed.markdown(f'💫 speed: {st.session_state.speed:.2f}  t/s')
        totalstring = f"""GENERATED STRING

{result}
---

Generated in {delta}

---

JSON FORMAT:
"""   
        with st.session_state.extractedJSON:
            st.markdown(totalstring)
        st.session_state.onlyJSON.json(final)    
        writehistory(st.session_state.logfilename,f'✨: {prompt}')
        writehistory(st.session_state.logfilename,f'🌀: {result}')
        writehistory(st.session_state.logfilename,f'---\n\n')

