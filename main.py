import socket
import TCP_Func as up2
import TCP_Func as up
if __name__ == "__main__":
    pinger=up.tcp_Sender("127.0.0.1",8080)
    pinger.send(b"Hello, World!")
    a=up2.tcp_Sender("127.0.0.1",8080)
    a.send(b"Hello, World!")


