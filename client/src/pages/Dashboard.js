import OverallMaster from "../charts/OverallMaster";
import Container from "react-bootstrap/esm/Container";
import Row from "react-bootstrap/esm/Row";
import Col from "react-bootstrap/esm/Col";
import { useRef, useState, useEffect } from "react";
import Video from "../pages/basicvideo.mp4";
import axios, * as others from "axios";

// ['Anger', 'Disgust', 'Fear', 'Joy', 'Neutral', 'Sadness', 'Surprise']

const Dashboard = () => {
  const [overallCumulative, setOverallCumulative] = useState([]);
  const [overallAudio, setOverallAudio] = useState([]);
  const [overallVideo, setOverallVideo] = useState([]);
  const [overallTranscript, setOverallTranscript] = useState([]);
  const [lastXDays, setLastXDays] = useState([]);

  useEffect(() => {
    axios
      .get("http://localhost:5000/getAverageEmotions?name=rama")
      .then(function (response) {
        console.log(response.data);
        setOverallAudio(response.data["audio"]);
        setOverallTranscript(response.data["text"]);
        setOverallVideo(response.data["video"]);
        setOverallCumulative(response.data["overall"]);
      })
      .then(() => {
        console.log(overallCumulative);
      });
    axios
      .get("http://localhost:5000/getLatestWeek?name=rama")
      .then(function (response) {
        console.log(response.data);
        setLastXDays(response.data);
      })
      .then(() => {
        console.log(lastXDays);
      });
  }, []);

  const videoRef = useRef(null);
  useEffect(() => {
    const video = videoRef.current;

    const playVideo = () => {
      video.play().catch((error) => {
        console.error("Error starting video playback:", error);
      });
    };

    if (video) {
      if (video.paused && video.readyState >= 3) {
        playVideo();
      } else {
        video.addEventListener("canplaythrough", playVideo);
      }
    }

    return () => {
      if (video) {
        video.removeEventListener("canplaythrough", playVideo);
      }
    };
  }, []);
  return (
    <>
      <Container>
        <Row>
          <Col>
            <h1>Overall Analysis</h1>
          </Col>
        </Row>
        <Row>
          <Col>
            <OverallMaster
              dataCumulative={overallCumulative}
              dataAudio={overallAudio}
              dataTranscript={overallTranscript}
              dataVideo={overallVideo}
              dataXDays={lastXDays}
            ></OverallMaster>
          </Col>
        </Row>
        <br></br>
        <Row>
          <Col>
            <h1>Daily Analysis</h1>
          </Col>
        </Row>
        <Row>
          <Col sm={7}>
            <video
              width={"750px"}
              height={"400px"}
              controls
              autostart
              autoPlay
              src={Video}
              type="video/mp4"
            />
          </Col>
          <Col sm={5}>
            <p style={{ textAlign: "justify" }}>
              Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
              eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut
              enim ad minim veniam, quis nostrud exercitation ullamco laboris
              nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in
              reprehenderit in voluptate velit esse cillum dolore eu fugiat
              nulla pariatur. Excepteur sint occaecat cupidatat non proident,
              sunt in culpa qui officia deserunt mollit anim id est laborum.
            </p>
          </Col>
        </Row>
      </Container>
    </>
  );
};

export default Dashboard;
