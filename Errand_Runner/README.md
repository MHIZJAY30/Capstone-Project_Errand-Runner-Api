# Capstone Project – Errand Runner API

A Django REST Framework-powered backend API that helps users request errands and get items delivered by available runners. This API is designed to solve a real-life frustration, helping people who can’t visit the market or store get their shopping done through trusted helpers.

# Project Overview
The *Errand Runner API* lets users:
- Register and log in
- Request errands by submitting a list of items
- Track the status of their errands (pending, in-progress, completed)
- Get matched with a runner
- Choose delivery or pickup options
- Review/rate the Runner
This project was built as a capstone to demonstrate backend skills with Django and REST APIs.

# Features
It has the following features
✅ User Registration & Authentication with JWT tokens
✅ User Profiles (with role: requester or runner)
✅ Create, Read, Update, Delete (CRUD) for errands
✅ Add multiple items to each errand
✅ Assign runners to errands
✅ Filter errands by category and status
✅ RESTful API design
✅ Review and rating system

# Installation
```bash
git clone <your-repo>
cd errand-runner-api
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

# Quick Start
Register: POST /api/auth/register/
Login: POST /api/auth/login/
Create errand: POST /api/errands/

# Full Documentation
See API_DOCUMENTATION.md for complete API reference.

# Tech Stack
Django 5.2.4
Django REST Framework 3.16.0
JWT Authentication
SQLite/PostgreSQL

# Database Design (ERD)
My ERD Diagram and API Endpoints. 
Note: I made use of draw.io for the diagram presentation of the relationship between the main parts of my backend project database.
https://docs.google.com/document/d/1hAQGyrIICMnB60SbxoreSwm_8IYWW2kXnvZxdU6kOFA/edit?usp=sharing

# Author
Juliet Duru 
| Capstone-Project | Backend Developer | Email: julietsamuel78@gmail.com

# License
This project is for educational and demonstration purposes only but if possible will be developed fully in the nearest future