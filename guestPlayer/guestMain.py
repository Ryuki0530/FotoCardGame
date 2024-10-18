import socket
import tkinter as tk
from tkinter import filedialog

# 接続先のホストIPとポート設定
host_ip = input("ホストのIPアドレスを入力してください: ")
port = 5002           # ホストと同じポートを使う
buffer_size = 4096    # 送信バッファサイズ

# ソケットを作成してホストに接続
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host_ip, port))

# tkinterを使ってファイルを選択
root = tk.Tk()
root.withdraw()  # ウィンドウを非表示にする
guest_files = filedialog.askopenfilenames(title="ゲスト側: 50枚の画像を選択", filetypes=[("画像ファイル", "*.png;*.jpg;*.jpeg")])

# 選択されたファイルをホストに送信
for file_path in guest_files:
    with open(file_path, 'rb') as f:
        data = f.read(buffer_size)
        while data:
            client_socket.sendall(data)
            data = f.read(buffer_size)

client_socket.close()
