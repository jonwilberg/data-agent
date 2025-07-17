import type { ChartData } from '../types/api';
import { isBarChart, isScatterChart } from '../types/api';
import { BarChart } from './BarChart';
import { ScatterChart } from './ScatterChart';
import { DataTable } from './DataTable';

interface ChartDisplayProps {
  data: ChartData;
}

export function ChartDisplay({ data }: ChartDisplayProps) {
  const renderChart = () => {
    if (isBarChart(data)) {
      return <BarChart data={data} />;
    } else if (isScatterChart(data)) {
      return <ScatterChart data={data} />;
    }
    
    // Fallback for unknown chart types
    return (
      <div className="flex-1 flex items-center justify-center text-gray-500">
        <div className="text-center">
          <div className="text-4xl mb-2">⚠️</div>
          <p>Unsupported chart type: {(data as any).chart_type}</p>
        </div>
      </div>
    );
  };

  return (
    <div className="flex-1 flex flex-col">
      <div className="h-[60%] min-h-0">
        {renderChart()}
      </div>
      
      <div className="h-[40%] overflow-y-auto">
        <div className="p-4">
          <DataTable data={data} />
        </div>
      </div>
    </div>
  );
}