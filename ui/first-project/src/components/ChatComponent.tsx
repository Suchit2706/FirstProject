import * as React from 'react';
import { LuBot, LuSendHorizontal } from 'react-icons/lu';
import useChat from '../hooks/chat';
import {
  Collapse,
  Button,
  Card,
  Typography,
  CardBody,
} from "@material-tailwind/react";

const ChatComponent: React.FunctionComponent = () => {
  const [input, setInput] = React.useState("");
  const { messages, sendMessage } = useChat();
  const [loading, setLoading] = React.useState(false);
  const [isOpen, setIsOpen] = React.useState(false);


  const handleSend = async () => {
    if (input.trim() === "") return; // Prevent sending empty messages
    console.log("Sending message:", input);
    // messages.push({ text: input, sender: "user" });
    setLoading(true);
    try{
        await sendMessage(input);
        setInput(""); // Clear the input field after sending
    }finally{
        setLoading(false);
    }
  }

  const toggleOpen = () => setIsOpen(!isOpen);

    return (
    <div className="flex flex-col h-[80vh] bg-white">
      <h2 className="p-4 font-semibold text-lg text-center bg-blue-100 flex text-blue-800 justify-center items-center gap-2">
        Friendly Neighbourhood Chatbot <LuBot size={25} />
      </h2>
      <div className="flex-1 overflow-y-auto p-4 space-y-2">
        {messages.map((msg, index) => (
            <div key={index} className={`p-3 rounded-lg max-w-xs whitespace-pre-wrap ${msg.sender === "user" ? "bg-blue-300 ml-auto" : "bg-gray-200"}`}>
                {
                  msg.sender === "bot" && (
                    <div key={index} className="accordion-item bg-gray-100 rounded-lg">
                      <button className="accordion-header p-2" onClick={toggleOpen} aria-expanded={isOpen}>Thinking</button>
                      
                      {
                        isOpen && (
                          <div className='p-3'>
                            <h3>Bot is thinking</h3>
                          </div>
                        )
                      }
                    </div>
                  )
                }
                
                {msg.text}
            </div>
        ))}
    </div>
      
      <div className="flex items-center p-4 bg-gray-50">
        <input
          type="text"
          placeholder="Type your message..."
          className="flex-1 p-2 border rounded-lg focus:outline-none"
          value={input}
          onChange={(e) => setInput(e.target.value)}
        />
        <button onClick={handleSend} className={`p-2 ${loading ? 'cursor-not-allowed' : 'hover:bg-blue-200'}`} disabled={loading}>
            <LuSendHorizontal size={25} />
        </button>
      </div>
    </div>
  );
};

export default ChatComponent;
