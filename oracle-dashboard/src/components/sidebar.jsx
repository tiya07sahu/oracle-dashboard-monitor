import { useState } from "react";
import {
  FaBars,
  FaHome,
  FaServer,
  FaDatabase,
  FaUsers,
  FaBell,
  FaChevronDown,
  FaChevronRight
} from "react-icons/fa";

function Sidebar({
  activeTab,
  setActiveTab,
  collapsed,
  setCollapsed
})
 {
     const [showDatabase, setShowDatabase] = useState(false);
  return (
    <div className={collapsed ? "sidebar collapsed" :"sidebar"}>
    
      <h2>MENU</h2>
        
        <button
  className="toggle-btn"
  onClick={() => setCollapsed(!collapsed)}
>
  <FaBars />
   </button>

      <button
           className={activeTab === "overview" ? "active" : ""}
           onClick={() => setActiveTab("overview")}
>
             <FaHome />
              {!collapsed && <span>Overview</span>}
      </button>

      <button
        className={activeTab === "server" ? "active" : ""}
        onClick={() => setActiveTab("server")}
      >
        <FaServer />
            {!collapsed && <span>Servers</span>}
      </button>
<button
  className={activeTab === "database" ? "active" : ""}
  onClick={() => {
    console.log("Database clicked");
    setActiveTab("database");
    setShowDatabase(!showDatabase);
  }}
>
  <FaDatabase />

  {!collapsed && (
    <>
      <span style={{ marginLeft: "10px" }}>
        Database Analysis
      </span>

      <span style={{ marginLeft: "auto" }}>
        {showDatabase ? (
          <FaChevronDown />
        ) : (
          <FaChevronRight />
        )}
      </span>
    </>
  )}
</button>

{showDatabase && !collapsed && (
  <div className="submenu">

    <button
      className={activeTab === "tablespace" ? "active" : ""}
      onClick={() => setActiveTab("tablespace")}
    >
      🗄 Tablespaces
    </button>

    <button
      className={activeTab === "datafiles" ? "active" : ""}
      onClick={() => setActiveTab("datafiles")}
    >
      💾 Data Files
    </button>

    <button
  className={activeTab === "performance" ? "active" : ""}
  onClick={() => setActiveTab("performance")}
>
  📈 Performance
</button>

    <button
  className={activeTab === "storage" ? "active" : ""}
  onClick={() => setActiveTab("storage")}
>
  📦 Storage
</button>

 <button
  className={activeTab === "backup" ? "active" : ""}
  onClick={() => setActiveTab("backup")}
>
  🛡 Backup
</button>
  </div>
)}

<button
  className={activeTab === "sessions" ? "active" : ""}
  onClick={() => setActiveTab("sessions")}
>
  <FaUsers />
  {!collapsed && <span>Sessions</span>}
</button>

<button
  className={activeTab === "alerts" ? "active" : ""}
  onClick={() => setActiveTab("alerts")}
>
  <FaBell />
  {!collapsed && <span>Alerts</span>}
</button>
    </div>
  );
}

export default Sidebar;