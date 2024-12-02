import cv2
from pyzbar.pyzbar import decode
import streamlit as st
import numpy as np
from PIL import Image

class QRCodeDetector:
    def detect_qr_codes(self, frame):
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        qr_codes = decode(gray_frame)
        return qr_codes

    def process_qr_codes(self, qr_codes):
        qr_data = ""
        if qr_codes:
            for qr_code in qr_codes:
                qr_data = qr_code.data.decode('utf-8')
                if qr_data.startswith("WIFI:") and "P:" in qr_data:
                    password_start = qr_data.find("P:") + 2
                    password_end = qr_data.find(";", password_start)
                    password = qr_data[password_start:password_end]
                    with open("scanned.txt", "w") as f:
                        f.write(f"WIFI Password: {password}")
                    return f"WIFI Password saved: {password}"
                else:
                    with open("scanned.txt", "w") as f:
                        f.write(qr_data)
                    return f"**QR Code data saved: {qr_data}**"
        return "No QR Code detected make sure ur QR Code picture is clear ."

def main():
    st.title("QR Code Scanner")
    st.write("Upload an image with a QR code, or use your webcam to scan one!")

    qr_detector = QRCodeDetector()

    image = st.camera_input("Capture from your webcam")

    uploaded_file = st.file_uploader("Or upload an image", type=["png", "jpg", "jpeg"])


    if image or uploaded_file:
        if image:
            img = Image.open(image)
        else:
            img = Image.open(uploaded_file)

        frame = np.array(img)

        qr_codes = qr_detector.detect_qr_codes(frame)
        result = qr_detector.process_qr_codes(qr_codes)

        st.image(frame, caption="Processed Image", channels="BGR")
        st.write(result)
    else:
        st.write("Please upload an image or capture one with your webcam.")

if __name__ == "__main__":
    main()
