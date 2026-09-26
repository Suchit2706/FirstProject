import os
import json
from openai import OpenAI
from agent_tools.tools_list import get_tools_list, get_functions_dict

# Set your API key (recommend: use environment variable)
client = OpenAI(
    api_key="ollama",
    base_url="http://localhost:11434/v1"
)


messages = [
    {"role": "system", "content": "You are a helpful assistant. Start with a greeting. Asnwer only for the tools provided. If the user asks for something else, politely decline and suggest using the tools."}
]

functions = get_functions_dict()

tools=get_tools_list()

def call_agent(messages, tools, functions):
    response = client.chat.completions.create(
        model="qwen3.5:4b",
        messages=messages,
        tools=tools,
        temperature=0.7,
        max_tokens=16384
    )
    message = response.choices[0].message
    print(f"Assistant: {message}")
    if message.tool_calls:
        print(f"Tool calls detected: {len(message.tool_calls)}")
        for tool_call in message.tool_calls:
            args = json.loads(tool_call.function.arguments)
            print(args)
            print("-----------")
            result = functions[tool_call.function.name](**args)
            print(f"Tool called: {tool_call.function.name} with arguments: {args} Result: {result}")
            messages.append({"role": "tool", "tool_call_id": tool_call.id, "content": f"Tool called: {tool_call.function.name} with arguments: {args} Result: {result}"})
            return call_agent(messages, tools, functions)
    else:
        print(f"Assistant: {message.content}")
    return message

while True:
    user_input = input("User: ")
    if user_input.lower() in ["exit", "quit"]:
        break
    messages.append({"role": "user", "content": user_input})

    message = call_agent(messages, tools, functions)

    messages.append({"role": "assistant", "content": message.content})
print("Exiting the chat.")