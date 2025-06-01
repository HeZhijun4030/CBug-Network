import socket
import time
import logging

logger = logging.getLogger("udp_ping")


class UDP_Ping:
    def __init__(self, host: str, port: int, timeout: float = 2.0, interval=1.0):
        self.target = (host, port)
        self.timeout = timeout
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(timeout)
        self.interval = interval

    def ping(self, count: int = 4, payload_size: int = 56):
        success = 0
        failures = 0
        rtt_list = []

        for seq in range(1, count + 1):
            try:

                timestamp = str(time.time()).encode('ascii')[:8].ljust(8, b'0')
                payload = (
                    f"PING/1.0 Seq={seq} Time={time.time()}"
                    .encode().ljust(payload_size, b'\0')
                )

                start_time = time.time()
                self.sock.sendto(payload, self.target)

                try:
                    data, addr = self.sock.recvfrom(1024)
                    end_time = time.time()
                    rtt = (end_time - start_time) * 1000
                    rtt_list.append(rtt)
                    success += 1
                    print(f"来自 {addr[0]} 的回复: 字节={len(data)} 时间={rtt:.2f}ms")
                except socket.timeout:
                    failures += 1
                    print(f"请求 #{seq} 超时")
                    continue

            except Exception as e:
                failures += 1
                print(f"请求 #{seq} 出错: {str(e)}")
                continue
            time.sleep(self.interval)

        if success > 0:
            print("\nPing 统计信息:")
            print(
                f"    数据包: 已发送 = {count}, 已接收 = {success}, 丢失 = {failures} ({(failures / count) * 100:.0f}% 丢失)")
            print(f"    往返时间(毫秒):")
            print(
                f"    最短 = {min(rtt_list):.2f}ms, 最长 = {max(rtt_list):.2f}ms, 平均 = {sum(rtt_list) / len(rtt_list):.2f}ms")
        else:
            print("\n所有请求均失败")

    def __del__(self):
        if hasattr(self, 'sock'):
            self.sock.close()
