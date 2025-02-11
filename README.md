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

This may sound like I'm stating water is wet, but you **need a mic** for this to work.

### Installing Dependencies
  ```
  python3 -m venv ~/.venv
  source ~/.venv/bin/activate
  sudo apt install portaudio19-dev
  pip install numpy pyaudio ollama faster-whisper librosa
  ```

## Tasks
- Audio from mic to wav
- Whisper to transcribe text accurately (STT)
- The generative AI to should respond to transcribed text
- Adding voice to the generative AI's speech

**Long term goal**: I'd like to create a neuro network that runs on several servers. Deepseek for the logical side of the brain that handles math and analytical thinking while using Llama for the right side of the brain for conversational skills where most of her personality sits.

## Installation
This has been running on a raspbarry pi 5 for a bit. 

```
sudo apt-get update && sudo apt-get upgrade -y 
```