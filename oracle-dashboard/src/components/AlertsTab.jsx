function AlertsTab({ tablespaces, sessions }) {

  const alerts = [];

  // Tablespace Alerts
  tablespaces.forEach((t) => {

    if (
      t.status === "Needs Extension" ||
      t.status === "Critical" ||
      t.percentage_used >= 90
    ) {
      alerts.push({
        priority: "Critical",
        resource: t.tablespace_name,
        module: "Tablespace",
        issue: `${t.percentage_used}% Used`,
        status: "Active"
      });
    }

    else if (t.percentage_used >= 80) {
      alerts.push({
        priority: "Warning",
        resource: t.tablespace_name,
        module: "Tablespace",
        issue: `${t.percentage_used}% Used`,
        status: "Monitoring"
      });
    }

  });

  // Session Alerts
  sessions.forEach((s) => {

    if (s.status === "KILLED") {

      alerts.push({
        priority: "Warning",
        resource: s.username,
        module: "Session",
        issue: "Killed Session",
        status: "Closed"
      });

    }

    else if (s.status === "ACTIVE") {

      alerts.push({
        priority: "Info",
        resource: s.username,
        module: "Session",
        issue: "Active Session",
        status: "Running"
      });

    }

  });

  return (

    <div className="card">

      <h2>🚨 Database Alerts</h2>

      <div className="table-wrapper">

        <table className="data-table">

          <thead>

            <tr>

              <th>Priority</th>
              <th>Resource</th>
              <th>Module</th>
              <th>Issue</th>
              <th>Status</th>

            </tr>

          </thead>

          <tbody>

            {alerts.length > 0 ? (

              alerts.map((a, i) => (

                <tr key={i}>

                  <td>
                    <span
                      className={
                        a.priority === "Critical"
                          ? "status-red"
                          : a.priority === "Warning"
                          ? "status-orange"
                          : "status-green"
                      }
                    >
                      {a.priority}
                    </span>
                  </td>

                  <td>{a.resource}</td>

                  <td>{a.module}</td>

                  <td>{a.issue}</td>

                  <td>{a.status}</td>

                </tr>

              ))

            ) : (

              <tr>

                <td colSpan="5" style={{ textAlign: "center" }}>
                  No Alerts Found
                </td>

              </tr>

            )}

          </tbody>

        </table>

      </div>

    </div>

  );

}

export default AlertsTab;