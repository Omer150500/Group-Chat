import socket
import threading
import tkinter as tk
from tkinter import messagebox

HOST = '127.0.0.1'
PORT = 50001

client_socket = None

# רשימת הודעות שתשמש להצגת הודעות בתיבת ההודעות
chat_messages = []

# התחברות לשרת
def connect_to_server():
    global client_socket
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((HOST, PORT))
        
        # בקשה לשם המשתמש
        name = name_entry.get()
        client_socket.sendall(name.encode('utf-8'))

        # קבלת הודעות מהשרת
        threading.Thread(target=receive_messages, daemon=True).start()
        messagebox.showinfo("Connected", f"Welcome {name}! You're connected to the chat.")

    except Exception as e:
        messagebox.showerror("Connection Error", f"Error connecting to the server: {e}")

# קבלת הודעות מהשרת
def receive_messages():
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                chat_messages.append(message)
                update_chat_box()
            else:
                break
        except:
            break

# עדכון תיבת ההודעות
def update_chat_box():
    chat_box.config(state=tk.NORMAL)  # הפיכת תיבת הטקסט לניתנת לעריכה
    chat_box.delete(1.0, tk.END)  # ניקוי התיבה
    for message in chat_messages:
        chat_box.insert(tk.END, message + '\n')  # הוספת כל ההודעות
    chat_box.config(state=tk.DISABLED)  # הפיכת התיבה לקריאה בלבד

# שליחת הודעה
def send_message():
    message = message_entry.get()
    if message:
        chat_messages.append(f"You: {message}")
        update_chat_box()
        client_socket.sendall(message.encode('utf-8'))  # שליחת ההודעה לשרת
        message_entry.delete(0, tk.END)  # ריקון שדה הקלט

# יצירת הממשק הגרפי
def create_gui():
    root = tk.Tk()
    root.title("Chat Application")

    # הגדרת גודל חלון
    root.geometry("600x500")
    root.configure(bg="#f0f0f0")

    # תיבת הודעות
    global chat_box
    chat_box = tk.Text(root, height=15, width=70, bg="#e0e0e0", fg="black", wrap=tk.WORD, state=tk.DISABLED)
    chat_box.pack(pady=10)

    # שדה קלט להודעות
    global message_entry
    message_entry = tk.Entry(root, width=50, font=("Arial", 14))
    message_entry.pack(pady=10)

    # כפתור לשליחת הודעה
    send_button = tk.Button(root, text="Send", width=20, height=2, bg="#4CAF50", fg="white", command=send_message)
    send_button.pack(pady=10)

    # שדה לקביעת שם
    name_label = tk.Label(root, text="Enter your name:", bg="#f0f0f0")
    name_label.pack(pady=5)
    global name_entry
    name_entry = tk.Entry(root, width=40)
    name_entry.pack(pady=5)

    # כפתור לחיבור לשרת
    connect_button = tk.Button(root, text="Connect", width=20, height=2, bg="#4CAF50", fg="white", command=connect_to_server)
    connect_button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
