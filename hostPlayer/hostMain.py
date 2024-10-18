import socket
import pygame
import tkinter as tk
from tkinter import filedialog

# 初期設定
host_ip = '0.0.0.0'  # 自分のIPアドレスを使う
port = 5002          # 任意のポート番号
buffer_size = 4096    # 送信バッファサイズ

# ソケット作成と接続待機
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host_ip, port))
server_socket.listen(1)
print(f"接続待機中... IP: {socket.gethostbyname(socket.gethostname())}, ポート: {port}")

conn, addr = server_socket.accept()
print(f"接続が確立されました: {addr}")

# tkinterを使ってファイルを選択
root = tk.Tk()
root.withdraw()  # ウィンドウを非表示にする
host_files = filedialog.askopenfilenames(title="ホスト側: 50枚の画像を選択", filetypes=[("画像ファイル", "*.png;*.jpg;*.jpeg")])

# 画像を受け取る処理
guest_images = []

print("画像を受信中...")
for _ in range(50):
    data = conn.recv(buffer_size)
    if data:
        with open(f"received_guest_image_{_}.png", 'wb') as f:
            f.write(data)
        guest_images.append(f"received_guest_image_{_}.png")

# Pygameを使って画像を表示する
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("カード表示")

# ホスト側の画像も表示用に準備
host_images = []
for file in host_files:
    host_images.append(pygame.image.load(file))

running = True
while running:
    screen.fill((255, 255, 255))

    # ゲスト側の最初の画像を画面に表示 (デモ用に1枚だけ)
    # if guest_images:
    #     img = pygame.image.load(guest_images[0])
    #     screen.blit(img, (100, 100))
    
    # # ホスト側の最初の画像も表示 (デモ用に1枚だけ)
    # if host_images:
    #     screen.blit(host_images[0], (400, 100))

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

conn.close()
server_socket.close()
pygame.quit()
