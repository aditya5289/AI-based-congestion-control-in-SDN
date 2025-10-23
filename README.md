AI-Based Congestion Control in SDN (Full Project)
=================================================
Contents:
- backend/: Flask REST API for model serving and utility endpoints
- ryu_app/: Ryu controller application that integrates ML prediction
- mininet/: Mininet topology script and traffic generator
- ai/: Scripts to generate dataset, train RandomForest model and save model.pkl
- frontend/: React app (simple) to display status and results
- .env.example: Example env file for backend (no real keys)

Quick start (recommended on Ubuntu 20.04):
1) Install system deps:
   sudo apt update
   sudo apt install python3-pip python3-venv git -y
   # for mininet & ryu, follow official docs; a simple install:
   sudo apt-get install mininet -y
   pip3 install ryu

2) Backend:
   cd backend
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   cp .env.example .env
   python server.py

3) AI model:
   cd ai
   python3 train_model.py
   # this will produce model.pkl in ai/

4) Ryu controller app:
   In a separate terminal, run:
   ryu-manager ryu_app/controller_ai.py
   (ensure python path includes ai/model.pkl usage)

5) Mininet topology (run as root):
   sudo python3 mininet/topology.py
   This script will start the topology and generate iperf traffic.

6) Frontend (optional):
   cd frontend
   npm install
   npm start

Notes:
- This project provides a working skeleton with simple ML integration (RandomForest).
- The Ryu controller periodically loads model.pkl and uses simplistic link stats to decide reroutes.
- Adapt and extend for your thesis experiments; see comments in each file for guidance.
