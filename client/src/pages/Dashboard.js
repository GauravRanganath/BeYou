import OverallMaster from "../charts/OverallMaster";
import Container from "react-bootstrap/esm/Container";
import Row from "react-bootstrap/esm/Row";
import Col from "react-bootstrap/esm/Col";
import {useRef, useEffect} from "react";
import ReactPlayer from 'react-player'

const Dashboard = () => {
  useEffect(() => {

  }, []);
  return (
    <>
      <Container>
        <Row>
          <Col>
            <h1>Dashboard</h1>
          </Col>
        </Row>
        <Row>
            <Col>
                <OverallMaster></OverallMaster>
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
