import axios from 'axios';
import React, { useState, useEffect } from 'react';
import DoughnutChart from '../../charts/DoughnutChart';
import { getCssVariable } from '../../utils/Utils';

function DashboardCard06() {
  const [chartData, setChartData] = useState(null);

  useEffect(() => {
    const fetchAPI = async () => {
      try {
        const response = await axios.get("http://localhost:8080/dash1");
        console.log("API Response:", response.data);

        // Convert API response to percentages
        const total = Object.values(response.data).reduce((acc, count) => acc + count, 0);
        const labels = Object.keys(response.data);
        const values = Object.values(response.data).map(count => (count / total) * 100); // Convert to %

        setChartData({
          labels,
          datasets: [
            {
              label: 'Distribución de Estados',
              data: values,
              backgroundColor: [
                getCssVariable('--color-violet-500'),
                getCssVariable('--color-sky-500'),
                getCssVariable('--color-violet-800'),
                getCssVariable('--color-emerald-500'),
                getCssVariable('--color-rose-500'),
              ],
              hoverBackgroundColor: [
                getCssVariable('--color-violet-600'),
                getCssVariable('--color-sky-600'),
                getCssVariable('--color-violet-900'),
                getCssVariable('--color-emerald-600'),
                getCssVariable('--color-rose-600'),
              ],
              borderWidth: 0,
            },
          ],
        });
      } catch (error) {
        console.error("Error fetching API data:", error);
      }
    };

    fetchAPI();
  }, []);

  return (
    <div className="flex flex-col col-span-full sm:col-span-6 xl:col-span-4 bg-white dark:bg-gray-800 shadow-xs rounded-xl">
      <header className="px-5 py-4 border-b border-gray-100 dark:border-gray-700/60">
        <h2 className="font-semibold text-gray-800 dark:text-gray-100">Distribución de Estados</h2>
      </header>
      <div className="p-5">
        {chartData ? (
          <DoughnutChart data={chartData} width={389} height={260} />
        ) : (
          <p className="text-center text-gray-500 dark:text-gray-400">Cargando gráfico...</p>
        )}
      </div>
    </div>
  );
}

export default DashboardCard06;
