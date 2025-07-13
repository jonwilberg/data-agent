import type { ChartData } from '../types/api';
import { isBarChart, isScatterChart } from '../types/api';
import { BarChart } from './BarChart';
import { ScatterChart } from './ScatterChart';

interface ChartDisplayProps {
  data: ChartData;
}

export function ChartDisplay({ data }: ChartDisplayProps) {
  if (isBarChart(data)) {
    return <BarChart data={data} />;
  } else if (isScatterChart(data)) {
    return <ScatterChart data={data} />;
  }
  
  // Fallback for unknown chart types
  return (
    <div className="h-96 flex items-center justify-center text-gray-500">
      <div className="text-center">
        <div className="text-4xl mb-2">⚠️</div>
        <p>Unsupported chart type: {(data as any).chart_type}</p>
      </div>
    </div>
  );
}