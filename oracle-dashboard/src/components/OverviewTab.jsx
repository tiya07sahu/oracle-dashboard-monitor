
import {
  FaServer,
  FaDatabase,
  FaCheckCircle,
  FaExclamationTriangle,
  FaUsers,
  FaChartPie
} from "react-icons/fa";

function OverviewTab({ tablespaces, sessions, server }) {

  const totalServers = server.length;
  const healthyServers = server.filter(s => s.status === "Healthy").length;
  const unhealthyServers = totalServers - healthyServers;

 const totalDatabases = server.length;

const healthyDatabases =
server.filter(db => db.status === "Healthy").length;

const unhealthyDatabases =
totalDatabases - healthyDatabases;

const criticalTablespaces =
tablespaces.filter(
t => t.status === "Critical"
).length;
  return (
    <>
    <div className="dashboard-cards">

  <div className="dashboard-card blue">
    <div className="card-icon"><FaServer /></div>
    <h4>Total Servers</h4>
    <h1>{totalServers}</h1>
    <p>Connected Servers</p>
    <div className="graph blue-line"></div>
  </div>

  <div className="dashboard-card green">
    <div className="card-icon"><FaCheckCircle /></div>
    <h4>Healthy Servers</h4>
    <h1>{healthyServers}</h1>
    <p>Running Normally</p>
    <div className="graph green-line"></div>
  </div>

  <div className="dashboard-card red">
    <div className="card-icon"><FaExclamationTriangle /></div>
    <h4>Unhealthy Servers</h4>
    <h1>{unhealthyServers}</h1>
    <p>Need Attention</p>
    <div className="graph red-line"></div>
  </div>

  <div className="dashboard-card blue">
    <div className="card-icon"><FaDatabase /></div>
    <h4>Total Databases</h4>
    <h1>{totalDatabases}</h1>
    <p>Connected Databases</p>
    <div className="graph blue-line"></div>
  </div>

  <div className="dashboard-card green">
    <div className="card-icon"><FaDatabase /></div>
    <h4>Healthy Databases</h4>
    <h1>{healthyDatabases}</h1>
    <p>Healthy</p>
    <div className="graph green-line"></div>
  </div>

  <div className="dashboard-card red">
    <div className="card-icon"><FaChartPie /></div>
    <h4>Critical Tablespaces</h4>
    <h1>{criticalTablespaces}</h1>
    <p>Need Attention</p>
    <div className="graph red-line"></div>
  </div>

</div>
    </>
  );
}

export default OverviewTab;