import sqlite3
from datetime import datetime, timedelta

def setup_database():
    conn = sqlite3.connect('stadium.db')
    cursor = conn.cursor()

    # Drop existing to ensure fresh start if run multiple times
    cursor.execute('DROP TABLE IF EXISTS Reward_Ledger')
    cursor.execute('DROP TABLE IF EXISTS Live_Match_State')
    cursor.execute('DROP TABLE IF EXISTS Venue_Wait_Times')
    cursor.execute('DROP TABLE IF EXISTS Tickets')
    cursor.execute('DROP TABLE IF EXISTS Events')
    cursor.execute('DROP TABLE IF EXISTS Users')

    # Create Tables
    cursor.execute('''
    CREATE TABLE Users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        total_loyalty_points INTEGER DEFAULT 0
    )
    ''')

    cursor.execute('''
    CREATE TABLE Events (
        event_id TEXT PRIMARY KEY,
        name TEXT,
        venue TEXT,
        toss_time TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE Tickets (
        ticket_id TEXT PRIMARY KEY,
        user_id INTEGER,
        event_id TEXT,
        scan_time TEXT,
        FOREIGN KEY (user_id) REFERENCES Users (user_id),
        FOREIGN KEY (event_id) REFERENCES Events (event_id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE Venue_Wait_Times (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        gate_name TEXT,
        density_percentage INTEGER
    )
    ''')

    cursor.execute('''
    CREATE TABLE Live_Match_State (
        event_id TEXT PRIMARY KEY,
        status TEXT,
        score TEXT,
        overs TEXT,
        batting_team TEXT,
        FOREIGN KEY (event_id) REFERENCES Events (event_id)
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE Reward_Ledger (
        ledger_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        points_awarded INTEGER,
        minutes_to_toss INTEGER,
        timestamp TEXT,
        FOREIGN KEY (user_id) REFERENCES Users (user_id)
    )
    ''')

    # Insert Seed Data
    
    # 1. Users
    cursor.execute("INSERT INTO Users (name, total_loyalty_points) VALUES ('Alice', 50)")
    cursor.execute("INSERT INTO Users (name, total_loyalty_points) VALUES ('Bob', 0)")
    
    # 2. Events
    # Simulate an upcoming match (toss in 3 hours) and a past match
    toss_upcoming = (datetime.now() + timedelta(hours=3)).isoformat()
    cursor.execute(f"INSERT INTO Events (event_id, name, venue, toss_time) VALUES ('IPL2026-SRH-RCB-0522', 'SRH vs RCB', 'Rajiv Gandhi International Stadium', '{toss_upcoming}')")
    cursor.execute(f"INSERT INTO Events (event_id, name, venue, toss_time) VALUES ('IPL2026-CSK-MI-0524', 'CSK vs MI', 'M. A. Chidambaram Stadium', '2026-05-24T19:00:00')")
    
    # 3. Tickets
    cursor.execute("INSERT INTO Tickets (ticket_id, user_id, event_id, scan_time) VALUES ('TKT-001', 1, 'IPL2026-SRH-RCB-0522', NULL)")
    cursor.execute("INSERT INTO Tickets (ticket_id, user_id, event_id, scan_time) VALUES ('TKT-002', 2, 'IPL2026-SRH-RCB-0522', NULL)")

    # 4. Venue_Wait_Times
    cursor.executemany("INSERT INTO Venue_Wait_Times (gate_name, density_percentage) VALUES (?, ?)", [
        ('Gate 1', 45),
        ('Gate 2', 20),
        ('Gate 4', 85),
        ('Gate 6', 10),
        ('Concession Stand A', 60)
    ])

    # 5. Live_Match_State
    cursor.execute("INSERT INTO Live_Match_State (event_id, status, score, overs, batting_team) VALUES ('IPL2026-SRH-RCB-0522', 'Live', '145/2', '14.2', 'SRH')")

    conn.commit()
    conn.close()
    print("Database stadium.db setup completed with seed data.")

if __name__ == '__main__':
    setup_database()
