import { useState, useRef } from "react";

interface Message{
    text: string;
    sender: "user" | "bot";
}

const useChat = () => {
    const [messages, setMessages] = useState<Message[]>([{ text: "Hi", sender: "user" }, { text: "Hello! How can I assist you today?", sender: "bot" }]);

    const streamAbortControllerRef = useRef<AbortController | null>(null);

    const updateBotMessage = (text: string) => {
        setMessages( (prev) => {
            const lastIndex = prev.length -1;
            const last = prev[lastIndex];

            if(last?.sender === "bot"){
                const updated = [...prev];
                updated[lastIndex] = {sender: "bot", text: last.text + text};
                return updated;
            }

            return [...prev, {sender: "bot", text}]

        })
    }

    const sendMessage = async (text: string) => {
        const newMessage: Message = { text, sender: "user" };
        setMessages([...messages, newMessage]);

        try{
            setMessages((prev) => [...prev, { text: "", sender: "bot" }]);
            const abortController = new AbortController();
            streamAbortControllerRef.current = abortController;
            const response = await fetch("http://localhost:8000/chat", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ message: text })
            });

            if (!response.body){
                throw new Error("ReadableStream not supported by the response.");
            }

            const reader = response.body.getReader();
            const decoder = new TextDecoder();
            let done = false;

            // Buffer to handle incomplete lines between chunks
            let buffer = '';

            while (!done){
                const {value, done: readerDone} = await reader.read();
                done = readerDone;

                if (value){
                    const chunk = decoder.decode(value, { stream: true });
                    buffer += chunk;
                    console.log("Received chunk:", chunk);
                    
                    // Process complete lines
                    const lines = buffer.split('\n');
                    // Keep the last incomplete line in buffer
                    buffer = lines.pop() || '';
                    
                    for (const line of lines) {
                        // console.log("Processing line:", line);
                        // Check for SSE data lines
                        if (line.startsWith('data: ')) {
                            const data = line.substring(6); // Remove "data: " prefix
                            
                            // Handle [DONE] signal (end of stream) - support both formats
                            if (data === '[DONE]' || data === '{"stream_end":true}' || data === '{"stream_end": true}') {
                                break;
                            }
                            
                            try {
                                const parsed = JSON.parse(data);
                                if (parsed.token !== undefined) {
                                    updateBotMessage(parsed.token);
                                }
                            } catch (error) {
                                console.warn('Failed to parse SSE data:', data, error);
                            }
                        }
                    }
                }
            }



            // const botMessage = await response.text();
            // setMessages([...messages, { text: botMessage, sender: "bot" }]);
        } catch (error) {
            console.error("Error sending message:", error);
        } finally {
            streamAbortControllerRef.current = null;
        }
    };

    useRef(() => {
        streamAbortControllerRef.current?.abort();
    });

    return { messages, sendMessage };
};

export default useChat;