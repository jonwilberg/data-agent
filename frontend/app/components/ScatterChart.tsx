import {
  Chart as ChartJS,
  LinearScale,
  PointElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Scatter } from 'react-chartjs-2';
import type { ScatterChartData } from '../types/api';

ChartJS.register(
  LinearScale,
  PointElement,
  Title,
  Tooltip,
  Legend
);

interface ScatterChartProps {
  data: ScatterChartData;
}

export function ScatterChart({ data }: ScatterChartProps) {
  const chartData = {
    datasets: [
      {
        label: data.chart_title,
        data: data.x_values.map((x, index) => ({
          x: x,
          y: data.y_values[index],
        })),
        backgroundColor: 'rgba(59, 130, 246, 0.6)',
        borderColor: 'rgba(59, 130, 246, 1)',
        pointRadius: 6,
        pointHoverRadius: 8,
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
      tooltip: {
        callbacks: {
          label: function(context: any) {
            const pointIndex = context.dataIndex;
            const label = data.labels[pointIndex];
            return `${label}: (${context.parsed.x}, ${context.parsed.y})`;
          }
        }
      }
    },
    scales: {
      x: {
        title: {
          display: true,
          text: data.x_axis_title,
        },
        type: 'linear' as const,
        position: 'bottom' as const,
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
      <Scatter data={chartData} options={options} />
    </div>
  );
}