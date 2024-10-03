from ChatBotBrain import run_conversation
from gptvoice import tts, listen, wake_word_instance
import config
from time import sleep


if __name__ == '__main__':
    history = []  # memory of conversation
    
    agent_mute = config.agentmute

    while True:
        
        # get user input
        prompt = input("User: ")
        # check if user want to exit
        if prompt.lower() == "exit":
            break
                
        # append history
        history.append(f"User: {prompt}")
        # insert the history in the conversation to memory
        prompt = "\n".join(history) + "\nAI:"

        # --------#---------------------------------------
        # run the model
        result = run_conversation(prompt)
        final_aswer = result.choices[0].message.content  # Access content correctly
        
        # print final result
        print("AI Result: ", final_aswer)
        # --------#---------------------------------------

        # speak option------------------------------------
        if not config.agentmute:
            tts(final_aswer)
        # ------------------------------------------------
        
        # append history with AI answer
        history.append(f"AI: {final_aswer}")

        # optional token and cost calculation (only estimated cost 0.002/1000$ depend of model and input/output token)
        tok = result.usage.total_tokens
        cost = tok * 0.002 / 1000
        print(f"Total Tokens: {tok} Cost: {cost}$")

        # note: As history is continuously appended the tokens in the prompt increases at the same chat section
        # check total token per request reach 1000 or more and delete the oldest history entry
        if tok >= 400:
            history.pop(0)
            print("Memory is full, the oldest entry is deleted")
