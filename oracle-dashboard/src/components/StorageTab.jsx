
import { useState } from "react";
 
function StorageTab({ storage }) {
console.log("Storage received:", storage);
  const [search, setSearch] = useState("");

  const filtered = storage
    .filter(item =>
      item.tablespace_name
        .toLowerCase()
        .includes(search.toLowerCase())
    )
    .sort((a, b) => b.size_mb - a.size_mb);

  const totalSize = storage.reduce(
    (sum, item) => sum + Number(item.size_mb),
    0
  );

  const largest = storage.length
    ? Math.max(...storage.map(x => Number(x.size_mb)))
    : 0;

  return (

    <div className="card">

      <h1>📦 Storage Management</h1>

      <p>Oracle Tablespace Storage Overview</p>

      <div className="dashboard-cards">

  <div className="dashboard-card blue">
    <div className="card-icon">📦</div>
    <h4>Total Tablespaces</h4>
    <h1>{storage.length}</h1>
    <p>Available Tablespaces</p>
    <div className="graph blue-line"></div>
  </div>

  <div className="dashboard-card green">
    <div className="card-icon">💾</div>
    <h4>Total Storage</h4>
    <h1>{(totalSize / 1024).toFixed(1)} GB</h1>
    <p>Allocated Storage</p>
    <div className="graph green-line"></div>
  </div>

  <div className="dashboard-card red">
    <div className="card-icon">📈</div>
    <h4>Largest</h4>
    <h1>{(largest / 1024).toFixed(1)} GB</h1>
    <p>Largest Tablespace</p>
    <div className="graph red-line"></div>
  </div>

  <div className="dashboard-card blue">
    <div className="card-icon">📊</div>
    <h4>Average</h4>
    <h1>
      {storage.length
        ? (totalSize / storage.length / 1024).toFixed(1)
        : 0} GB
    </h1>
    <p>Average Size</p>
    <div className="graph blue-line"></div>
  </div>

      </div>

      <div className="table-toolbar">

        <input
          className="toolbar-search"
          placeholder="🔍 Search Tablespace..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />

      </div>

      <p className="table-count">

        Showing {filtered.length} Tablespaces

      </p>

      <div className="table-wrapper">

        <table className="data-table">

          <thead>

            <tr>

              <th>Tablespace</th>
              <th>Size</th>
              <th>Status</th>

            </tr>

          </thead>

          <tbody>

            {

              filtered.map((item, index) => (

                <tr key={index}>

                  <td>📦 {item.tablespace_name}</td>

                  <td>{Number(item.size_mb).toFixed(2)} MB</td>

                  <td>

                    <span
                      className={
                        Number(item.size_mb) > 30000
                          ? "status-red"
                          : Number(item.size_mb) > 10000
                          ? "status-orange"
                          : "status-green"
                      }
                    >

                      {
                        Number(item.size_mb) > 30000
                          ? "Critical"
                          : Number(item.size_mb) > 10000
                          ? "Warning"
                          : "Healthy"
                      }

                    </span>

                  </td>

                </tr>

              ))

            }

          </tbody>

        </table>

      </div>

    </div>

  );

}

export default StorageTab;