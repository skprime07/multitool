import streamlit as st
import os
import time
import requests
import smtplib
import pyttsx3
import speech_recognition as sr
import google.generativeai as genai
from datetime import datetime, timedelta
import calendar
import pyautogui
from io import BytesIO
import base64
from email.message import EmailMessage
import pywhatkit
import subprocess
import json
from gtts import gTTS
import base64
from io import BytesIO


# Page config
st.set_page_config(
    page_title="🚀 Multi-Tool Dashboard",
    page_icon="🛠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Working CSS with Amazing Effects - Updated with Red Crayola Background
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #EF3054 0%, #C41E3A 50%, #FF6B8A 100%);
        background-attachment: fixed;
    }
    
    /* Floating bubbles background */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: 0;
        background-image: 
            radial-gradient(circle at 20% 80%, rgba(255, 255, 255, 0.1) 2px, transparent 2px),
            radial-gradient(circle at 80% 20%, rgba(255, 255, 255, 0.15) 1px, transparent 1px),
            radial-gradient(circle at 40% 40%, rgba(255, 255, 255, 0.08) 3px, transparent 3px);
        background-size: 200px 200px, 150px 150px, 300px 300px;
        animation: floatingBubbles 20s infinite linear;
    }
    
    @keyframes floatingBubbles {
        0% { transform: translateY(100vh); }
        100% { transform: translateY(-100vh); }
    }
    
    /* Main content container */
    .main .block-container {
        position: relative;
        z-index: 1;
        background: transparent;
    }
    
    /* Header */
    .main-header {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 3rem 2rem;
        border-radius: 25px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        position: relative;
        overflow: hidden;
        animation: headerFloat 6s ease-in-out infinite alternate;
    }
    
    @keyframes headerFloat {
        0% { transform: translateY(0px); }
        100% { transform: translateY(-10px); }
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent 30%, rgba(255,255,255,0.2) 50%, transparent 70%);
        animation: shimmer 3s infinite;
        pointer-events: none;
    }
    
    @keyframes shimmer {
        0% { transform: translateX(-100%) translateY(-100%); }
        100% { transform: translateX(100%) translateY(100%); }
    }
    
    .main-header h1 {
        font-size: 3.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
        text-shadow: 0 4px 20px rgba(0,0,0,0.3);
        background: linear-gradient(135deg, #ffffff 0%, #f0f0f0 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: textGlow 2s ease-in-out infinite alternate;
        position: relative;
        z-index: 2;
    }
    
    @keyframes textGlow {
        0% { filter: drop-shadow(0 4px 20px rgba(255,255,255,0.3)); }
        100% { filter: drop-shadow(0 4px 40px rgba(255,255,255,0.6)); }
    }
    
    .main-header p {
        font-size: 1.3rem;
        font-weight: 400;
        opacity: 0.9;
        text-shadow: 0 2px 10px rgba(0,0,0,0.2);
        position: relative;
        z-index: 2;
    }
    
    /* Feature cards */
    .feature-card {
        background: rgba(255, 255, 255, 0.12);
        backdrop-filter: blur(25px);
        -webkit-backdrop-filter: blur(25px);
        border: 1px solid rgba(255, 255, 255, 0.18);
        padding: 2rem;
        border-radius: 20px;
        margin: 1.5rem 0;
        color: white;
        box-shadow: 0 25px 50px rgba(0,0,0,0.15);
        transition: all 0.4s ease;
        position: relative;
        overflow: hidden;
        animation: cardFloat 4s ease-in-out infinite alternate;
    }
    
    @keyframes cardFloat {
        0% { transform: translateY(0px); }
        100% { transform: translateY(-5px); }
    }
    
    .feature-card::before {
        content: '';
        position: absolute;
        top: -2px;
        left: -2px;
        right: -2px;
        bottom: -2px;
        background: linear-gradient(45deg, #ff0000, #ff7300, #fffb00, #48ff00, #00ffd5, #002bff, #7a00ff, #ff00c8, #ff0000);
        background-size: 400%;
        border-radius: 20px;
        z-index: -1;
        animation: rainbowBorder 3s linear infinite;
        opacity: 0;
        transition: opacity 0.3s;
    }
    
    .feature-card:hover::before {
        opacity: 0.7;
    }
    
    @keyframes rainbowBorder {
        0% { background-position: 0% 50%; }
        100% { background-position: 400% 50%; }
    }
    
    .feature-card:hover {
        transform: translateY(-15px) scale(1.05);
        box-shadow: 0 50px 100px rgba(0,0,0,0.3);
    }
    
    .feature-card h3 {
        font-size: 1.8rem;
        font-weight: 600;
        margin-bottom: 1rem;
        text-shadow: 0 2px 10px rgba(0,0,0,0.3);
        animation: titleBounce 2s ease-in-out infinite;
    }
    
    @keyframes titleBounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-3px); }
    }
    
    /* Command cards */
    .command-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.15);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        color: white;
        box-shadow: 0 15px 30px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        animation: commandPulse 3s ease-in-out infinite;
    }
    
    @keyframes commandPulse {
        0%, 100% { box-shadow: 0 15px 30px rgba(0,0,0,0.1); }
        50% { box-shadow: 0 20px 40px rgba(0,0,0,0.2), 0 0 30px rgba(255,255,255,0.1); }
    }
    
    .command-card:hover {
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 25px 50px rgba(0,0,0,0.25);
    }
    
    /* Terminal */
    .linux-terminal {
        background: rgba(0, 0, 0, 0.8);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(0, 255, 0, 0.3);
        color: #00ff00;
        padding: 2rem;
        border-radius: 15px;
        font-family: 'Fira Code', 'Courier New', monospace;
        margin: 1.5rem 0;
        box-shadow: 0 20px 40px rgba(0,0,0,0.4), 0 0 20px rgba(0,255,0,0.1) inset;
        position: relative;
        overflow: hidden;
        animation: terminalGlow 2s ease-in-out infinite alternate;
    }
    
    @keyframes terminalGlow {
        0% { 
            box-shadow: 0 20px 40px rgba(0,0,0,0.4), 0 0 20px rgba(0,255,0,0.1) inset;
            border-color: rgba(0, 255, 0, 0.3);
        }
        100% { 
            box-shadow: 0 25px 50px rgba(0,0,0,0.5), 0 0 40px rgba(0,255,0,0.2) inset;
            border-color: rgba(0, 255, 0, 0.6);
        }
    }
    
    .linux-terminal::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 30px;
        background: linear-gradient(90deg, #ff5f56, #ffbd2e, #27ca3f);
        border-radius: 15px 15px 0 0;
    }
    
    .linux-terminal::after {
        content: '●    ●';
        position: absolute;
        top: 8px;
        left: 15px;
        color: #333;
        font-size: 12px;
    }
    
    /* Success/Error messages */
    .success-message {
        background: rgba(76, 175, 80, 0.15);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(76, 175, 80, 0.3);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin: 1.5rem 0;
        text-align: center;
        box-shadow: 0 15px 30px rgba(76, 175, 80, 0.2);
        animation: successBounce 0.5s ease-out;
    }
    
    @keyframes successBounce {
        0% { opacity: 0; transform: scale(0.3) translateY(50px); }
        50% { transform: scale(1.1) translateY(-10px); }
        100% { opacity: 1; transform: scale(1) translateY(0); }
    }
    
    .error-message {
        background: rgba(244, 67, 54, 0.15);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(244, 67, 54, 0.3);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin: 1.5rem 0;
        text-align: center;
        box-shadow: 0 15px 30px rgba(244, 67, 54, 0.2);
        animation: errorShake 0.5s ease-out;
    }
    
    @keyframes errorShake {
        0%, 100% { transform: translateX(0); }
        10%, 30%, 50%, 70%, 90% { transform: translateX(-5px); }
        20%, 40%, 60%, 80% { transform: translateX(5px); }
    }
    
    /* Buttons */
    .stButton > button {
        background: rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        color: white !important;
        padding: 1rem 2.5rem !important;
        border-radius: 50px !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        transition: all 0.4s ease !important;
        width: 100% !important;
        box-shadow: 0 10px 25px rgba(0,0,0,0.15) !important;
        position: relative !important;
        overflow: hidden !important;
        animation: buttonFloat 3s ease-in-out infinite alternate !important;
    }
    
    @keyframes buttonFloat {
        0% { transform: translateY(0px); }
        100% { transform: translateY(-2px); }
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        transition: left 0.6s;
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-5px) scale(1.02) !important;
        box-shadow: 0 20px 40px rgba(0,0,0,0.25) !important;
        border: 1px solid rgba(255, 255, 255, 0.4) !important;
        background: rgba(255, 255, 255, 0.15) !important;
    }
    
    /* Sidebar */
    .sidebar-content {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.15);
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        color: white;
        box-shadow: 0 15px 30px rgba(0,0,0,0.1);
        animation: sidebarFloat 4s ease-in-out infinite alternate;
    }
    
    @keyframes sidebarFloat {
        0% { transform: translateY(0px); }
        100% { transform: translateY(-5px); }
    }
    
    .sidebar-content h3 {
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 1rem;
        text-shadow: 0 2px 10px rgba(0,0,0,0.3);
        animation: sidebarTitleGlow 2s ease-in-out infinite alternate;
    }
    
    @keyframes sidebarTitleGlow {
        0% { text-shadow: 0 2px 10px rgba(0,0,0,0.3); }
        100% { text-shadow: 0 2px 20px rgba(255,255,255,0.4); }
    }
    
    /* Weather card */
    .weather-card {
        background: rgba(116, 185, 255, 0.15);
        backdrop-filter: blur(25px);
        -webkit-backdrop-filter: blur(25px);
        border: 1px solid rgba(116, 185, 255, 0.3);
        padding: 2.5rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin: 2rem 0;
        box-shadow: 0 25px 50px rgba(116, 185, 255, 0.2);
        transition: all 0.3s ease;
        animation: weatherStorm 3s ease-in-out infinite;
    }
    
    @keyframes weatherStorm {
        0%, 100% { box-shadow: 0 25px 50px rgba(116, 185, 255, 0.2); }
        50% { box-shadow: 0 30px 60px rgba(116, 185, 255, 0.3); }
    }
    
    .weather-card:hover {
        transform: translateY(-10px) scale(1.03);
    }
    
    /* AI response */
    .ai-response {
        background: rgba(162, 155, 254, 0.15);
        backdrop-filter: blur(25px);
        -webkit-backdrop-filter: blur(25px);
        border: 1px solid rgba(162, 155, 254, 0.3);
        padding: 2.5rem;
        border-radius: 20px;
        color: white;
        margin: 2rem 0;
        box-shadow: 0 25px 50px rgba(162, 155, 254, 0.2);
        animation: aiThinking 2s ease-in-out infinite alternate;
    }
    
    @keyframes aiThinking {
        0% { box-shadow: 0 25px 50px rgba(162, 155, 254, 0.2); }
        100% { box-shadow: 0 30px 60px rgba(162, 155, 254, 0.3); }
    }
    
    .ai-response h4 {
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 1.5rem;
        text-shadow: 0 2px 10px rgba(0,0,0,0.3);
    }
    
    /* Category header */
    .category-header {
        background: rgba(239, 48, 84, 0.2);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(239, 48, 84, 0.3);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin: 1.5rem 0;
        text-align: center;
        font-weight: 600;
        font-size: 1.3rem;
        box-shadow: 0 15px 30px rgba(239, 48, 84, 0.2);
        text-shadow: 0 2px 10px rgba(0,0,0,0.3);
        animation: neonPulse 2s ease-in-out infinite alternate;
    }
    
    @keyframes neonPulse {
        0% { text-shadow: 0 2px 10px rgba(0,0,0,0.3); }
        100% { text-shadow: 0 2px 20px rgba(239, 48, 84, 0.8); }
    }
    
    /* Metric containers */
    .metric-container {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.15);
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        color: white;
        box-shadow: 0 15px 30px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        animation: metricBounce 2s ease-in-out infinite;
    }
    
    @keyframes metricBounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-3px); }
    }
    
    .metric-container:hover {
        transform: translateY(-8px) scale(1.05);
        box-shadow: 0 25px 50px rgba(0,0,0,0.2);
    }
    
    /* Input fields */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select {
        background: rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(15px) !important;
        -webkit-backdrop-filter: blur(15px) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 12px !important;
        color: white !important;
        padding: 1rem !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stSelectbox > div > div > select:focus {
        border: 1px solid rgba(255, 255, 255, 0.4) !important;
        box-shadow: 0 0 20px rgba(255, 255, 255, 0.2) !important;
        background: rgba(255, 255, 255, 0.15) !important;
    }
    
    .stTextInput > div > div > input::placeholder,
    .stTextArea > div > div > textarea::placeholder {
        color: rgba(255, 255, 255, 0.6) !important;
    }
    
    /* Footer */
    .footer {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(25px);
        -webkit-backdrop-filter: blur(25px);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        color: white;
        margin-top: 3rem;
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        animation: footerWave 4s ease-in-out infinite;
        position: relative;
        overflow: hidden;
    }
    
    @keyframes footerWave {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-3px); }
    }
    
    .footer::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        animation: footerShimmer 3s infinite;
    }
    
    @keyframes footerShimmer {
        0% { left: -100%; }
        100% { left: 100%; }
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: rgba(255, 255, 255, 0.3);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(255, 255, 255, 0.5);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'gemini_api_key' not in st.session_state:
    st.session_state.gemini_api_key = ""
if 'command_history' not in st.session_state:
    st.session_state.command_history = []
if 'custom_screenshot' not in st.session_state:
    st.session_state.custom_screenshot = None

# Linux Commands Dictionary
LINUX_COMMANDS = {
    "📁 File Operations": {
        "ls": "List directory contents",
        "ls -la": "List all files with detailed information",
        "pwd": "Print working directory",
        "cd": "Change directory",
        "mkdir": "Create directory",
        "rmdir": "Remove empty directory",
        "rm": "Remove files",
        "rm -rf": "Remove directory recursively",
        "cp": "Copy files/directories",
        "mv": "Move/rename files",
        "find": "Find files and directories",
        "locate": "Find files by name",
        "which": "Locate command",
        "whereis": "Locate binary, source, manual",
        "file": "Determine file type",
        "stat": "Display file statistics",
        "touch": "Create empty file or update timestamp",
        "ln": "Create links",
        "chmod": "Change file permissions",
        "chown": "Change file ownership",
        "chgrp": "Change group ownership"
    },
    "📄 Text Processing": {
        "cat": "Display file contents",
        "less": "View file contents page by page",
        "more": "View file contents page by page",
        "head": "Display first lines of file",
        "tail": "Display last lines of file",
        "grep": "Search text patterns",
        "sed": "Stream editor",
        "awk": "Pattern scanning and processing",
        "sort": "Sort lines of text",
        "uniq": "Report unique lines",
        "wc": "Word, line, character count",
        "cut": "Extract columns from text",
        "tr": "Translate characters",
        "tee": "Write output to both file and stdout",
        "diff": "Compare files",
        "comm": "Compare sorted files",
        "join": "Join lines of files"
    },
    "🔧 System Information": {
        "uname": "System information",
        "whoami": "Current username",
        "id": "User and group IDs",
        "uptime": "System uptime",
        "date": "Current date and time",
        "cal": "Calendar",
        "w": "Who is logged in",
        "who": "Show logged in users",
        "last": "Show last logins",
        "df": "Disk space usage",
        "du": "Directory space usage",
        "free": "Memory usage",
        "top": "Running processes",
        "htop": "Interactive process viewer",
        "ps": "Process status",
        "pstree": "Process tree",
        "lscpu": "CPU information",
        "lsblk": "Block devices",
        "lsusb": "USB devices",
        "lspci": "PCI devices"
    },
    "🌐 Network Operations": {
        "ping": "Test network connectivity",
        "wget": "Download files from web",
        "curl": "Transfer data to/from server",
        "ssh": "Secure shell remote login",
        "scp": "Secure copy over network",
        "rsync": "Synchronize files/directories",
        "netstat": "Network connections",
        "ss": "Socket statistics",
        "iptables": "Firewall configuration",
        "nslookup": "DNS lookup",
        "dig": "DNS lookup tool",
        "host": "DNS lookup utility",
        "traceroute": "Trace network route",
        "ifconfig": "Network interface configuration",
        "ip": "Show/manipulate routing",
        "route": "Show/manipulate routing table"
    },
    "🔒 Process Management": {
        "jobs": "List active jobs",
        "bg": "Put job in background",
        "fg": "Bring job to foreground",
        "nohup": "Run command immune to hangups",
        "kill": "Terminate process",
        "killall": "Kill processes by name",
        "pkill": "Kill processes by criteria",
        "pgrep": "Find processes by criteria",
        "screen": "Terminal multiplexer",
        "tmux": "Terminal multiplexer",
        "crontab": "Schedule tasks",
        "at": "Schedule one-time tasks",
        "systemctl": "Control systemd services",
        "service": "Control system services"
    },
    "📦 Archive Operations": {
        "tar": "Archive files",
        "gzip": "Compress files",
        "gunzip": "Decompress gzip files",
        "zip": "Create zip archives",
        "unzip": "Extract zip archives",
        "7z": "7-zip archiver",
        "rar": "RAR archiver",
        "unrar": "Extract RAR archives"
    },
    "🛠 System Administration": {
        "sudo": "Execute as another user",
        "su": "Switch user",
        "passwd": "Change password",
        "useradd": "Add user account",
        "userdel": "Delete user account",
        "usermod": "Modify user account",
        "groupadd": "Add group",
        "groupdel": "Delete group",
        "mount": "Mount filesystem",
        "umount": "Unmount filesystem",
        "fdisk": "Partition disks",
        "mkfs": "Create filesystem",
        "fsck": "Check filesystem",
        "crontab -e": "Edit cron jobs",
        "history": "Command history",
        "alias": "Create command aliases",
        "env": "Environment variables",
        "export": "Set environment variables",
        "source": "Execute commands from file",
        "man": "Manual pages",
        "info": "Info documents",
        "help": "Help for built-in commands"
    }
}

# Header
st.markdown("""
<div class="main-header">
    <h1>🚀 Multi-Tool Dashboard</h1>
    <p>Your all-in-one productivity suite with AI integration & 50+ Linux Commands</p>
</div>
""", unsafe_allow_html=True)

# Sidebar for navigation
with st.sidebar:
    st.markdown("""
    <div class="sidebar-content">
        <h3>🎯 Navigation</h3>
        <p>Select a tool from the menu below</p>
    </div>
    """, unsafe_allow_html=True)
    
    selected_tool = st.selectbox(
        "Choose a tool:",
        [
            "🏠 Home", 
            "🐧 Linux Commands", 
            "📅 Date & Time", 
            "📁 File System (ls)", 
            "📱 WhatsApp Message", 
            "📧 Email", 
            "📱 SMS", 
            "🗣️ Text to Speech", 
            "🎤 Voice Recognition", 
            "📸 Screenshot", 
            "🤖 AI Assistant", 
            "📍 PIN Code Lookup", 
            "🌤️ Weather",
            "📞 Make a Phone Call",
            "🔗 LinkedIn Post",
            "🐦 Post on Twitter",
            "📸 Instagram Post"
        ]
    )


# Function to execute commands safely (Remote SSH only)
def execute_command(command, ssh_details):
    """Execute command remotely via SSH"""
    try:
        username, ip_address = ssh_details
        ssh_command = f"ssh {username}@{ip_address} '{command}'"
        result = subprocess.run(ssh_command, shell=True, capture_output=True, text=True, timeout=30)
        
        return {
            'success': True,
            'stdout': result.stdout,
            'stderr': result.stderr,
            'returncode': result.returncode
        }
    except subprocess.TimeoutExpired:
        return {
            'success': False,
            'error': 'Command timed out (30 seconds)'
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

# Main content based on selection
if selected_tool == "🏠 Home":
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>🐧 Linux Commands</h3>
            <p>50+ categorized Linux commands with remote SSH execution</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>📱 Communication</h3>
            <p>WhatsApp, SMS, and email integration</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <h3>🤖 AI Powered</h3>
            <p>Google Gemini integration for smart assistance</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 🚀 Quick Stats")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
        <div class="metric-container">
            <h2>15</h2>
            <p>Tools Available 🛠</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="metric-container">
            <h2>50+</h2>
            <p>Linux Commands 🐧</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="metric-container">
            <h2>✅</h2>
            <p>Communication 📱</p>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
        <div class="metric-container">
            <h2>✅</h2>
            <p>AI Assistant 🤖</p>
        </div>
        """, unsafe_allow_html=True)

elif selected_tool == "🐧 Linux Commands":
    st.markdown("### 🐧 Linux Command Center (Remote SSH)")
    
    # SSH configuration
    with st.expander("🔧 SSH Configuration", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            ssh_username = st.text_input("👤 Username", placeholder="root")
        with col2:
            ssh_ip = st.text_input("🌐 IP Address", placeholder="192.168.1.100")
        
        if ssh_username and ssh_ip:
            ssh_details = (ssh_username, ssh_ip)
            st.success(f"✅ SSH configured for {ssh_username}@{ssh_ip}")
        else:
            ssh_details = None
            st.warning("⚠ Please configure SSH credentials to execute commands")
    
    # Command execution modes
    tab1, tab2, tab3 = st.tabs(["📚 Command Categories", "⚡ Quick Execute", "📜 Command History"])
    
    with tab1:
        st.markdown("### 📚 Categorized Linux Commands")
        
        # Display commands by category
        for category, commands in LINUX_COMMANDS.items():
            with st.expander(f"{category} ({len(commands)} commands)"):
                st.markdown(f"""
                <div class="category-header">
                    {category}
                </div>
                """, unsafe_allow_html=True)
                
                cols = st.columns(2)
                for i, (cmd, desc) in enumerate(commands.items()):
                    with cols[i % 2]:
                        st.markdown(f"""
                        <div class="command-card">
                            <strong>$ {cmd}</strong><br>
                            <small>{desc}</small>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Execute button for each command
                        if st.button(f"Execute: {cmd}", key=f"exec_{cmd}_{category}"):
                            if not ssh_details:
                                st.error("❌ Please configure SSH credentials first")
                            elif cmd in ["rm -rf", "sudo", "passwd", "useradd", "userdel", "fdisk", "mkfs"]:
                                st.warning(f"⚠ Command '{cmd}' requires additional parameters and can be dangerous. Use the Quick Execute tab for custom commands.")
                            else:
                                with st.spinner(f"Executing {cmd} on {ssh_ip}..."):
                                    result = execute_command(cmd, ssh_details)
                                    
                                    if result['success']:
                                        st.session_state.command_history.append({
                                            'command': cmd,
                                            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                            'host': ssh_ip,
                                            'success': True
                                        })
                                        
                                        st.markdown(f"""
                                        <div class="success-message">
                                            ✅ Command executed successfully on {ssh_ip}
                                        </div>
                                        """, unsafe_allow_html=True)
                                        
                                        if result['stdout']:
                                            st.markdown(f"""
                                            <div class="linux-terminal">
                                                <strong>{ssh_username}@{ssh_ip}:~$ {cmd}</strong><br>
                                                {result['stdout']}
                                            </div>
                                            """, unsafe_allow_html=True)
                                        
                                        if result['stderr']:
                                            st.warning(f"Warnings/Errors: {result['stderr']}")
                                    else:
                                        st.session_state.command_history.append({
                                            'command': cmd,
                                            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                            'host': ssh_ip,
                                            'success': False,
                                            'error': result.get('error', 'Unknown error')
                                        })
                                        
                                        st.markdown(f"""
                                        <div class="error-message">
                                            ❌ Command failed: {result.get('error', 'Unknown error')}
                                        </div>
                                        """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("### ⚡ Quick Command Execution")
        
        if not ssh_details:
            st.error("❌ Please configure SSH credentials in the SSH Configuration section above")
        else:
            # Quick command suggestions
            st.markdown("*Popular Commands:*")
            quick_commands = ["ls -la", "pwd", "whoami", "uname -a", "free -h", "df -h", "ps aux", "date", "uptime"]
            
            cols = st.columns(5)
            for i, cmd in enumerate(quick_commands):
                with cols[i % 5]:
                    if st.button(cmd, key=f"quick_{cmd}"):
                        with st.spinner(f"Executing {cmd} on {ssh_ip}..."):
                            result = execute_command(cmd, ssh_details)
                            
                            if result['success']:
                                st.markdown(f"""
                                <div class="linux-terminal">
                                    <strong>{ssh_username}@{ssh_ip}:~$ {cmd}</strong><br>
                                    {result['stdout']}
                                </div>
                                """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Custom command input
            custom_command = st.text_input("💻 Enter custom command:", placeholder="Enter any Linux command...")
            
            col1, col2 = st.columns([3, 1])
            with col1:
                if st.button("🚀 Execute Custom Command"):
                    if custom_command:
                        # Warning for dangerous commands
                        dangerous_commands = ["rm -rf", "dd", "mkfs", "fdisk", ":(){ :|:& };:", "sudo rm", "chmod -R 777"]
                        if any(danger in custom_command for danger in dangerous_commands):
                            st.error("⚠ Potentially dangerous command detected. Please review before executing.")
                            
                            if st.button("⚠ Execute Anyway (Use with caution)", key="dangerous_confirm"):
                                with st.spinner("Executing..."):
                                    result = execute_command(custom_command, ssh_details)
                                    
                                    if result['success']:
                                        st.markdown(f"""
                                        <div class="linux-terminal">
                                            <strong>{ssh_username}@{ssh_ip}:~$ {custom_command}</strong><br>
                                            {result['stdout']}
                                        </div>
                                        """, unsafe_allow_html=True)
                                    else:
                                        st.error(f"Command failed: {result.get('error')}")
                        else:
                            with st.spinner("Executing..."):
                                result = execute_command(custom_command, ssh_details)
                                
                                st.session_state.command_history.append({
                                    'command': custom_command,
                                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                    'host': ssh_ip,
                                    'success': result['success']
                                })
                                
                                if result['success']:
                                    st.markdown(f"""
                                    <div class="linux-terminal">
                                        <strong>{ssh_username}@{ssh_ip}:~$ {custom_command}</strong><br>
                                        {result['stdout']}
                                    </div>
                                    """, unsafe_allow_html=True)
                                    
                                    if result['stderr']:
                                        st.warning(f"Warnings: {result['stderr']}")
                                else:
                                    st.markdown(f"""
                                    <div class="error-message">
                                        ❌ Command failed: {result.get('error')}
                                    </div>
                                    """, unsafe_allow_html=True)
            
            with col2:
                if st.button("📋 Command Help"):
                    if custom_command:
                        help_cmd = f"man {custom_command.split()[0]}"
                        with st.spinner("Getting help..."):
                            result = execute_command(help_cmd, ssh_details)
                            if result['success']:
                                st.text_area("Command Help:", result['stdout'], height=200)
                            else:
                                st.info("No manual page available for this command.")
    
    with tab3:
        st.markdown("### 📜 Command History")
        
        if st.session_state.command_history:
            # Display statistics
            total_commands = len(st.session_state.command_history)
            successful_commands = sum(1 for cmd in st.session_state.command_history if cmd.get('success', False))
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"""
                <div class="metric-container">
                    <h2>{total_commands}</h2>
                    <p>Total Commands</p>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                <div class="metric-container">
                    <h2>{successful_commands}</h2>
                    <p>Successful</p>
                </div>
                """, unsafe_allow_html=True)
            with col3:
                st.markdown(f"""
                <div class="metric-container">
                    <h2>{(successful_commands/total_commands)*100:.1f}%</h2>
                    <p>Success Rate</p>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Display command history
            for i, cmd_info in enumerate(reversed(st.session_state.command_history[-10:])):  # Show last 10 commands
                status_icon = "✅" if cmd_info.get('success', False) else "❌"
                st.markdown(f"""
                <div class="command-card">
                    {status_icon} <strong>{cmd_info['command']}</strong><br>
                    <small>📅 {cmd_info['timestamp']} | 🖥 {cmd_info.get('host', 'Unknown')}</small>
                </div>
                """, unsafe_allow_html=True)
            
            if st.button("🗑 Clear History"):
                st.session_state.command_history = []
                st.success("Command history cleared!")
                st.rerun()
        else:
            st.info("No command history available. Execute some commands to see them here.")

elif selected_tool == "📅 Date & Time":
    st.markdown("### 📅 Date & Time Information")
    
    # SSH configuration
    with st.expander("🔧 SSH Configuration"):
        col1, col2 = st.columns(2)
        
        with col1:
            username = st.text_input("👤 Username", placeholder="root")
            ip_address = st.text_input("🌐 Remote IP", placeholder="192.168.1.100")
        
        with col2:
            command_type = st.selectbox("📅 Command", ["date", "cal", "uptime", "timedatectl"])
        
        if st.button("🚀 Execute Remote Command"):
            if username and ip_address:
                result = execute_command(command_type, (username, ip_address))
                
                if result['success']:
                    st.markdown(f"""
                    <div class="success-message">
                        ✅ Command executed successfully on {ip_address}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown(f"""
                    <div class="linux-terminal">
                        <strong>{username}@{ip_address}:~$ {command_type}</strong><br>
                        {result['stdout']}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="error-message">
                        ❌ Error: {result.get('error')}
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.warning("Please fill in username and IP address.")

elif selected_tool == "📁 File System (ls)":
    st.markdown("### 📁 File System Commands (Remote SSH)")
    
    # SSH configuration
    with st.expander("🔧 SSH Configuration", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            username = st.text_input("👤 Username", placeholder="root")
            ip_address = st.text_input("🌐 Remote IP", placeholder="192.168.1.100")
        
        with col2:
            remote_path = st.text_input("📁 Remote Path", value=".", placeholder="/home/user")
            ls_options = st.selectbox("📋 ls Options", ["ls", "ls -la", "ls -lh", "ls -lt", "ls -ltr"])
        
        if st.button("🚀 Execute Remote ls"):
            if username and ip_address:
                command = f"cd {remote_path} && {ls_options}"
                result = execute_command(command, (username, ip_address))
                
                if result['success']:
                    st.markdown(f"""
                    <div class="success-message">
                        ✅ Command executed successfully on {ip_address}:{remote_path}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown(f"""
                    <div class="linux-terminal">
                        <strong>{username}@{ip_address}:~$ {ls_options}</strong><br>
                        {result['stdout']}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="error-message">
                        ❌ Error: {result.get('error')}
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.warning("Please fill in username and IP address.")

elif selected_tool == "📱 WhatsApp Message":
    st.markdown("### 📱 WhatsApp Message Sender")
    
    with st.form("whatsapp_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            phone_number = st.text_input("📞 Phone Number", placeholder="+1234567890")
            message = st.text_area("💬 Message", placeholder="Enter your message here...")
        
        with col2:
            send_time = st.time_input("⏰ Send Time", value=datetime.now().time())
            instant_send = st.checkbox("📤 Send Instantly")
        
        submitted = st.form_submit_button("📱 Send WhatsApp Message")
        
        if submitted:
            if phone_number and message:
                try:
                    if instant_send:
                        pywhatkit.sendwhatmsg_instantly(phone_number, message)
                        st.markdown("""
                        <div class="success-message">
                            ✅ WhatsApp message sent instantly!
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        current_time = datetime.now()
                        send_datetime = datetime.combine(current_time.date(), send_time)
                        
                        if send_datetime <= current_time:
                            send_datetime += timedelta(days=1)
                        
                        pywhatkit.sendwhatmsg(phone_number, message, send_datetime.hour, send_datetime.minute)
                        st.markdown(f"""
                        <div class="success-message">
                            ✅ WhatsApp message scheduled for {send_datetime.strftime('%Y-%m-%d %H:%M')}
                        </div>
                        """, unsafe_allow_html=True)
                        
                except Exception as e:
                    st.markdown(f"""
                    <div class="error-message">
                        ❌ Error sending WhatsApp message: {str(e)}
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.warning("Please fill in phone number and message.")

elif selected_tool == "📧 Email":
    st.markdown("### 📧 Email Sender")
    
    with st.form("email_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            sender_email = st.text_input("📧 Your Email", placeholder="your.email@gmail.com")
            sender_password = st.text_input("🔒 Password", type="password", placeholder="Your app password")
            recipient_email = st.text_input("📨 Recipient Email", placeholder="recipient@example.com")
        
        with col2:
            subject = st.text_input("📝 Subject", placeholder="Email Subject")
            body = st.text_area("📄 Message Body", placeholder="Enter your email message here...")
            smtp_server = st.selectbox("📧 SMTP Server", ["smtp.gmail.com", "smtp.outlook.com", "smtp.yahoo.com"])
        
        submitted = st.form_submit_button("📧 Send Email")
        
        if submitted:
            if sender_email and sender_password and recipient_email and subject and body:
                try:
                    msg = EmailMessage()
                    msg['Subject'] = subject
                    msg['From'] = sender_email
                    msg['To'] = recipient_email
                    msg.set_content(body)
                    
                    with smtplib.SMTP_SSL(smtp_server, 465) as server:
                        server.login(sender_email, sender_password)
                        server.send_message(msg)
                    
                    st.markdown("""
                    <div class="success-message">
                        ✅ Email sent successfully!
                    </div>
                    """, unsafe_allow_html=True)
                    
                except Exception as e:
                    st.markdown(f"""
                    <div class="error-message">
                        ❌ Error sending email: {str(e)}
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.warning("Please fill in all required fields.")

elif selected_tool == "📱 SMS":
    st.markdown("### 📱 SMS Sender")
    st.info("📝 This feature requires SMS API integration (Twilio, etc.)")
    
    with st.form("sms_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            api_key = st.text_input("🔑 API Key", type="password", placeholder="Your SMS API key")
            phone_number = st.text_input("📞 Phone Number", placeholder="+1234567890")
        
        with col2:
            message = st.text_area("💬 SMS Message", placeholder="Enter your SMS message here...")
            service = st.selectbox("📡 SMS Service", ["Twilio", "TextBelt", "Other"])
        
        submitted = st.form_submit_button("📱 Send SMS")
        
        if submitted:
            st.info("SMS functionality requires API setup. This is a placeholder for SMS integration.")

elif selected_tool == "🗣️ Text to Speech":
    st.markdown("### 🗣️ Text to Speech (gTTS)")

    if "tts_audio" not in st.session_state:
        st.session_state.tts_audio = None

    with st.form("tts_form"):
        text_input = st.text_area("📝 Enter text to speak", placeholder="Type your message here...")

        col1, col2 = st.columns(2)
        with col1:
            lang = st.selectbox("🌐 Language", ["en", "hi", "fr", "de", "es"], index=0)
        with col2:
            slow = st.checkbox("🐢 Slow mode", value=False)

        submitted = st.form_submit_button("🗣️ Convert to Speech")

        if submitted:
            if text_input:
                try:
                    tts = gTTS(text=text_input, lang=lang, slow=slow)
                    audio_bytes = BytesIO()
                    tts.write_to_fp(audio_bytes)
                    audio_bytes.seek(0)

                    st.session_state.tts_audio = audio_bytes.getvalue()

                    st.markdown("""
                    <div class="success-message">
                        ✅ Text converted to speech successfully!
                    </div>
                    """, unsafe_allow_html=True)

                    st.audio(st.session_state.tts_audio, format="audio/mp3")

                except Exception as e:
                    st.markdown(f"""
                    <div class="error-message">
                        ❌ Error in text-to-speech: {str(e)}
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.warning("Please enter some text to convert.")

    # Download button outside form
    if st.session_state.tts_audio:
        st.download_button("📥 Download Audio", data=st.session_state.tts_audio, file_name="speech.mp3", mime="audio/mpeg")

elif selected_tool == "🎤 Voice Recognition":
    st.markdown("### 🎤 Voice Recognition")
    
    if st.button("🎤 Start Voice Recognition"):
        try:
            r = sr.Recognizer()
            with sr.Microphone() as source:
                st.info("🎤 Listening... Please speak now!")
                audio = r.listen(source, timeout=10)
                
            st.info("🔄 Processing audio...")
            text = r.recognize_google(audio)
            
            st.markdown(f"""
            <div class="success-message">
                ✅ Voice recognized successfully!
            </div>
            """, unsafe_allow_html=True)
            
            st.text_area("🗣 Recognized Speech:", text, height=100)
            
        except sr.UnknownValueError:
            st.markdown("""
            <div class="error-message">
                ❌ Could not understand audio. Please try again.
            </div>
            """, unsafe_allow_html=True)
        except sr.RequestError as e:
            st.markdown(f"""
            <div class="error-message">
                ❌ Error with speech recognition service: {str(e)}
            </div>
            """, unsafe_allow_html=True)
        except Exception as e:
            st.markdown(f"""
            <div class="error-message">
                ❌ Error in voice recognition: {str(e)}
            </div>
            """, unsafe_allow_html=True)

elif selected_tool == "📸 Screenshot":
    st.markdown("### 📸 Screenshot Tool")
    
    tab1, tab2 = st.tabs(["📸 Take Screenshot", "🖼 Custom Screenshot"])
    
    with tab1:
        if st.button("📸 Capture Full Screen"):
            try:
                screenshot = pyautogui.screenshot()
                img_buffer = BytesIO()
                screenshot.save(img_buffer, format='PNG')
                img_str = base64.b64encode(img_buffer.getvalue()).decode()
                
                st.markdown("""
                <div class="success-message">
                    ✅ Screenshot captured successfully!
                </div>
                """, unsafe_allow_html=True)
                
                st.image(screenshot, caption="Full Screen Screenshot", use_column_width=True)
                
                # Download button outside form
                st.download_button(
                    label="📥 Download Screenshot",
                    data=img_buffer.getvalue(),
                    file_name=f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
                    mime="image/png"
                )
                
            except Exception as e:
                st.markdown(f"""
                <div class="error-message">
                    ❌ Error taking screenshot: {str(e)}
                </div>
                """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("### 🖼 Custom Screenshot")
        
        with st.form("screenshot_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                x = st.number_input("📍 X Position", value=0, min_value=0)
                y = st.number_input("📍 Y Position", value=0, min_value=0)
            
            with col2:
                width = st.number_input("📏 Width", value=800, min_value=1)
                height = st.number_input("📏 Height", value=600, min_value=1)
            
            submitted = st.form_submit_button("📸 Take Custom Screenshot")
            
            if submitted:
                try:
                    screenshot = pyautogui.screenshot(region=(x, y, width, height))
                    img_buffer = BytesIO()
                    screenshot.save(img_buffer, format='PNG')
                    
                    st.session_state.custom_screenshot = img_buffer.getvalue()
                    
                    st.markdown("""
                    <div class="success-message">
                        ✅ Custom screenshot captured successfully!
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.image(screenshot, caption=f"Custom Screenshot ({x}, {y}, {width}, {height})", use_column_width=True)
                    
                except Exception as e:
                    st.markdown(f"""
                    <div class="error-message">
                        ❌ Error taking custom screenshot: {str(e)}
                    </div>
                    """, unsafe_allow_html=True)
        
        # Download button outside form
        if st.session_state.custom_screenshot:
            st.download_button(
                label="📥 Download Custom Screenshot",
                data=st.session_state.custom_screenshot,
                file_name=f"custom_screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
                mime="image/png"
            )

elif selected_tool == "🤖 AI Assistant":
    st.markdown("### 🤖 AI Assistant (Google Gemini)")
    
    # API Key input
    with st.expander("🔑 API Configuration", expanded=not st.session_state.gemini_api_key):
        api_key = st.text_input("🔑 Google Gemini API Key", 
                               type="password", 
                               value=st.session_state.gemini_api_key,
                               placeholder="Enter your Google Gemini API key")
        
        if st.button("💾 Save API Key"):
            st.session_state.gemini_api_key = api_key
            st.success("✅ API Key saved!")
    
    if st.session_state.gemini_api_key:
        try:
            genai.configure(api_key=st.session_state.gemini_api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # Chat interface
            user_input = st.text_area("💬 Ask AI anything:", placeholder="Type your question here...")
            
            col1, col2 = st.columns([3, 1])
            with col1:
                if st.button("🚀 Ask AI"):
                    if user_input:
                        with st.spinner("🤖 AI is thinking..."):
                            try:
                                response = model.generate_content(user_input)
                                
                                st.markdown(f"""
                                <div class="ai-response">
                                    <h4>🤖 AI Response:</h4>
                                    {response.text}
                                </div>
                                """, unsafe_allow_html=True)
                                
                            except Exception as e:
                                st.markdown(f"""
                                <div class="error-message">
                                    ❌ Error getting AI response: {str(e)}
                                </div>
                                """, unsafe_allow_html=True)
                    else:
                        st.warning("Please enter a question for the AI.")
            
            with col2:
                if st.button("🗑 Clear"):
                    st.rerun()
            
        except Exception as e:
            st.markdown(f"""
            <div class="error-message">
                ❌ Error initializing AI: {str(e)}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("🔑 Please configure your Google Gemini API key to use the AI assistant.")

elif selected_tool == "📍 PIN Code Lookup":
    st.markdown("### 📍 PIN Code Lookup")
    
    with st.form("pincode_form"):
        pincode = st.text_input("📍 Enter PIN Code", placeholder="110001")
        submitted = st.form_submit_button("🔍 Lookup PIN Code")
        
        if submitted:
            if pincode:
                try:
                    # Using Indian postal API
                    url = f"https://api.postalpincode.in/pincode/{pincode}"
                    response = requests.get(url)
                    data = response.json()
                    
                    if data[0]['Status'] == 'Success':
                        post_office = data[0]['PostOffice'][0]
                        
                        st.markdown(f"""
                        <div class="success-message">
                            ✅ PIN Code information found!
                        </div>
                        """, unsafe_allow_html=True)
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.info(f"📍 **PIN Code:** {pincode}")
                            st.info(f"🏢 **Post Office:** {post_office['Name']}")
                            st.info(f"🏛 **District:** {post_office['District']}")
                        
                        with col2:
                            st.info(f"🗺 **State:** {post_office['State']}")
                            st.info(f"🏳 **Country:** {post_office['Country']}")
                            st.info(f"🌍 **Region:** {post_office['Region']}")
                    else:
                        st.markdown("""
                        <div class="error-message">
                            ❌ PIN Code not found. Please check the PIN code and try again.
                        </div>
                        """, unsafe_allow_html=True)
                        
                except Exception as e:
                    st.markdown(f"""
                    <div class="error-message">
                        ❌ Error looking up PIN code: {str(e)}
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.warning("Please enter a PIN code.")

elif selected_tool == "🌤️ Weather":
    st.markdown("### 🌤️ Weather Information")
    
    with st.form("weather_form"):
        city = st.text_input("🏙 City Name", placeholder="New York")
        api_key = st.text_input("🔑 OpenWeatherMap API Key", type="password", placeholder="Your API key")
        submitted = st.form_submit_button("🌤️ Get Weather")
        
        if submitted:
            if city and api_key:
                try:
                    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
                    response = requests.get(url)
                    data = response.json()
                    
                    if response.status_code == 200:
                        st.markdown(f"""
                        <div class="weather-card">
                            <h3>🌤️ Weather in {city.title()}</h3>
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <div>
                                    <h2>{data['main']['temp']}°C</h2>
                                    <p>{data['weather'][0]['description'].title()}</p>
                                </div>
                                <div style="text-align: right;">
                                    <p>💧 Humidity: {data['main']['humidity']}%</p>
                                    <p>🌬️ Wind: {data['wind']['speed']} m/s</p>
                                    <p>🌡️ Feels like: {data['main']['feels_like']}°C</p>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Additional weather details
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.markdown(f"""
                            <div class="metric-container">
                                <h2>{data['main']['temp']}°C</h2>
                                <p>🌡️ Temperature</p>
                            </div>
                            """, unsafe_allow_html=True)
                            st.markdown(f"""
                            <div class="metric-container">
                                <h2>{data['main']['feels_like']}°C</h2>
                                <p>🌡️ Feels Like</p>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        with col2:
                            st.markdown(f"""
                            <div class="metric-container">
                                <h2>{data['main']['humidity']}%</h2>
                                <p>💧 Humidity</p>
                            </div>
                            """, unsafe_allow_html=True)
                            st.markdown(f"""
                            <div class="metric-container">
                                <h2>{data['wind']['speed']} m/s</h2>
                                <p>🌬️ Wind Speed</p>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        with col3:
                            st.markdown(f"""
                            <div class="metric-container">
                                <h2>{data['main']['temp_min']}°C</h2>
                                <p>🔽 Min Temp</p>
                            </div>
                            """, unsafe_allow_html=True)
                            st.markdown(f"""
                            <div class="metric-container">
                                <h2>{data['main']['temp_max']}°C</h2>
                                <p>🔼 Max Temp</p>
                            </div>
                            """, unsafe_allow_html=True)
                        
                    else:
                        st.markdown(f"""
                        <div class="error-message">
                            ❌ Error: {data.get('message', 'City not found')}
                        </div>
                        """, unsafe_allow_html=True)
                        
                except Exception as e:
                    st.markdown(f"""
                    <div class="error-message">
                        ❌ Error getting weather data: {str(e)}
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.warning("Please enter both city name and API key.")
    
    st.markdown("---")
    st.info("🔑 Get your free API key from [OpenWeatherMap](https://openweathermap.org/api)")

elif selected_tool == "📞 Make a Phone Call":
    st.markdown("### 📞 Make a Phone Call Using Twilio")
    
    with st.form("phone_call_form"):
        account_sid = st.text_input("🆔 Twilio Account SID", type="password")
        auth_token = st.text_input("🔑 Twilio Auth Token", type="password")
        from_number = st.text_input("📞 From (Twilio Number)", placeholder="+1234567890")
        to_number = st.text_input("📞 To (Recipient Number)", placeholder="+0987654321")
        message = st.text_area("🗣️ Message to speak", placeholder="Hello! This is a test call from Python.")
        
        submitted = st.form_submit_button("📞 Make Call")
        
        if submitted:
            try:
                from twilio.rest import Client
                client = Client(account_sid, auth_token)
                call = client.calls.create(
                    to=to_number,
                    from_=from_number,
                    twiml=f"<Response><Say>{message}</Say></Response>"
                )
                st.markdown(f"""
                <div class="success-message">
                    ✅ Call initiated successfully! SID: {call.sid}
                </div>
                """, unsafe_allow_html=True)
            except Exception as e:
                st.markdown(f"""
                <div class="error-message">
                    ❌ Error making call: {str(e)}
                </div>
                """, unsafe_allow_html=True)

elif selected_tool == "🔗 LinkedIn Post":
    st.markdown("### 🔗 Post a Message on LinkedIn")
    
    with st.form("linkedin_form"):
        access_token = st.text_input("🔑 LinkedIn Access Token", type="password")
        message = st.text_area("💬 Post Content", placeholder="Write your LinkedIn post here...")
        submitted = st.form_submit_button("📤 Post to LinkedIn")
        
        if submitted:
            try:
                headers = {
                    "Authorization": f"Bearer {access_token}",
                    "Content-Type": "application/json",
                    "X-Restli-Protocol-Version": "2.0.0"
                }
                # First get user URN
                user_response = requests.get("https://api.linkedin.com/v2/me", headers=headers)
                user_id = user_response.json()["id"]
                urn = f"urn:li:person:{user_id}"
                
                post_data = {
                    "author": urn,
                    "lifecycleState": "PUBLISHED",
                    "specificContent": {
                        "com.linkedin.ugc.ShareContent": {
                            "shareCommentary": {"text": message},
                            "shareMediaCategory": "NONE"
                        }
                    },
                    "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"}
                }
                post_response = requests.post("https://api.linkedin.com/v2/ugcPosts", headers=headers, json=post_data)
                
                if post_response.status_code == 201:
                    st.markdown("""
                    <div class="success-message">
                        ✅ LinkedIn post published successfully!
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="error-message">
                        ❌ Failed to post: {post_response.text}
                    </div>
                    """, unsafe_allow_html=True)
            except Exception as e:
                st.markdown(f"""
                <div class="error-message">
                    ❌ Error: {str(e)}
                </div>
                """, unsafe_allow_html=True)

elif selected_tool == "🐦 Post on Twitter":
    st.markdown("### 🐦 Post a Tweet")
    
    with st.form("twitter_form"):
        api_key = st.text_input("🔑 API Key")
        api_secret = st.text_input("🔒 API Secret", type="password")
        access_token = st.text_input("🪪 Access Token")
        access_secret = st.text_input("🔐 Access Token Secret", type="password")
        tweet = st.text_area("💬 Tweet Content", placeholder="What's happening?")
        
        submitted = st.form_submit_button("📤 Post Tweet")
        
        if submitted:
            try:
                import tweepy
                auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_secret)
                api = tweepy.API(auth)
                api.update_status(tweet)
                st.markdown("""
                <div class="success-message">
                    ✅ Tweet posted successfully!
                </div>
                """, unsafe_allow_html=True)
            except Exception as e:
                st.markdown(f"""
                <div class="error-message">
                    ❌ Error posting tweet: {str(e)}
                </div>
                """, unsafe_allow_html=True)

elif selected_tool == "📸 Instagram Post":
    st.markdown("### 📸 Post on Instagram")
    
    with st.form("instagram_form"):
        username = st.text_input("👤 Instagram Username")
        password = st.text_input("🔑 Instagram Password", type="password")
        image_path = st.text_input("🖼️ Local Image Path (absolute path)")
        caption = st.text_area("💬 Caption", placeholder="Write your caption here...")

        submitted = st.form_submit_button("📤 Post to Instagram")

        if submitted:
            try:
                from instagrapi import Client
                cl = Client()
                cl.login(username, password)
                cl.photo_upload(image_path, caption)
                st.markdown("""
                <div class="success-message">
                    ✅ Image posted to Instagram!
                </div>
                """, unsafe_allow_html=True)
            except Exception as e:
                st.markdown(f"""
                <div class="error-message">
                    ❌ Error posting to Instagram: {str(e)}
                </div>
                """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div class="footer">
    <p>🚀 <strong>Multi-Tool Dashboard</strong> - Your complete productivity suite</p>
    <p>Built with ❤️ using Streamlit | Features: Linux Commands, AI Assistant, Communication Tools & More</p>
</div>
""", unsafe_allow_html=True)