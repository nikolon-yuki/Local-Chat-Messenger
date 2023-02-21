import socket
import os
from faker import Faker

# TCP/IPソケットの作成
# socketメソッドは、常にソケットオブジェクトを返します。 https://docs.python.org/3/library/socket.html#socket-objects
sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

# ソケットを作成したら、ソケットにアドレスを紐付け、接続を待ち受け、受け入れる必要があります。
# ローカルソケットを使用しているため、AF_UNIXはファイル名をアドレスとして取り込みます。
server_address = "socket_file"

# ファイルが既に存在しないことを確認する
try:
    os.unlink(server_address)
except FileNotFoundError:
    pass

# ソケットをアドレスに紐付ける
print("Starting up on {}".format(server_address))
sock.bind(server_address)

# 接続の着信を最大1件まで待ち受けます。1個以上の未受信の接続を受信すると、自動的に接続を拒否します。複数回接続する場合は、1以上に設定します。
sock.listen(1)

# サーバが常に接続を待ち受けるためのループ
while True:
    # acceptはキューにある次の接続を受け入れる。これは(connection, client_address)のタプルを返します。
    # ソケットは全二重なので、接続はクライアントとデータを送受信するための別のソケットオブジェクトです。
    connection, client_address = sock.accept()
    try:
        print("connection from", client_address)

        # データを小分けにして受信し、再送信する。
        while True:
            data = connection.recv(16)
            data_str = data.decode("utf-8")
            print("Received " + data_str)
            
            if data:
                fake = Faker()
                # 現在のクライアントにメッセージを送り返す
                response = "Processing " + fake.name()
                connection.sendall(response.encode())
            else:
                print("no data from", client_address)
                break

    finally:
        # 接続のクリーンアップ
        print("Closing current connection")
        connection.close()
