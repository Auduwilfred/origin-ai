"use client";

import { useState } from "react";
import axios from "axios";

export default function Home() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  const sendMessage = async () => {
    if (!input) return;

    const newMessages = [...messages, { role: "user", content: input }];
    setMessages(newMessages);

    const res = await axios.post("https://origin-ai.onrender.com/chat", {
      message: input
    });

    setMessages([
      ...newMessages,
      { role: "assistant", content: res.data.response }
    ]);

    setInput("");
  };

  return (
    <div style={styles.container}>
      <div style={styles.chat}>
        {messages.map((msg, i) => (
          <div
            key={i}
            style={
              msg.role === "user"
                ? styles.user
                : styles.bot
            }
          >
            {msg.content}
          </div>
        ))}
      </div>

      <div style={styles.inputBar}>
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask Cypher..."
          style={styles.input}
        />

        <button onClick={sendMessage} style={styles.button}>
          Send
        </button>
      </div>
    </div>
  );
}

const styles = {
  container: {
    background: "#000",
    color: "#fff",
    height: "100vh",
    display: "flex",
    flexDirection: "column",
  },
  chat: {
    flex: 1,
    padding: 20,
    overflowY: "auto",
  },
  user: {
    background: "#2563eb",
    padding: 10,
    margin: 10,
    borderRadius: 10,
    alignSelf: "flex-end",
    maxWidth: "70%",
  },
  bot: {
    background: "#111",
    padding: 10,
    margin: 10,
    borderRadius: 10,
    alignSelf: "flex-start",
    maxWidth: "70%",
  },
  inputBar: {
    display: "flex",
    padding: 10,
    borderTop: "1px solid #222",
  },
  input: {
    flex: 1,
    padding: 12,
    borderRadius: 8,
    border: "none",
    background: "#111",
    color: "#fff",
  },
  button: {
    marginLeft: 10,
    padding: "10px 20px",
    background: "#2563eb",
    border: "none",
    borderRadius: 8,
    color: "#fff",
    cursor: "pointer",
  },
};
