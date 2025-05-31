import chainlit as cl
import requests
import asyncio




BASE_URL = "https://crud-ai-agent.vercel.app/agent" 


@cl.on_chat_start
async def chat_start():
    if cl.user_session.get("messages") is None:
        cl.user_session.set("messages", [])
            
    if len(cl.user_session.get("messages")) > 0 :
        for doc in cl.user_session.get("messages"):
            await cl.Message(content=f"{doc['role']}: {doc['content']}").send()
    else:            
        await cl.Message(content="Hey, CrudMaster Here! How can I help u Today?").send()

@cl.on_message
async def on_user_message(message: cl.Message):
    message_history = cl.user_session.get("messages")

    msg = cl.Message(content="Working....")
    await msg.send()

    message_history.append({"role": "user", "content": message.content})

    try:
        response = requests.post(BASE_URL, json={"user_input" : str(message.content)})
        
        message_history.append({"role": "assistant", "content": response.json()})        
        if response.status_code == 200:
            
            await cl.Message(content=response.json()).send()
        else:
            raise Exception    
        
    except Exception as e:
        msg.content = f"Error: {str(e)}"
        await msg.update()
                
        
        
        
        
        
        

# have to handle the scenario, where it says got error but also updating the doc, 