// import {
//   Chart as ChartJS,
//   CategoryScale,
//   LinearScale,
//   BarElement,
//   Tooltip,
//   Legend
// } from "chart.js";

// import { Bar } from "react-chartjs-2";

// ChartJS.register(
//   CategoryScale,
//   LinearScale,
//   BarElement,
//   Tooltip,
//   Legend
// );

// function ServerChart({ server }) {

//   const data = {
//     labels: server.map(item => item.host),
//     datasets: [
//       {
//         label: "CPU %",
//         data: server.map(item => item.cpu),
//         backgroundColor: "#3b82f6"
//       }
//     ]
//   };

//   return (
//     <div className="card">
//       <h2>Server CPU Usage</h2>

//       <Bar
//         data={data}
//         options={{
//           responsive: true,
//           plugins: {
//             legend: {
//               labels: {
//                 color: "white"
//               }
//             }
//           },
//           scales: {
//             x: {
//               ticks: {
//                 color: "white"
//               }
//             },
//             y: {
//               ticks: {
//                 color: "white"
//               }
//             }
//           }
//         }}
//       />
//     </div>
//   );
// }

// export default ServerChart;
function ServerTab() {
  return (
    <h1 style={{ color: "white" }}>
      Server Tab Working
    </h1>
  );
}

export default ServerTab;