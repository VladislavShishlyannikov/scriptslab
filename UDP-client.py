import socket

def udp_client(message, host='127.0.0.1', port=5000):
    # Создаем UDP-сокет
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
        # Отправляем сообщение на сервер
        client_socket.sendto(message.encode(), (host, port))
        # Получаем ответ от сервера
        data, _ = client_socket.recvfrom(1024)
        print(f"Ответ от сервера: {data.decode()}")

if __name__ == "__main__":
    msg = input("Введите сообщение для отправки: ")
    udp_client(msg)
