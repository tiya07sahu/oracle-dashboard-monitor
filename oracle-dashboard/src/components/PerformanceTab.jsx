import { useState } from "react";

function PerformanceTab({ performance }) {
console.log("Performance received:", performance);
  const [search, setSearch] = useState("");

  const filtered = performance.filter(item =>
    item.metric.toLowerCase().includes(search.toLowerCase())
  );

  return (

    <div className="card">
      <h1>⚡ Oracle Performance Monitoring</h1>
      <p>
        Real-Time Oracle Database Performance Statistics
      </p>

      {/* Summary Cards */}

      <div className="datafile-summary">

        {filtered.map((item,index)=>(

          <div className="summary-box" key={index}>

            <h4>{item.metric}</h4>

            <h2>

              {Number(item.value).toLocaleString()}

            </h2>

          </div>

        ))}

      </div>

      {/* Toolbar */}

      <div className="table-toolbar">

        <input
          className="toolbar-search"
          placeholder="🔍 Search Metric..."
          value={search}
          onChange={(e)=>setSearch(e.target.value)}
        />

      </div>

      <p className="table-count">

        Showing {filtered.length} Metrics

      </p>

      {/* Table */}

      <div className="table-wrapper">

        <table className="data-table">

          <thead>

            <tr>

              <th>Performance Metric</th>

              <th>Current Value</th>

              <th>Status</th>

            </tr>

          </thead>

          <tbody>

            {

              filtered.map((item,index)=>(

                <tr key={index}>

                  <td>

                    ⚡ {item.metric}

                  </td>

                  <td>

                    {Number(item.value).toLocaleString()}

                  </td>

                  <td>

                    <span className="status-green">

                      Active

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

export default PerformanceTab;