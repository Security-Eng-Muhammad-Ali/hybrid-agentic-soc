#!/usr/bin/env python3
"""
=============================================================
  Hybrid Agentic SOC - Attack Simulation Script v3
  Author: Muhammad Ali (Security-Eng-Muhammad-Ali)
  GitHub: https://github.com/Security-Eng-Muhammad-Ali/hybrid-agentic-soc
  
  Purpose: Simulate multi-vector attacks to test the full
           Wazuh → n8n → AI investigation pipeline
           
  Attack Types:
  - LOW RISK  (Level 3-6):  Single failed logins, file touches
  - MEDIUM RISK (Level 7-11): FIM violations, user creation
  - HIGH RISK (Level 12+):  Brute force, privilege escalation
=============================================================
"""

import subprocess
import time
import os

print("=" * 60)
print("  Hybrid Agentic SOC - Attack Simulation Script v3")
print("  Guaranteed LOW + MEDIUM + HIGH Alerts")
print("=" * 60)

def run(cmd):
    """Execute shell command silently"""
    subprocess.run(cmd, shell=True, capture_output=True)

# ============================================
# LOW RISK (Level 3-6)
# Action: Auto-Close + Google Sheets Log
# ============================================
print("\n[LOW RISK] Starting Low Risk Simulation...")

# Single failed SSH login attempts
for i in range(3):
    run("ssh fakeuser@localhost -o ConnectTimeout=1 -o StrictHostKeyChecking=no 2>/dev/null")
    time.sleep(1)

# Benign system activity
run("sudo cat /var/log/syslog 2>/dev/null | tail -5")
run("sudo touch /tmp/low_test_file")
run("sudo rm -f /tmp/low_test_file")

print("    [LOW] Done. Waiting 10 seconds...")
time.sleep(10)

# ============================================
# MEDIUM RISK (Level 7-11)
# Action: Gmail Notification to Analyst
# ============================================
print("\n[MEDIUM RISK] Starting Medium Risk Simulation...")

# File Integrity Violations on /etc (triggers FIM - level 7)
# These files are monitored by Wazuh Syscheck
critical_files = [
    "/etc/passwd",
    "/etc/hosts",
    "/etc/crontab",
    "/etc/ssh/sshd_config",
    "/etc/hostname"
]

for f in critical_files:
    run(f"sudo touch {f}")
    time.sleep(2)

# Multiple /etc file modifications (FIM correlation)
for i in range(5):
    run(f"sudo touch /etc/medtest_{i}")
    time.sleep(1)
    run(f"sudo rm -f /etc/medtest_{i}")
    time.sleep(1)

# User creation (level 8)
run("sudo useradd mediumtestuser 2>/dev/null")
time.sleep(3)
run("sudo userdel mediumtestuser 2>/dev/null")

print("    [MEDIUM] Done. Waiting 15 seconds...")
time.sleep(15)

# ============================================
# HIGH RISK (Level 12+)
# Action: VirusTotal + AbuseIPDB + AI Investigation
# ============================================
print("\n[HIGH RISK] Starting High Risk Simulation...")

# Mass SSH brute force (triggers Wazuh correlation rule 100001 - level 12)
print("    Running SSH brute force (20 attempts)...")
for i in range(20):
    run(f"ssh attacker{i}@localhost -o ConnectTimeout=1 -o StrictHostKeyChecking=no 2>/dev/null")
    time.sleep(0.5)

# Multiple user creation + sudo group add (triggers rule 100002 - level 13)
print("    Running suspicious user activity...")
for i in range(3):
    run(f"sudo useradd highuser{i} 2>/dev/null")
    time.sleep(1)
    run(f"sudo usermod -aG sudo highuser{i} 2>/dev/null")
    time.sleep(1)
    run(f"sudo userdel highuser{i} 2>/dev/null")
    time.sleep(1)

# Critical system file modifications (FIM high alert)
print("    Modifying critical system files...")
run("sudo touch /etc/passwd")
run("sudo touch /etc/shadow")
run("sudo touch /etc/ssh/sshd_config")
run("sudo touch /etc/sudoers")
time.sleep(2)

# Attacker recon behavior
run("sudo find / -perm -4000 2>/dev/null")     # SUID file search
run("sudo cat /etc/shadow 2>/dev/null")          # Password file access
run("sudo cat /etc/sudoers 2>/dev/null")         # Sudo config access
run("sudo last -n 50 2>/dev/null")               # Login history
run("sudo lastb -n 50 2>/dev/null")              # Failed login history

print("    [HIGH] Done. Waiting 30 seconds for Wazuh correlation...")
time.sleep(30)

# ============================================
# SUMMARY
# ============================================
print("\n" + "=" * 60)
print("  All Attacks Simulated!")
print("")
print("  Expected Results:")
print("  LOW  → Google Sheets auto-logged (Status: Auto-Closed)")
print("  MED  → Gmail notification sent to analyst")
print("  HIGH → VirusTotal + AbuseIPDB checked")
print("         → Mistral AI investigation report generated")
print("         → Google Sheets logged with AI summary")
print("")
print("  Now check:")
print("  1. Wazuh Dashboard → Linux-agent → alerts + levels")
print("  2. n8n Executions → Low/Medium/High branches")
print("  3. Google Sheet → Auto-closed + AI response rows")
print("  4. Gmail → Medium risk email notification")
print("=" * 60)
