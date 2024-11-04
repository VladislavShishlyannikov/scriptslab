import socket

def udp_server(host='127.0.0.1', port=5000):
    # Создаем UDP-сокет
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        # Привязываем его к адресу и порту
        server_socket.bind((host, port))
        print(f"UDP сервер запущен на {host}:{port}. Ожидание сообщений...")

        while True:
            # Ожидаем данных от клиента
            data, addr = server_socket.recvfrom(1024)
            print(f"Получено сообщение от {addr}: {data.decode()}")
            # Отправляем данные обратно
            server_socket.sendto(data, addr)

if __name__ == "__main__":
    udp_server()
