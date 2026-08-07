# 🛡️ Hybrid Agentic SOC — Rule Engine + AI Agent Investigation

> An end-to-end Security Operations Center (SOC) automation pipeline that combines deterministic rule-based routing with AI-powered threat investigation, deployed on AWS.

---

## 📌 Problem Statement

Traditional SOC analysts face **alert fatigue** — hundreds of alerts daily, 70-90% of which are low-risk and repetitive. Manual triage is slow, expensive, and prone to burnout. At the same time, blindly applying AI to every alert is cost-prohibitive and unreliable.

**The solution:** A hybrid pipeline where rules handle routine alerts automatically, and AI is reserved for high-risk cases — enriched with real threat intelligence.

---

## 🏗️ Architecture

```
Wazuh SIEM (Agent)
        │
        ▼
   Alert Generated
        │
        ▼
  n8n Webhook Trigger
        │
        ▼
  Rule Engine (Switch Node)
        │
   ┌────┴────────────────┐
   │                     │                     │
LOW (0-6)          MEDIUM (7-11)          HIGH (12+)
   │                     │                     │
Auto-Close         Gmail Notify        VirusTotal Check
+ Sheet Log        + Sheet Log              │
+ Correlation                         AbuseIPDB Check
                                           │
                                    Ollama AI (Mistral 7B)
                                    Enriched Investigation
                                           │
                                    Google Sheets Report
                                    + Correlation Update
```

---

## ⚙️ Tech Stack

| Component | Tool | Purpose |
|-----------|------|---------|
| SIEM | Wazuh 4.14 | Alert detection & log collection |
| Automation | n8n (self-hosted) | Rule engine & workflow orchestration |
| AI Model | Ollama + Mistral 7B | Local LLM for threat investigation |
| Threat Intel | VirusTotal API | IP malicious detection score |
| Threat Intel | AbuseIPDB API | IP reputation & abuse confidence |
| Notifications | Gmail SMTP | Medium risk analyst notifications |
| Storage | Google Sheets | Audit trail & correlation engine |
| Infrastructure | AWS EC2 | Cloud deployment |

---

## 🚀 Key Features

### 🔴 Intelligent Alert Routing
- **LOW (Level 0-6):** Auto-closed, logged to Google Sheets audit trail
- **MEDIUM (Level 7-11):** Analyst notified via Gmail with full alert details
- **HIGH (Level 12+):** Full AI investigation pipeline triggered

### 🧠 AI-Powered Investigation (High Risk Only)
- VirusTotal IP check (malicious engine count)
- AbuseIPDB reputation score, country, ISP, Tor node detection
- Mistral 7B generates structured 3-point SOC report:
  1. Threat Summary (with actual TI scores)
  2. Risk Assessment
  3. Recommended Containment Actions

### 🔗 Multi-Dimensional Correlation Engine
Tracks patterns across 4 dimensions:
- **IP Correlation** — Same source IP frequency, levels, attack types
- **Agent Correlation** — Which agents are being targeted most
- **Pattern Correlation** — Which attack patterns repeat most
- **Attack Chain** — Low → Medium → High progression from same IP

### 💰 Cost-Optimized AI Usage
- AI called **only** for HIGH risk alerts (5-10% of total)
- Local Ollama model = **zero per-call API cost**
- 90% token cost reduction vs calling AI on every alert

### 🔒 Data Privacy by Design
- Mistral 7B runs **locally on EC2** — no data sent to OpenAI or external APIs
- All processing stays within AWS VPC
- Enterprise-grade privacy compliance (GDPR, HIPAA friendly)

---

## 📊 Real Results

During testing, the system detected **real external attackers**:

| Source IP | Detections | Origin | Type |
|-----------|-----------|--------|------|
| 185.220.101.45 | 17/91 VT engines | Germany | Tor Exit Node (100% AbuseIPDB) |
| 161.118.212.147 | Multiple attempts | External | SSH Brute Force |
| 87.152.6.217 | Detected | External | Real Attack Attempt |

---

## 🤖 Sample AI Investigation Report

```
Title: Security Alert Report – SSH Brute Force from Malicious IP

1. THREAT SUMMARY:
Multiple SSH brute force attempts detected from 185.220.101.45.
VirusTotal: 17/91 engines flagged malicious, reputation score -20.
AbuseIPDB: 100% confidence score, 143 reports, Germany (DE).
IP associated with Tor-Exit traffic (for-privacy.net). Confirmed malicious.

2. RISK ASSESSMENT:
HIGH — Active brute force from confirmed Tor exit node with maximum
abuse confidence. Likelihood of credential compromise if not contained.

3. RECOMMENDED ACTIONS:
- Block 185.220.101.45 at firewall/security group level immediately
- Implement SSH rate limiting and key-based authentication only
- Review auth logs for any successful logins from this IP
- Add IP to blocklist and monitor for related Tor exit node IPs
- Consider implementing Tor exit node blocklist service
```

---

## 🏢 Business Value

