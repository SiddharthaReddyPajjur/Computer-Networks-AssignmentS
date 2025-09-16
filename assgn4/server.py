import cv2, socket, struct, time

ADDR = ("0.0.0.0", 9999)      # listen on all interfaces
CHUNK = 60000                # bytes per UDP packet (~60 KB)
FPS = 24                     # desired frame rate

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
video = cv2.VideoCapture("sample.mp4")

while True:
    ret, frame = video.read()
    if not ret:
        break
    # JPEG compress
    ok, enc = cv2.imencode(".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
    data = enc.tobytes()

    # send in chunks with marker bit
    for i in range(0, len(data), CHUNK):
        end = i + CHUNK
        chunk = data[i:end]
        marker = 1 if end >= len(data) else 0
        header = struct.pack("!?H", marker, len(chunk))
        sock.sendto(header + chunk, ADDR)

    time.sleep(1/FPS)

video.release()
sock.close()
