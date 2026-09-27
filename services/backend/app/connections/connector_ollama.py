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
    stream = client.chat.completions.create(
        model="qwen3.5:4b",
        messages=messages,
        tools=tools,
        temperature=0.7,
        max_tokens=16384,
        stream=True,
        extra_body={
            "think": True
        }
    )

    content_parts = []
    tool_calls_by_index = {}
    thinking_started = False
    answer_started = False

    for chunk in stream:
        delta = chunk.choices[0].delta
        delta_fields = delta.model_dump()
        thinking = (
            delta_fields.get("reasoning")
            or delta_fields.get("thinking")
            or delta_fields.get("reasoning_content")
        )

        if thinking:
            if not thinking_started:
                print("\n[thinking] ", end="", flush=True)
                thinking_started = True
            print(thinking, end="", flush=True)

        if delta.content:
            if not answer_started:
                print("\n[answer] ", end="", flush=True)
                answer_started = True
            print(delta.content, end="", flush=True)
            content_parts.append(delta.content)

        for call_delta in delta.tool_calls or []:
            tool_call = tool_calls_by_index.setdefault(
                call_delta.index,
                {
                    "id": None,
                    "type": "function",
                    "function": {"name": "", "arguments": ""},
                },
            )

            if call_delta.id:
                tool_call["id"] = call_delta.id

            if call_delta.function.name:
                tool_call["function"]["name"] += call_delta.function.name

            if call_delta.function.arguments:
                tool_call["function"]["arguments"] += call_delta.function.arguments
        

    print()
    content = "".join(content_parts)

    if tool_calls_by_index:
        tool_calls = [
            tool_calls_by_index[index]
            for index in sorted(tool_calls_by_index)
        ]
        messages.append({
            "role": "assistant",
            "content": content or None,
            "tool_calls": tool_calls,
        })

        for tool_call in tool_calls:
            name = tool_call["function"]["name"]
            args = json.loads(tool_call["function"]["arguments"])
            result = functions[name](**args)
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call["id"],
                "content": json.dumps(result, default=str),
            })

        return call_agent(messages, tools, functions)

    return content

while True:
    user_input = input("User: ")
    if user_input.lower() in ["exit", "quit"]:
        break
    messages.append({"role": "user", "content": user_input})

    response_text = call_agent(messages, tools, functions)

    messages.append({"role": "assistant", "content": response_text})
print("Exiting the chat.")