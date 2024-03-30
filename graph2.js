import React, { useState, useEffect } from "react";
import Chart from "react-apexcharts";
import axios from "axios";

function BarChart() {
  const [chartData, setChartData] = useState({
    categories: [],
    series: [{ name: "Sales on this day", data: [] }],
  });

  useEffect(() => {
    fetchData();
  }, []);
  
  const fetchData = async () => {
    try {
      const response = await axios.get('http://localhost:5000/graph/65ff25f08691f346bdf92609');
      if (!response.data.labels || !response.data.values) {
        console.error('Error: Labels or values are missing in the response');
        return;
      }
      setChartData({
        categories: response.data.labels,
        series: [{ name: "Sales on this day", data: response.data.values }],
      });
    } catch (error) {
      console.error('Error fetching chart data:', error);
    }
  };
  

  return (
    <div className="container-fluid mb-5">
      <p></p>
      <h3 className="text-center mt-3 mb-3">Bar Chart in ReactJS</h3>
      <Chart
        type="bar"
        width="60%"
        height={500}
        series={chartData.series}
        options={{
          title: {
            text: "Bar Chart Developed by DevOps Team",
            style: { fontSize: "30px" },
          },
          subtitle: {
            text: "This is a Bar Chart Graph",
            style: { fontSize: "18px" },
          },
          colors: ["#f90000"],
          theme: { mode: "light" },
          xaxis: {
            categories: chartData.categories,
            title: {
              text: "Dates",
              style: { color: "#f90000", fontSize: "20px" },
            },
          },
          yaxis: {
            title: {
              text: "Sales",
              style: { color: "#f90000", fontSize: "15px" },
            },
          },
          legend: { show: true, position: "right" },
          dataLabels: { style: { colors: ["#f4f4f4"], fontSize: "15px" } },
        }}
      />
    </div>
  );
}

export default BarChart;