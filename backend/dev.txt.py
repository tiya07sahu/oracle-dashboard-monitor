import streamlit as st
import pandas as pd
import paramiko
import re
import base64
import os
from streamlit_autorefresh import st_autorefresh
from pathlib import Path
from db_conn_new import get_oracle_connection
import socket

# File paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH = os.path.join(BASE_DIR, 'sail_Logo.png')
CSV_PATH = os.path.join(BASE_DIR, 'credentials.csv')

# Target filesystems to highlight
TARGET_FS = ["/dev/sdal", "tmpfs", "/dev/sda2", "/dev/sda4"]

# Database configurations
DB_CONFIGS = ["rundb1", "rundb2" , "devp30"]    


# Tablespace SQL Query
TABLESPACE_QUERY = """
WITH ts_alloc AS (
  SELECT
    tablespace_name,
    SUM(bytes) / 1024 / 1024 AS allocated_mb,
    SUM(DECODE(autoextensible, 'YES', maxbytes, bytes)) / 1024 / 1024 AS max_mb
  FROM dba_data_files
  GROUP BY tablespace_name
),
ts_free AS (
  SELECT
    tablespace_name,
    SUM(bytes) / 1024 / 1024 AS free_mb
  FROM dba_free_space
  GROUP BY tablespace_name
),
ts_autoextend AS (
  SELECT
    tablespace_name,
    SUM(DECODE(autoextensible, 'YES', maxbytes - bytes, 0)) / 1024 / 1024 AS available_extension_mb
  FROM dba_data_files
  GROUP BY tablespace_name
)
SELECT
  a.tablespace_name AS "Tablespace Name",
  ROUND(a.max_mb, 2) AS "Max MB",
  ROUND(a.allocated_mb, 2) AS "Allocated MB",
  ROUND(NVL(f.free_mb, 0), 2) AS "Free MB",
  ROUND((a.allocated_mb - NVL(f.free_mb, 0)), 2) AS "Used MB",
  CASE
    WHEN a.allocated_mb = 0 THEN 0
    ELSE ROUND(((a.allocated_mb - NVL(f.free_mb, 0)) / a.allocated_mb) * 100, 2)
  END AS "Percentage Used",
  ROUND(NVL(x.available_extension_mb, 0), 2) AS "Available Extension MB",
  CASE
    WHEN a.allocated_mb = 0 THEN 0
    ELSE ROUND((NVL(f.free_mb, 0) / a.allocated_mb) * 100, 2)
  END AS "Percentage Free"
FROM ts_alloc a
LEFT JOIN ts_free f ON a.tablespace_name = f.tablespace_name
LEFT JOIN ts_autoextend x ON a.tablespace_name = x.tablespace_name
ORDER BY a.tablespace_name
"""

# Sessions SQL Query
SESSIONS_QUERY = """
SELECT 
    s.sid,
    s.serial#,
    s.username,
    s.status,
    s.osuser,
    s.machine,
    s.program,
    s.module,
    s.action,
    TO_CHAR(s.logon_time, 'DD-MON-YYYY HH24:MI:SS') AS logon_time,
    ROUND((SYSDATE - s.logon_time) * 24, 2) AS hours_connected,
    s.blocking_session,
    s.sql_id,
    s.prev_sql_id,
    ROUND(st.value/1024/1024, 2) AS memory_mb
FROM v$session s
LEFT JOIN v$sesstat st ON s.sid = st.sid AND st.statistic# = (
    SELECT statistic# FROM v$statname WHERE name = 'session pga memory'
)
WHERE s.type = 'USER'
ORDER BY s.status DESC, s.logon_time DESC
"""
DASHBOARD_TITLE = "Server Status Monitoring Dashboard"
HEADER_COLOR = "#19359B"  # A deep, bold blue matching the image
# LOGO_PATH = "/dashboard/dash/bsp_vt/sail_logo.png" # Replace with the actual path or URL to your logo


