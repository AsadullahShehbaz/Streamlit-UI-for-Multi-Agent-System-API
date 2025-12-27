# 🤖 AI Researcher Agent

<div align="center">

![AI Researcher Agent](https://img.shields.io/badge/AI-Researcher%20Agent-blueviolet?style=for-the-badge&logo=robot)
![Python](https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red?style=for-the-badge&logo=streamlit)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**A cutting-edge Multi-Agent System for Research · Discovery · Automation**

[Features](#-features) • [Demo](#-demo) • [Installation](#-installation) • [Usage](#-usage) • [API](#-api-documentation) • [Contributing](#-contributing)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Demo](#-demo)
- [Architecture](#-architecture)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [API Documentation](#-api-documentation)
- [Project Structure](#-project-structure)
- [Technologies](#-technologies)
- [Contributing](#-contributing)
- [License](#-license)
- [Support](#-support)

---

## 🌟 Overview

**AI Researcher Agent** is a sophisticated multi-agent research platform that leverages artificial intelligence to conduct comprehensive research, analyze data, and generate structured reports. Built with a stunning, modern UI and powered by advanced AI models, it provides researchers, students, and professionals with an intelligent assistant for their research needs.

### Key Highlights

✨ **AI-Powered Research** - Utilizes advanced language models for intelligent research  
🚀 **Lightning Fast** - Get comprehensive results in seconds  
🎯 **Accurate Analysis** - Multi-agent system ensures precision and reliability  
🔒 **Secure & Private** - Enterprise-grade security for your data  
📊 **Structured Reports** - Well-organized, downloadable research outputs  
💬 **Interactive Chat** - Natural conversation interface for queries  

---

## ✨ Features

### 🔐 **Authentication System**
- Secure user registration and login
- JWT token-based authentication
- Session management
- Password encryption

### 💬 **Research Chat Interface**
- Interactive conversational AI
- Real-time research generation
- Chat history persistence
- Export conversations as Markdown
- Copy to clipboard functionality

### 📊 **Research Management**
- View detailed research reports
- Download reports in Markdown format
- Delete and manage research data
- Track research history
- Status monitoring

### 🧪 **API Testing Dashboard**
- Health check monitoring
- Endpoint testing interface
- Response time tracking
- JSON response visualization
- Real-time status indicators

### 🎨 **Premium UI/UX**
- Modern glass morphism design
- Animated gradient backgrounds
- Smooth transitions and hover effects
- Responsive layout for all devices
- Dark mode optimized
- Custom scrollbars and styling

---

## 🎬 Demo

### Home Dashboard
![Home Dashboard](screenshots/home.png)
*Beautiful landing page with authentication and research history*

### Research Chat
![Research Chat](screenshots/chat.png)
*Interactive AI-powered research assistant with real-time generation*

### View Research
![View Research](screenshots/view.png)
*Detailed research reports with management options*

### API Testing
![API Testing](screenshots/api-test.png)
*Developer-friendly API testing dashboard*

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (Streamlit)                     │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │    Home     │  │    Chat     │  │   View Research     │ │
│  └─────────────┘  └─────────────┘  └─────────────────────┘ │
│  ┌─────────────┐  ┌─────────────┐                          │
│  │  API Test   │  │ Auth System │                          │
│  └─────────────┘  └─────────────┘                          │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ REST API
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     Backend API Server                       │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │    Auth     │  │  Research   │  │   User Management   │ │
│  │  Endpoints  │  │  Endpoints  │  │     Endpoints       │ │
│  └─────────────┘  └─────────────┘  └─────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                  Multi-Agent AI System                       │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │  Research   │  │  Analysis   │  │   Report Generation │ │
│  │    Agent    │  │    Agent    │  │        Agent        │ │
│  └─────────────┘  └─────────────┘  └─────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 Installation

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/ai-researcher-agent.git
cd ai-researcher-agent
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Set Up Environment Variables

Create a `.env` file in the root directory:

```env
# API Configuration
API_BASE_URL=http://localhost:8000
API_TIMEOUT=30

# Security
SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# AI Model Configuration
AI_MODEL=gpt-4
MAX_ITERATIONS=5
TEMPERATURE=0.7

# Database (if applicable)
DATABASE_URL=postgresql://user:password@localhost/dbname
```

### Step 5: Run the Application

```bash
streamlit run 1_🏠_Home.py
```

The application will be available at `http://localhost:8501`

---

## ⚙️ Configuration

### `config.py`

```python
SESSION_KEYS = {
    "token": None,
    "user_info": None,
    "current_research_id": None,
    "messages": []
}

API_ENDPOINTS = {
    "register": "/api/v1/auth/register",
    "login": "/api/v1/auth/login",
    "user": "/api/v1/users/me",
    "research": "/api/v1/research",
    "history": "/api/v1/research/history"
}
```

### Customization Options

You can customize the following in the UI:

- **Theme Colors**: Modify gradient values in the CSS sections
- **Animation Speed**: Adjust animation duration in `@keyframes`
- **API Timeout**: Change timeout values in `utils.py`
- **Max Iterations**: Configure AI research depth in environment variables

---

## 📖 Usage

### 1. User Registration & Login

```python
# Register a new user
1. Navigate to Home page
2. Click on "Register" tab in sidebar
3. Enter username, email, and password
4. Click "Create Account"

# Login
1. Click on "Login" tab
2. Enter credentials
3. Click "Login"
```

### 2. Start Research

```python
# Chat Interface
1. Navigate to "Chat Research" page
2. Type your research query in the chat input
3. Press Enter or click send
4. Wait for AI to generate comprehensive report
5. Download or copy the results
```

### 3. View Research History

```python
# View Previous Research
1. Navigate to "View Research" page
2. Enter Research ID or select from history
3. Click "Load Research"
4. View detailed report
5. Download as Markdown or Delete
```

### 4. API Testing

```python
# Test API Endpoints
1. Navigate to "API Test" page
2. Click "Check API Health" for health check
3. Select authenticated endpoint
4. Click "Run Test" to execute
5. View response data and metrics
```

---

## 🔌 API Documentation

### Authentication Endpoints

#### Register User
```http
POST /api/v1/auth/register
Content-Type: application/json

{
  "username": "string",
  "email": "string",
  "password": "string"
}
```

**Response:**
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "created_at": "2025-12-26T21:29:00"
}
```

#### Login
```http
POST /api/v1/auth/login
Content-Type: application/x-www-form-urlencoded

username=string&password=string
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "username": "john_doe",
  "email": "john@example.com"
}
```

### Research Endpoints

#### Create Research
```http
POST /api/v1/research
Authorization: Bearer {token}
Content-Type: application/json

{
  "query": "Give me a complete 10 days roadmap to learn Vector DB Pinecone",
  "max_iterations": 2
}
```

**Response:**
```json
{
  "id": 8,
  "query": "Give me a complete 10 days roadmap...",
  "status": "completed",
  "final_report": "# 10-Day Pinecone Learning Roadmap...",
  "created_at": "2025-12-26T21:29:00"
}
```

#### Get Research History
```http
GET /api/v1/research/history?limit=20
Authorization: Bearer {token}
```

**Response:**
```json
[
  {
    "id": 8,
    "query": "Give me a complete 10 days roadmap...",
    "status": "completed",
    "created_at": "2025-12-26T21:29:00"
  }
]
```

#### Get Research by ID
```http
GET /api/v1/research/{research_id}
Authorization: Bearer {token}
```

#### Delete Research
```http
DELETE /api/v1/research/{research_id}
Authorization: Bearer {token}
```

### User Endpoints

#### Get Current User
```http
GET /api/v1/users/me
Authorization: Bearer {token}
```

**Response:**
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "created_at": "2025-12-25T10:00:00"
}
```

---

## 📁 Project Structure

```
ai-researcher-agent/
│
├── 1_🏠_Home.py                    # Main home page
├── pages/
│   ├── 1_💬_Chat_Research.py      # Research chat interface
│   ├── 2_📊_View_Research.py      # View research details
│   └── 3_🧪_API_Test.py           # API testing dashboard
│
├── config.py                       # Configuration settings
├── utils.py                        # Utility functions
│
├── requirements.txt                # Python dependencies
├── .env                           # Environment variables
├── .gitignore                     # Git ignore rules
│
├── screenshots/                   # UI screenshots
│   ├── home.png
│   ├── chat.png
│   ├── view.png
│   └── api-test.png
│
├── README.md                      # This file
└── LICENSE                        # MIT License
```

---

## 🛠️ Technologies

### Frontend
- **Streamlit** - Web application framework
- **HTML/CSS** - Custom styling and animations
- **JavaScript** - Interactive elements

### Backend
- **Python** - Core programming language
- **FastAPI** - REST API framework (assumed)
- **JWT** - Authentication tokens

### AI/ML
- **OpenAI GPT** - Language model for research
- **LangChain** - Multi-agent orchestration
- **Vector Databases** - Semantic search

### Styling
- **Glass Morphism** - Modern UI design
- **Gradient Animations** - Dynamic backgrounds
- **Custom CSS** - Responsive design

---

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. **Commit your changes**
   ```bash
   git commit -m 'Add some AmazingFeature'
   ```
4. **Push to the branch**
   ```bash
   git push origin feature/AmazingFeature
   ```
5. **Open a Pull Request**

### Contribution Guidelines

- Follow PEP 8 style guide for Python code
- Write clear commit messages
- Add tests for new features
- Update documentation as needed
- Ensure all tests pass before submitting PR

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2025 AI Researcher Agent

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
```

---

## 🙏 Acknowledgments

- **Streamlit Team** - For the amazing web framework
- **OpenAI** - For powerful language models
- **Community Contributors** - For valuable feedback and contributions

---

## 📞 Support

### Having Issues?

- 📧 **Email**: support@airesearcher.com
- 💬 **Discord**: [Join our community](https://discord.gg/airesearcher)
- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/yourusername/ai-researcher-agent/issues)
- 📖 **Documentation**: [Full Docs](https://docs.airesearcher.com)

### FAQ

**Q: How do I reset my password?**  
A: Currently, password reset is handled through the backend API. Contact support for assistance.

**Q: Can I use my own AI model?**  
A: Yes! Configure your model in the `.env` file under `AI_MODEL` setting.

**Q: Is there a usage limit?**  
A: Depends on your API backend configuration. Check with your backend administrator.

**Q: How secure is my data?**  
A: All data is encrypted, and we use JWT tokens for authentication. Your research is private.

---

## 🗺️ Roadmap

### Version 2.0 (Upcoming)
- [ ] Multi-language support
- [ ] Voice input for research queries
- [ ] Export to PDF format
- [ ] Team collaboration features
- [ ] Advanced analytics dashboard

### Version 3.0 (Future)
- [ ] Mobile application
- [ ] Browser extension
- [ ] Integration with popular research tools
- [ ] Custom AI model training
- [ ] Advanced visualization tools

---

## ⭐ Star History

If you find this project useful, please consider giving it a star!

[![Star History Chart](https://api.star-history.com/svg?repos=yourusername/ai-researcher-agent&type=Date)](https://star-history.com/#yourusername/ai-researcher-agent&Date)

---

<div align="center">

**Made with ❤️ by the AI Researcher Agent Team**

[Website](https://airesearcher.com) • [Documentation](https://docs.airesearcher.com) • [Twitter](https://twitter.com/airesearcher)

</div>
