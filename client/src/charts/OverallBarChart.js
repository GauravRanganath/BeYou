import React from "react";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";
import { Bar } from "react-chartjs-2";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

export const options = {
  responsive: true,
  plugins: {
    legend: {
      position: "top",
      display: "true",
    },
    title: {
      display: false,
    },
  },
};

export function OverallBarChart({ setColor, dataArr={dataArr}, showLegend = true }) {
  return (
    <Bar
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
        labels: [
          "Anger",
          "Disgust",
          "Fear",
          "Joy",
          "Neutral",
          "Sadness",
          "Surprise",
        ],
        datasets: [
          {
            label: "Dataset 1",
            data: dataArr,
            backgroundColor: setColor,
          },
        ],
      }}
    />
  );
}
