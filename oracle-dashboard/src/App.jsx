import { useEffect, useState } from "react";
import "./App.css";

function App() {
  const [tablespaces, setTablespaces] = useState([]);
  const [sessions, setSessions] = useState([]);
  const [server, setServer] = useState([]);

  const [dbName, setDbName] = useState("rundb1");

  useEffect(() => {
    fetch(`http://127.0.0.1:8000/tablespaces/${dbName}`)
  .then(res => res.json())
  .then(data => {
    console.log("TABLESPACES:", data);
    setTablespaces(data);
  });

    fetch(`http://127.0.0.1:8000/sessions/${dbName}`)
  .then(res => res.json())
  .then(data => {
    console.log("SESSIONS:", data);
    setSessions(data);
  });

    fetch("http://127.0.0.1:8000/servers")
      .then((res) => res.json())
      .then((data) => setServer(data));
  }, [dbName]);

  return (
    <div className="dashboard">
      <h1>Oracle Database Dashboard</h1>

      <select
  value={dbName}
  onChange={(e) => setDbName(e.target.value)}
>
  <option value="rundb1">RunDB1</option>
  <option value="rundb2">RunDB2</option>
</select>

      {/* Summary Cards */}
      <div className="cards">
        <div className="summary-card">
          <h2>Tablespaces</h2>
          <p>{tablespaces.length}</p>
        </div>

        <div className="summary-card">
          <h2>Sessions</h2>
          <p>{sessions.length}</p>
        </div>

        <div className="summary-card">
          <h2>Servers</h2>
          <p>{server.length}</p>
        </div>
      </div>

      {/* Tables Section */}
      <div className="tables">

        {/* Tablespaces */}
        <div className="card">
          <h2>Tablespaces</h2>

          <table>
            <thead>
              <tr>
                <th>Tablespace Name</th>
              </tr>
            </thead>

            <tbody>
              {tablespaces.map((item, index) => (
                <tr key={index}>
                  <td>{item[0]}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Sessions */}
        <div className="card">
          <h2>Sessions</h2>

          <table>
            <thead>
              <tr>
                <th>Username</th>
                <th>Status</th>
                <th>Machine</th>
              </tr>
            </thead>

            <tbody>
              {sessions.map((item, index) => (
                <tr key={index}>
                  <td>{item[0]}</td>
                  <td>{item[1]}</td>
                  <td>{item[2]}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Server Health */}
        <div className="card">
          <h2>Server Health</h2>

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
    </div>
  );
}

export default App;