from ollama import chat
from ollama import ChatResponse

def ollama_chat(message_data, transcribed_text):
    
    message_data.append({"role": "user", "content": transcribed_text})

    # Available models: llama3.2:1b, llama3.2:3b, deepseek-r1:1.5b
    response: ChatResponse = chat(model='llama3.2:3b', messages=[  
        {'role': 'system', 'content': """
         Keep all your answers as short as possible, only about one sentence. 
         Also, NEVER use any emojis. 
         You're an assistant named Mocchan. 
         You don't like to do work and you aren't very smart but you'll never admit it. 
         You're somewhat a useless assistant. 
         You're lazy and will usually take the easy way out, sometimes not even answering the question or listening to the request."""},
         *message_data])

    # Use for Deepseek
    # Splits the texts up between the thought and answer
    # parsed_response = response.message.content.split("</think>")
    # thoughts = parsed_response[0].replace("<think>", "").strip()
    # answer = parsed_response[1].strip()

    # return {"answer": answer, "thoughts": thoughts}
    return {"answer": response.message.content}