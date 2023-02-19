import React, {useEffect} from "react";

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

const labels = ["1", "2", "3", "4", "5", "6", "7"];
const subindex = {0: "Anger", 1: "Disgust", 2: "Fear", 3: "Joy", 4: "Neutral", 5: "Sadness", 6: "Surprise"};
const border_subindex = {0: "rgba(255, 99, 132, 1)", 1: "rgba(54, 162, 235, 1)", 2: "rgba(255, 206, 86, 1)", 3: "rgba(75, 192, 192, 1)", 4: "rgba(153, 102, 255, 1)", 5: "rgba(255, 159, 64, 1)", 6: "rgba(255, 99, 132, 1)"};
const background_subindex = {0: "rgba(255, 99, 132, 0.2)", 1: "rgba(54, 162, 235, 0.2)", 2: "rgba(255, 206, 86, 0.2)", 3: "rgba(75, 192, 192, 0.2)", 4: "rgba(153, 102, 255, 0.2)", 5: "rgba(255, 159, 64, 0.2)", 6: "rgba(255, 99, 132, 0.2)"};
const format_func = (lastXDays) => {
    if (lastXDays===undefined) return [];
    let data = [];
    for (let i = 0; i < 7; i++) {
        let temp = {
            label: subindex[i],
            data: [],
            borderColor: border_subindex[i],
            backgroundColor: background_subindex[i]
        };
        for (let j = 0; j < lastXDays.length; j++) {
            temp["data"].push(lastXDays[j][i]);
        }
        data.push(temp);
    }
    return {labels, datasets: data};
}
//
// export const data = {
//   labels,
//   datasets: [
//     {
//       label: "Anger",
//       data: [1, 4, 5, 6, 7, 5, 5],
//       borderColor: "rgba(255, 99, 132, 1)",
//       backgroundColor: "rgba(255, 99, 132, 0.2)",
//     },
//     {
//       label: "Disgust",
//       data: [5, 6, 5, 6, 1, 5, 1],
//       borderColor: "rgba(54, 162, 235, 1)",
//       backgroundColor: "rgba(54, 162, 235, 0.2)",
//     },
//     {
//       label: "Fear",
//       data: [5, 6, 5, 6, 1, 5, 1],
//       borderColor: "rgba(255, 206, 86, 1)",
//       backgroundColor: "rgba(255, 206, 86, 0.2)",
//     },
//     {
//       label: "Joy",
//       data: [5, 6, 5, 6, 1, 5, 1],
//       borderColor: "rgba(75, 192, 192, 1)",
//       backgroundColor: "rgba(75, 192, 192, 0.2)",
//     },
//     {
//       label: "Neutral",
//       data: [5, 6, 5, 6, 1, 5, 1],
//       borderColor: "rgba(128,128,128, 1)",
//       backgroundColor: "rgba(128,128,128, 0.2)",
//     },
//     {
//       label: "Sadness",
//       data: [5, 6, 5, 6, 1, 5, 1],
//       borderColor: "rgba(255, 159, 64, 1)",
//       backgroundColor: "rgba(255, 159, 64, 0.2)",
//     },
//     {
//       label: "Surprise",
//       data: [5, 6, 5, 6, 1, 5, 1],
//       borderColor: "rgba(153, 102, 255, 1)",
//       backgroundColor: "rgba(153, 102, 255, 0.2)",
//     },
//   ],
// };
export function OverallLineChart({dataXDays, showLegend=true}) {
  useEffect(() => {
    console.log("dataXDays", dataXDays);
    const true_data = format_func(dataXDays);
    console.log(true_data)
  })
    let true_data = format_func(dataXDays);
    if (true_data.length===0) return (<div></div>);
    else {
        return (
            <Line
              options={{
                responsive: true,
                plugins: {
                  legend: {
                    position: "top",
                    display: showLegend
                  },
                  title: {
                    display: false,
                  },
                },
              }}
              data={true_data}
            />
        );
    }
}
