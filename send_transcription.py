import requests
import os
from play_audio import play
from dotenv import load_dotenv
load_dotenv()

endpoint = os.getenv('API_ENDPOINT')
server_ip = os.getenv('SERVER_IP')
port = os.getenv('SERVER_PORT')

url = f"http://{server_ip}:{port}{endpoint}"

def send_transcription(text):
    output_dir = "./output"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "output.wav")
    
    print(f"Client ready to write to: {os.path.abspath(output_path)}")

    if os.path.exists("./output/output.wav"):
      # Removes audio file
      os.remove("./output/output.wav")

    try:
        print("Sending request to server...")
        response = requests.post(
            url,
            json={'text': text}
        )

        # Check for HTTP errors first
        response.raise_for_status()

        # Get filename from headers or use default
        content_disp = response.headers.get('Content-Disposition', '')
        filename = 'output.wav'  # Default name
        
        if 'filename=' in content_disp:
            filename = content_disp.split('filename=')[-1].strip('"')
        
        # Build full save path
        save_path = os.path.join('./output', filename)

        # Save the binary content
        with open(save_path, 'wb') as f:
            f.write(response.content)
        
        play("./output/output.wav", device_index=1)
        print(save_path)
        return True
    except Exception as e:
        print(f"Error details: {str(e)}")
        return False