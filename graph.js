import React, { useState, useEffect } from "react";
import Chart from "react-apexcharts";
import axios from "axios";

function BarChart({id}) {
  const [chartData, setChartData] = useState({
    categories: [],
    series: [{ name: "Sales on this day", data: [] }],
  });

  useEffect(() => {
    fetchData();
  }, [id]);

  const fetchData = async () => {
    try {
      //const response = await axios.post( 'http://localhost:5000/sales/gengraph',id); // Assuming '/chart-data' is the endpoint from Flask API
      const response = await fetch('http://localhost:5000/sales/gengraph', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: id
      });
      const jsonData = await response.json();
      setChartData({
        categories: jsonData.labels,
        series: [{ name: "Sales on this day", data: jsonData.values }],
      });
    } catch (error) {
      console.error('Error fetching chart data:', error);
    }
  };

  return (
    <div className="container-fluid mb-5">
      
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