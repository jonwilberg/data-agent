import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Bar } from 'react-chartjs-2';
import type { BarChartData } from '../types/api';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

interface BarChartProps {
  data: BarChartData;
}

export function BarChart({ data }: BarChartProps) {
  const chartData = {
    labels: data.labels,
    datasets: [
      {
        label: data.chart_title,
        data: data.values,
        backgroundColor: 'rgba(59, 130, 246, 0.6)',
        borderColor: 'rgba(59, 130, 246, 1)',
        borderWidth: 1,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: false,
      },
      title: {
        display: true,
        text: data.chart_title,
      },
    },
    scales: {
      x: {
        title: {
          display: true,
          text: data.x_axis_title,
        },
      },
      y: {
        title: {
          display: true,
          text: data.y_axis_title,
        },
        beginAtZero: true,
      },
    },
  };

  return (
    <div className="h-96">
      <Bar data={chartData} options={options} />
    </div>
  );
}