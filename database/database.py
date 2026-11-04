
import sqlite3
from pathlib import Path
from contextlib import contextmanager


class Database:
    """Manages the SQLite database connection and initialization."""

    def __init__(self, db_path=None):

        if db_path is None:
            db_path = (
                Path(__file__).resolve().parent
                / "school_transport.db"
            )

        self.db_path = Path(db_path)

    @contextmanager
    def connect(self):
        """Open, commit or roll back, and close a connection."""

        connection = sqlite3.connect(self.db_path)

        # Return database rows that can be accessed by column name.
        connection.row_factory = sqlite3.Row

        # Enable foreign-key enforcement for this connection.
        connection.execute("PRAGMA foreign_keys = ON")

        try:
            yield connection
            connection.commit()

        except Exception:
            connection.rollback()
            raise

        finally:
            connection.close()

    def initialize(self):
        """Create the database tables if they do not exist."""

        with self.connect() as connection:

            connection.executescript("""

                CREATE TABLE IF NOT EXISTS learners (
                    learner_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    grade TEXT NOT NULL,
                    contact TEXT NOT NULL
                );


                CREATE TABLE IF NOT EXISTS routes (
                    route_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    distance_km REAL NOT NULL
                        CHECK(distance_km > 0 AND distance_km <= 200)
                );


                CREATE TABLE IF NOT EXISTS route_stops (
                    route_id TEXT NOT NULL,
                    stop_order INTEGER NOT NULL
                        CHECK(stop_order >= 1),
                    stop_name TEXT NOT NULL
                        CHECK(length(trim(stop_name)) > 0),

                    PRIMARY KEY (route_id, stop_order),

                    FOREIGN KEY (route_id)
                        REFERENCES routes(route_id)
                        ON DELETE CASCADE
                );


                CREATE TABLE IF NOT EXISTS vehicles (
                    registration TEXT PRIMARY KEY,
                    vehicle_type TEXT NOT NULL
                        CHECK(vehicle_type IN (
                            'bus', 'minibus', 'van'
                        )),
                    capacity INTEGER NOT NULL,
                    route_id TEXT,

                    CHECK (
                        (vehicle_type = 'bus'
                            AND capacity BETWEEN 31 AND 70)
                        OR
                        (vehicle_type = 'minibus'
                            AND capacity BETWEEN 15 AND 30)
                        OR
                        (vehicle_type = 'van'
                            AND capacity BETWEEN 8 AND 14)
                    ),

                    FOREIGN KEY (route_id)
                        REFERENCES routes(route_id)
                        ON DELETE RESTRICT
                );


                CREATE TABLE IF NOT EXISTS subscriptions (
                    subscription_id TEXT PRIMARY KEY,
                    learner_id TEXT NOT NULL,
                    route_id TEXT NOT NULL,
                    registration TEXT NOT NULL,
                    monthly_charge INTEGER NOT NULL
                        CHECK(monthly_charge >= 0),
                    active INTEGER NOT NULL DEFAULT 1
                        CHECK(active IN (0, 1)),
                    created_at TEXT NOT NULL
                        DEFAULT CURRENT_TIMESTAMP,

                    FOREIGN KEY (learner_id)
                        REFERENCES learners(learner_id),

                    FOREIGN KEY (route_id)
                        REFERENCES routes(route_id),

                    FOREIGN KEY (registration)
                        REFERENCES vehicles(registration)
                );


                CREATE UNIQUE INDEX IF NOT EXISTS
                    one_active_subscription_per_learner
                ON subscriptions(learner_id)
                WHERE active = 1;

            """)

        print("Database initialized successfully.")
