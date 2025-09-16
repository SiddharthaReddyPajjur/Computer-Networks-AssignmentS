import cv2, socket, struct, numpy as np

PORT = 9999
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", PORT))

buffer = b""
while True:
    packet, _ = sock.recvfrom(65536)
    marker, size = struct.unpack("!?H", packet[:3])
    buffer += packet[3:]
    if marker:
        img = cv2.imdecode(np.frombuffer(buffer, dtype=np.uint8), cv2.IMREAD_COLOR)
        if img is not None:
            cv2.imshow("UDP Stream", img)
        buffer = b""
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

cv2.destroyAllWindows()
sock.close()
