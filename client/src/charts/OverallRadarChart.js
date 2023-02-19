import React from "react";
import {
  Chart as ChartJS,
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend,
} from "chart.js";
import { Radar } from "react-chartjs-2";

ChartJS.register(
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
  Legend
);

export function OverallRadarChart({setColor, dataArr, showLegend=true}) {
  return (
    <Radar
      options={{
        responsive: true,
        plugins: {
          legend: {
            position: "top",
            display: showLegend,
          },
          title: {
            display: false,
          },
        },
      }}
      data={{
        labels: ['Anger', 'Disgust', 'Fear', 'Joy', 'Neutral', 'Sadness', 'Surprise'],
        datasets: [
          {
            label: "# of Votes",
            data: dataArr,
            backgroundColor: setColor,
            borderColor: setColor,
            borderWidth: 1,
          },
        ],
      }}
    />
  );
}
