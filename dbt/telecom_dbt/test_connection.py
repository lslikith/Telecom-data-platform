import snowflake.connector

try:
    conn = snowflake.connector.connect(
        account="AVQXGPE-JC49269",
        user="LIKITH",
        password="Likithliki@9535",
        warehouse="TELECOM_WH",
        database="TELECOM_DB",
        schema="STAGING",
        role="ACCOUNTADMIN",
        insecure_mode=True
    )

    print("✅ Connected successfully!")

    conn.close()

except Exception as e:
    print(type(e).__name__)
    print(e)