# === Enhanced Styling ===
def apply_custom_style():
    st.markdown("""
    <style>
    :root {
        --primary: #6366F1;
        --primary-light: #818CF8;
        --primary-dark: #4F46E5;
        --secondary: #8B5CF6;
        --accent: #EC4899;
        --success: #10B981;
        --warning: #F59E0B;
        --danger: #EF4444;
        --bg-primary: #F8FAFC;
        --bg-secondary: #F1F5F9;
        --bg-tertiary: #E2E8F0;
        --card-bg: #FFFFFF;
        --border-color: #E2E8F0;
        --text-primary: #1E293B;
        --text-secondary: #64748B;
        --text-muted: #94A3B8;
    }

    .stApp {
        background: linear-gradient(135deg, #F8FAFC 0%, #F0F4F8 100%);
        color: var(--text-primary) !important;
    }

    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }

    /* Cards & Sections */
    .section {
        background: linear-gradient(135deg, #FFFFFF 0%, #F8FAFC 100%);
        border: 1px solid var(--border-color);
        border-radius: 16px;
        padding: 24px;
        margin: 16px 0;
        box-shadow: 0 4px 20px rgba(99, 102, 241, 0.08);
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }

    .section:hover {
        border-color: var(--primary-light);
        box-shadow: 0 8px 32px rgba(99, 102, 241, 0.12);
        transform: translateY(-2px);
    }

    /* Metrics */
    .metric {
        font-size: 24px;
        font-weight: 600;
        margin-bottom: 8px;
        background: linear-gradient(135deg, var(--primary), var(--secondary));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    div[data-testid="metric-container"] {
        background: linear-gradient(135deg, #FFFFFF 0%, #F8FAFC 100%);
        border: 1.5px solid var(--border-color);
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 2px 12px rgba(99, 102, 241, 0.06);
        transition: all 0.3s ease;
    }

    div[data-testid="metric-container"]:hover {
        border-color: var(--primary-light);
        box-shadow: 0 6px 24px rgba(99, 102, 241, 0.12);
    }

    div[data-testid="metric-container"] > div {
        color: var(--text-primary) !important;
    }

    /* Typography */
    h1, h2, h3, h4, h5, h6 {
        color: var(--text-primary) !important;
        font-weight: 700;
        letter-spacing: -0.5px;
    }

    h1 {
        font-size: 2.5rem;
        background: linear-gradient(135deg, var(--primary), var(--secondary));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 1rem;
    }

    h2 {
        font-size: 1.875rem;
        margin-bottom: 0.75rem;
    }

    h3 {
        font-size: 1.5rem;
        margin-bottom: 0.5rem;
    }

    p {
        color: var(--text-secondary);
        line-height: 1.6;
    }

    /* DataFrames */
    .dataframe {
        background-color: #FFFFFF !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 12px !important;
        overflow: hidden !important;
        box-shadow: 0 2px 8px rgba(99, 102, 241, 0.04);
    }

    .dataframe thead th {
        background: linear-gradient(135deg, #F1F5F9, #E2E8F0) !important;
        color: var(--text-primary) !important;
        border-color: var(--border-color) !important;
        font-weight: 600;
    }

    .dataframe tbody tr {
        border-color: var(--border-color) !important;
    }

    .dataframe tbody tr:hover {
        background-color: #F8FAFC !important;
    }

    .dataframe tbody tr:nth-child(even) {
        background-color: #FFFFFF !important;
    }

    .dataframe tbody tr:nth-child(odd) {
        background-color: #F8FAFC !important;
    }

    .dataframe tbody td {
        color: var(--text-secondary) !important;
    }

    /* Inputs & Controls */
    .stSelectbox > div > div,
    .stMultiSelect > div > div,
    .stTextInput > div > div,
    .stNumberInput > div > div,
    .stTextArea > div > div,
    .stDateInput > div > div {
        background-color: #FFFFFF !important;
        color: var(--text-primary) !important;
        border: 1.5px solid var(--border-color) !important;
        border-radius: 10px !important;
        transition: all 0.3s ease;
    }

    .stSelectbox > div > div:hover,
    .stMultiSelect > div > div:hover,
    .stTextInput > div > div:hover,
    .stNumberInput > div > div:hover,
    .stTextArea > div > div:hover,
    .stDateInput > div > div:hover {
        border-color: var(--primary-light) !important;
        box-shadow: 0 0 12px rgba(99, 102, 241, 0.12) !important;
    }

    .stSelectbox > div > div:focus-within,
    .stMultiSelect > div > div:focus-within,
    .stTextInput > div > div:focus-within,
    .stNumberInput > div > div:focus-within,
    .stTextArea > div > div:focus-within,
    .stDateInput > div > div:focus-within {
        border-color: var(--primary) !important;
        box-shadow: 0 0 16px rgba(99, 102, 241, 0.2) !important;
    }

    /* Buttons */
    .stButton > button {
        background: white !important;
        color: black !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        padding: 12px 28px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.2) !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(99, 102, 241, 0.3) !important;
    }

    /* Expanders */
    .stExpander {
        background-color: transparent !important;
    }

    .stExpander > div {
        background-color: #FFFFFF !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 12px !important;
        transition: all 0.3s ease;
    }

    .stExpander > div:hover {
        border-color: var(--primary-light) !important;
        box-shadow: 0 4px 16px rgba(99, 102, 241, 0.08) !important;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] button {
        background-color: transparent !important;
        border-bottom: 2px solid var(--border-color) !important;
        color: var(--text-secondary) !important;
        transition: all 0.3s ease;
        font-weight: 500;
    }

    .stTabs [data-baseweb="tab-list"] button:hover {
        color: var(--primary) !important;
        border-bottom-color: var(--primary-light) !important;
    }

    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
        background: linear-gradient(135deg, var(--primary), var(--secondary)) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
        border-color: var(--primary) !important;
    }

    /* Status Badges */
    .status-critical {
        background: linear-gradient(135deg, #FEE2E2, #FEL2E2) !important;
        color: #991B1B !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        padding: 8px 12px !important;
        border: 1px solid #FECACA !important;
        display: inline-block;
        box-shadow: 0 2px 8px rgba(239, 68, 68, 0.1);
    }

    .status-warning {
        background: linear-gradient(135deg, #FEF3C7, #FEF08A) !important;
        color: #92400E !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        padding: 8px 12px !important;
        border: 1px solid #FCD34D !important;
        display: inline-block;
        box-shadow: 0 2px 8px rgba(245, 158, 11, 0.1);
    }

    .status-good {
        background: linear-gradient(135deg, #DCFCE7, #D1FAE5) !important;
        color: #166534 !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        padding: 8px 12px !important;
        border: 1px solid #86EFAC !important;
        display: inline-block;
        box-shadow: 0 2px 8px rgba(16, 185, 129, 0.1);
    }

    .status-down {
        background: linear-gradient(135deg, #FCE7F3, #FBE7F3) !important;
        color: #831843 !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        padding: 8px 12px !important;
        border: 1px solid #F472B6 !important;
        display: inline-block;
        box-shadow: 0 2px 8px rgba(236, 72, 153, 0.1);
    }

    /* Scrollbars */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }

    ::-webkit-scrollbar-track {
        background: #F1F5F9;
    }

    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, var(--primary), var(--secondary));
        border-radius: 4px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, var(--primary-light), var(--secondary));
    }

    /* Utility Classes */
    .glass-effect {
        background: rgba(255, 255, 255, 0.8) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid var(--border-color) !important;
    }

    .gradient-text {
        background: linear-gradient(135deg, var(--primary), var(--secondary));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
</style>

    """, unsafe_allow_html=True)

