import socket
import threading
import tkinter as tk

class ChatClientGUI:
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_ip = None
        self.server_port = 4007

        self.nick = None
        self.connected = False

        self.root = tk.Tk()
        self.root.title("PVRC Client")
        icon_path = "./assets/logo.png"
        icon = tk.PhotoImage(file=icon_path)
        self.root.iconphoto(True, icon)

        self.ip_label = tk.Label(self.root, text="Enter server IP:")
        self.ip_label.pack()

        self.ip_entry = tk.Entry(self.root)
        self.ip_entry.pack()

        self.port_label = tk.Label(self.root, text="Enter server port (default 4007):")
        self.port_label.pack()

        self.port_entry = tk.Entry(self.root)
        self.port_entry.pack()

        self.nick_label = tk.Label(self.root, text="Enter your nickname:")
        self.nick_label.pack()
        self.nick_entry = tk.Entry(self.root)
        self.nick_entry.pack()

        self.connect_button = tk.Button(self.root, text="Connect", command=self.connect)
        self.connect_button.pack()

        self.chat_text = tk.Text(self.root, state=tk.DISABLED)
        self.chat_text.pack()

        self.message_entry = tk.Entry(self.root, state=tk.DISABLED)
        self.message_entry.pack()

        self.send_button = tk.Button(self.root, text="Send", command=self.send_message, state=tk.DISABLED)
        self.send_button.pack()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.message_entry.bind("<Return>", self.send_message_on_enter)

    def connect(self):
        self.server_ip = self.ip_entry.get()
        self.server_port = self.port_entry.get() or self.server_port
        self.server_port = int(self.server_port)
        
        self.nick = self.nick_entry.get()
        self.client_socket.connect((self.server_ip, self.server_port))
        self.client_socket.send(self.nick.encode())
        self.connected = True
        self.connect_button.config(state=tk.DISABLED)
        self.ip_entry.config(state=tk.DISABLED)
        self.port_entry.config(state=tk.DISABLED)
        self.nick_entry.config(state=tk.DISABLED)
        self.message_entry.config(state=tk.NORMAL)
        self.send_button.config(state=tk.NORMAL)
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

    def send_message(self, event=None):
        message = self.message_entry.get()
        if message:
            full_message = f"{message}"
            self.client_socket.send(full_message.encode())
            self.message_entry.delete(0, tk.END)

    def display_message(self, message):
        self.chat_text.config(state=tk.NORMAL)
        self.chat_text.insert(tk.END, message + "\n")
        self.chat_text.config(state=tk.DISABLED)
        self.chat_text.see(tk.END)

    def on_closing(self):
        self.client_socket.close()
        self.root.destroy()

    def send_message_on_enter(self, event):
        self.send_message()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    client = ChatClientGUI()
    client.run()
