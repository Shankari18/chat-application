import socket
import threading
import datetime
class ChatServer:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(('127.0.0.1', 12345))
        self.server.listen(5)
        print("Server started on port 12345, waiting for a connection...")
        self.running = True
        input_thread = threading.Thread(target=self.check_for_exit, daemon=True)
        input_thread.start()
        while self.running:  
            try:
                self.server.settimeout(1.0)  
                self.client, self.addr = self.server.accept()
                print(f"Connected to {self.addr}")
                self.receive_thread = threading.Thread(target=self.receive_messages, daemon=True)
                self.receive_thread.start()
            except socket.timeout:
                continue
    def check_for_exit(self):
        while True:
            command = input("")
            if command.lower() in ["exit", "stop"]:
                print("Stopping server...")
                self.running = False
                self.server.close()
                break
    def receive_messages(self):
        while self.running:
            try:
                message = self.client.recv(1024).decode('utf-8')
                if message:
                    print(f"Client: {message}") 
                    response = self.generate_response(message)
                    self.client.send(response.encode('utf-8'))  
                    if message.lower() == "bye":
                        print("Client said bye. Closing connection...")
                        self.client.close()
                        break  
            except (ConnectionResetError, OSError):
                print("Client disconnected. Waiting for a new connection...")
                break
            except Exception as e:
                print(f"Error: {e}")
                break
    def generate_response(self, message):
        message = message.lower()
        if "hello" in message:
            return "Hello! How can I assist you today?"
        elif "how are you" in message:
            return "I'm just a chat server, but I'm doing great! How about you?"
        elif "date" in message:
            return f"Today's date is {datetime.datetime.now().strftime('%Y-%m-%d')}"
        elif "time" in message:
            return f"The current time is {datetime.datetime.now().strftime('%H:%M:%S')}"
        elif "bye" in message:
            return "Goodbye! Have a great day!"
        else:
            return "I'm here to chat! Ask me anything."
if __name__ == "__main__":
    ChatServer()

