import socket

def tcp_server(host='127.0.0.1', port=8080):
    # Создаем TCP-сокет
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        # Привязываем его к адресу и порту
        server_socket.bind((host, port))
        # Переводим в режим ожидания подключения
        server_socket.listen()
        print(f"TCP сервер запущен на {host}:{port}. Ожидание подключения...")

        # Принимаем подключение от клиента
        conn, addr = server_socket.accept()
        with conn:
            print(f"Подключение установлено с {addr}")
            while True:
                # Получаем данные от клиента
                data = conn.recv(1024)
                if not data:
                    break
                print(f"Получено сообщение: {data.decode()}")
                # Отправляем данные обратно (echo)
                conn.sendall(data)

if __name__ == "__main__":
    tcp_server()
