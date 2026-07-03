function DatabaseTab({ setActiveTab }) {
  return (
    <div className="card">

      <h1>Database Analysis</h1>

      <p>Select a monitoring module.</p>

      <div className="db-buttons">

        <button onClick={() => setActiveTab("tablespace")}>
          🗄
          <br />
          Tablespaces
        </button>

        <button onClick={() => setActiveTab("datafiles")}>
          💾
          <br />
          Data Files
        </button>

        <button onClick={() => setActiveTab("performance")}>
          📈
          <br />
          Performance
        </button>

        <button onClick={() => setActiveTab("storage")}>
          📦
          <br />
          Storage
        </button>

        {/* NEW */}
        <button onClick={() => setActiveTab("backup")}>
          🛡
          <br />
          Backup
        </button>

      </div>

    </div>
  );
}

export default DatabaseTab;