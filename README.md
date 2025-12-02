<div align="center">

# 🛰️ **AI-Based Congestion Control in SDN**  
### 🚀 *Hybrid LSTM + DQN Framework for Intelligent, Proactive Traffic Engineering*

<img src="banner.svg" width="100%" alt="Project Banner">

---

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Click%20Here-blue?style=for-the-badge)](https://chat.qwen.ai/s/deploy/t_c71b65ef-a811-4795-97ee-73fd25bca398)
[![Video Demo](https://img.shields.io/badge/Video%20Demo-Watch%20Now-red?style=for-the-badge)](https://screenrec.com/share/tPUz4E7hH2)
![Python](https://img.shields.io/badge/Python-3.8%2B-yellow?style=for-the-badge)
![Ryu](https://img.shields.io/badge/SDN-Ryu%20Controller-red?style=for-the-badge)
![Mininet](https://img.shields.io/badge/Emulation-Mininet-lightgrey?style=for-the-badge)
![AI](https://img.shields.io/badge/AI-LSTM%20%2F%20DQN-green?style=for-the-badge)

---

<img src="assets/logo.png" width="180px" alt="Project Logo">

### *“Predict congestion before it happens. Reroute traffic before failures occur.”*

</div>

---

## 🎥 **Demo Previews**

### 🔹 **GIF Preview (Working Application)**
> _GIF will be uploaded soon._  
> ![Demo GIF Placeholder](assets/demo.gif)

### 🔹 **Full Video Demonstration**
🎬 [Watch the full demo](https://screenrec.com/share/tPUz4E7hH2)

---

## 📘 **Overview**

This is a **research-grade full-stack SDN-AI system** integrating:

- 🔮 **LSTM** for congestion prediction  
- 🧠 **DQN** for intelligent routing decisions  
- 🔌 **Ryu SDN controller** for OpenFlow rule installation  
- 🧪 **Mininet** topology emulation  
- 🖥️ **React dashboard**  
- ⚙️ **Flask model server**

This repository is ideal for:  
✔ M.Tech / B.Tech Thesis  
✔ IEEE / Elsevier Research Papers  
✔ Industry SDN-AI Prototypes  
✔ Academic Tutorials & Workshops  

---

## 🏗️ **Architecture**

```mermaid
flowchart TD
    A[Mininet Hosts & Switches] -->|Telemetry| B[Ryu SDN Controller]
    B --> C[LSTM Predictor]
    B --> D[DQN Routing Agent]
    C --> E[Congestion Risk Score]
    D --> F[Optimal Path Decision]
    E --> B
    F --> B
    B -->|OpenFlow Rules| A

    epository Structure
1234567891011
AI-SDN/
│
├── backend/        # Flask inference API
├── ryu_app/        # Ryu controller logic + AI integration
├── mininet/        # Topologies, iperf traffic, utilities
├── ai/             # Dataset, training scripts, LSTM/DQN models
├── frontend/       # React dashboard
│
├── assets/         # Banner, logo, GIFs, graphs
├── .env.example    # Environment template

⚡ Features
🔮 Predictive Congestion Control
LSTM forecasts link congestion 3–5 seconds ahead.
🧠 Intelligent Routing with DQN
Learns optimal routing using a custom reward function.
⚙️ Real-Time SDN Integration
Ryu instantly installs OpenFlow rules after AI decisions.
🧪 Rich Emulation Environment
Supports Fat-tree, Mesh, Linear, and Leaf-Spine topologies.
📊 Interactive Dashboard
React UI displays congestion alerts, link utilization, and flow rules.
🛠️ Setup Guide
1️⃣ Install System Dependencies
bash
1234
sudo apt update
sudo apt install python3-pip python3-venv git -y
sudo apt-get install mininet -y
pip3 install ryu
2️⃣ Backend Setup
bash
123456
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python server.py
3️⃣ Train LSTM/DQN Models
bash
12
cd ai
python3 train_model.py
Trained artifacts: model.pkl, reward_curve.png, accuracy_graph.png

4️⃣ Run Ryu Controller
bash
1
ryu-manager ryu_app/controller_ai.py
5️⃣ Start Mininet
bash
1
sudo python3 mininet/topology.py
6️⃣ Launch React Dashboard
bash
123
cd frontend
npm install
npm start
📡 Backend API Documentation
Endpoint
Method
Description
/predict
POST
Returns congestion probability
/stats
GET
Provides real-time port statistics
/route
POST
Computes optimal route via DQN
/health
GET
Health status of backend service
🧠 Dataset & Training
Input Features
Bandwidth usage
Packet drop rate
Queue length
RTT
Inter-arrival times
Training Details
Model
Epochs / Episodes
Optimizer
Loss Function
LSTM
50
Adam
MSE
DQN
5,000 episodes
Q-Learning
TD Error
📊 Performance Graphs
Graphs will be generated after training.

accuracy_graph.png
reward_curve.png
latency_comparison.png
🗺️ Project Roadmap
✅ LSTM congestion predictor
✅ DQN intelligent routing agent
✅ SDN integration with Ryu
✅ Mininet support
✅ React frontend
⬜ Multi-agent RL support
⬜ Transformer-based predictor
⬜ sFlow/NetFlow integration
⬜ Intent-Based Networking (IBN)
⬜ gRPC-based fast telemetry plane
👥 Contributors
Name
Role
Aditya Kumar Maurya
Lead Developer / Research
Abhishek Yadav
SDN & Controller Logic
Sujal Gupta
AI Training & Integration
📄 License
This project is licensed under the MIT License.
Free to use for research and development.

📝 Citation
bibtex
123456
@thesis{maurya2025sdnai,
  title={AI-Based Congestion Control in SDN using LSTM and DQN},
  author={Maurya, Aditya Kumar and Yadav, Abhishek and Gupta, Sujal},
  school={Madan Mohan Malaviya University of Technology (MMMUT)},
  year={2025}
}
📧 Contact
📨 Aditya Kumar Maurya
📩 adityamaurya@mmmut.ac.in

