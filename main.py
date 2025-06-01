import socket
import UDP_Func.udp_ping as up


if __name__ == "__main__":
    pinger = up.UDP_Ping("4.2.2.2", 53,timeout=0.01)
    pinger.ping(140)
