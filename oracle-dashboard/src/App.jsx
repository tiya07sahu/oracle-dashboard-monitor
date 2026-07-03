
import { useEffect, useState } from "react";
import "./App.css";

import ServerTab from "./components/ServerTab";
import SessionTab from "./components/SessionTab";
import TablespaceTab from "./components/TablespaceTab";
import OverviewTab from "./components/OverviewTab";
import Sidebar from "./components/SidebarTab";
import DatabaseTab from "./components/DatabaseTab";
import AlertsTab from "./components/AlertsTab";
import DataFilesTab from "./components/DataFilesTab";
import StorageTab from "./components/StorageTab";
import PerformanceTab from "./components/PerformanceTab";
import BackupTab from "./components/BackupTab";

function App() {
  const [tablespaces, setTablespaces] = useState([]);
  const [sessions, setSessions] = useState([]);
  const [server, setServer] = useState([]);
  const [dbName, setDbName] = useState("rundb1");
  const [activeTab, setActiveTab] = useState("overview");
  const [filter, setFilter] = useState("ALL");
  const [collapsed, setCollapsed] = useState(false);
  const [search, setSearch] = useState("");
  const [darkMode,setDarkMode] = useState(true);
  const [datafiles, setDatafiles] = useState([]);
  const [storage, setStorage] = useState([]);
  const [performance, setPerformance] = useState([]);
  const [backup, setBackup] = useState([]);
  // SERVER DATA (loads once)

useEffect(() => {
  fetch("http://127.0.0.1:8000/servers")
    .then((res) => res.json())
    .then((data) => {
  console.log("SERVERS DATA:", data);
  setServer(data);
})
    .catch((err) => {
      console.error(err);
    });
}, []);


// DATABASE DATA (changes with RunDB1 / RunDB2)
useEffect(() => {
fetch(`http://127.0.0.1:8000/tablespaces/${dbName}`)
    .then((res) => {
      console.log("TABLESPACE STATUS:", res.status);
      return res.json();
    })
    .then((data) => {
  console.log("TABLESPACES DATA:", data);
  setTablespaces(data);
})
    .catch((err) => {
      console.error(err);
    });

  fetch(`http://127.0.0.1:8000/sessions/${dbName}`)
    .then((res) => {
      console.log("SESSION STATUS:", res.status);
      return res.json();
    })
    .then((data) => {
  console.log("SESSIONS DATA:", data);
  setSessions(data);
})
    .catch((err) => {
      console.error(err);
    });
    fetch(`http://127.0.0.1:8000/datafiles/${dbName}`)
  .then((res) => res.json())
  .then((data) => {
    console.log("DATAFILES:", data);
    setDatafiles(data);
  })
  .catch(console.error);

}, [dbName]);
useEffect(() => {
  fetch(`http://127.0.0.1:8000/storage/${dbName}`)
    .then(res => res.json())
    .then(data => {
      console.log("STORAGE:", data);
      setStorage(data);
    })
    .catch(console.error);
}, [dbName]);

useEffect(() => {
  fetch(`http://127.0.0.1:8000/performance/${dbName}`)
    .then(res => res.json())
    .then(data => {
      console.log("PERFORMANCE:", data);
      setPerformance(data);
    })
    .catch(console.error);
}, [dbName]);
useEffect(() => {
fetch(`http://localhost:8000/backup/${dbName}`)
  .then(res => res.json())
  .then(data => setBackup(data))
  .catch(console.error);
  }, [dbName]);

console.log("TABLESPACES:", tablespaces);
console.log("SESSIONS:", sessions);
console.log("SERVER:", server);
console.log("BACKUP:", backup);

console.log("TABLESPACES", tablespaces);
  return (
  <div className={darkMode ? "app-layout dark" : "app-layout light"}>

    <Sidebar
      activeTab={activeTab}
      setActiveTab={setActiveTab}
      collapsed={collapsed}
      setCollapsed={setCollapsed}
    />

    <div className="main-content">

      <div className="top-header">

  <div>

    <h1> 
{activeTab === "overview" && "C&IT And Server Dashboard"}
{activeTab === "server" && "Server Monitoring"}
{activeTab === "tablespace" && "Tablespace Monitoring"}
{activeTab === "datafiles" && "Data Files"}
{activeTab === "performance" && "Performance Analysis"}
{activeTab === "storage" && "Storage Management"}
{activeTab === "sessions" && "Session Monitoring"}
{activeTab === "alerts" && "Database Alerts"}
{activeTab === "database" && "Database Analysis"}
</h1>
   {activeTab === "overview" && (
<p>
Monitor Server Health, Storage, Sessions, Performance,
and Database Resources in Real Time
</p>
)}
  </div>


  <div className="header-right">
    <button
      className="theme-btn"
      onClick={() => setDarkMode(!darkMode)}
    >
      {darkMode ? "☀ Light" : "🌙 Dark"}
    </button>

    <div className="time-box">
      {new Date().toLocaleString()}
    </div>
  </div>

</div>
{activeTab !== "overview" && (
     <select
  value={dbName}
  onChange={(e)=>setDbName(e.target.value)}
>
  <option value="rundb1">RunDB1</option>
  <option value="rundb2">RunDB2</option>
</select>
      )}
      
      {activeTab === "overview" && (
        
        <OverviewTab
          tablespaces={tablespaces}
          sessions={sessions}
          server={server}
        />
          
      )}

      {activeTab === "server" && (
        <ServerTab server={server} />
      )}

      {activeTab === "tablespace" && (
        <TablespaceTab tablespaces={tablespaces} />
      )}

      {activeTab === "sessions" && (
        <SessionTab sessions={sessions} />
      )}

      {activeTab === "database" && (
    <DatabaseTab setActiveTab={setActiveTab} />
)}

{activeTab === "datafiles" && (
    <DataFilesTab datafiles={datafiles} />
)}


{activeTab === "storage" && (
  <StorageTab storage={storage} />
)}

{activeTab === "performance" && (
  <PerformanceTab performance={performance} />
)}
{activeTab === "backup" && (
    <BackupTab backup={backup} />
)}

{activeTab==="alerts" && (
<AlertsTab
tablespaces={tablespaces}
sessions={sessions}
/>

)}

    </div>

  </div>
);

}

export default App