import OverallMaster from "../charts/OverallMaster";
import Container from "react-bootstrap/esm/Container";
import Row from "react-bootstrap/esm/Row";
import Col from "react-bootstrap/esm/Col";
import { useRef, useState, useEffect } from "react";
import ReactPlayer from 'react-player';
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

  useEffect(() => {
    const video = videoRef.current;

    const playVideo = () => {
      video.play()
        .catch(error => {
          console.error('Error starting video playback:', error);
        });
    };

    if (video) {
      if (video.paused && video.readyState >= 3) {
        playVideo();
      } else {
        video.addEventListener('canplaythrough', playVideo);
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
            <video controls autostart autoPlay src={Video} type="video/mp4" />
        </Row>
      </Container>
    </>
  );
};

export default Dashboard;
