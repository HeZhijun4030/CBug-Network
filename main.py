import socket
import UDP_Func.core as us

# 测试代码
if __name__ == "__main__":
    sender = us.udp_Sender()
    sender.ip = "192.168.1.7"
    sender.port = 9999

    sender.send(b"Hello World", expect_reply=True)

