import React, { useState, useEffect } from "react";
import Chart from "react-apexcharts";
import axios from "axios";
import BarChart from "./graph";

function Revenue() {

  const [routeSuffix, setRouteSuffix] = useState('')

  const [chartData, setChartData] = useState({
    categories: [],
    series: [{ name: "Sales on this day", data: [] }],
  });

  const handleDailyRevenue = async () => {
    const response = await axios.get('http://localhost:5000/revenueday')
  }

  const handleMonthlyRevenue = async () => {
    const response = await axios.get('http://localhost:5000/revenuemonth') 
  }

  return (
    <div>
      <button onClick={handleDailyRevenue}>Daily Revenue</button>
      <button onClick={handleMonthlyRevenue}>Monthly Revenue</button>

      <input 
        type="text"
        value={routeSuffix}
        onChange = {(e) => setRouteSuffix(e.target.value)}
      />

      {routeSuffix && routeSuffix.trim() !== '' && (
        <BarChart id={routeSuffix} />
      )}

    </div>
  );
}

export default Revenue;