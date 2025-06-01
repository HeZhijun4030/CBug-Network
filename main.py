import socket
import UDP_Func

# 测试代码
if __name__ == "__main__":
    sender = UDP_Func.udp_Sender()
    sender.ip = "192.168.1.7"
    sender.port = 9999

    sender.UDP_sendto(b"Hello World", expect_reply=True)

