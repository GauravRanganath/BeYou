import OverallMaster from "../charts/OverallMaster";
import Container from "react-bootstrap/esm/Container";
import Row from "react-bootstrap/esm/Row";
import Col from "react-bootstrap/esm/Col";
import { useRef, useState, useEffect } from "react";
import ReactPlayer from "react-player";
import axios, * as others from "axios";
import Select from "react-select";

// ['Anger', 'Disgust', 'Fear', 'Joy', 'Neutral', 'Sadness', 'Surprise']

const Dashboard = () => {
  const [overallCumulative, setOverallCumulative] = useState([]);
  const [overallAudio, setOverallAudio] = useState([]);
  const [overallVideo, setOverallVideo] = useState([]);
  const [allData, setAllData] = useState([]);
  const [overallTranscript, setOverallTranscript] = useState([]);
  const [lastXDays, setLastXDays] = useState([]);
  const [fileName, setFileName] = useState("");

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
      .get("http://localhost:5000/getData?name=rama")
      .then(function (response) {
        console.log("ALLDATA:", response.data);
        let data = response.data;
        for (let i = 0; i < data.length; i++) {
          let epoch = parseInt(data[i]["epoch_date"]);
          let temp = new Date(epoch);
          data[i]["id"] = i;
          data[i]["value"] = data[i]["video_name"];
          data[i]["label"] = temp.toString();
        }
        console.log("ALLDATA PRUNED:", response.data);
        setAllData(data);
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

  useEffect(() => {}, []);
  return (
    <>
      <Container>
        <Row>
          <Col>
            <br></br>
            <br></br>
            <h1>Overall Analysis</h1>
            <br></br>
            <br></br>
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
        <br></br>
        <Row>
          <Col md={3}></Col>
          <Col md={6}>
            <Select
              options={allData}
              onChange={(value) => {
                axios
                  .get(
                    "http://localhost:5000/boxes?filename=" +
                      value["video_name"]
                  )
                  .then(function (response) {
                    console.log("UPLOAD: complete", response.data);
                    setFileName("videos/" + value["video_name"]);
                  });
              }}
            />
            <div></div>
            <div style={{margin: "auto"}} className="player-wrapper">
              <ReactPlayer
                // className='react-player fixed-bottom'
                url={fileName}
                // width='20%'
                // height='20%'
                controls={true}
              />
            </div>
          </Col>
          <Col md={3}></Col>
        </Row>
      </Container>
    </>
  );
};

export default Dashboard;