def encode_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            b64 = base64.b64encode(img_file.read()).decode()
        return b64
    except:
        return None

# === Server Monitoring Functions ===
def read_credentials(path):
    try:
        df = pd.read_csv(path)
        required_cols = ["Host", "User", "Password"]
        if not all(col in df.columns for col in required_cols):
            st.error(f"CSV must contain: {required_cols}")
            return []
        return df.to_dict(orient="records")
    except Exception as e:
        st.error(f"Error reading CSV: {e}")
        return []

def ssh_exec(client, cmd):
    stdin, stdout, stderr = client.exec_command(cmd)
    return stdout.read().decode()

def parse_cpu_linux(client):
    try:
        output = ssh_exec(client, "uname")
        if "HP-UX" in output:
            output = ssh_exec(client, "sar 1 1 | tail -1")
            parts = output.split()
            if len(parts) >= 5:
                idle = float(parts[-1])
                return round(100 - idle, 2)
        elif "AIX" in output or "SunOS" in output:
            output = ssh_exec(client, "vmstat 1 2 | tail -1")
            parts = output.split()
            if len(parts) >= 15:
                idle = float(parts[14])
                return round(100 - idle, 2)
        else:
            output = ssh_exec(client, "top -bn1 | grep '%Cpu' || mpstat 1 1")
            idle_match = re.search(r'(\d+.\d+)\s*id', output)
            if idle_match:
                idle = float(idle_match.group(1))
                return round(100 - idle, 2)
    except:
        return None
    return None

def parse_mem_linux(client):
    try:
        os_check = ssh_exec(client, "uname")
        if "HP-UX" in os_check:
            return 1024, 512, 512, 0  # Placeholder
        elif "AIX" in os_check or "SunOS" in os_check:
            output = ssh_exec(client, "vmstat")
            lines = output.strip().splitlines()
            if len(lines) >= 3:
                parts = lines[-1].split()
                if len(parts) >= 5:
                    free = int(parts[4]) // 1024
                    total = 1024
                    used = total - free
                    return total, used, free, 0
        else:
            output = ssh_exec(client, "free -m")
            lines = output.splitlines()
            for line in lines:
                if line.lower().startswith("mem:"):
                    parts = line.split()
                    total = int(parts[1])
                    used = int(parts[2])
                    free = int(parts[3])
                    buff_cache = int(parts[5]) if len(parts) > 5 else 0
                    return total, used, free, buff_cache
    except:
        return None, None, None, None
    return None, None, None, None

def parse_filesystem(client):
    try:
        os_type = ssh_exec(client, "uname").strip()
        if "HP-UX" in os_type:
            output = ssh_exec(client, "bdf")
        elif "AIX" in os_type or "SunOS" in os_type:
            output = ssh_exec(client, "df -k")
        else:
            output = ssh_exec(client, "df -h")

        fs_list = []
        lines = output.strip().splitlines()
        for line in lines[1:]:
            parts = line.split()
            if len(parts) >= 6:
                fs_list.append({
                    "Filesystem": parts[0],
                    "Size": parts[1],
                    "Used": parts[2],
                    "Available": parts[3],
                    "Use%": parts[4],
                    "Mounted on": parts[5]
                })
        return fs_list
    except:
        return []

