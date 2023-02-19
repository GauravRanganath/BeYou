import OverallMaster from "../charts/OverallMaster";
import Container from "react-bootstrap/esm/Container";
import Row from "react-bootstrap/esm/Row";
import Col from "react-bootstrap/esm/Col";
import {useRef, useEffect} from "react";
import Video from "../pages/basicvideo.mp4"

const Dashboard = () => {
  const videoRef = useRef(null);
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
        video.removeEventListener('canplaythrough', playVideo);
      }
    };
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
            <video controls autostart autoPlay src={Video} type="video/mp4" />
        </Row>
      </Container>
    </>
  );
};

export default Dashboard;
