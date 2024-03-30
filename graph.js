import React, { useState, useEffect } from "react";
// import  { useRef } from 'react';
import { Bar } from "react-chartjs-2";

const BarChart = ({ dataroute }) => {
    const [chartData, setChartData] = useState({
        labels: [],
        datasets: [{ label: "Sales on this day", data: [] }],
    });
    let isMounted = true; // Flag to track component mount status
    useEffect(() => {
        fetch(dataroute)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Failed to fetch chart data');
                }
                return response.json();
            })
            .then(jsonData => {
                if (isMounted) {
                    setChartData({
                        labels: jsonData.labels,
                        datasets: [
                            {
                                label: "Sales on this day",
                                data: jsonData.values,
                                backgroundColor: "#f90000", // Customize the color if needed
                            },
                        ],
                    });
                }
            })
            .catch(error => {
                console.error("Error fetching chart data:", error.message);
            });
    
        return () => {
            isMounted = false; // Set isMounted to false when component unmounts
        };
    }, [dataroute]);
    
    

  return (
    <div className="container-fluid mb-5">
      <p>{dataroute}</p>
      <h3 className="text-center mt-3 mb-3">Bar Chart in ReactJS</h3>
      <Bar
        data={chartData}
        options={{
          scales: {
            x: {
              title: {
                display: true,
                text: "Dates",
                color: "#f90000",
                font: { size: 20 },
              },
            },
            y: {
              title: {
                display: true,
                text: "Sales",
                color: "#f90000",
                font: { size: 15 },
              },
            },
          },
          plugins: {
            title: {
              display: true,
              text: "Bar Chart Developed by DevOps Team",
              color: "#f90000",
              font: { size: 30 },
            },
            subtitle: {
              display: true,
              text: "This is a Bar Chart Graph",
              color: "#f90000",
              font: { size: 18 },
            },
            legend: { display: true, position: "right" },
          },
        }}
      />
    </div>
  );
};

export default BarChart;
