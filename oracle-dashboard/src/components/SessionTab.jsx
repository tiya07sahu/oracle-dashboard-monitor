import { useState } from "react";

function SessionTab({ sessions }) {
  const [filter, setFilter] = useState("ALL");
  const [searchUser, setSearchUser] = useState("");
  const [searchMachine, setSearchMachine] = useState("");

  
  const filteredSessions = sessions.filter((item) => {
    const statusMatch =
      filter === "ALL" || item.status === filter;

    const userMatch =
      (item.username || "")
        .toLowerCase()
        .includes(searchUser.toLowerCase());

    const machineMatch =
      (item.machine || "")
        .toLowerCase()
        .includes(searchMachine.toLowerCase());

    return statusMatch && userMatch && machineMatch;
  });

  return (
    <>
      <div className="cards">

        <div className="summary-card">
          <h2>Total Sessions</h2>
          <p>{sessions.length}</p>
        </div>
<div className="summary-card active-card">
  <h2>Active</h2>
  <p>
    {filteredSessions.filter(s => s.status === "ACTIVE").length}
  </p>
</div>

<div className="summary-card inactive-card">
  <h2>Inactive</h2>
  <p>
    {filteredSessions.filter(s => s.status === "INACTIVE").length}
  </p>
</div>

<div className="summary-card killed-card">
  <h2>Killed</h2>
  <p>
    {filteredSessions.filter(s => s.status === "KILLED").length}
  </p>
</div>

      </div>


      <div className="card">

        <h2>Session Management</h2>

        <div className="table-container">

          <div className="filter-buttons">

            <button onClick={() => setFilter("ALL")}>
              All
            </button>

            <button onClick={() => setFilter("ACTIVE")}>
              Active
            </button>

            <button onClick={() => setFilter("INACTIVE")}>
              Inactive
            </button>

            <button onClick={() => setFilter("KILLED")}>
              Killed
            </button>

            <input
              type="text"
              className="search-box"
              placeholder="🔍 Search Username..."
              value={searchUser}
              onChange={(e) =>
                setSearchUser(e.target.value)
              }
            />

            <input
              type="text"
              className="search-box"
              placeholder="🔍 Search Machine..."
              value={searchMachine}
              onChange={(e) =>
                setSearchMachine(e.target.value)
              }
            />

            <button
              className="reset-btn"
              onClick={() => {
                setFilter("ALL");
                setSearchUser("");
                setSearchMachine("");
              }}
            >
              Clear Filters
            </button>

          </div>
          <p className="session-count">

  Showing <strong>{filteredSessions.length}</strong> Sessions

  {searchUser && (
    <> | User: <strong>{searchUser}</strong></>
  )}

  {filter !== "ALL" && (
    <> | Status: <strong>{filter}</strong></>
  )}

</p>

          <table>

            <thead>

              <tr>
                <th>SID</th>
                <th>SERIAL#</th>
                <th>USERNAME</th>
                <th>STATUS</th>
                <th>OSUSER</th>
                <th>MACHINE</th>
                <th>PROGRAM</th>
                <th>MODULE</th>
                <th>ACTION</th>
                <th>LOGON TIME</th>
              </tr>

            </thead>

            <tbody>

              {filteredSessions.length === 0 ? (

                <tr>

                  <td
                    colSpan="10"
                    style={{
                      textAlign: "center",
                      padding: "40px",
                      color: "#94a3b8",
                    }}
                  >
                    😕 No Sessions Found
                  </td>

                </tr>

              ) : (

                filteredSessions.map((item, index) => (

                  <tr
                    key={index}
                    style={{
                      backgroundColor:
                        item.status === "ACTIVE"
                          ? "#1f4d2e"
                          : item.status === "INACTIVE"
                          ? "#665300"
                          : item.status === "KILLED"
                          ? "#5a1f1f"
                          : "transparent",
                    }}
                  >

                    <td>{item.sid}</td>
                    <td>{item["serial#"]}</td>
                    <td>{item.username}</td>
                    <td>{item.status}</td>
                    <td>{item.osuser}</td>
                    <td>{item.machine}</td>
                    <td>{item.program}</td>
                    <td>{item.module}</td>
                    <td>{item.action}</td>
                    <td>{item.logon_time}</td>

                  </tr>

                ))

              )}

            </tbody>

          </table>

        </div>

      </div>
    </>
  );
}

export default SessionTab;