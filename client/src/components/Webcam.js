import { useRef, useState, useCallback } from "react";
import Webcam from "react-webcam";
import Button from "react-bootstrap/Button";
import { useAudioRecorder } from "react-audio-voice-recorder";
import "./../index.css";
import first from "./../img/1.png";
import second from "./../img/2.png";

const WebcamStreamCapture = () => {
  const webcamRef = useRef(null);
  const mediaRecorderRef = useRef(null);
  const [capturing, setCapturing] = useState(false);
  const [recordedChunks, setRecordedChunks] = useState([]);
  const [typeWriterPhase, setTypewriterPhase] = useState(0);

  const handleStartCaptureClick = useCallback(() => {
    setTypewriterPhase(1);
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
    setTypewriterPhase(2);
    mediaRecorderRef.current.stop();
    setCapturing(false);
  }, [mediaRecorderRef, webcamRef, setCapturing]);

  const handleDownload = useCallback(() => {
    setTypewriterPhase(3);
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
      <br></br>
      {typeWriterPhase === 0 && (
        <div className="typewriter" style={{ display: "inline-block" }}>
          <h1 className="question">Hi Rama! How was your day?</h1>
        </div>
      )}
      {typeWriterPhase === 1 && (
        <div className="typewriter" style={{ display: "inline-block" }}>
          <h1 className="question">
            Remember to <em>be you</em> when you self reflect!
          </h1>
        </div>
      )}
      {typeWriterPhase === 2 && (
        <div className="typewriter" style={{ display: "inline-block" }}>
          <h1 className="question">
            If you're happy with your reflection, hit upload!
          </h1>
        </div>
      )}
      {typeWriterPhase === 3 && (
        <div className="typewriter" style={{ display: "inline-block" }}>
          <h1 className="question">
            You're response has been sent to your therapist. Cya tomorrow!
          </h1>
        </div>
      )}
      <br></br>
      <br></br>
      <Webcam audio={true} muted={true} ref={webcamRef} />
      <br />
      <br></br>
      <div style={{ display: "inline" }}>
        <img width={"50px"} src={first} />
        {capturing ? (
          <Button
            className="journalButton"
            variant="dark"
            onClick={handleStopCaptureClick}
          >
            Stop Reflecting
          </Button>
        ) : (
          <Button
            className="journalButton"
            variant="dark"
            onClick={handleStartCaptureClick}
          >
            Start Reflecting
          </Button>
        )}
        {recordedChunks.length > 0 && (
          <Button
            className="journalButton"
            variant="dark"
            onClick={handleDownload}
          >
            Download
          </Button>
        )}
        <img width={"50px"} src={second} />
      </div>
    </>
  );
};

export default WebcamStreamCapture;
