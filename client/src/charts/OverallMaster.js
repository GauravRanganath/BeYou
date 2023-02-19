import "./charts.css";
import Button from "react-bootstrap/Button";
import ButtonGroup from "react-bootstrap/ButtonGroup";
import { useState } from "react";
import { OverallLineChart } from "./OverallLineChart";
import { OverallDoughnutChart } from "./OverallDoughnutChart";
import { OverallRadarChart } from "./OverallRadarChart";
import { OverallBarChart } from "./OverallBarChart";
import Container from "react-bootstrap/esm/Container";
import Row from "react-bootstrap/esm/Row";
import Col from "react-bootstrap/esm/Col";

function OverallMaster() {
  const [chartType, setChartType] = useState("percent");

  return (
    <>
      <Container>
        <Row>
          <Col sm={6}>
            {chartType === "line" && <OverallLineChart />}
            {chartType === "percent" && (
              <div
                style={{
                  position: "relative",
                  marginBottom: "1%",
                  padding: "1%",
                  display: "flex",
                  justifyContent: "center",
                }}
              >
                <OverallDoughnutChart />
              </div>
            )}
            {chartType === "radar" && (
              <div
                style={{
                  position: "relative",
                  marginBottom: "1%",
                  padding: "1%",
                  display: "flex",
                  justifyContent: "center",
                }}
              >
                <OverallRadarChart />
              </div>
            )}
            {chartType === "bar" && <OverallBarChart />}
          </Col>
          <Col sm={6}>
            <Row>
              <Col sm={3}>
                {chartType === "line" && <OverallLineChart />}
                {chartType === "percent" && (
                  <div
                    style={{
                      position: "relative",
                      marginBottom: "1%",
                      padding: "1%",
                      display: "flex",
                      justifyContent: "center",
                    }}
                  >
                    <OverallDoughnutChart />
                  </div>
                )}
                {chartType === "radar" && (
                  <div
                    style={{
                      position: "relative",
                      marginBottom: "1%",
                      padding: "1%",
                      display: "flex",
                      justifyContent: "center",
                    }}
                  >
                    <OverallRadarChart />
                  </div>
                )}
                {chartType === "bar" && <OverallBarChart />}
              </Col>
              <Col sm={3}>
                {chartType === "line" && <OverallLineChart />}
                {chartType === "percent" && (
                  <div
                    style={{
                      position: "relative",
                      marginBottom: "1%",
                      padding: "1%",
                      display: "flex",
                      justifyContent: "center",
                    }}
                  >
                    <OverallDoughnutChart />
                  </div>
                )}
                {chartType === "radar" && (
                  <div
                    style={{
                      position: "relative",
                      marginBottom: "1%",
                      padding: "1%",
                      display: "flex",
                      justifyContent: "center",
                    }}
                  >
                    <OverallRadarChart />
                  </div>
                )}
                {chartType === "bar" && <OverallBarChart />}
              </Col>
            </Row>
            <Row>
              <Col sm={3}>
                {chartType === "line" && <OverallLineChart />}
                {chartType === "percent" && (
                  <div
                    style={{
                      position: "relative",
                      marginBottom: "1%",
                      padding: "1%",
                      display: "flex",
                      justifyContent: "center",
                    }}
                  >
                    <OverallDoughnutChart />
                  </div>
                )}
                {chartType === "radar" && (
                  <div
                    style={{
                      position: "relative",
                      marginBottom: "1%",
                      padding: "1%",
                      display: "flex",
                      justifyContent: "center",
                    }}
                  >
                    <OverallRadarChart />
                  </div>
                )}
                {chartType === "bar" && <OverallBarChart />}
              </Col>
            </Row>
          </Col>
        </Row>

        <ButtonGroup aria-label="Basic example">
          <Button variant="secondary" onClick={() => setChartType("percent")}>
            Percent
          </Button>
          <Button variant="secondary" onClick={() => setChartType("bar")}>
            Bar Chart
          </Button>
          <Button variant="secondary" onClick={() => setChartType("radar")}>
            Radar
          </Button>
          <Button variant="secondary" onClick={() => setChartType("line")}>
            Last 7 Days
          </Button>
        </ButtonGroup>
      </Container>
    </>
  );
}

export default OverallMaster;
