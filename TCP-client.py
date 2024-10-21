import socket

def tcp_client(message, host='127.0.0.1', port=8080):
    # Создаем TCP-сокет
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        # Подключаемся к серверу
        client_socket.connect((host, port))
        # Отправляем сообщение на сервер
        client_socket.sendall(message.encode())
        # Получаем ответ от сервера
        data = client_socket.recv(1024)
        print(f"Ответ от сервера: {data.decode()}")

if __name__ == "__main__":
    msg = input("Введите сообщение для отправки: ")
    tcp_client(msg)
