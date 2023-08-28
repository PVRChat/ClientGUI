import socket
import threading
import tkinter as tk

class ChatClientGUI:
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_ip = "192.168.1.103"
        self.server_port = 4007

        self.nick = None

        self.root = tk.Tk()
        self.root.title("Chat Client")

        self.nick_label = tk.Label(self.root, text="Enter your nickname:")
        self.nick_label.pack()

        self.nick_entry = tk.Entry(self.root)
        self.nick_entry.pack()

        self.connect_button = tk.Button(self.root, text="Connect", command=self.connect)
        self.connect_button.pack()

        self.chat_text = tk.Text(self.root, state=tk.DISABLED)
        self.chat_text.pack()

        self.message_entry = tk.Entry(self.root)
        self.message_entry.pack()

        self.send_button = tk.Button(self.root, text="Send", command=self.send_message)
        self.send_button.pack()

    def connect(self):
        self.nick = self.nick_entry.get()
        self.client_socket.connect((self.server_ip, self.server_port))
        self.client_socket.send(self.nick.encode())
        self.receive_thread = threading.Thread(target=self.receive_messages)
        self.receive_thread.start()

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode()
                if message:
                    self.display_message(message)
            except:
                break

    def send_message(self):
        message = self.message_entry.get()
        full_message = f"{self.nick}: {message}"
        self.client_socket.send(full_message.encode())
        self.message_entry.delete(0, tk.END)

    def display_message(self, message):
        self.chat_text.config(state=tk.NORMAL)
        self.chat_text.insert(tk.END, message + "\n")
        self.chat_text.config(state=tk.DISABLED)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    client = ChatClientGUI()
    client.run()
