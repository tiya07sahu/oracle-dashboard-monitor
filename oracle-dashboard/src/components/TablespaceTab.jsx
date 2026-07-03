import { useState } from "react";

function TablespaceTab({ tablespaces }) {

  const [filter, setFilter] = useState("ALL");

  const filteredTablespaces =
    filter === "ALL"
      ? tablespaces
      : tablespaces.filter(
          t => t.status === filter
        );

  return (
    <>

      {/* Filter Buttons */}

      <div className="filter-buttons">

        <button onClick={() => setFilter("ALL")}>
          All
        </button>

        <button onClick={() => setFilter("Healthy")}>
          Healthy
        </button>

        <button onClick={() => setFilter("Warning")}>
          Warning
        </button>

        <button onClick={() => setFilter("Critical")}>
          Critical
        </button>

      </div>

      {/* Summary Cards */}

      <div className="cards">

        <div className="summary-card">
          <h2>Total Tablespaces</h2>
          <p>{tablespaces.length}</p>
        </div>

        <div className="summary-card">
          <h2>Healthy</h2>
          <p>
            {
              tablespaces.filter(
                t => t.status === "Healthy"
              ).length
            }
          </p>
        </div>

        <div className="summary-card">
          <h2>Warning</h2>
          <p>
            {
              tablespaces.filter(
                t => t.status === "Warning"
              ).length
            }
          </p>
        </div>

        <div className="summary-card">
          <h2>Critical</h2>
          <p>
            {
              tablespaces.filter(
                t => t.status === "Critical"
              ).length
            }
          </p>
        </div>

      </div>

      {/* Table */}

      <div className="card">

        <h2>Tablespace Monitoring</h2>

        <div className="table-container">

          <table>

            <thead>

              <tr>

                <th>Name</th>
                <th>Max MB</th>
                <th>Allocated MB</th>
                <th>Free MB</th>
                <th>Used MB</th>
                <th>% Used</th>
                <th>Available Extension</th>
                <th>% Free</th>
                <th>Status</th>

              </tr>

            </thead>

            <tbody>

              {filteredTablespaces.map((item, index) => (

                <tr
                  key={index}
                  style={{
                    backgroundColor:
                      item.status === "Critical"
                        ? "#5b1f1f"
                        : item.status === "Warning"
                        ? "#5b4b12"
                        : "#243041"
                  }}
                >

                  <td>{item.tablespace_name}</td>

                  <td>{item.max_mb}</td>

                  <td>{item.allocated_mb}</td>

                  <td>{item.free_mb}</td>

                  <td>{item.used_mb}</td>

                  <td>{item.percentage_used}%</td>

                  <td>{item.available_extension_mb}</td>

                  <td>{item.percentage_free}%</td>

                  <td>

                    <span
                      className={
                        item.status === "Healthy"
                          ? "status-green"
                          : item.status === "Warning"
                          ? "status-yellow"
                          : "status-red"
                      }
                    >
                      {item.status}
                    </span>

                  </td>

                </tr>

              ))}

            </tbody>

          </table>

        </div>

      </div>

    </>
  );
}

export default TablespaceTab;