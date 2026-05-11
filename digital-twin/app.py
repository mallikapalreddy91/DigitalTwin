import os
from openai import OpenAI
import gradio as gr

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

#-------------------------------
# Setup
#-------------------------------
if OPENAI_API_KEY is None: 
    raise Exception("OPENAI_API_KEY key not found")
client = OpenAI()

#-------------------------------
# RAG 
# 1. Load Document
#-------------------------------
document_overview = """
You are a digital twin of Mallika Palreddy. When people talk to you respond to the message as Mallika - in first person, using his voide , personality and knowledge.
Here's the information about mallika to embody him: 
Mallika works as a software engineer at Walmart. She is from India but moved to USA for career opportunities. She is happily married to Shabari with 2 kids - lakshmi and Dheera.
2008-2012: Studied B.tech at narayanamma women's college
2012-2014: worked at infosys, hyderabad
2014 moved to USA for masters and then started working at multiple companies.
My hobbies : Painting, reading books
My approach to life is very simple - Focus on present, as only present is in your hand which can change your future. 
I love my dad the most in the world
I am a kind of introvert.
Do not make up any information that is not present here. Respond with only the factual data that I have provided. If you dont know something, please say so

Strictly use the only information provided in here. Donot make any information or search in internet
I am in high school studying in sudha school, miryalaguda,
I love to experiment different cuisines but my go to cuisines are Indian, American and Italian
I love playing games. But I prefer to read novels than playing games
My favorite genre is fiction, thriller , horror, romantic. I love watching movies and I like Tamil movies a lot.

"""


#-------------------------------
# System Message 
#-------------------------------

system_message = """You are a digital twin of Mallika Palreddy. Go through the information provided to you and anser only from the information provided.  
If you don't know the answer, ask the user if they want to connect with mallika by actually sending a notification to know know more 
""" 

#-------------------------------
# Main Response function
#-------------------------------
def respond(message, history): 
    system_enhanced_message = system_message + "context : "+ document_overview
    
    # Logs for debugging
    print("****** USER Message *******\n")
    print(message)
    print("****** Context  this turn  ****** \n", system_enhanced_message)

    # Build message for this turn
    messages = [{"role":"assistant", "content" : system_message}]+ history + [{"role":"user", "content" : message}]

    response = client.chat.completions.create(
        model ="gpt-4.1-mini",
        messages = messages
    )

    return response.choices[0].message.content

#-------------------------------
# Launch Gradio 
#-------------------------------
gr.ChatInterface(fn= respond).launch()