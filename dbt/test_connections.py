import snowflake.connector

try:
    conn = snowflake.connector.connect(
        account="AVQXGPE-JC49269",
        user="LIKITH",
        password="YOUR_NEW_PASSWORD",
        warehouse="TELECOM_WH",
        database="TELECOM_DB",
        schema="STAGING",
        role="ACCOUNTADMIN"
    )

    print("✅ Connected successfully!")

    cur = conn.cursor()
    cur.execute("SELECT CURRENT_VERSION()")
    print(cur.fetchone())

    cur.close()
    conn.close()

except Exception as e:
    print("❌ Error:")
    print(e)