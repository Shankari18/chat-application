import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
class ChatClient:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat Client")
        self.chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=20, state=tk.DISABLED)
        self.chat_area.grid(row=0, column=0, padx=10, pady=10, columnspan=2)
        self.message_entry = tk.Entry(root, width=40)
        self.message_entry.grid(row=1, column=0, padx=10, pady=10)
        self.message_entry.bind("<Return>", self.send_message)
        self.send_button = tk.Button(root, text="Send", command=self.send_message)
        self.send_button.grid(row=1, column=1, padx=10, pady=10)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client.connect(('127.0.0.1', 12345))
        except ConnectionRefusedError:
            print("Server is not running! Start the server first.")
            self.root.quit()
            return
        self.receive_thread = threading.Thread(target=self.receive_messages, daemon=True)
        self.receive_thread.start()
    def send_message(self, event=None):
        message = self.message_entry.get()
        if message:
            self.client.send(message.encode('utf-8'))
            self.chat_area.config(state=tk.NORMAL)
            self.chat_area.insert(tk.END, f"You: {message}\n")
            self.chat_area.config(state=tk.DISABLED)
            self.chat_area.yview(tk.END)
            self.message_entry.delete(0, tk.END)
            if message.lower() in ["exit", "stop"]:
                print("Stopping client...")
                self.client.close()
                self.root.quit()
    def receive_messages(self):
        while True:
            try:
                message = self.client.recv(1024).decode('utf-8')
                if message:
                    print(f"Received: {message}")  # Debugging line
                    self.chat_area.config(state=tk.NORMAL)
                    self.chat_area.insert(tk.END, f"Server: {message}\n")
                    self.chat_area.config(state=tk.DISABLED)
                    self.chat_area.yview(tk.END)
            except ConnectionResetError:
                print("Server disconnected. Closing client.")
                break
            except Exception as e:
                print(f"Error: {e}")
                break
if __name__ == "__main__":
    root = tk.Tk()
    client = ChatClient(root)
    root.mainloop()
