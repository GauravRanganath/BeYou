import React from "react";

import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";
import { Line } from "react-chartjs-2";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

export const options = {
  responsive: true,
  plugins: {
    legend: {
      position: "top",
    },
    title: {
      display: true,
      text: "Chart.js Line Chart",
    },
  },
};

const labels = ["1", "2", "3", "4", "5", "6", "7"];

export const data = {
  labels,
  datasets: [
    {
      label: "Anger",
      data: [1, 4, 5, 6, 7, 5, 5],
      borderColor: 'rgba(255, 99, 132, 1)',
      backgroundColor: 'rgba(255, 99, 132, 0.2)',
    },
    {
      label: "Disgust",
      data: [5, 6, 5, 6, 1, 5, 1],
      borderColor: 'rgba(54, 162, 235, 1)',
      backgroundColor: 'rgba(54, 162, 235, 0.2)',
    },
    {
      label: "Fear",
      data: [5, 6, 5, 6, 1, 5, 1],
      borderColor: 'rgba(255, 206, 86, 1)',
      backgroundColor: 'rgba(255, 206, 86, 0.2)',
    },
    {
      label: "Joy",
      data: [5, 6, 5, 6, 1, 5, 1],
      borderColor: 'rgba(75, 192, 192, 1)',
      backgroundColor: 'rgba(75, 192, 192, 0.2)',
    },
    {
      label: "Neutral",
      data: [5, 6, 5, 6, 1, 5, 1],
      borderColor: 'rgba(128,128,128, 1)',
      backgroundColor: 'rgba(128,128,128, 0.2)',
    },
    {
      label: "Sadness",
      data: [5, 6, 5, 6, 1, 5, 1],
      borderColor: 'rgba(255, 159, 64, 1)',
      backgroundColor: 'rgba(255, 159, 64, 0.2)',
    },
    {
      label: "Surprise",
      data: [5, 6, 5, 6, 1, 5, 1],
      borderColor: 'rgba(153, 102, 255, 1)',
      backgroundColor: 'rgba(153, 102, 255, 0.2)',
    },
  ],
};

export function OverallLineChart() {
  return <Line options={options} data={data} />;
}
