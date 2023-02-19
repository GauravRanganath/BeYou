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

function OverallMaster({
  dataCumulative,
  dataAudio,
  dataVideo,
  dataTranscript,
  dataXDays,
}) {
  const [chartType, setChartType] = useState("percent");

  console.log(dataCumulative);
  return (
    <>
      <Container>
        <Row>
          <Col sm={6}>
            <h2>Cumulative</h2>
            {chartType === "line" && <OverallLineChart dataXDays={dataXDays} />}
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
                <OverallDoughnutChart dataArr={dataCumulative} />
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
                <OverallRadarChart dataArr={dataCumulative} />
              </div>
            )}
            {chartType === "bar" && (
              <OverallBarChart dataArr={dataCumulative} />
            )}
            <br></br>
            <ButtonGroup aria-label="Basic example">
              <Button
                variant="secondary"
                onClick={() => setChartType("percent")}
              >
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
          </Col>
          <Col sm={6}>
            <Row>
              <Col sm={6}>
                <h4>Audio</h4>
                {chartType === "line" && (
                  <OverallLineChart showLegend={false} />
                )}
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
                    <OverallDoughnutChart
                      dataArr={dataAudio}
                      showLegend={false}
                    />
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
                    <OverallRadarChart
                      setColor={"rgba(54, 162, 235, 0.2)"}
                      dataArr={dataAudio}
                      showLegend={false}
                    />
                  </div>
                )}
                {chartType === "bar" && (
                  <OverallBarChart
                    setColor={"rgba(54, 162, 235, 0.2)"}
                    dataArr={dataAudio}
                    showLegend={false}
                  />
                )}
              </Col>
              <Col sm={6}>
                <h4>Video</h4>
                {chartType === "line" && (
                  <OverallLineChart showLegend={false} />
                )}
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
                    <OverallDoughnutChart
                      dataArr={dataVideo}
                      showLegend={false}
                    />
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
                    <OverallRadarChart
                      setColor={"rgba(255, 206, 86, 0.2)"}
                      dataArr={dataVideo}
                      showLegend={false}
                    />
                  </div>
                )}
                {chartType === "bar" && (
                  <OverallBarChart
                    setColor={"rgba(255, 206, 86, 0.2)"}
                    dataArr={dataVideo}
                    showLegend={false}
                  />
                )}
              </Col>
            </Row>
            <br></br>
            <Row>
              <Col sm={6}>
                <h4>Subject Matter</h4>
                {chartType === "line" && (
                  <OverallLineChart showLegend={false} />
                )}
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
                    <OverallDoughnutChart
                      dataArr={dataTranscript}
                      showLegend={false}
                    />
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
                    <OverallRadarChart
                      setColor={"rgba(75, 192, 192, 0.2)"}
                      dataArr={dataTranscript}
                      showLegend={false}
                    />
                  </div>
                )}
                {chartType === "bar" && (
                  <OverallBarChart
                    setColor={"rgba(75, 192, 192, 0.2)"}
                    dataArr={dataTranscript}
                    showLegend={false}
                  />
                )}
              </Col>
            </Row>
          </Col>
        </Row>
        <br></br>
        <br></br>
      </Container>
    </>
  );
}

export default OverallMaster;