def colorize_usage(value):
    try:
        val = float(value)
        if val >= 90:
            return '#D32F2F'  # Red
        else:
            return '#388E3C'  # Green
    except:
        return '#9E9E9E'

# === Database Functions ===
def get_status(row):
    max_mb = row["Max MB"]
    pct_free = row["Percentage Free"]
    if pct_free <= (10 if max_mb < 1000 else 5):
        return "Needs Extension"
    return "Normal"

def highlight_status(row):
    max_mb = row["Max MB"]
    pct_free = row["Percentage Free"]
    avail_ext = row["Available Extension MB"]

    if avail_ext < 10000:
        if max_mb >= 1000 and pct_free <= 5:
            color = "#ffcccc"  # Light red
        elif max_mb < 1000 and pct_free <= 10:
            color = "#fff5cc"  # Light yellow
        else:
            color = ""
    else:
        color = ""

    return [f"background-color: {color}"] * len(row)

@st.cache_data(ttl=300)
# def fetch_tablespace_data(env, db):
def fetch_tablespace_data(db):
    try:
        conn = get_oracle_connection(db)
        cursor = conn.cursor()
        cursor.execute(TABLESPACE_QUERY)
        cols = [desc[0] for desc in cursor.description]
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return pd.DataFrame(data, columns=cols)
    except Exception as e:
        st.error(f"Error fetching tablespace data: {e}")
        return pd.DataFrame()

@st.cache_data(ttl=300)
# def fetch_sessions_data(env, db):
def fetch_sessions_data(db):
    try:
        # conn = get_oracle_connection(env, db)
        conn = get_oracle_connection(db)
        cursor = conn.cursor()
        cursor.execute(SESSIONS_QUERY)
        cols = [desc[0] for desc in cursor.description]
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return pd.DataFrame(data, columns=cols)
    except Exception as e:
        st.error(f"Error fetching sessions data: {e}")
        return pd.DataFrame()

@st.cache_data(ttl=300)
# def fetch_db_info(env, db):
def fetch_db_info(db):
    try:
        # conn = get_oracle_connection(env, db)
        conn = get_oracle_connection(db)
        cursor = conn.cursor()

        cursor.execute("SELECT sys_context('USERENV','DB_NAME') FROM dual")
        db_name = cursor.fetchone()[0]

        cursor.execute("SELECT sys_context('USERENV','SERVER_HOST') FROM dual")
        host = cursor.fetchone()[0]

        try:
            ip = socket.gethostbyname(host)
        except:
            ip = "Unavailable"

        cursor.close()
        conn.close()
        # return db_name, ip
        return db_name, host
    except Exception as e:
        return "Unknown", "Unknown"

# === Tab Functions ===
def server_monitoring_tab():
    st_autorefresh(interval=300000, key="refresh_key")  # 5 minutes
    
    st.markdown("### ðŸ–¥ï¸ Server Health Monitoring")
    
    credentials = read_credentials(CSV_PATH)
    if not credentials:
        st.warning("No server credentials found.")
        return

    # Initialize session state for server data if not exists
    if 'server_data_cache' not in st.session_state:
        st.session_state.server_data_cache = {}
    
    # Initialize session state for expanded servers if not exists
    # if 'expanded_servers' not in st.session_state:
    #     st.session_state.expanded_servers = set()

    # Create basic server list with connection test (lightweight)
    # server_list = []
    # for cred in credentials:
    #     host = cred["Host"]
    
    host_list = [cred["Host"] for cred in credentials]
    selected_host = st.selectbox("Select a server:", ["-- Select --"] + host_list)

    if selected_host == "-- Select --":
        st.info("Please select a server to continue.")
        return

    # Get credentials for this server
    selected_cred = next((c for c in credentials if c["Host"] == selected_host), None)
    if not selected_cred:
        st.error("Could not find credentials for selected server.")
        return

    st.write(f"### ðŸ–¥ï¸ Selected Server: **{selected_host}**")
        
        # Check if we have cached data for this server
        # if host in st.session_state.server_data_cache:
        #     cached_data = st.session_state.server_data_cache[host]
        #     server_list.append({
        #         "host": host,
        #         "status": cached_data.get("status", "UNKNOWN"),
        #         "status_level": cached_data.get("status_level", 3),
        #         "credentials": cred
        #     })
        # else:
        #     # Just add basic info without connecting
        #     server_list.append({
        #         "host": host,
        #         "status": "CLICK TO LOAD",
        #         "status_level": 5,
        #         "credentials": cred
        #     })
        
    if selected_host in st.session_state.server_data_cache:
        cached = st.session_state.server_data_cache[selected_host]
        status = cached.get("status", "UNKNOWN")
        level = cached.get("status_level", 3)
    else:
        status = "CLICK LOAD"
        level = 5

    # Display basic status
    st.markdown(f"**Status:** {status} (Level {level})")    

    # Sort servers by status level
    # server_list.sort(key=lambda x: x["status_level"])

    # Display servers
    # for server_info in server_list:
    #     host = server_info["host"]
    #     status = server_info["status"]
    #     cred = server_info["credentials"]
        
    #     # Create unique key for each server expander
    #     expander_key = f"server_expander_{host}"
        
    #     # Check if this server is expanded
    #     is_expanded = st.expander(f"ðŸ–¥ï¸ Server: {host}  â€” Status: **{status}**", expanded=False)
        
    #     if is_expanded:
    #         # Check if we need to fetch data (either not cached or user wants to refresh)
    #         if host not in st.session_state.server_data_cache:
        # ---------------------------------
    # LOAD BUTTON - fetch server data
    # ---------------------------------
    if st.button("ðŸ”„ Load / Refresh Server Data"):
        with st.spinner(f"Connecting to {selected_host}..."):
            server_data = fetch_server_data(selected_cred)
            st.session_state.server_data_cache[selected_host] = server_data
            st.success("Server data updated!")
                # Show loading message
                # with st.spinner(f"Connecting to {host}..."):
                #     # Fetch server data
                #     server_data = fetch_server_data(cred)
                #     # Cache the data
                #     st.session_state.server_data_cache[host] = server_data
            
            # Get cached data
            # data = st.session_state.server_data_cache[host]
            
            # # Display server data
            # display_server_details(host, data)
    if selected_host in st.session_state.server_data_cache:
        st.markdown("### ðŸ“Š Server Details")
        display_server_details(selected_host, st.session_state.server_data_cache[selected_host])
    else:
        st.info("Click the **Load / Refresh** button to fetch server data.")        

