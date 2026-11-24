import sqlite3
from pathlib import Path


class Database:
    """
    Central SQLite database manager.

    Responsibilities
    ----------------
    • Database connection
    • Table creation
    • Schema migration
    """

    def __init__(self):

        from cae_config.settings import Settings

        self.database_path = Settings.DATABASE_FILE

        self.database_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.create_tables()

        self.migrate_database()

    # --------------------------------------------------
    # Connection
    # --------------------------------------------------

    def connect(self):

        return sqlite3.connect(
            self.database_path
        )

    # --------------------------------------------------

    def get_database_path(self):

        return self.database_path

    # --------------------------------------------------
    # Create Tables
    # --------------------------------------------------

    def create_tables(self):

        conn = self.connect()

        cursor = conn.cursor()

        # ==================================================
        # Opportunities
        # ==================================================

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS opportunities(

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                source TEXT,

                business_name TEXT,

                category TEXT,

                address TEXT,

                phone TEXT,

                website TEXT,

                rating REAL,

                reviews INTEGER,

                opportunity_score INTEGER DEFAULT 0,

                technology TEXT DEFAULT 'Unknown',

                priority TEXT DEFAULT 'MEDIUM',

                recommended_services TEXT,

                status TEXT DEFAULT 'NEW',

                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

            )
            """
        )

        # ==================================================
        # Website Analysis
        # ==================================================

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS website_analysis(

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                opportunity_id INTEGER,

                website_exists INTEGER,

                https_enabled INTEGER,

                contact_form INTEGER,

                email_found INTEGER,

                page_title TEXT,

                meta_description TEXT,

                analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY(opportunity_id)
                    REFERENCES opportunities(id)

            )
            """
        )

        # ==================================================
        # CRM
        # ==================================================

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS crm(

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                opportunity_id INTEGER UNIQUE,

                status TEXT DEFAULT 'NEW',

                last_contacted TIMESTAMP,

                follow_up_date TIMESTAMP,

                notes TEXT DEFAULT '',

                email_generated INTEGER DEFAULT 0,

                proposal_generated INTEGER DEFAULT 0,

                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY(opportunity_id)
                    REFERENCES opportunities(id)

            )
            """
        )

        # ==================================================
        # Proposals
        # ==================================================

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS proposals(

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                proposal_number TEXT UNIQUE,

                opportunity_id INTEGER,

                status TEXT DEFAULT 'DRAFT',

                markdown_path TEXT,

                pdf_path TEXT,

                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY(opportunity_id)
                    REFERENCES opportunities(id)

            )
            """
        )

        # ==================================================
        # Outreach
        # ==================================================

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS outreach(

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                outreach_number TEXT UNIQUE,

                opportunity_id INTEGER,

                status TEXT DEFAULT 'DRAFT',

                folder_path TEXT,

                json_path TEXT,

                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY(opportunity_id)
                    REFERENCES opportunities(id)

            )
            """
        )

        conn.commit()

        conn.close()

        # --------------------------------------------------
    # Database Migration
    # --------------------------------------------------

    def migrate_database(self):
        """
        Execute all database migrations.
        Safe to run every application startup.
        """

        self.migrate_opportunities()

        self.migrate_proposals()

        self.migrate_outreach()

        self.migrate_crm()

    # --------------------------------------------------
    # Opportunities
    # --------------------------------------------------

    def migrate_opportunities(self):

        conn = self.connect()

        cursor = conn.cursor()

        cursor.execute(
            "PRAGMA table_info(opportunities)"
        )

        existing_columns = {
            row[1] for row in cursor.fetchall()
        }

        required_columns = {

            # ------------------------------------------
            # Business Intelligence
            # ------------------------------------------

            "primary_service":
                "TEXT",

            "estimated_value":
                "INTEGER DEFAULT 0",

            "estimated_hours":
                "INTEGER DEFAULT 0",

            "difficulty":
                "TEXT DEFAULT 'Easy'",

            "closing_probability":
                "INTEGER DEFAULT 0",

            "roi_score":
                "INTEGER DEFAULT 0",

            "sales_reason":
                "TEXT",

            "last_contacted":
                "TIMESTAMP",

            "follow_up_date":
                "TIMESTAMP",

            "notes":
                "TEXT DEFAULT ''",

            # ------------------------------------------
            # Website Intelligence
            # ------------------------------------------

            "website_report_json":
                "TEXT",

            "website_findings_json":
                "TEXT",

            "website_structured_findings_json":
                "TEXT",

            # ------------------------------------------
            # Contact Intelligence
            # ------------------------------------------

            "business_email":
                "TEXT",

            "contact_page":
                 "TEXT",

            "facebook_url":
                "TEXT",

            "linkedin_url":
                "TEXT",

            "instagram_url":
                "TEXT",

            "owner_name":
                "TEXT",
        }

        for column, definition in required_columns.items():

            if column not in existing_columns:

                print(
                    f"Migration: opportunities.{column}"
                )

                cursor.execute(

                    f"""

                    ALTER TABLE opportunities

                    ADD COLUMN

                    {column} {definition}

                    """

                )

        conn.commit()

        conn.close()

    # --------------------------------------------------
    # Proposal Migration
    # --------------------------------------------------

    def migrate_proposals(self):

        conn = self.connect()

        cursor = conn.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS proposals(

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                proposal_number TEXT UNIQUE,

                opportunity_id INTEGER,

                status TEXT DEFAULT 'DRAFT',

                markdown_path TEXT,

                pdf_path TEXT,

                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

            )
            """
        )

        conn.commit()

        conn.close()

    # --------------------------------------------------
    # Outreach Migration
    # --------------------------------------------------

    def migrate_outreach(self):

        conn = self.connect()

        cursor = conn.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS outreach(

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                outreach_number TEXT UNIQUE,

                opportunity_id INTEGER,

                status TEXT DEFAULT 'DRAFT',

                folder_path TEXT,

                json_path TEXT,

                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

            )
            """
        )

        conn.commit()

        conn.close()

    # --------------------------------------------------
    # CRM Migration
    # --------------------------------------------------

    def migrate_crm(self):

        conn = self.connect()

        cursor = conn.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS crm(

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                opportunity_id INTEGER UNIQUE,

                status TEXT DEFAULT 'NEW',

                last_contacted TIMESTAMP,

                follow_up_date TIMESTAMP,

                notes TEXT DEFAULT '',

                email_generated INTEGER DEFAULT 0,

                proposal_generated INTEGER DEFAULT 0,

                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

            )
            """
        )

        conn.commit()

        conn.close()
        # --------------------------------------------------
    # Database Version
    # --------------------------------------------------

    def get_schema_version(self):

        conn = self.connect()

        cursor = conn.cursor()

        cursor.execute(
            "PRAGMA user_version"
        )

        version = cursor.fetchone()[0]

        conn.close()

        return version

    # --------------------------------------------------

    def set_schema_version(
        self,
        version,
    ):

        conn = self.connect()

        cursor = conn.cursor()

        cursor.execute(
            f"PRAGMA user_version = {version}"
        )

        conn.commit()

        conn.close()

    # --------------------------------------------------
    # Database Health
    # --------------------------------------------------

    def table_exists(
        self,
        table_name,
    ):

        conn = self.connect()

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT name

            FROM sqlite_master

            WHERE type='table'

            AND name=?
            """,
            (
                table_name,
            ),
        )

        exists = cursor.fetchone() is not None

        conn.close()

        return exists

    # --------------------------------------------------

    def list_tables(self):

        conn = self.connect()

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT name

            FROM sqlite_master

            WHERE type='table'

            ORDER BY name
            """
        )

        tables = [

            row[0]

            for row in cursor.fetchall()

        ]

        conn.close()

        return tables

    # --------------------------------------------------
    # Generic Execute
    # --------------------------------------------------

    def execute(
        self,
        query,
        parameters=(),
    ):

        conn = self.connect()

        cursor = conn.cursor()

        cursor.execute(
            query,
            parameters,
        )

        conn.commit()

        conn.close()

    # --------------------------------------------------
    # Generic Query
    # --------------------------------------------------

    def fetch_all(
        self,
        query,
        parameters=(),
    ):

        conn = self.connect()

        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()

        cursor.execute(
            query,
            parameters,
        )

        rows = cursor.fetchall()

        conn.close()

        return rows

    # --------------------------------------------------

    def fetch_one(
        self,
        query,
        parameters=(),
    ):

        conn = self.connect()

        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()

        cursor.execute(
            query,
            parameters,
        )

        row = cursor.fetchone()

        conn.close()

        return row