import {
  RadialBarChart,
  RadialBar,
  PolarAngleAxis
} from "recharts";

function SystemGauge({ title, value, color }) {

  const data = [{ value }];

  return (
    <div className="gauge-card">

      <RadialBarChart
        width={140}
        height={140}
        innerRadius="70%"
        outerRadius="100%"
        data={data}
        startAngle={90}
        endAngle={-270}
      >

        <PolarAngleAxis
          type="number"
          domain={[0,100]}
          tick={false}
        />

        <RadialBar
          dataKey="value"
          cornerRadius={12}
          fill={color}
        />

      </RadialBarChart>

      <h2>{value}%</h2>

      <p>{title}</p>

    </div>
  );
}

export default SystemGauge;