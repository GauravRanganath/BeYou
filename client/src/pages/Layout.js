import { Outlet } from "react-router-dom";
import BasicNavBar from "../components/Navbar";
import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import './../index.css'

const Layout = () => {
  return (
    <>
      <BasicNavBar />
      <Container>
        <Row>
          <Col className="layoutContainer">
            <Outlet />
          </Col>
        </Row>
      </Container>
    </>
  );
};

export default Layout;