def fetch_server_data(cred):
    """Fetch server data via SSH connection"""
    host = cred["Host"]
    user = cred["User"]
    password = cred["Password"]
    
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=host, username=user, password=password, timeout=7)

        cpu = parse_cpu_linux(client)
        cpu_color = colorize_usage(cpu) if cpu is not None else '#9E9E9E'

        if cpu is not None:
            if cpu >= 90:
                row_style = 'background: linear-gradient(145deg, #D32F2F, #F44336);'
                status = 'CRITICAL'
                status_level = 0
            elif cpu >= 80:
                row_style = 'background: linear-gradient(145deg, #F57C00, #FF9800);'
                status = 'NEED ATTENTION'
                status_level = 1
            else:
                row_style = 'background: linear-gradient(145deg, #388E3C, #4CAF50);'
                status = 'UP'
                status_level = 2
        else:
            row_style = 'background: linear-gradient(145deg, #616161, #757575);'
            status = 'UNKNOWN'
            status_level = 3

        mem = parse_mem_linux(client)
        fs = parse_filesystem(client)
        
        client.close()

        return {
            "cpu": cpu,
            "cpu_color": cpu_color,
            "mem": mem,
            "fs": fs,
            "status": status,
            "row_style": row_style,
            "status_level": status_level,
            "connected": True
        }

    except Exception as e:
        return {
            "cpu": None,
            "cpu_color": "#9E9E9E",
            "mem": (None, None, None, None),
            "fs": [],
            "status": "DOWN",
            "row_style": 'background: linear-gradient(145deg, #8B0000, #B71C1C);',
            "status_level": 4,
            "connected": False,
            "error": str(e)
        }

