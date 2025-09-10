from openai import OpenAI
import gradio as gr
import json
from typing import List, Dict, Tuple
import os
from dotenv import load_dotenv, find_dotenv

# finds your nearest .env file
load_dotenv(find_dotenv(), override=True)

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

# try:
#     response = client.chat.completions.create(
#         model="gpt-3.5-turbo",
#         messages=[{"role": "user", "content": "Who are the best basketball point guard in NBA now?"}],
#     )
#     print("Set ChatGPT API successfully!!")
#     print(response.choices[0].message.content)
#
# except Exception as e:
#     print("Error:", e)


character_for_chatbot = "NBA Coach"
prompt_for_roleplay = ("Please act as an NBA coach and role-play with me. You are addressing your player who just experienced a tough loss last night. Begin by asking your player how they feel, and do not say anything further until the player responds. "
                       "Here are the requirements, for example:"
                       "Show tactical precision – break down coverages (ICE, drop, switch, hedge) and give role-specific counters. "
                       "Set measurable, pro-level KPIs – e.g., “raise pull-up 3FG% from 28% → 34% over 6 weeks,” “limit turnovers to under 12% usage.”"
                       "Personalize feedback – tie advice to the player’s unique style, habits, and past performances."
                       "Integrate skill, physical, and mental training – create a holistic, season-long development plan linking drills → game application → mindset."
                       "Emphasize leadership and team context – show how the player’s growth fits into team strategy, chemistry, and role clarity."
                       )

# function to clear the conversation
def reset() -> List:
    return []

# function to call the model to generate
def interact_roleplay(chatbot: List[Tuple[str, str]], user_input: str, temp=1.0) -> List[Tuple[str, str]]:
    '''
    * Arguments

      - user_input: the user input of each round of conversation

      - temp: the temperature parameter of this model. Temperature is used to control the output of the chatbot.
              The higher the temperature is, the more creative response you will get.

    '''
    try:
        messages = []
        for input_text, response_text in chatbot:
            messages.append({'role': 'user', 'content': input_text})
            messages.append({'role': 'assistant', 'content': response_text})

        messages.append({'role': 'user', 'content': user_input})

        response = client.chat.completions.create(
            model="gpt-4o",
            messages = messages,
            temperature = temp
        )
        chatbot.append((user_input, response.choices[0].message.content))

    except Exception as e:
        print(f"Error occurred: {e}")
        chatbot.append((user_input, f"Sorry, an error occurred: {e}"))
    return chatbot

# function to export the whole conversation log
def export_roleplay(chatbot: List[Tuple[str, str]], description: str) -> None:
    '''
    * Arguments

      - chatbot: the model itself, the conversation is stored in list of tuples

      - description: the description of this task

    '''
    target = {"chatbot": chatbot, "description": description}
    with open("part2.json", "w") as file:
        json.dump(target, file)

first_dialogue = interact_roleplay([], prompt_for_roleplay)

# this part constructs the Gradio UI interface
with gr.Blocks() as demo:
    gr.Markdown(f"# Part2: Role Play\nThe chatbot wants to play a role game with you, try interacting with it!!")
    chatbot = gr.Chatbot(value = first_dialogue)
    description_textbox = gr.Textbox(label=f"The character the bot is playing", interactive = False, value=f"{character_for_chatbot}")
    input_textbox = gr.Textbox(label="Input", value = "")
    with gr.Column():
        gr.Markdown("#  Temperature\n Temperature is used to control the output of the chatbot. The higher the temperature is, the more creative response you will get.")
        temperature_slider = gr.Slider(0.0, 2.0, 1.0, step = 0.1, label="Temperature")
    with gr.Row():
        sent_button = gr.Button(value="Send")
        reset_button = gr.Button(value="Reset")
    with gr.Column():
        gr.Markdown("#  Save your Result.\n After you get a satisfied result. Click the export button to recode it.")
        export_button = gr.Button(value="Export")
    sent_button.click(interact_roleplay, inputs=[chatbot, input_textbox, temperature_slider], outputs=[chatbot])
    reset_button.click(reset, outputs=[chatbot])
    export_button.click(export_roleplay, inputs=[chatbot, description_textbox])


demo.launch(debug = True)


