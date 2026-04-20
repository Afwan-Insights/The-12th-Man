<div align="center">
  <h1>🏟️ The 12th Man</h1>
  <p><b>An AI-Powered Smart Stadium Assistant & Telemetry Dashboard</b></p>
  
  [![Live Demo](https://img.shields.io/badge/Live_Demo-Test_the_App_Here-FF4B4B?style=for-the-badge)](https://the-12th-man-app-444179922745.us-central1.run.app/)
  
  ![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
  ![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)
  ![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat&logo=javascript&logoColor=black)
  ![SQLite](https://img.shields.io/badge/SQLite-07405E?style=flat&logo=sqlite&logoColor=white)
  ![Google Cloud Run](https://img.shields.io/badge/Google_Cloud-4285F4?style=flat&logo=google-cloud&logoColor=white)
</div>

<br/>

> <img width="1895" height="871" alt="Screenshot 2026-04-20 163746" src="https://github.com/user-attachments/assets/13a12fd2-deae-465d-b3c4-b610c900596e" />


---

## 🎯 The Vision
Managing crowd flow for 40,000+ fans requires actionable data, not just passive observation. **The 12th Man** utilizes a dual-source architecture to actively route fans, shave peak congestion, and ensure safe stadium exits.

## 🧠 Core Architecture

### 1. Live Telemetry Engine
Real-time tracking of wait times at entry gates and concessions to intelligently route fans away from bottlenecks.

### 2. AI Semantic Concierge (VenueScout)
A context-aware agent that dynamically handles SOS reporting, stadium policies, and emergency routing based on the user's specific geographic zone in the arena.

<br/>

> <img width="1892" height="866" alt="Screenshot 2026-04-20 163955 end" src="https://github.com/user-attachments/assets/7c9cfbed-a783-437f-8cfb-f322c4e5dfae" />


---

## ⚙️ How the Solution Works

* 🎟️ **Gamification & Peak Shaving:** Incentivizes early arrivals with dynamic loyalty points and unlocks live offers (e.g., Fast-Track Entry) to stagger crowd flow and prevent gate congestion.
* 🔄 **Dynamic Match States:** When a match concludes, the interface programmatically shifts from an "Entry" state to a "Safe Exit & Transit" state, replacing gate data with live Metro updates and safe drop-off zones.
* ☁️ **Serverless Deployment:** Architected natively through Google Antigravity's MCP and deployed directly from source to Google Cloud Run, utilizing startup event hooks to ensure high availability. 

## 📝 Technical Assumptions & Constraints
* **Database Volatility:** For this prototype, a SQLite database is auto-generated on container startup to simulate live telemetry. In a full production environment, this would be mapped to a managed instance like Google Cloud SQL (PostgreSQL).
* **AI Routing:** The semantic routing relies on customized Python logic for the prototype, which would be swapped for a dedicated LLM orchestration layer in a production state.