def display_server_details(host, data):
    """Display server details in the expander"""
    cpu = data["cpu"]
    cpu_color = data["cpu_color"]
    row_style = data["row_style"]
    status = data["status"]
    total, used, free, buff_cache = data["mem"]
    fs = data["fs"]
    connected = data["connected"]
    
    if not connected:
        st.markdown(f"""
        <div class='section status-down'>
            <h3>ðŸ›‘ {host} is DOWN</h3>
            <p>Server is not responding to connection attempts</p>
            <p><small>Error: {data.get('error', 'Unknown error')}</small></p>
        </div>
        """, unsafe_allow_html=True)
        return

    # Add refresh button
    col1, col2, col3 = st.columns([1, 1, 8])
    with col1:
        if st.button("ðŸ”„ Refresh", key=f"refresh_{host}"):
            # Clear cache for this server to force refresh
            if host in st.session_state.server_data_cache:
                del st.session_state.server_data_cache[host]
            st.rerun()
    
    with col2:
        st.markdown(f"**Last Updated:** {data.get('last_updated', 'Just now')}")

    st.markdown(f'<div class="section" style="{row_style} color: white;">', unsafe_allow_html=True)
    
    # CPU Metrics
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f'<div class="metric" style="color:{cpu_color}">âš™ï¸ CPU Usage: {cpu if cpu is not None else "N/A"}%</div>', unsafe_allow_html=True)
    
    # Memory Metrics
    if None not in (total, used, free):
        mem_usage_pct = round((used / total) * 100, 2)
        mem_color = colorize_usage(mem_usage_pct)
        with col2:
            st.markdown(f'<div class="metric" style="color:{mem_color}">ðŸ’¾ Memory Usage: {used}MB / {total}MB ({mem_usage_pct}%)</div>', unsafe_allow_html=True)
        st.markdown(f'<div style="color:#E3F2FD; margin-top: 10px;">ðŸ“Š Free: {free}MB | Buff/Cache: {buff_cache}MB</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="metric" style="color:#FFA726;">ðŸ’¾ Memory data unavailable</div>', unsafe_allow_html=True)

    # Filesystem Table
    if fs:
        st.markdown("### ðŸ“ Filesystem Usage")
        df_fs = pd.DataFrame(fs)

        def color_filesystem_usage(val):
            try:
                pct = int(val.strip('%'))
                if pct > 90:
                    return 'color: #D32F2F; font-weight: bold;'  # Red
                else:
                    return 'color: #388E3C; font-weight: bold;'  # Green
            except:
                return ''

        def highlight_target(row):
            if row["Filesystem"] in TARGET_FS:
                return ['background-color: rgba(0,77,64,0.8); color: white; font-weight: bold;'] * len(row)
            else:
                return [''] * len(row)

        st.dataframe(
            df_fs.style
                .apply(highlight_target, axis=1)
                .map(color_filesystem_usage, subset=['Use%']),
            height=300,
            use_container_width=True
        )
    else:
        st.markdown('<div style="color:#FFA726;">ðŸ“ No filesystem info available.</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
    
    # Store last updated time
    import datetime
    data['last_updated'] = datetime.datetime.now().strftime("%H:%M:%S")

def database_monitoring_tab():
    st.markdown("### ðŸ—„ï¸ Oracle Database Tablespace Monitoring")
    
    # Database selection
    col1 = st.columns(1)[0]
    # with col1:
    #     selected_env = st.selectbox("Select Database Environment", list(DB_CONFIGS))
    # with col2:
    #     db_list = DB_CONFIGS[selected_env]
    #     selected_db = st.selectbox("Select Database", db_list)
        
    with col1:
        selected_db = st.selectbox("Select Database", DB_CONFIGS)    

    if selected_db:
        # db_name, ip_address = fetch_db_info(selected_env, selected_db)
        ip_address = fetch_db_info(selected_db)
        
        # REPLACE THIS SECTION - Make database info more compact
        st.markdown(f"""
        <div style='background: linear-gradient(145deg, #1565C0, #1E88E5); border: 1px solid #42A5F5; border-radius: 8px; padding: 12px; margin: 10px 0; box-shadow: 0 4px 10px rgba(0,0,0,0.2);'>
            <div style='display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 15px;'>               
                <span style='color: #FFFFFF ; font-size: 0.9rem;'><strong>Database:</strong> <span style='color: #FFFFFF ;'>{selected_db}</span></span>                
                <span style='color: #FFFFFF ; font-size: 0.9rem;'><strong>Server IP:</strong> <span style='color: #FFFFFF ;'>{ip_address}</span></span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # df = fetch_tablespace_data(selected_env, selected_db)
        df = fetch_tablespace_data(selected_db)
        if df.empty:
            st.warning("No tablespace data available.")
            return

        df["Status"] = df.apply(get_status, axis=1)

        total_ts = len(df)
        needs_ext = (df["Status"] == "Needs Extension").sum()

        # KPI Metrics
        kpi1, kpi2, kpi3 = st.columns(3)
        kpi1.metric(label="Total Tablespaces", value=total_ts)
        kpi2.metric(label="Needs Extension", value=needs_ext, delta=f"{(needs_ext/total_ts)*100:.1f}%" if total_ts else "0%")
        kpi3.metric(label="Normal", value=total_ts - needs_ext)

        st.markdown("---")

        styled_df = df.style.apply(highlight_status, axis=1).format({
            "Max MB": "{:,.0f}",
            "Allocated MB": "{:,.0f}",
            "Free MB": "{:,.0f}",
            "Used MB": "{:,.0f}",
            "Percentage Used": "{:.2f}%",
            "Available Extension MB": "{:,.0f}",
            "Percentage Free": "{:.2f}%",
        })

        st.dataframe(styled_df, height=500, use_container_width=True)

        st.markdown(
            f"<div style='text-align:right; color:#B3E5FC; font-size:0.8em; margin-top: 15px;'>Last updated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}</div>",
            unsafe_allow_html=True
        )
    else:
        st.info("Please select a database.")

def sessions_monitoring_tab():
    st.markdown("### ðŸ‘¥ Oracle Database Sessions Monitoring")
    
    # Database selection
    # col1, col2 = st.columns(2)
    # with col1:
    #     selected_env = st.selectbox("Select Environment", list(DB_CONFIGS.keys()), key="sessions_env")
    # with col2:
    #     db_list = DB_CONFIGS[selected_env]
    #     selected_db = st.selectbox("Select Database", db_list, key="sessions_db")
    col1 = st.columns(1)[0]
    with col1:
    #     selected_env = st.selectbox("Select Environment", list(DB_CONFIGS.keys()), key="sessions_env")
    # with col2:
    #     db_list = DB_CONFIGS[selected_env]
        selected_db = st.selectbox("Select Database", DB_CONFIGS, key="sessions_db")

    if selected_db:
        # db_name, ip_address = fetch_db_info(selected_env, selected_db)
        ip_address = fetch_db_info(selected_db)
        st.markdown(f"""
        <div style='background: linear-gradient(145deg, #1565C0, #1E88E5); border: 1px solid #42A5F5; border-radius: 8px; padding: 12px; margin: 10px 0; box-shadow: 0 4px 10px rgba(0,0,0,0.2);'>
            <div style='display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 15px;'>                
                <span style='color: #FFFFFF ; font-size: 0.9rem;'><strong>Database:</strong> <span style='color: #FFFFFF ;'>{selected_db}</span></span>               
                <span style='color: #FFFFFF ; font-size: 0.9rem;'><strong>Server IP:</strong> <span style='color: #FFFFFF ;'>{ip_address}</span></span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # df_sessions = fetch_sessions_data(selected_env, selected_db)
        df_sessions = fetch_sessions_data(selected_db)
        if df_sessions.empty:
            st.warning("No session data available.")
            return

        # Session Statistics
        total_sessions = len(df_sessions)
        active_sessions = len(df_sessions[df_sessions['STATUS'] == 'ACTIVE'])
        inactive_sessions = len(df_sessions[df_sessions['STATUS'] == 'INACTIVE'])
        blocked_sessions = len(df_sessions[df_sessions['BLOCKING_SESSION'].notna()])

        # KPI Metrics
        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        kpi1.metric(label="Total Sessions", value=total_sessions)
        kpi2.metric(label="Active Sessions", value=active_sessions)
        kpi3.metric(label="Inactive Sessions", value=inactive_sessions)
        kpi4.metric(label="Blocked Sessions", value=blocked_sessions)

        st.markdown("---")

        # Filter options
        st.markdown("#### ðŸ” Filter Options")
        filter_col1, filter_col2, filter_col3 = st.columns(3)
        
        with filter_col1:
            status_filter = st.multiselect(
                "Filter by Status",
                options=df_sessions['STATUS'].unique(),
                default=df_sessions['STATUS'].unique()
            )
        
        with filter_col2:
            username_filter = st.multiselect(
                "Filter by Username",
                options=df_sessions['USERNAME'].dropna().unique(),
                default=df_sessions['USERNAME'].dropna().unique()
            )
        
        with filter_col3:
            min_hours = st.number_input("Min Hours Connected", min_value=0.0, value=0.0, step=0.1)

        # Apply filters
        filtered_df = df_sessions[
            (df_sessions['STATUS'].isin(status_filter)) &
            (df_sessions['USERNAME'].isin(username_filter)) &
            (df_sessions['HOURS_CONNECTED'] >= min_hours)
        ]

        # Session status highlighting
        def highlight_session_status(row):
            status = row['STATUS']
            if status == 'ACTIVE':
                return ['background-color: rgba(76, 175, 80, 0.3);'] * len(row)  # Light green
            elif status == 'INACTIVE':
                return ['background-color: rgba(255, 193, 7, 0.3);'] * len(row)  # Light yellow
            elif status == 'KILLED':
                return ['background-color: rgba(244, 67, 54, 0.3);'] * len(row)  # Light red
            else:
                return [''] * len(row)

        # Display filtered sessions
        st.markdown(f"#### ðŸ“‹ Session Details ({len(filtered_df)} sessions)")
        
        if not filtered_df.empty:
            styled_sessions = filtered_df.style.apply(highlight_session_status, axis=1).format({
                'HOURS_CONNECTED': '{:.2f}',
                'MEMORY_MB': '{:.2f}'
            })
            
            st.dataframe(styled_sessions, height=600, use_container_width=True)
        else:
            st.info("No sessions match the current filters.")

        # Session summary by user
        st.markdown("#### ðŸ“Š Sessions Summary by User")
        if not filtered_df.empty:
            user_summary = filtered_df.groupby(['USERNAME', 'STATUS']).size().reset_index(name='Count')
            user_pivot = user_summary.pivot(index='USERNAME', columns='STATUS', values='Count').fillna(0).astype(int)
            st.dataframe(user_pivot, use_container_width=True)

        st.markdown(
            f"<div style='text-align:right; color:#B3E5FC; font-size:0.8em; margin-top: 15px;'>Last updated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}</div>",
            unsafe_allow_html=True
        )
    else:
        st.info("Please select a database.")

# === Main Application ===
# def main():
#     st.set_page_config(page_title="BSP C&IT Server Status Monitoring Dashboard", layout="wide", initial_sidebar_state="expanded")
#     apply_custom_style()

#     # Header with logo
#     logo_b64 = encode_image(LOGO_PATH)
#     if logo_b64:
#         st.markdown(f"""
#         <div style='display:flex; align-items:center; margin-bottom:30px; padding: 20px; background: linear-gradient(145deg, #0D47A1, #1976D2); border-radius: 15px; box-shadow: 0 8px 25px rgba(0,0,0,0.3);'>
#             <img src="data:image/png;base64,{logo_b64}" style="width:150px; margin-right:50px; filter: drop-shadow(2px 2px 4px rgba(0,0,0,0.3));" />
#             <div>
#                 <h1 style='color:white; margin:0; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);'>Bhilai Steel Plant - C&IT</h1>
#                 <h3 style='color:#E3F2FD; margin:0; font-weight:300;'>Advanced Monitoring Dashboard</h3>
#             </div>
#         </div>
#         """, unsafe_allow_html=True)
#     else:
#         st.markdown("""
#         <div style='margin-bottom:30px; padding: 25px; background: linear-gradient(145deg, #0D47A1, #1976D2); border-radius: 15px; box-shadow: 0 8px 25px rgba(0,0,0,0.3);'>
#             <h1 style='color:white; margin:0; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);'>Bhilai Steel Plant - C&IT</h1>
#             <h3 style='color:#E3F2FD; margin:0; font-weight:300;'>Advanced Monitoring Dashboard</h3>
#         </div>
#         """, unsafe_allow_html=True)
        
def main():
    # Set wide layout for maximum space
    st.set_page_config(layout="wide")

    # 1. Custom CSS for the Header Block
    st.markdown(
        f"""
        <style>
        /* Container for the entire header */
        .header-container {{
            background-color: {HEADER_COLOR};
            padding: 10px 20px;
            display: flex; /* Enables flexbox for content alignment */
            align-items: center; /* Vertically center logo and text */
            
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* Optional: subtle shadow */
        }}
        /* Styling for the Logo image */
        .header-logo {{
            height: 50px; /* Adjust height as needed */
            width: auto;
            margin-right: 15px;
            background-color: white; /* Mimics the white background behind the logo */
            border-radius: 5px; /* Optional: slight rounding for the white block */
            padding: 5px;
        }}
        /* Styling for the Title text */
        .header-title {{
            color: white;
            font-size: 2.5em;
            font-weight: 700;
            margin: 0; /* Remove default paragraph margins */
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

    # 2. Render the Header using HTML
    # Note: Replace 'LOGO_PATH' with the actual source of your image
    header_html = f"""
    <div class="header-container">
        
        <p class="header-title">{DASHBOARD_TITLE}</p>
    </div>
    """

    # Because Streamlit image embedding is tricky with pure HTML, we'll use columns for the logo and title:
    logo_col, title_col = st.columns([0.5, 7])

    # with logo_col:
    #     # Use a placeholder image or a simple text/emoji if you don't have the file path
    #     # If you have the image file, use st.image(LOGO_PATH, width=50) here
    #     st.markdown(
    #         f"""
    #         <div class="header-container" style="background-color: {HEADER_COLOR}; padding: 10px 0px 10px 20px; margin: -20px 0 -20px -20px; justify-content: start;">
    #             <img src='https://via.placeholder.com/50/FFFFFF?text=SAIL' class="header-logo" style="height: 50px; background-color: white; padding: 5px; border-radius: 5px;">
    #         </div>
    #         """, unsafe_allow_html=True
    #     )


    # with title_col:
    st.markdown(
        f"""
        <div class="header-container" style="background-color: {HEADER_COLOR}; padding: 10px 20px 10px 0px; margin: -20px -20px -20px 0; justify-content: center;">
            <p class="header-title">{DASHBOARD_TITLE}</p>
        </div>
        """, unsafe_allow_html=True
    )
        
    # Hack to clean up the space after the header and ensure the whole line is blue
    st.markdown(
        f"""
        <style>
        .css-1dp5vir {{ visibility: hidden; }} /* Hides the column gutter */
        .css-1lcbmhc {{ padding-top: 0rem; }} /* Adjusts top padding of main container */
        </style>
        """,
        unsafe_allow_html=True
    )

    # 3. Separator and Main Content
    st.markdown("<hr style='margin-top: 0; margin-bottom: 20px;'>", unsafe_allow_html=True)
    # st.write("Your main dashboard content starts here...")        

    # Create tabs
    tab1, tab2, tab3 = st.tabs(["ðŸ–¥ï¸ Server Monitoring", "ðŸ—„ï¸ Database Monitoring", "ðŸ‘¥ Sessions Monitoring"])
    
    with tab1:
        server_monitoring_tab()
    
    with tab2:
        database_monitoring_tab()
    
    with tab3:
        sessions_monitoring_tab()

if __name__ == "__main__":
    main()