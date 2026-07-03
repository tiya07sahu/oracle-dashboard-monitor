import ServerChart from "./ServerChart";
function ServerTab({ server }) {
  return (
    <>
      <div className="cards">

        <div className="summary-card">
    <h2>Total Servers</h2>
    <p>{server.length}</p>
  </div>

      <div className="summary-card active-card">
  <h2>CPU Usage</h2>
  <p>{server[0]?.cpu}%</p>
</div>

<div className="summary-card inactive-card">
  <h2>Memory Usage</h2>
  <p>{server[0]?.memory}%</p>
</div>

<div className="summary-card killed-card">
  <h2>Disk Usage</h2>
  <p>{server[0]?.disk}%</p>
</div>

      </div>
        <ServerChart server={server} />
      <div className="card">
        <h2>Server Health</h2>

        <div className="table-container">
          <table>
            <thead>
              <tr>
                <th>Host</th>
                <th>CPU %</th>
                <th>Memory %</th>
                <th>Disk %</th>
                <th>Status</th>
              </tr>
            </thead>

            <tbody>
              {server.map((item, index) => (
                <tr key={index}>
                  <td>{item.host}</td>
                  <td>{item.cpu}</td>
                  <td>{item.memory}</td>
                  <td>{item.disk}</td>
                  <td>{item.status}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

      </div>
    </>
  );
}

export default ServerTab;