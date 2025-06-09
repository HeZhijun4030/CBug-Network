import TCP_Func as up
if __name__ == "__main__":
    pinger=up.tcp_Sender("4.2.2.1",53)
    pinger.send(b"Hello World!")
    up.logger.info("Message sent successfully")



