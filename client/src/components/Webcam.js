import { useRef, useState, useCallback } from "react";
import Webcam from "react-webcam";
import Button from "react-bootstrap/Button";
import { useAudioRecorder } from "react-audio-voice-recorder";
import "./../index.css";

const WebcamStreamCapture = () => {
  const webcamRef = useRef(null);
  const mediaRecorderRef = useRef(null);
  const [capturing, setCapturing] = useState(false);
  const [recordedChunks, setRecordedChunks] = useState([]);

  const handleStartCaptureClick = useCallback(() => {
    setCapturing(true);
    mediaRecorderRef.current = new MediaRecorder(webcamRef.current.stream, {
      mimeType: "video/webm",
    });
    mediaRecorderRef.current.addEventListener(
      "dataavailable",
      handleDataAvailable
    );
    mediaRecorderRef.current.start();
  }, [webcamRef, setCapturing, mediaRecorderRef]);

  const handleDataAvailable = useCallback(
    ({ data }) => {
      if (data.size > 0) {
        setRecordedChunks((prev) => prev.concat(data));
      }
    },
    [setRecordedChunks]
  );

  const handleStopCaptureClick = useCallback(() => {
    mediaRecorderRef.current.stop();
    setCapturing(false);
  }, [mediaRecorderRef, webcamRef, setCapturing]);

  const handleDownload = useCallback(() => {
    if (recordedChunks.length) {
      const blob = new Blob(recordedChunks, {
        type: "video/webm",
      });

      const data = new FormData();
      let name = "rama";
      let date = Date.now().toString();
      let fileName = name + "_" + date + ".webm";
      data.append("file", blob, fileName);

      fetch("http://localhost:5000/upload", {
        method: "POST",
        body: data,
      }).then((response) => {
        console.log(response);
      });
      setRecordedChunks([]);
    }
  }, [recordedChunks]);

  return (
    <>
      <Webcam audio={true} muted={true} ref={webcamRef} />
      <br />
      {capturing ? (
        <Button className="journalButton" variant="dark" onClick={handleStopCaptureClick}>
          Stop Capture
        </Button>
      ) : (
        <Button className="journalButton" variant="dark" onClick={handleStartCaptureClick}>
          Start Capture
        </Button>
      )}
      {recordedChunks.length > 0 && (
        <Button className="journalButton" variant="dark" onClick={handleDownload}>
          Download
        </Button>
      )}
    </>
  );
};

export default WebcamStreamCapture;
