import socket
import threading
import time


class DNS_Relay_Server:  # 一个relay server实例，通过缓存文件和外部地址来初始化
    def __init__(self, cache_file, name_server):
        # url_IP字典:通过域名查询ID
        self.url_ip = {}
        # key是域名，value是IP地址
        self.cache_file = cache_file
        self.load_file()
        # print(self.url_ip)
        self.name_server = name_server
        # trans字典：通过DNS响应的ID来获得原始的DNS数据包发送方
        self.trans = {}

    def load_file(self, ):
        f = open(self.cache_file, 'r', encoding='utf-8')
        for line in f:
            ip, name = line.split(' ')
            self.url_ip[name.strip('\n')] = ip
        f.close()

    def run(self):
        buffer_size = 512
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_socket.bind(('', 53))
        server_socket.setblocking(False)
        while True:
            try:
                data, addr = server_socket.recvfrom(buffer_size)
                threading.Thread(target=self.handle, args=(server_socket, data, addr)).start()
            except Exception as e:
                continue

    def get_name(self, data):
        position = 12
        length = 0
        name = ""
        while data[position] != 0:

            num = int(data[position])
            length += num + 1
            for i in range(1, num + 1):
                name += chr(data[position + i])
            position += num + 1
            if data[position] != 0:
                name += '.'

        return name, length + 1

    def handle(self, server_socket, data, addr):
            start = time.time()
            RecvDp = DNS_Packege(data)
            # print("RecvDp.QR={}".format(RecvDp.type))
            if not RecvDp.QR:
                # statement
                RecvDp.name, RecvDp.name_length = self.get_name(data)

                if RecvDp.name in self.url_ip and RecvDp.type==1:
                    ip = self.url_ip[RecvDp.name]
                    # 被intercept的情况
                    if ip == '0.0.0.0':
                        response = RecvDp.generate_response(ip=ip, Intercepted=True)
                        server_socket.sendto(response, addr)
                        print(RecvDp.name, end='  ')
                        print("Intercept!  {}s".format(time.time()-start))
                    # local resolve的情况
                    else:
                        response = RecvDp.generate_response(ip=ip, Intercepted=False)
                        server_socket.sendto(response, addr)
                        print(RecvDp.name, end='  ')
                        print("Local Resolve!  {}s".format(time.time()-start))

                # relay的情况
                else:
                    self.trans[RecvDp.ID] = addr, RecvDp.name
                    server_socket.sendto(data, self.name_server)

            else:
                # statement
                if RecvDp.ID in self.trans:
                    target_addr, target_name = self.trans[RecvDp.ID]
                    server_socket.sendto(data, target_addr)
                    print(target_name, end='  ')
                    print("Relay!  {}s".format(time.time()-start))
                    del self.trans[RecvDp.ID]


class DNS_Packege:  # 一个DNS Frame实例，用于解析和生成DNS帧
    def __init__(self, data):
        Msg_arr = bytearray(data)
        self.data = data
        # ID
        self.ID = (Msg_arr[0] << 8) + Msg_arr[1]
        # FLAGS
        self.QR = Msg_arr[2] >> 7
        # 资源记录数量
        self.QDCOUNT = (Msg_arr[4] << 8) + Msg_arr[5]
        self.type = (Msg_arr[-4]<<8)+Msg_arr[-3]
        # query内容解析
        self.name = ""
        self.name_length = 0

    def generate_response(self, ip, Intercepted):
        res = bytearray(32 + self.name_length)
        # print(self.name_length)
        # res-ID
        res[0] = self.ID >> 8
        res[1] = self.ID % 256
        if not Intercepted:
            # res-FLAG
            res[2:4] = b'\x81\x80'
        else:
            # res-FLAG
            res[2:4] = b'\x81\x83'
        # res-Questions
        res[4:6] = b'\x00\x01'
        # res-Answer RRS
        res[6:8] = b'\x00\x01'
        # res-Authority RRs
        res[8:10] = b'\x00\x00'
        # res-Additional RRs
        res[10:12] = b'\x00\x00'
        res[12:16 + self.name_length] = self.data[12:16 + self.name_length]
        # 处理ip
        strbytes = ip.split('.')
        for i in range(0, len(strbytes)):
            strbytes[i] = int(strbytes[i])
        res[-4:] = bytes(strbytes)
        # Answers-datalength
        res[-6:-4] = b'\x00\x04'
        # Answers-ttl
        res[-10:-6] = b'\x00\x00\x00\x7e'
        # Answer-class:IN
        res[-12:-10] = b'\x00\x01'
        # Answer=type:A
        res[-14:-12] = b'\x00\x01'
        # Answer-name point to qname
        res[-16:-14] = b'\xC0\x0C'
        return bytes(res)


if __name__ == '__main__':
    cache_file = 'example.txt'
    name_server = ('223.5.5.5', 53)
    relay_server = DNS_Relay_Server(cache_file, name_server)  # 构造一个DNS_Relay_Server实例
    relay_server.run()
