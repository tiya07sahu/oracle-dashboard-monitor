import { useState } from "react";
function DataFilesTab({ datafiles }) {
   const [searchFile, setSearchFile] = useState("");
   const [selectedTablespace, setSelectedTablespace] =   useState("ALL");
   const [sortOrder, setSortOrder] = useState("DESC"); 
   const totalFiles = datafiles.length;
   const totalSize = datafiles.reduce(
    (sum, file) => sum + Number(file.size_mb),
    0
  );

  const autoExtend = datafiles.filter(
    file => file.autoextend === "YES"
  ).length;

  const available = datafiles.filter(
    file => file.status === "AVAILABLE"
  ).length;
  const filteredData = datafiles
.filter(file => {

  const fileMatch =
    file.file_name
      .toLowerCase()
      .includes(searchFile.toLowerCase());

  const tablespaceMatch =
    selectedTablespace === "ALL" ||
    file.tablespace_name === selectedTablespace;

  return fileMatch && tablespaceMatch;

})
.sort((a,b)=>{

  if(sortOrder==="ASC"){
    return Number(a.size_mb)-Number(b.size_mb);
  }

  return Number(b.size_mb)-Number(a.size_mb);

});

const tablespaces = [
  "ALL",
  ...new Set(datafiles.map(file => file.tablespace_name))
];
  return (

    <div className="card">

      <h1>📁 Oracle Data Files</h1>

      <p>
        Physical database files currently available in Oracle.
      </p>
<div className="dashboard-cards">

  <div className="dashboard-card blue">
    <div className="card-icon">📁</div>
    <h4>Total Files</h4>
    <h1>{totalFiles}</h1>
    <p>Oracle Datafiles</p>
    <div className="graph blue-line"></div>
  </div>

  <div className="dashboard-card green">
    <div className="card-icon">💽</div>
    <h4>Total Size</h4>
    <h1>{(totalSize / 1024).toFixed(1)} GB</h1>
    <p>Allocated Storage</p>
    <div className="graph green-line"></div>
  </div>

  <div className="dashboard-card blue">
    <div className="card-icon">📈</div>
    <h4>Auto Extend</h4>
    <h1>{autoExtend}</h1>
    <p>Enabled Files</p>
    <div className="graph blue-line"></div>
  </div>

  <div className="dashboard-card red">
    <div className="card-icon">✅</div>
    <h4>Available</h4>
    <h1>{available}</h1>
    <p>Healthy Files</p>
    <div className="graph red-line"></div>
  </div>

      </div>
    <div className="table-toolbar">

<input
type="text"
className="toolbar-search"
placeholder="🔍 Search File..."
value={searchFile}
onChange={(e)=>setSearchFile(e.target.value)}
/>

<select
className="toolbar-select"
value={selectedTablespace}
onChange={(e)=>setSelectedTablespace(e.target.value)}
>

{
tablespaces.map((ts,index)=>(
<option key={index} value={ts}>
{ts}
</option>
))
}

</select>

<select
className="toolbar-select"
value={sortOrder}
onChange={(e)=>setSortOrder(e.target.value)}
>

<option value="DESC">
Largest First
</option>

<option value="ASC">
Smallest First
</option>

</select>

<button
className="toolbar-reset"
onClick={()=>{

setSearchFile("");
setSelectedTablespace("ALL");
setSortOrder("DESC");

}}
>

Reset

</button>

</div>
<p className="table-info">

Showing <strong>{filteredData.length}</strong> of{" "}
<strong>{datafiles.length}</strong> Data Files

{selectedTablespace !== "ALL" && (
  <>
    {" "} | Tablespace: <strong>{selectedTablespace}</strong>
  </>
)}

{" "} | {sortOrder === "DESC" ? "Largest First" : "Smallest First"}

</p>
     <div className="table-wrapper">
      <table className="data-table">

        <thead>
          <tr>
            <th>File</th>
            <th>Tablespace</th>
            <th>Size</th>
            <th>Auto Extend</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
         {filteredData.length === 0 ? (
<tr>
<td
colSpan="6"
style={{
textAlign:"center",
padding:"35px",
color:"#94a3b8"
}}
>
No Data Files Found
</td>
</tr>
) : (
            filteredData.map((file,index)=>(
              <tr key={index}>
                <td>
<div className="file-cell">
<div className="file-title">
📄 {file.file_name.split("/").pop()}
</div>
<div className="file-path">
{file.file_name.substring(
0,
file.file_name.lastIndexOf("/")
)}
</div>
</div>
</td>
                <td>{file.tablespace_name}</td>
                <td>{file.size_mb} MB</td>
                <td>
                  <span
                    className={
                      file.autoextend==="YES"
                      ? "badge-blue"
                      : "badge-gray"
                    }
                  >

                    {file.autoextend}
                  </span>
                </td>

                <td>

<span
className={
file.status==="AVAILABLE"
? "status-green"
: "status-red"
}
>

{file.status}

</span>

</td>
              </tr>
            ))
          )}

        </tbody>
      </table>
    </div>
    </div>
  );
}
export default DataFilesTab;