import json
import socket
import logging

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
logger = logging.getLogger("tcp_service")
logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.WARNING)
formatter = logging.Formatter('[%(asctime)s][%(name)s][%(levelname)s]%(message)s', '%H:%M:%S')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


class tcp_Sender:
    def __init__(self, ip="127.0.0.1", port=8080, timeout=2.0,buffer_size=1024):
        self.buffer_size = buffer_size
        self.ip = ip  # 默认本地地址
        self.port = port  # 默认端口
        self.timeout = timeout  # 接收超时时间


    def send(self, msg: bytes):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.ip, self.port))
            logger.info(f"已连接 {self.ip}:{self.port}")
            s.sendall(msg)
            logger.info(f"已发送消息到 {self.ip}:{self.port}")
            s.settimeout(self.timeout)


            try:
                data= s.recv(self.buffer_size)
                print(f"收到回复: {data.decode()}")
                return data
            except socket.timeout:
                logger.error("等待回复超时")
                return None
            except ConnectionResetError:
                logger.error("连接被远程主机重置")
                return None

    def send_json(self, msg):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.connect((self.ip, self.port))
                s.sendall(json.dumps(msg))
                logger.info(f"已发送消息到 {self.ip}:{self.port}")
                s.settimeout(self.timeout)
            except socket.timeout:
                logger.error("等待回复超时")
                return None
            except ConnectionResetError:
                logger.error("连接被远程主机重置")
                return None
            try:
                data, addr = s.recvfrom(self.buffer_size)
                logger.info(f"收到来自 {addr} 的回复: {data.decode()}")
                return data, addr
            except socket.timeout:
                logger.error("等待回复超时")
                return None
            except ConnectionResetError:
                logger.error("连接被远程主机重置")
                return None

    def __del__(self):
        if hasattr(self, 'sock'):
            self.sock.close()
