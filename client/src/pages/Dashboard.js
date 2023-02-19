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
            <div className='player-wrapper'>
              <ReactPlayer
              // className='react-player fixed-bottom'
              url='videos/demo_video.mp4'
              // width='20%'
              // height='20%'
              controls = {true}
            />
        </div>
        </Row>

      </Container>
    </>
  );
};

export default Dashboard;
