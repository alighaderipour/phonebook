from sqlalchemy.engine import URL


class Config:
    SECRET_KEY = 'your-secret-key-here'  # Change this for production

    SQLALCHEMY_DATABASE_URI = URL.create(
        "mssql+pyodbc",
        username="sa",
        password="SQL@ mri2025",
        host="Mri-Nobat",
        database="phonebooks",  # Your database name
        query={
            "driver": "ODBC Driver 17 for SQL Server",
            "TrustServerCertificate": "yes",
            "unicode_results": "yes",
            "charset": "utf8",
            "Trusted_Connection": "no"
        }
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False