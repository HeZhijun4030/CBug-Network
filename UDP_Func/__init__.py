import json
import socket
import logging

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
logger = logging.getLogger("udp_service")
logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.WARNING)
formatter = logging.Formatter('[%(asctime)s][%(name)s][%(levelname)s]%(message)s','%H:%M:%S')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

class udp_Sender:
    def __init__(self):
        self.ip = "127.0.0.1"  #默认本地地址
        self.port = 8080  #默认端口
        self.timeout = 2.0  #接收超时时间

    def UDP_sendto(self, msg: bytes, expect_reply=False):
        """发送UDP消息
        Args:
            msg: 要发送的字节消息
            expect_reply: 是否期待回复 (默认False)
        """
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.sendto(msg, (self.ip, self.port))
            logger.info(f"已发送消息到 {self.ip}:{self.port}")

            if expect_reply:
                s.settimeout(self.timeout)
                try:
                    data, addr = s.recvfrom(1024)
                    logger.info(f"收到来自 {addr} 的回复: {data.decode()}")
                    return data
                except socket.timeout:
                    logger.error("等待回复超时")
                except ConnectionResetError:
                    logger.error("连接被远程主机重置")
    def send_json(self, msg,expect_reply=False):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.sendto(json.dumps(msg).encode(), (self.ip, self.port))
            if expect_reply:
                s.settimeout(self.timeout)
                try:
                    data, addr = s.recvfrom(1024)
                    logger.info(f"收到来自 {addr} 的回复: {data.decode()}")
                    return data
                except socket.timeout:
                    logger.error("等待回复超时")
                except ConnectionResetError:
                    logger.error("连接被远程主机重置")

class udp_Server:
    def __init__(self):
        self.ip = "127.0.0.1"
        self.port = 8080

    def start_udp_server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.bind((self.ip, self.port))
            logger.warning("UDP服务端已启动，等待消息...")
            while True:
                data, addr = s.recvfrom(1024)
                logger.info(f"收到来自 {addr} 的消息: {data.decode()}")
                s.sendto(b"ACK", addr)
