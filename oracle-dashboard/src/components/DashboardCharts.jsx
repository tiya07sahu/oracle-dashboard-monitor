import {
  PieChart,
  Pie,
  Cell,
  ResponsiveContainer,
  Legend
} from "recharts";

const data = [
  { name: "Healthy", value: 85 },
  { name: "Critical", value: 15 }
];

const COLORS = ["#00E396", "#FF4560"];

function DashboardCharts() {
  return (
    <div className="chart-card">

      <h2>System Health</h2>

      <ResponsiveContainer width="100%" height={280}>
        <PieChart>

          <Pie
            data={data}
            dataKey="value"
            cx="50%"
            cy="50%"
            innerRadius={60}
            outerRadius={90}
            label
          >
            {data.map((entry, index) => (
              <Cell
                key={index}
                fill={COLORS[index]}
              />
            ))}
          </Pie>

          <Legend />

        </PieChart>
      </ResponsiveContainer>

    </div>
  );
}

export default DashboardCharts;