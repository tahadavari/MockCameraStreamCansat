import cv2
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()


def generate_video():
    cap = cv2.VideoCapture(0)  # Access the webcam (0 is the default camera)

    while True:
        success, frame = cap.read()
        if not success:
            break

        # Encode the frame in JPEG format
        _, jpeg = cv2.imencode('.jpg', frame)
        # Convert to bytes
        frame = jpeg.tobytes()

        # Yield the frame with the appropriate headers
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

    cap.release()


@app.get("/stream")
def stream():
    return StreamingResponse(generate_video(), media_type="multipart/x-mixed-replace; boundary=frame")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
