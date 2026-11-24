# VideoLib

A clean and minimal Django web application for managing and streaming video content.

## Overview

VideoLib is a lightweight platform designed to organize, categorize, and stream video files. It includes basic authentication and a simple user interface for effortless video library management.

## Features

- **Video Streaming & Management:** Upload, organize, and view videos.
- **Categorization:** Filter videos by categories and tags.
- **User Authentication:** Simple registration and login functionality.
- **Admin Dashboard:** Manage content through Django's built-in administration panel.

## Tech Stack

- **Backend:** Python, Django
- **Database:** SQLite
- **Frontend:** HTML5, CSS3, JavaScript
- **Version Control:** Git, GitHub

## Project Structure

```text
videolib/
├── library/            # Main application logic (views, models, templates)
├── videolib_project/   # Core Django configuration settings
├── media/              # User-uploaded video and media files (ignored by Git)
├── manage.py           # Django management script
├── start.sh            # Custom startup script
└── README.md           # Project documentation
```

## Quick Start Guide

### 1. Clone the repository
```bash
git clone https://github.com/khaliloofh/VideoLib.git
cd VideoLib
```

### 2. Set up a virtual environment
```bash
# On Linux / macOS:
python3 -m venv venv
source venv/bin/activate

# On Windows:
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install django
# Or if you have a requirements file:
# pip install -r requirements.txt
```

### 4. Database Setup & Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create a Superuser (Optional)
To access the Django admin dashboard:
```bash
python manage.py createsuperuser
```

### 6. Run the Application
```bash
python manage.py runserver
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your web browser to view the application.

## License

This project is open-source and available for personal or educational use.
