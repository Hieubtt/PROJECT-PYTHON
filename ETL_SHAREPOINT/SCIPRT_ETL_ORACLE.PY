import pandas as pd
from sqlalchemy import create_engine
from office365.sharepoint.client_context import ClientContext
from office365.runtime.auth.client_credential import ClientCredential

# ==========================
# SHAREPOINT CONFIG
# ==========================

site_url = "https://yourcompany.sharepoint.com/sites/yoursite"
client_id = "YOUR_CLIENT_ID"
client_secret = "YOUR_CLIENT_SECRET"

file_url = "/sites/yoursite/Shared Documents/data.xlsx"
local_file = "data.xlsx"

# ==========================
# DOWNLOAD FILE FROM SHAREPOINT
# ==========================

ctx = ClientContext(site_url).with_credentials(
    ClientCredential(client_id, client_secret)
)

with open(local_file, "wb") as local_file_obj:
    ctx.web.get_file_by_server_relative_url(file_url).download(local_file_obj).execute_query()

print("Download Excel success")

# ==========================
# READ EXCEL
# ==========================

df = pd.read_excel(local_file)

print("Data preview:")
print(df.head())

# ==========================
# ORACLE CONNECTION
# ==========================

username = "hieubtt"
password = "hieubtt#2026"
host = "localhost"
port = "1521"
service = "ORCL"

engine = create_engine(
    f"oracle+oracledb://{username}:{password}@{host}:{port}/?service_name={service}"
)

# ==========================
# INSERT DATA TO ORACLE
# ==========================

table_name = "SHAREPOINT_EXCEL_DATA"

df.to_sql(
    table_name,
    engine,
    if_exists="append",
    index=False
)

print("Data inserted into Oracle successfully")
