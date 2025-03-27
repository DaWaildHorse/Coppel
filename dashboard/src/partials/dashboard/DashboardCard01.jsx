import axios from 'axios';
import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import BarChart01 from '../../charts/BarChart01';
import EditMenu from '../../components/DropdownEditMenu';

function DashboardCard01() {
  const [data, setData] = useState(null);
  const [chartData, setChartData] = useState(null);

  useEffect(() => {
    const fetchAPI = async () => {
      try {
        const response = await axios.get("http://localhost:8080/main");
        console.log("API Response:", response.data);
        setData(response.data);

        // Convert data to format suitable for Chart.js
        const labels = Object.keys(response.data);
        const values = Object.values(response.data).map(time => {
          const parts = time.split(":").map(Number);
          return parts[0] * 3600 + parts[1] * 60 + parts[2]; // Convert hh:mm:ss to total seconds
        });

        setChartData({
          labels,
          datasets: [
            {
              label: "Tiempo de Espera (segundos)",
              data: values,
              backgroundColor: '#6366F1', // Tailwind Violet-500
              borderColor: '#4F46E5',
              borderWidth: 2,
            }
          ]
        });
      } catch (error) {
        console.error("Error fetching API data:", error);
      }
    };

    fetchAPI();
  }, []);

  return (
    <div className="flex flex-col col-span-full sm:col-span-6 xl:col-span-4 bg-white dark:bg-gray-800 shadow-md rounded-xl">
      <div className="px-5 pt-5">
        <header className="flex justify-between items-start mb-2">
          <h2 className="text-lg font-semibold text-gray-800 dark:text-gray-100">Tiempo de Espera</h2>
          <EditMenu align="right" className="relative inline-flex">
            <li><Link className="text-sm text-gray-600 dark:text-gray-300 hover:text-gray-800 dark:hover:text-gray-200 flex py-1 px-3" to="#0">Option 1</Link></li>
            <li><Link className="text-sm text-gray-600 dark:text-gray-300 hover:text-gray-800 dark:hover:text-gray-200 flex py-1 px-3" to="#0">Option 2</Link></li>
            <li><Link className="text-sm text-red-500 hover:text-red-600 flex py-1 px-3" to="#0">Remove</Link></li>
          </EditMenu>
        </header>
      </div>

      {/* Display the text data */}
      <div className="px-5 pb-5">
        {data ? (
          <ul className="list-none space-y-2">
            {Object.entries(data).map(([state, time]) => (
              <li key={state} className="text-gray-800 dark:text-gray-100 text-lg">
                📍 <strong>{state}:</strong> {time}
              </li>
            ))}
          </ul>
        ) : (
          <p className="text-center text-gray-500 dark:text-gray-400">Cargando datos...</p>
        )}
      </div>

      {/* Display the graph */}
      <div className="grow px-5 pb-5">
        {chartData ? (
          <BarChart01 data={chartData} width={400} height={200} />
        ) : (
          <p className="text-center text-gray-500 dark:text-gray-400">Cargando gráfico...</p>
        )}
      </div>
    </div>
  );
}

export default DashboardCard01;
