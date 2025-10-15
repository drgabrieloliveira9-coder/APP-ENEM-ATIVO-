# ENEM 2025 StudyApp

## Overview

A comprehensive web-based study platform designed for students preparing for Brazil's ENEM 2025 exam. The application provides organized educational content across all ENEM subject areas, automated essay evaluation, study schedules, mind maps, and progress tracking. Built as a self-contained Flask application with SQLite database, it delivers 500+ study summaries, interactive learning tools, and administrative capabilities for content management.

## User Preferences

Preferred communication style: Simple, everyday language.

## Recent Changes

**October 15, 2025 - Dark Theme Transformation**
- Complete UI redesign from light purple/lilac theme to dark technological blue/black theme
- All templates updated with consistent dark palette (bg-slate-950 backgrounds, blue-600/500 gradients)
- Interactive elements redesigned with blue hover states and smooth transitions
- Cards use semi-transparent dark backgrounds (bg-slate-900/50) with blue borders for depth
- Text optimized for dark mode readability (text-gray-300, text-white)
- Modern technological aesthetic with glow effects on headings and interactive hover states

## System Architecture

### Application Framework
- **Web Framework**: Flask 2.3.2 serving a monolithic web application
- **Template Engine**: Jinja2 templates with server-side rendering
- **Frontend**: HTML5 with Tailwind CSS (CDN-based, no build process)
- **Design Theme**: Dark mode with blue/black color palette for technological aesthetic
- **Language**: Python 3.11+ for all backend logic

### Data Architecture
- **Database**: SQLite3 with pure Python sqlite3 library (no ORM)
- **Schema Design**: Relational structure with foreign key constraints
  - `areas`: Subject areas (4 main ENEM categories)
  - `topics`: Study topics linked to areas
  - `resumos`: Study summaries with bullets and tips
  - `questoes`: Multiple-choice questions with answers and detailed explanations
  - `explicacoes`: Detailed explanations with examples and tips for each topic
  - `essays`: Stored essay submissions with scores and feedback
  - `progress`: User progress tracking per topic
- **Data Population**: Seed scripts for initial content (`db_init.py`, `seed_resumos.py`, `seed_conteudo_completo.py`)
- **Connection Pattern**: Factory pattern with `get_db()` creating per-request connections

### Security Model
- **Session Management**: Flask sessions with secret key from environment
- **Admin Authentication**: Simple password-based protection using environment variable `ADMIN_PASS`
- **SQL Injection Protection**: Parameterized queries throughout
- **Default Credentials**: admin123 (configurable via `.env`)

### Feature Modules

**Essay Evaluation System**
- Rule-based scoring algorithm (0-1000 points)
- Keyword detection for structural elements (introduction, thesis, conclusion)
- Word count validation and feedback generation
- Persistent storage of submissions and evaluations

**Study Schedule Generator**
- Client-side JavaScript for schedule building
- CSV export functionality for download
- Dynamic topic filtering by subject area
- Priority and duration assignment

**Content Organization**
- Hierarchical navigation: Areas → Topics → Content
- Search functionality across summaries
- Filter by subject area
- Mind map visualizations using SVG with interactive curved lines and color-coded branches
- Detailed explanations with practical examples and study tips
- Interactive question bank with explanations

**Question System**
- Multiple-choice questions (5 alternatives) per topic
- Interactive answer selection with radio buttons
- Visual feedback system showing correct/incorrect answers
- Automatic correction when revealing the answer
- Enhanced explanations with detailed educational content
- Questions organized by subject area and topic
- Difficulty level indication
- Color-coded feedback (green for correct, red for incorrect)

**Quiz System (ENEM Simulator)**
- Interactive quiz with 1500 questions from all ENEM areas
- Configurable question count: 10 (quick), 20 (medium), or 30 (complete)
- Random question selection from entire database
- Secure server-side answer validation (IDs only in client session)
- 60% minimum score for ENEM approval
- Detailed results page with:
  - Percentage score and approval status
  - Correct/incorrect answer breakdown
  - Full question review with explanations
  - Visual feedback (green for correct, red for incorrect)
- Navigation between questions with progress bar
- Client-side validation preventing incomplete submissions

**Progress Tracking**
- REST API endpoint for marking topics complete
- User-based progress storage (simple user identification)
- Last reviewed timestamps

### Routing Architecture
- **Public Routes**: Home, areas, topics, summaries, exercises/questions, mind maps, essay tool, schedule generator
- **Exercise Routes**: Question list by area, individual question view with answer reveal
- **Admin Routes**: Protected by session-based authentication
- **API Endpoints**: JSON responses for AJAX interactions (progress tracking)
- **File Downloads**: CSV export for study schedules

### Design Patterns
- **Template Inheritance**: Base template with block structure for consistent UI
- **Database Abstraction**: `get_db()` factory for connection management
- **Row Factory**: SQLite Row objects for dictionary-like access
- **Flash Messages**: Server-side feedback for user actions

## External Dependencies

### Python Libraries
- **Flask 2.3.2**: Web framework for routing, templating, and request handling
- **python-dotenv 1.0.0**: Environment variable management for configuration
- **sqlite3**: Built-in Python library (no external dependency)
- **csv**: Built-in Python library for schedule export
- **datetime**: Built-in Python library for timestamps
- **pathlib**: Built-in Python library for file path handling

### Frontend Dependencies
- **Tailwind CSS**: Loaded via CDN (https://cdn.tailwindcss.com) - no build process required
- **Browser APIs**: Fetch API for AJAX requests, localStorage potential for client-side data

### Environment Configuration
- **Required Variables**: 
  - `SECRET_KEY`: Flask session encryption (defaults to development key)
  - `ADMIN_PASS`: Admin panel password (defaults to "admin123")
- **Configuration File**: `.env` in root directory (not version controlled)

### Database
- **SQLite 3**: File-based database (`data.db`) with no external server required
- **Initialization**: `db_init.py` creates schema and enables foreign keys
- **Seeding**: 
  - `seed_resumos.py` populates initial 500+ study summaries
  - `seed_conteudo_completo.py` adds detailed explanations and practice questions with answers

### Deployment Considerations
- **Replit Compatibility**: Designed for Replit Agent v3 deployment
- **Alternative Platforms**: Compatible with any Python WSGI host (Heroku, VPS, etc.)
- **No Build Step**: Direct Flask execution with `python app.py` or `flask run`
- **Static Assets**: All CSS via CDN, no asset compilation needed