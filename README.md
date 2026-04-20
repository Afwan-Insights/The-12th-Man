
# The 12th Man - Smart Stadium Assistant

**Live Demo:** https://the-12th-man-app-444179922745.us-central1.run.app/

## 🎯 Chosen Vertical
Event Management & Smart Logistics

## 🧠 Approach and Logic
Managing crowd flow for 40,000+ fans requires actionable data, not just passive observation. The 12th Man utilizes a dual-source architecture:
1. **Live Telemetry Engine:** Real-time tracking of wait times at entry gates and concessions to intelligently route fans.
2. **AI Semantic Concierge:** A context-aware agent that dynamically handles SOS reporting, policies, and emergency routing based on the user's specific stadium zone.

## ⚙️ How the Solution Works
* **Gamification & Peak Shaving:** The application incentivizes early arrivals with dynamic loyalty points and unlocks live offers (e.g., Fast-Track Entry) to stagger crowd flow and prevent gate congestion.
* **Dynamic Match States:** When a match concludes, the interface programmatically shifts from an "Entry" state to a "Safe Exit & Transit" state, replacing gate data with live Metro updates and safe drop-off zones.
* **Serverless Cloud Architecture:** Deployed directly from source to Google Cloud Run, utilizing startup event hooks to ensure high availability. 

## 📝 Assumptions Made
* **Database Volatility:** For this prototype, a SQLite database is auto-generated on container startup to simulate live telemetry. In a full production environment, this would be mapped to a managed instance like Google Cloud SQL (PostgreSQL).
* **AI Routing:** The semantic routing relies on customized Python logic for the prototype, which would be swapped for a dedicated LLM orchestration layer in a production state.