import UDP_Func.udp_ping as up
if __name__ == "__main__":
    pinger=up.UDP_Ping("127.0.0.1",8080,interval=0)
    pinger.ping(10000,payload_size=1024)


