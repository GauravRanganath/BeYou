import landing from "./../img/landing.png";
import Container from "react-bootstrap/esm/Container";
import Row from "react-bootstrap/esm/Row";
import Col from "react-bootstrap/esm/Col";
import Button from "react-bootstrap/esm/Button";

const Home = () => {
  return (
    <>
      <Container>
        <Row>
          <Col sm={6}>
            <div style={{ textAlign: "left", marginTop: "200px" }}>
              <h1 style={{ fontSize: "48px" }}>Discover the power of</h1>
              <h1 style={{ fontSize: "120px", textDecoration: "underline" }}>
                Being You.
              </h1>
              <p>I am a...</p>
              <div style={{ display: "inline" }}>
                <Button variant="dark" style={{ marginRight: "10px" }}>
                  Patient
                </Button>
                <Button variant="dark">Therapist</Button>
              </div>
            </div>
          </Col>
          <Col sm={6}>
            <img width={"100%"} src={landing} alt="landing" />
          </Col>
        </Row>
      </Container>
    </>
  );
};

export default Home;
