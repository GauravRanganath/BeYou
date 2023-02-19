import OverallMaster from "../charts/OverallMaster";
import Container from "react-bootstrap/esm/Container";
import Row from "react-bootstrap/esm/Row";
import Col from "react-bootstrap/esm/Col";

const Dashboard = () => {
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
      </Container>
    </>
  );
};

export default Dashboard;
