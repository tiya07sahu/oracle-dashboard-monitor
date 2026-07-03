import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend
} from "chart.js";

import { Doughnut } from "react-chartjs-2";

ChartJS.register(
  ArcElement,
  Tooltip,
  Legend
);

function SessionChart({ sessions }) {

  const active =
    sessions.filter(
      s => s.status === "ACTIVE"
    ).length;

  const inactive =
    sessions.filter(
      s => s.status === "INACTIVE"
    ).length;

  const killed =
    sessions.filter(
      s => s.status === "KILLED"
    ).length;

  const data = {
    labels: [
      "Active",
      "Inactive",
      "Killed"
    ],
    datasets: [
      {
        data: [
          active,
          inactive,
          killed
        ],
        backgroundColor: [
          "#22c55e",
          "#facc15",
          "#ef4444"
        ]
      }
    ]
  };

  return (
    <div className="card">
      <h2>Session Distribution</h2>

      <div
        style={{
          width: "350px",
          margin: "auto"
        }}
      >
        <Doughnut data={data} />
      </div>
    </div>
  );
}

export default SessionChart;