from openrouter import OpenRouter # Import Open Rouder
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs.play import play
import os

load_dotenv()

elevenlabs = ElevenLabs(
  api_key=os.getenv("ELEVENLABS_API_KEY"),
)

voice1 = "N2lVS1w4EtoT3dr4eOWO"
voice2 = "pNInz6obpgDQGcFmaJgB"
voice3 = "pFZP5JQG7iQjIQuC4Bku"

def say_eleven(text, voice):
    audio = elevenlabs.text_to_speech.convert(
        text=text,
        voice_id=voice,
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128",
    )
    play(audio)

client = OpenRouter(
    api_key=os.getenv("HackClubAI"),  # Key Goes Here
    server_url="https://ai.hackclub.com/proxy/v1",                                        # AI Server
)

msg = []                # This is where the history goes for the messages.
role = "You are all philosephers discussing the utmost imporant things. "  # This goes to all the AI's. Tell them what they are supposed to do, how they are to respond, etc.
def generate_content(model_name, name):
    return client.chat.send (
            model=model_name, 
            messages=[
                {"role": "system",               # This is how we can give it a custom role.
                    "content": (
                        f"You are {name}."             # Tells it its name. This doesn't have to be anything specific.
                        f"{role}"                   # Role defined above.
                        f"Previous messages: {msg}" # History 
                    )
                },
                {"role": "user", "content": "respond like a human would"}  # Here it says "go" because then we aren't giving it a specific instruction, so it will do what it wants.
            ],
            stream=False,
    )
    

while True:
            # Sometimes one of the AI's have an issue. 
    # GROK: 
    response = generate_content("x-ai/grok-4.1-fast", "Grok")
    response =response.choices[0].message.content# This is the result
    print(f"\033[32mGrok: {response}\033[0m\n")    # I put color here so each AI has its own color
    msg.append(f"Grok: {response}")
    say_eleven(response, voice2)



    # GEMINI:
    response = generate_content("google/gemini-2.5-flash", "Gemini")
    response =response.choices[0].message.content
    
    print(f"\033[31mGemini: {response}\033[0m\n")
    msg.append(f"Gemini: {response}")
    say_eleven(response, voice3)
    # OpenAI:
    response = generate_content("openai/gpt-5-mini", "OpenAI")
    response = response.choices[0].message.content
    print(f"\033[34mChatGPT: {response}\033[0m\n")
    msg.append(f"ChatGPT: {response}")
    say_eleven(response, voice1)
