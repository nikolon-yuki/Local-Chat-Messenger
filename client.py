import socket

# サーバー側で待ち受けているUnixドメインソケットのアドレス
server_address = "socket_file"

# TCP/IPソケットの作成
sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

# サーバー側のアドレスに接続する
print("connecting to {}".format(server_address))
sock.connect(server_address)

# メッセージを送信する
# message = "Hello, server!"
message = input()
sock.sendall(message.encode())

# サーバーからの応答を受信する
response = sock.recv(16)
response_str = response.decode("utf-8")
print("Received " + response_str)

# ソケットをクローズする
sock.close()

