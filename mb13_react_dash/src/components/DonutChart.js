import React from 'react';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';
import { Doughnut } from 'react-chartjs-2';
import * as d3 from "d3";
import * as d3Collection from 'd3-collection';


ChartJS.register(ArcElement, Tooltip, Legend);

export const DonutChart = ({data}) => {

  const MassageData = (rawData) => {
    rawData.sort((a,b) => {
      return d3.descending(a.value, b.value)
    });

    let massagedData = {
      labels: rawData.map(d=> d.test),
      datasets: [
        {
          label: 'Failure Types',
          data: rawData.map(d=> d.value),
          borderWidth: 1,
          backgroundColor: [
            'rgba(255, 99, 132, 0.2)',
            'rgba(54, 162, 235, 0.2)',
            'rgba(255, 206, 86, 0.2)',
          ],
          borderColor: [
            'rgba(255, 99, 132, 1)',
            'rgba(54, 162, 235, 1)',
            'rgba(255, 206, 86, 1)',
          ],
        }
      ]
    }

    return massagedData
  }

  MassageData(data)

  return(
    <Doughnut data={MassageData(data)} />
  );
}
