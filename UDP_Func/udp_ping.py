import socket
import time
import logging

logger = logging.getLogger("udp_ping")
import threading


class UDP_Ping:
    def __init__(self, host: str, port: int, timeout: float = 2.0, interval=1.0):
        self.target = (host, port)
        self.timeout = timeout
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(timeout)
        self.interval = interval

        self._thread = None
        self._stop_event = threading.Event()
        self._callback = None
        self._stats = {'sent': 0, 'received': 0, 'lost': 0,
                      'min_rtt': float('inf'), 'max_rtt': 0, 'avg_rtt': 0}

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


    def set_callback(self, callback):

        self._callback = callback

    def _ping_thread(self):

        seq = 1
        rtt_list = []
        while not self._stop_event.is_set():
            try:
                payload = f"PING/1.0 Seq={seq} Time={time.time()}".encode().ljust(56, b'\0')
                start_time = time.time()
                self.sock.sendto(payload, self.target)
                self._stats['sent'] += 1

                try:
                    data, addr = self.sock.recvfrom(1024)
                    rtt = (time.time() - start_time) * 1000
                    rtt_list.append(rtt)
                    self._stats['received'] += 1
                    self._stats['min_rtt'] = min(self._stats['min_rtt'], rtt)
                    self._stats['max_rtt'] = max(self._stats['max_rtt'], int(rtt))

                    self._stats['avg_rtt'] = sum(rtt_list) / len(rtt_list) if rtt_list else 0
                    if self._callback:
                        self._callback(self._stats)
                    logger.info(f"来自 {addr[0]} 的回复: 字节={len(data)} 时间={rtt:.2f}ms")
                except socket.timeout:
                    self._stats['lost'] += 1
                    if self._callback:
                        self._callback(self._stats)
                    logger.warning(f"请求 #{seq} 超时")

            except Exception as e:
                self._stats['lost'] += 1
                if self._callback:
                    self._callback(self._stats)
                logger.error(f"请求 #{seq} 出错: {str(e)}")

            seq += 1
            self._stop_event.wait(self.interval)

    def start_continuous(self):

        if self._thread is None or not self._thread.is_alive():
            self._stop_event.clear()
            self._thread = threading.Thread(target=self._ping_thread, daemon=True)
            self._thread.start()

    def stop_continuous(self):

        self._stop_event.set()
        if self._thread is not None:
            self._thread.join(timeout=1)
            self._thread = None

    def __del__(self):
        self.stop_continuous()
        if hasattr(self, 'sock'):
            self.sock.close()