import { useState } from "react";

function BackupTab({ backup = [] }) {

  const [search, setSearch] = useState("");

  const filtered = backup.filter(item =>
    item.type.toLowerCase().includes(search.toLowerCase())
  );

  const completed = backup.filter(
    b => b.status === "COMPLETED"
  ).length;

  const failed = backup.filter(
    b => b.status === "FAILED"
  ).length;

  const running = backup.filter(
    b => b.status === "RUNNING"
  ).length;

  return (

    <div className="card">

      <h1>🛡 Backup Monitoring</h1>

      <p>Oracle RMAN Backup History</p>

      {/* Summary Cards */}
<div className="dashboard-cards">

  <div className="dashboard-card blue">
    <div className="card-icon">🛡</div>
    <h4>Total Backups</h4>
    <h1>{backup.length}</h1>
    <p>RMAN Jobs</p>
    <div className="graph blue-line"></div>
  </div>

  <div className="dashboard-card green">
    <div className="card-icon">✅</div>
    <h4>Completed</h4>
    <h1>
      {backup.filter(
        b => b.status === "COMPLETED"
      ).length}
    </h1>
    <p>Successful Backups</p>
    <div className="graph green-line"></div>
  </div>

  <div className="dashboard-card red">
    <div className="card-icon">❌</div>
    <h4>Failed</h4>
    <h1>
      {backup.filter(
        b => b.status === "FAILED"
      ).length}
    </h1>
    <p>Failed Backups</p>
    <div className="graph red-line"></div>
  </div>

  <div className="dashboard-card blue">
    <div className="card-icon">⏳</div>
    <h4>Running</h4>
    <h1>
      {backup.filter(
        b => b.status === "RUNNING"
      ).length}
    </h1>
    <p>Running Jobs</p>
    <div className="graph blue-line"></div>
  </div>

</div>
      {/* Search */}

      <div className="table-toolbar">

        <input
          className="toolbar-search"
          placeholder="🔍 Search Backup Type..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />

      </div>

      <p className="table-count">

        Showing {filtered.length} Backup Records

      </p>

      {/* Table */}

      <div className="table-wrapper">

        <table className="data-table">

          <thead>

            <tr>

              <th>Session</th>
              <th>Backup Type</th>
              <th>Status</th>
              <th>Start Time</th>
              <th>End Time</th>

            </tr>

          </thead>

          <tbody>

            {

              filtered.length > 0 ? (

                filtered.map((item, index) => (

                  <tr key={index}>

                    <td>{item.session}</td>

                    <td>{item.type}</td>

                    <td>

                      <span
                        className={
                          item.status === "COMPLETED"
                            ? "status-green"
                            : item.status === "FAILED"
                            ? "status-red"
                            : "status-orange"
                        }
                      >

                        {item.status}

                      </span>

                    </td>

                    <td>{item.start}</td>

                    <td>{item.end}</td>

                  </tr>

                ))

              ) : (

                <tr>

                  <td colSpan="5" style={{ textAlign: "center" }}>
                    No Backup Data Available
                  </td>

                </tr>

              )

            }

          </tbody>

        </table>

      </div>

    </div>

  );

}

export default BackupTab;