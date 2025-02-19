# Project U.S.A.G.I

![screenshot](./images/project_usagi.png)

**U**sually **S**kips **A**ll **G**iven **I**nstructions

This AI will be named Mocchan and will be based off a rabbit.

## Concept
The concept is quite simple. A virtual assistant is supposed to make our lives easier by helping us do tasks, usually through text or voice control. However, this virtual AI assistant is useless and not very nice.

This also gives me an oppertunity to learn Python and AI Tech. So something comes out of it, I guess.

## Dependencies

### Main
- Python3
- Pip

### Ears
- **pyaudio** - For inputing voice and saving it as a wav file to inject into WhisperModel.
- **WhisperModel** - using faster-whisper for transcribing audio into text

**Note**: This may sound like I'm stating water is wet, but you **need a mic** for this to work. I'm currently using a Raspi 5 to transcribe a tiny.en model. Hopefully I will get a NUC or something and run it on that to transcribe faster and more accurately in the future. The current transcribe time is about 2-3 seconds. Lets get it down to 1! This pyaudio and and faster whisper

### Brain
- **Ollama** - For generative ai (llama3.1)

**Note**: Depending on what you need, you can use Llama, Minstrel, or Deepseek. Deepseek has less personality than the other models, but I'm currently using llama3.1 (8b) due to hardware constraints. I'm currently using a 4080 for a conversational ai, instant results is crucial. Hopefully, I can get my hands on a 4090 and try the llama3.3 (70b) in the future. (Or an a100. Let me dream.)

## Mouth
These are the current TTS generators that I'm testing. Mocchan says that she would have a voice of a pouty, lazy teen. I have to listen to her.

**E2/F5 TTS**

**Note**: This is the best model i could find. The quality is amazing but it's not super quick. I feel that it's loading the model twice, so that could be a factor. So far it takes 5-6 seconds to produce audio from speaking into the mic to outputing the audio. I've managed to change her voice to a young female voice and she no longer sounds like a 54 year old man who is happily divorced and on his sailboat.

Stupid cheap USB speaker I bought has no volume control. used this command to turn down the volume on the raspberry pi 5:

```
amixer -c 3 set 'PCM' 70%
```

## Installing Dependencies
### Setup for raspi 5
  ```
  sudo apt-get update && sudo apt-get upgrade -y 
  python3 -m venv ~/.venv
  source ~/.venv/bin/activate
  sudo apt install portaudio19-dev -y
  sudo apt-get install espeak-ng -y
  pip install --upgrade pip setuptools wheel
  curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
  source "$HOME/.cargo/env"
  pip install sudachipy --no-build-isolation
  pip install numpy pyaudio ollama faster-whisper librosa setuptools_rust TTS torch ffmpeg pydub python-dotenv
  ```
  #### Notes
  ```
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
  ```
  This is for rust which is needed for sudachipy (a dependancy for TTS)

### Setup for brain (Machine running ollama LLM)
  I'm working in linux. Sorry Windows and Mac people, you can install it by going to the documentation: [Ollama](https://github.com/ollama/ollama?tab=readme-ov-file#ollama) 

  **Installation for Linux**
  ```
  sudo apt-get update && sudo apt-get upgrade -y
  sudo apt-get install curl
  curl -fsSL https://ollama.com/install.sh | sh
  ```

  **Pulling model**
  Change the model if you want

  ```
  ollama pull llama3.1
  ```

  **Serving ollama**
  Default port it 11434

  ```
  ollama serve
  ```

## To-Dos/Goals
- ~~Audio from mic to wav~~
- ~~Whisper to transcribe text accurately (STT)~~
- ~~The generative AI to should respond to transcribed text~~ **
- Adding voice to Mocchan's speech.
- Give Mocchan a face

**Long term goal**: I'd like to create a neuro network that runs on several servers. Deepseek for the logical side of the brain that handles math and analytical thinking while using Llama for the right side of the brain for conversational skills where most of her personality sits.
