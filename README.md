# Project U.S.A.G.I
**U**sually **S**kips **A**ll **G**iven **I**nstructions

This AI will be named Mocchan and will be based off a rabbit.

## Concept
The concept is quite simple. A virtual assistant is supposed to make our lives easier by helping us do tasks, usually through text or voice control. However, this virtual AI assistant is useless.

This also gives me an oppertunity to learn Python and AI Tech. So something comes out of it, I guess.

## Dependencies
- Python3
- Pip
- Ollama - For generative ai
- WhisperModel - For transcribing audio into text
- pyaudio - For inputing voice and saving it as a wav file to inject into WhisperModel
- TTS - For synthesizing and training voices for Text-to-Speech

This may sound like I'm stating water is wet, but you **need a mic** for this to work.

### Installing Dependencies
  ```
  python3 -m venv ~/.venv
  source ~/.venv/bin/activate
  sudo apt install portaudio19-dev -y
  sudo apt-get install espeak-ng -y
  pip install --upgrade pip setuptools wheel
  curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
  source "$HOME/.cargo/env"
  pip install sudachipy --no-build-isolation
  pip install numpy pyaudio ollama faster-whisper librosa setuptools_rust TTS torch ffmpeg pydub
  ```

```
  curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```
  This is for rust which is needed for sudachipy (a dependancy for TTS)

## Tasks
- ~~Audio from mic to wav~~
- ~~Whisper to transcribe text accurately (STT)~~ *
- ~~The generative AI to should respond to transcribed text~~ **
- Adding voice to Mocchan's speech. She says that she would have a voice of a pouty, lazy teen.
- Give Mocchan a face

* Currently using a Raspberry pi 5 to transcribe a tiny.en model. Hopefully I will get a NUC or something and run it on that to transcribe more accurately in the future.

** I'm running the LLM using Llama3.1, an 8b model to generate the text. It's the only model that performs well and is instant with the GPU I currently have.

**Long term goal**: I'd like to create a neuro network that runs on several servers. Deepseek for the logical side of the brain that handles math and analytical thinking while using Llama for the right side of the brain for conversational skills where most of her personality sits.

## Installation
This has been running on a raspbarry pi 5 for a bit. 

```
sudo apt-get update && sudo apt-get upgrade -y 
```