import subprocess
from datetime import datetime
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

app = FastAPI()

# --- SECURITY BLOCK START ---
origins = [
    "http://localhost:8080", 
    "https://the-12th-man-app-444179922745.us-central1.run.app" 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"], 
    allow_headers=["*"],
)

@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response

class SOSReport(BaseModel):
    zone: str = Field(..., min_length=1, max_length=50)
    issue_type: str = Field(..., min_length=3, max_length=100)
    urgency: int = Field(..., ge=1, le=5) 

@app.post("/api/sos-report")
async def receive_sos(report: SOSReport):
    print(f"Secure SOS received from Zone {report.zone}")
    return {"status": "success", "message": "Report validated and securely logged."}
# --- SECURITY BLOCK END ---

@app.post("/api/loyalty/scan")
def scan_ticket(req: ScanRequest):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT t.user_id, e.toss_time 
        FROM Tickets t 
        JOIN Events e ON t.event_id = e.event_id 
        WHERE t.ticket_id = ?
    ''', (req.ticket_id,))
    row = cursor.fetchone()

    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="Ticket not found")

    user_id = row['user_id']
    toss_time_str = row['toss_time']

    # Mark ticket as scanned
    cursor.execute('UPDATE Tickets SET scan_time = ? WHERE ticket_id = ?', (req.scan_time, req.ticket_id))

    # Safely parse times
    toss_time = datetime.fromisoformat(toss_time_str.replace("Z", "+00:00"))
    scan_time_obj = datetime.fromisoformat(req.scan_time.replace("Z", "+00:00"))
    
    diff = toss_time - scan_time_obj
    minutes_to_toss = int(diff.total_seconds() / 60)

    # Gamified Reward System
    points = 0
    if minutes_to_toss >= 180:
        points = 200 # Platinum
    elif minutes_to_toss >= 120:
        points = 100 # Gold
    elif minutes_to_toss > 0:
        points = 20 # Standard

    if points > 0:
        cursor.execute('UPDATE Users SET total_loyalty_points = total_loyalty_points + ? WHERE user_id = ?', (points, user_id))
        # Add to Analytics Ledger
        cursor.execute('''
            INSERT INTO Reward_Ledger (user_id, points_awarded, minutes_to_toss, timestamp)
            VALUES (?, ?, ?, ?)
        ''', (user_id, points, minutes_to_toss, req.scan_time))

    conn.commit()
    conn.close()

    return {
        "message": "Scan successful", 
        "points_awarded": points, 
        "minutes_to_toss": minutes_to_toss
    }

@app.get("/api/telemetry/wait-times")
def get_wait_times():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Venue_Wait_Times')
    rows = cursor.fetchall()
    conn.close()
    return [{"gate_name": r['gate_name'], "density_percentage": r['density_percentage']} for r in rows]

@app.get("/api/match/status")
def get_match_status(event_id: Optional[str] = None):
    conn = get_db_connection()
    cursor = conn.cursor()
    if event_id:
        cursor.execute('SELECT * FROM Live_Match_State WHERE event_id = ?', (event_id,))
    else:
        cursor.execute('SELECT * FROM Live_Match_State LIMIT 1')
    
    row = cursor.fetchone()
    conn.close()

    if not row:
        return {"status": "No active match found"}

    return {
        "event_id": row['event_id'],
        "status": row['status'],
        "score": row['score'],
        "overs": row['overs'],
        "batting_team": row['batting_team']
    }

class ChatMessage(BaseModel):
    role: str # "user" or "assistant"
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]

@app.post("/api/ai/chat")
def ai_chat(req: ChatRequest):
    if not req.messages:
        return {"reply": "Hi! I am the AI Concierge. How can I help?"}

    # Extract the last message for context routing
    last_message = req.messages[-1].content.lower()

    # Rule-Based Semantic Routing Mock
    if any(keyword in last_message for keyword in ["rules", "allowed", "power bank"]):
        # Mock Vector DB
        reply = "As per stadium policy, power banks up to 10,000mAh are allowed. Outside food is strictly prohibited."
    elif any(keyword in last_message for keyword in ["wait", "crowd", "line", "gate"]):
        # Mock SQL Agent execution
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT gate_name, density_percentage FROM Venue_Wait_Times ORDER BY density_percentage ASC')
        rows = cursor.fetchall()
        conn.close()
        
        reply = "Here are the live wait times at the venue:\n"
        for r in rows:
            reply += f"- {r['gate_name']}: {r['density_percentage']}% congested\n"
    else:
        reply = "I'm your AI Concierge. You can ask me about stadium rules or live wait times!"

    return {"reply": reply}

# Mount the decoupled frontend directory natively at the root
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
