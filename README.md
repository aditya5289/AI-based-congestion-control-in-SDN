<div align="center">

# 🚀 AI-Based Congestion Control in SDN  
### **A Hybrid LSTM + DQN Framework for Intelligent, Proactive Traffic Engineering**

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Click%20Here-blue?style=for-the-badge)](https://chat.qwen.ai/s/deploy/t_c71b65ef-a811-4795-97ee-73fd25bca398)
![Python](https://img.shields.io/badge/Python-3.8+-yellow?style=for-the-badge)
![Ryu](https://img.shields.io/badge/SDN-Ryu%20Controller-red?style=for-the-badge)
![Mininet](https://img.shields.io/badge/Mininet-Emulation-lightgrey?style=for-the-badge)
![AI](https://img.shields.io/badge/AI-Deep%20Learning%20%2F%20Reinforcement%20Learning-green?style=for-the-badge)

---

### ⚡ *Proactively predict congestion. Reroute traffic before it fails.  
A fully-integrated research framework for AI-driven SDN control.*

</div>

---

# 📘 **Overview**

This project implements a **complete SDN-based congestion control system** integrating:

- **LSTM** for real-time congestion prediction  
- **Deep Reinforcement Learning (DQN)** for intelligent routing  
- **Ryu SDN Controller** for dynamic flow management  
- **Mininet** for topology emulation  
- **Flask Backend** for ML model serving  
- **React Dashboard** for visualization  

Designed specifically for:

🎓 **Thesis Projects**  
📚 **Research Papers**  
🔬 **Network Experiments**  
🧠 **AI-in-Networking Innovation**

---

# 🏛️ **System Architecture**

lua
Copy code
               +----------------------------+
               |        Frontend (React)    |
               |   Visual Analytics & UI    |
               +-------------+--------------+
                             |
                             v
+---------------------+ REST +----------------------+
| Mininet Topology | <-------- | Backend (Flask API) |
| Hosts, Switches | Stats | Model Inference |
+----------+----------+ +----------+-----------+
| |
v v
+----------+---------------------------------+-----------+
| Ryu SDN Controller |
| - Polls switch stats |
| - Runs LSTM predictor |
| - Runs DQN routing agent |
| - Installs OpenFlow rules |
+---------------------+-----------------------------------+
|
v
Network Traffic Flow

yaml
Copy code

---

# 📂 **Repository Structure**

AI-SDN/
│
├── backend/ # Flask API for ML services
├── ryu_app/ # Ryu SDN controller logic with AI integration
├── mininet/ # Topology + traffic generation
├── ai/ # Dataset, training scripts, LSTM/DQN models
├── frontend/ # React visualization panel (optional)
│
├── .env.example # Backend config template
└── README.md

yaml
Copy code

---

# ✨ **Key Features**

### 🔮 **1. AI-Powered Congestion Prediction**
- Multivariate LSTM model
- Predicts queue buildup 3–5 seconds before congestion

### 🧠 **2. Intelligent Routing via DQN**
- Learns optimal paths
- Minimizes latency and packet loss
- Avoids congested links autonomously

### 🔌 **3. Real SDN Integration**
- Compatible with **OpenFlow 1.3**
- Fully implemented in **Ryu**

### 🧪 **4. Mininet-Based Emulation**
- Supports Fat-Tree, Mesh, Leaf-Spine, and custom topologies

### 📊 **5. Visualization Dashboard**
- Displays real-time utilization  
- Congestion alerts  
- Flow decisions  

---

# 🛠️ **Installation Guide (Ubuntu 20.04 Recommended)**

> ✔ Python 3.8+  
> ✔ Mininet  
> ✔ Ryu  
> ✔ Node.js (optional for frontend)

---

## **1️⃣ Install System Dependencies**

```bash
sudo apt update
sudo apt install python3-pip python3-venv git -y

# Install Mininet & Ryu
sudo apt-get install mininet -y
pip3 install ryu
2️⃣ Start Backend Server
bash
Copy code
cd backend
python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
cp .env.example .env

python server.py
3️⃣ Train the AI Model
bash
Copy code
cd ai
python3 train_model.py
Output: model.pkl

4️⃣ Start Ryu Controller
bash
Copy code
ryu-manager ryu_app/controller_ai.py
5️⃣ Run Mininet Topology
bash
Copy code
sudo python3 mininet/topology.py
This will:

Create the topology

Start traffic

Trigger congestion

Allow AI controller to react

6️⃣ Launch React Dashboard (Optional)
bash
Copy code
cd frontend
npm install
npm start
📡 Backend API Endpoints
🔵 GET /stats
Returns real-time SDN statistics.

🔵 POST /predict
Send telemetry → get LSTM congestion prediction.

🔵 POST /route
Request route computed by DQN agent.

🧪 Sample Output Visuals (Placeholders)
(Add your own screenshots here)

css
Copy code
[ Dashboard Screenshot Placeholder ]
[ Traffic Graph Placeholder ]
[ Routing Decision Logs ]
📝 For Researchers
This project is fully extendable for academic work:

🧩 Possible Enhancements
Replace RandomForest with full LSTM / GRU

Swap DQN with Double-DQN, Dueling-DQN, PPO, or A3C

Add deep attention models

Integrate telemetry from sFlow / NetFlow

📐 Experimental Ideas
Compare multiple RL reward functions

Test under adversarial microbursts

Evaluate controller delay impact

🎓 Citation (APA / IEEE Style)
If you use this project in research:

APA
css
Copy code
Maurya, A. K., Yadav, A., & Gupta, S. (2025). 
AI-Based Congestion Control in SDN using LSTM and DQN.  
Madan Mohan Malaviya University of Technology.
IEEE
css
Copy code
A. K. Maurya, A. Yadav, and S. Gupta, 
"AI-Based Congestion Control in SDN using LSTM and DQN," 
MMMUT, India, 2025.
🤝 Contributing
Pull requests and ideas are welcome!
Please open an issue for feature suggestions.

📧 Contact
Aditya Kumar Maurya
📩 adityamaurya@mmmut.ac.in
