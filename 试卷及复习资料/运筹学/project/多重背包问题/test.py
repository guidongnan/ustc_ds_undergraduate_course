from multi_pack import *


def main():
    path = './dataset/little.txt'
    path2 = './dataset/normal.txt'
    path3 = './dataset/large.txt'
    V, w, v, p = parse_data(path)
    start = time.time()
    mul_pack_dp(V, w, v, p)
    print(time.time()-start)
    V, w, v, p = parse_data(path2)
    start = time.time()
    mul_pack_dp(V, w, v, p)
    print(time.time()-start)
    V, w, v, p = parse_data(path3)
    start = time.time()
    mul_pack_dp(V, w, v, p)
    print(time.time()-start)


if __name__ == '__main__':
    main()