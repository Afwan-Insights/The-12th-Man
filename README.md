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

> <img width="1895" height="871" alt="Screenshot 2026-04-20 163746" src="https://github.com/user-attachments/assets/9f7ac15e-88fa-4119-98c1-b6f49c380f4f" />


---

## 🎯 The Vision
Managing crowd flow for 40,000+ fans requires actionable data, not just passive observation. **The 12th Man** utilizes a dual-source architecture to actively route fans, shave peak congestion, and ensure safe stadium exits.

## 🧠 Core Architecture

### 1. Live Telemetry Engine
Real-time tracking of wait times at entry gates and concessions to intelligently route fans away from bottlenecks.

### 2. AI Semantic Concierge (VenueScout)
A context-aware agent that dynamically handles SOS reporting, stadium policies, and emergency routing based on the user's specific geographic zone in the arena.

<br/>

> <img width="1892" height="866" alt="Screenshot 2026-04-20 163955 end" src="https://github.com/user-attachments/assets/66ac4acd-c2e0-435e-bf2e-e2037626dcc3" />


---

## ⚙️ How the Solution Works

* 🚨 **Crowdsourcing Real-Time Intelligence:** By encouraging attendees to report issues via the SOS camera tool, the crowd transforms from a logistical challenge into our greatest real-time information asset.
* 🤖 **Context-Aware RAG Assistant:** Utilizing a Retrieval-Augmented Generation (RAG) framework, the AI Concierge understands the user's exact context to provide instant, accurate, and calming responses during emergencies, significantly reducing crowd panic.
* 🎟️ **Gamification & Peak Shaving:** Incentivizes early arrivals with dynamic loyalty points and unlocks live offers (e.g., Fast-Track Entry) to stagger crowd flow. 
* 🏆 **High-Engagement Climax:** The gamification loop culminates at the finals, where the fans who scored the highest loyalty points throughout the season are featured and cheered by the crowd on the main stadium screens.
* 🔄 **Dynamic Match States:** When a match concludes, the interface programmatically shifts from an "Entry" state to a "Safe Exit & Transit" state, replacing gate data with live Metro updates and safe drop-off zones.

---

## 💻 Tech Stack & Deployment
* **Backend:** FastAPI (Python), SQLite
* **Frontend:** Vanilla JavaScript, HTML5, CSS3
* **Deployment:** Architected natively through Google Antigravity's MCP and deployed directly from source to **Google Cloud Run** using a serverless containerized architecture.

---

## 🚀 Future Roadmap
While this prototype successfully validates the core crowd-routing logic, the next iterations of The 12th Man would focus on enterprise scale:
1. **Live Ticketing API Integration:** Connecting directly to ticketing providers (e.g., Ticketmaster, BookMyShow) to authenticate users and automatically assign entry zones based on their actual seat blocks.
2. **Computer Vision Telemetry:** Replacing the simulated SQLite database with live edge-computing feeds from stadium security cameras to automatically calculate gate density without requiring manual inputs.
3. **Proactive Push Notifications:** Transitioning the web application into a full PWA (Progressive Web App) to utilize WebSockets, allowing the system to actively push rerouting alerts to fans' lock screens if a gate suddenly becomes congested.<img width="1895" height="871" alt="Screenshot 2026-04-20 163746" src="https://github.com/user-attachments/assets/68098694-6f79-4956-bb94-40ba17609fdf" />
