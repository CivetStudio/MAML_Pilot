import socket


def scan_port(target_ip, port):
    try:
        # 创建 TCP 套接字
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 设置连接超时时间（单位：秒）
        sock.settimeout(1)
        # 尝试连接目标 IP 的指定端口
        result = sock.connect_ex((target_ip, port))
        # 检查连接结果
        if result == 0:
            print(f"端口 {port} 开放")
        else:
            pass
            # print(f"端口 {port} 关闭")
        # 关闭套接字
        sock.close()
    except Exception as e:
        print(f"扫描端口 {port} 出错:", e)


def scan_ports(target_ip, start_port, end_port):
    print(f"开始扫描 {target_ip} 的端口范围 {start_port}-{end_port}...")
    # 循环扫描指定范围内的端口
    for port in range(start_port, end_port + 1):
        scan_port(target_ip, port)
    print("端口扫描完成")


if __name__ == "__main__":
    target_ip = "192.168.0.19"  # 目标 IP 地址
    start_port = 1  # 起始端口号
    end_port = 9999  # 结束端口号
    scan_ports(target_ip, start_port, end_port)
