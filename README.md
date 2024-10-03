# BugBlitzPro - (Alpha-1.0.0)

<p align="center">
  <img src="media/BugBlitzPro.png" alt="BugBlitzPro Logo" width="200"/>
</p>


<p align="center">
  <strong>A powerful Bug Bounty Workflow Management System <span style="color: #ff69b4;">(Alpha-1.0.0)</span></strong>
</p>

<p align="center">
  <a href="#key-features">Key Features</a> •
  <a href="#installation">Installation</a> •
  <a href="#usage">Usage</a> •
  <a href="#contributing">Contributing</a> •
  <a href="#license">License</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-1.0.0-blue.svg" alt="Version 1.0.0">
  <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License MIT">
  <img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="Python 3.8+">
</p>

---

## 🚀 Key Features

- 📊 **Project Management**: Create and manage multiple bug bounty projects
- 🛠️ **Custom Tool Integration**: Add and configure your own security tools
- 🔄 **Workflow Automation**: Design complex workflows with a drag-and-drop interface `(Partially Implemented)`
- 📈 **Result Visualization**: Analyze and visualize tool outputs and scan results `(To-Do)`
- 🔐 **User Authentication**: Secure multi-user support with role-based access control
- 📱 **Responsive Design**: Fully responsive web interface for desktop and mobile devices
- 🌐 **Cross-Platform Compatibility**: Set up programming language binaries across different operating systems

## 🛠️ Installation

### Prerequisites

- Python 3.8+
- Node.js and npm
- Redis (for Celery task queue)

### Windows Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/sc4rfurry/BugBlitzPro.git
   cd BugBlitzPro
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Install Node.js dependencies:
   ```bash
   npm install
   ```

5. Set up the environment variables:
   - Copy `.env.example` to `.env`
   - Update the variables in `.env` with your configuration

6. Build the CSS:
   ```bash
   npm run build-css
   ```

### Linux/macOS Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/sc4rfurry/BugBlitzPro.git
   cd BugBlitzPro
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Install Node.js dependencies:
   ```bash
   npm install
   ```

5. Set up the environment variables:
   - Copy `.env.example` to `.env`
   - Update the variables in `.env` with your configuration

6. Build the CSS:
   ```bash
   npm run build-css
   ```

## 🖥️ Usage

1. Start the Flask development server:
   ```bash
   python run.py
   ```

2. Start the Celery worker (in a separate terminal):
   ```bash
   celery -A app.celery worker --loglevel=info
   ```

3. Access the application in your web browser at `http://localhost:5000`

4. Log in with the default admin credentials:
   - Username: admin
   - Password: admin

   (Make sure to change these credentials after your first login)

## 🤝 Contributing

We welcome contributions to BugBlitzPro!


## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<p align="center">
  Made with ❤️ by <span style="color: #ff69b4;">@sc4rfurry</span>
</p>