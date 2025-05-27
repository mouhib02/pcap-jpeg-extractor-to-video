from scapy.all import rdpcap, TCP
import cv2
import numpy as np
import os

def extract_images_from_stream_to_video(pcap_file, output_video):
    print(f"[+] open the pcap file : {pcap_file}")
    packets = rdpcap(pcap_file)
    tcp_streams = {}

    for pkt in packets:
        if TCP in pkt and pkt.haslayer('Raw'):
            ip = pkt[0]
            tcp = pkt[TCP]
            stream_id = (ip.src, tcp.sport, ip.dst, tcp.dport)
            if stream_id not in tcp_streams:
                tcp_streams[stream_id] = b""
            tcp_streams[stream_id] += bytes(pkt['Raw'].load)

    jpeg_start = b'\xff\xd8'
    jpeg_end = b'\xff\xd9'
    frames = []

    for stream_id, data in tcp_streams.items():
        start = 0
        while True:
            start_index = data.find(jpeg_start, start)
            if start_index == -1:
                break
            end_index = data.find(jpeg_end, start_index)
            if end_index == -1:
                break

            img_data = data[start_index:end_index + 2]
            img_array = np.frombuffer(img_data, dtype=np.uint8)
            frame = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

            if frame is not None:
                frames.append(frame)
            start = end_index + 2

    if not frames:
        print("[!] we can't find the frame .")
        return

    
    height, width, _ = frames[0].shape
    fps = 5  # Frame per second

    
    output_dir = os.path.dirname(output_video)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    
    if not output_video.endswith(".mp4"):
        output_video += ".mp4"

    
    out = cv2.VideoWriter(output_video, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

    for frame in frames:
        out.write(frame)
    out.release()

    print(f"[🎬] select the path of out: {output_video}")


if __name__ == "__main__":
    print("=== PCAP to Video ===\n")
    pcap_path = input("📄 put hte path of pcap file: ").strip()
    video_path = input("🎥 put the path of output  (for exapmle: output.mp4): ").strip()

    if not os.path.isfile(pcap_path):
        print("[!] pcap file don't exist.")
    else:
        extract_images_from_stream_to_video(pcap_path, video_path)

