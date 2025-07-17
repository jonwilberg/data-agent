import type { ChartData } from '../types/api';
import { isBarChart, isScatterChart } from '../types/api';

interface DataTableProps {
  data: ChartData;
}

export function DataTable({ data }: DataTableProps) {
  if (isBarChart(data)) {
    return (
      <div className="overflow-x-auto">
        <table className="w-full text-sm border-collapse border border-gray-300 text-gray-800">
          <thead>
            <tr className="bg-gray-50">
              <th className="border border-gray-300 px-4 py-2 text-left font-semibold">{data.x_axis_title}</th>
              <th className="border border-gray-300 px-4 py-2 text-left font-semibold">{data.y_axis_title}</th>
            </tr>
          </thead>
          <tbody>
            {data.labels.map((label, index) => (
              <tr key={index} className="hover:bg-gray-50">
                <td className="border border-gray-300 px-4 py-2">{label}</td>
                <td className="border border-gray-300 px-4 py-2">{data.values[index]}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    );
  }
  
  if (isScatterChart(data)) {
    return (
      <div className="overflow-x-auto">
        <table className="w-full text-sm border-collapse border border-gray-300 text-gray-800">
          <thead>
            <tr className="bg-gray-50">
              <th className="border border-gray-300 px-4 py-2 text-left font-semibold">Label</th>
              <th className="border border-gray-300 px-4 py-2 text-left font-semibold">{data.x_axis_title}</th>
              <th className="border border-gray-300 px-4 py-2 text-left font-semibold">{data.y_axis_title}</th>
            </tr>
          </thead>
          <tbody>
            {data.labels.map((label, index) => (
              <tr key={index} className="hover:bg-gray-50">
                <td className="border border-gray-300 px-4 py-2">{label}</td>
                <td className="border border-gray-300 px-4 py-2">{data.x_values[index]}</td>
                <td className="border border-gray-300 px-4 py-2">{data.y_values[index]}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    );
  }
  
  return null;
}