| Metric | Before | After |
|--------|--------|-------|
| Alert review time | Manual, 30-40 min/alert | Automated, seconds |
| Analyst alert load | 100% of alerts | Only HIGH risk (5-10%) |
| AI cost | Per-call API pricing | Local model, zero marginal cost |
| Threat context | Raw alert only | TI-enriched + correlated |
| Audit trail | Manual/none | Automated Google Sheets |
| Data privacy | External API risk | 100% on-premise (VPC) |

---

## 🛠️ Setup Guide

### Prerequisites
- AWS Account
- 3 EC2 instances (t3.medium for Wazuh, t2.micro for n8n, t3.large for Ollama)
- Google Cloud Project (for Sheets + Gmail OAuth)
- VirusTotal free API key
- AbuseIPDB free API key

### EC2 Setup

**Instance 1: Wazuh Manager**
```bash
# Install Wazuh (official script)
curl -sO https://packages.wazuh.com/4.14/wazuh-install.sh
sudo bash wazuh-install.sh -a
```

**Instance 2: n8n Server**
```bash
docker run -d \
  --name n8n \
  -p 5678:5678 \
  -v n8n_data:/home/node/.n8n \
  -e N8N_SECURE_COOKIE=false \
  -e WEBHOOK_URL=http://<YOUR_PUBLIC_IP>.nip.io:5678/ \
  --restart unless-stopped \
  n8nio/n8n
```

**Instance 3: Ollama (Mistral 7B)**
```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull mistral
```

### Wazuh Agent Setup
```bash
# On target server
wget https://packages.wazuh.com/4.x/apt/pool/main/w/wazuh-agent/wazuh-agent_4.14.5-1_amd64.deb
sudo WAZUH_MANAGER='<WAZUH_MANAGER_IP>' dpkg -i wazuh-agent_4.14.5-1_amd64.deb
sudo systemctl start wazuh-agent
```

### Wazuh → n8n Integration
```bash
# On Wazuh Manager
sudo nano /var/ossec/integrations/custom-n8n
```
```bash
#!/bin/sh
WEBHOOK_URL="http://<N8N_PRIVATE_IP>:5678/webhook/wazuh-alerts"
curl -s -X POST -H "Content-Type: application/json" -d @${1} ${WEBHOOK_URL}
exit 0
```
```bash
sudo chmod +x /var/ossec/integrations/custom-n8n
sudo chown root:wazuh /var/ossec/integrations/custom-n8n
```

Add to `/var/ossec/etc/ossec.conf`:
```xml
<integration>
  <name>custom-n8n</name>
  <hook_url>http://<N8N_PRIVATE_IP>:5678/webhook/wazuh-alerts</hook_url>
  <level>3</level>
  <alert_format>json</alert_format>
</integration>
```

### Custom High-Risk Rules
```xml
<!-- /var/ossec/etc/rules/local_rules.xml -->
<group name="local,syslog,sshd,">
  <rule id="100001" level="12" frequency="8" timeframe="60">
    <if_matched_sid>5710</if_matched_sid>
    <same_source_ip />
    <description>High Risk: Multiple SSH brute force attempts</description>
    <mitre><id>T1110</id></mitre>
  </rule>
  <rule id="100002" level="13">
    <if_sid>5901</if_sid>
    <description>High Risk: New user added to system</description>
    <mitre><id>T1136</id></mitre>
  </rule>
</group>
```

---

## 📁 Project Structure

```
hybrid-agentic-soc/
├── n8n-workflows/
│   ├── wazuh-alert-router.json      # Main workflow (export from n8n)
│   └── grafana-data-api.json        # Dashboard data API workflow
├── wazuh-config/
│   ├── custom-n8n                   # Integration script
│   ├── ossec.conf (snippet)         # Integration config
│   └── local_rules.xml             # Custom detection rules
├── attack-simulation/
│   └── attack_simulation.py        # Multi-vector attack simulator
├── screenshots/
│   ├── n8n-workflow.png
│   ├── google-sheets-log.png
│   ├── gmail-alert.png
│   ├── ai-investigation.png
│   └── grafana-dashboard.png
└── README.md
```

---

## 🎯 MITRE ATT&CK Coverage

| Technique | ID | Detection |
|-----------|-----|-----------|
| Brute Force | T1110 | SSH failed login correlation |
| Valid Accounts | T1078 | Successful root login detection |
| Create Account | T1136 | New user addition monitoring |
| Modify Authentication | T1556 | PAM events monitoring |
| File & Directory Permissions | T1222 | FIM via Wazuh Syscheck |

---

## 🔮 Future Improvements

- [ ] Analyst approve/reject loop (human-in-the-loop)
- [ ] Custom SOC dashboard with AI summaries
- [ ] Multi-agent correlation (same attacker across multiple targets)
- [ ] Automated IP blocking via AWS Security Groups API
- [ ] Slack integration for team notifications
- [ ] Threat hunting queries based on correlation patterns

---

## 👨‍💻 Author

**Muhammad Ali**
Junior SOC Engineer | Detection Engineering | Cloud Security

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue)](https://linkedin.com/in/your-profile)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-black)](https://github.com/Security-Eng-Muhammad-Ali)

---

## 📜 License

MIT License — feel free to use, modify, and build upon this project.

---

*Built with ❤️ for the cybersecurity community — proving that powerful SOC automation doesn't require expensive enterprise tools.*
