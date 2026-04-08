# SEAIT Campus Guide System Documentation

## Table of Contents
1. [System Overview](#system-overview)
2. [Architecture](#architecture)
3. [Frontend (PWA)](#frontend-pwa)
4. [Backend Services](#backend-services)
5. [Database Structure](#database-structure)
6. [Key Features](#key-features)
7. [File Structure](#file-structure)
8. [Setup & Installation](#setup--installation)
9. [API Reference](#api-reference)
10. [Dependencies](#dependencies)

---

## System Overview

**SEAIT Campus Guide** is a comprehensive Progressive Web App (PWA) designed for the South East Asian Institute of Technology (SEAIT) campus. The system helps students, faculty, and visitors navigate the campus efficiently through an interactive map, QR code scanning, AI-powered chatbot assistance, and real-time notifications.

### Purpose
- Provide indoor and outdoor campus navigation
- Help users locate buildings, classrooms, and facilities
- Offer AI-assisted guidance through a chatbot
- Enable QR code-based quick location access
- Support administrative functions for campus management
- Work fully offline as an installable PWA on mobile and desktop

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    SEAIT Campus Guide (TechnoPath)              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │           Progressive Web App (PWA)                      │  │
│  │         ┌──────────────────────────────────────┐       │  │
│  │         │  Vue.js 3 + Vite + Pinia State         │       │  │
│  │         │  ┌─────────┐ ┌─────────┐ ┌──────────┐   │       │  │
│  │         │  │HomeView │ │Navigate │ │Chatbot   │   │       │  │
│  │         │  │ (Map)   │ │ (Route) │ │(AI Bot)  │   │       │  │
│  │         │  └─────────┘ └─────────┘ └──────────┘   │       │  │
│  │         │  ┌─────────┐ ┌─────────┐ ┌──────────┐   │       │  │
│  │         │  │Settings │ │  QR     │ │Explore   │   │       │  │
│  │         │  │ (Admin) │ │ Scanner │ │(Map View)│   │       │  │
│  │         │  └─────────┘ └─────────┘ └──────────┘   │       │  │
│  │         └──────────────────────────────────────────┘       │  │
│  │         ┌──────────────────────────────────────┐           │  │
│  │         │   Offline Storage: IndexedDB         │           │  │
│  │         │   Dexie.js wrapper for client DB      │           │  │
│  │         └──────────────────────────────────────┘           │  │
│  └───────────────────────────────────────────────────────────┘  │
│                           │                                     │
│         ┌─────────────────┼─────────────────┐                  │
│         │                 │                 │                  │
│    ┌────▼────┐    ┌─────▼─────┐   ┌────▼────┐                │
│    │ Django  │    │   Flask   │   │  Web    │                │
│    │Backend  │    │ Chatbot   │   │Server   │                │
│    │(Port    │    │ (Port     │   │(Static) │                │
│    │ 8000)   │    │  5000)    │   │         │                │
│    └────┬────┘    └─────┬─────┘   └─────────┘                │
│         │               │                                     │
│    ┌────▼────┐    ┌─────▼─────┐                               │
│    │ SQLite  │    │  SQLite   │                               │
│    │ (Main)  │    │(Chatbot)  │                               │
│    └─────────┘    └───────────┘                               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Technology Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | Vue.js 3 + Vite |
| **State Management** | Pinia |
| **Backend API** | Python Django + Django REST Framework |
| **Chatbot Service** | Python Flask |
| **Authentication** | JWT (SimpleJWT) |
| **Databases** | SQLite (development), PostgreSQL (production ready) |
| **HTTP Client** | Axios |
| **QR Scanning** | jsQR (browser-based) |
| **Offline Storage** | IndexedDB (Dexie.js) |
| **Map Rendering** | Leaflet.js + SVG |
| **Pathfinding** | Dijkstra (JavaScript, client-side) |
| **GPS** | Web Geolocation API |
| **PWA Support** | Vite PWA Plugin, Service Worker |

---

## Frontend (PWA)

### Main Entry Point
**File**: `frontend/src/main.js`

The application uses a custom UI design with orange color scheme (`#FF9800`) optimized for both mobile and desktop viewing.

### Core Views

#### 1. Home View (`HomeView.vue`)
- **Interactive Map**: Full-screen SVG map with zoom/pan capabilities
- **Facility Selector**: Dropdown for buildings (RST Building, MST Building, JST Building)
- **Room Selector**: Dropdown for classrooms (CL1-CL10)
- **Search Bar**: Location search with autocomplete
- **Action Buttons**:
  - Menu (building/room/instructor info)
  - Locate (set current position)
  - Rate (app rating)
  - Notifications (with unread badge)
  - Chatbot (AI assistant)
  - QR Scanner

#### 2. Navigate View (`NavigateView.vue`)
- Turn-by-turn navigation interface
- Route visualization on map
- Building and room selection for navigation
- Floor-aware pathfinding (multi-floor support)
- Dijkstra algorithm for shortest path calculation

#### 3. Settings View (`SettingsView.vue`)
- **Login Admin**: Admin authentication (JWT-based)
- **Dark Mode**: Theme toggle
- **About Us**: Application information
- **Version Info**: Current version display
- **Check for Updates**: Update checker

#### 4. Chatbot View (`ChatbotView.vue`)
- AI conversation interface
- Offline FAQ fallback support
- Chat history with IndexedDB
- Quick action chips for common questions

#### 5. Explore/Map View (`ExploreView.vue`)
- Full-screen interactive map
- Facility and room filters
- Floor selector (Ground to 3rd floor)
- Map legend and building information

### Additional Views

| View | Description |
|--------|-------------|
| `BuildingInfoView` | Detailed building information |
| `AdminPanelView` | Room administration panel (admin only) |
| `FeedbackView` | User feedback and ratings |
| `NotificationsView` | Push notification history |
| `FavoritesView` | Saved locations |

### Navigation Structure

```javascript
App.vue (Root Shell)
├── Bottom Navigation (Mobile) / Sidebar (Desktop)
│   ├── Home (index: 0)
│   ├── Navigate (index: 1)
│   └── Settings (index: 2)
├── Menu Sheet (slide-up panel)
│   ├── Building Info
│   ├── Instructor Info
│   ├── Feedback
│   ├── Favorites
│   └── About
```

---

## Backend Services

### 1. Django Backend (`backend_django/`)

**Main File**: `backend_django/manage.py`

**Purpose**: Primary REST API server for the application

**Key Apps**:
- `users` - Admin user management with role-based access
- `facilities` - Campus buildings and facilities
- `rooms` - Classrooms, offices, and labs
- `navigation` - Navigation nodes and edges for pathfinding
- `chatbot` - FAQ entries and AI chat logs
- `notifications` - Push notifications and announcements
- `feedback` - User feedback and ratings

**Endpoints**:
- `/admin/` - Django Admin Panel (desktop-only)
- `/api/auth/login/` - JWT token obtain
- `/api/auth/refresh/` - JWT token refresh
- `/api/users/` - User management (CRUD)
- `/api/facilities/` - Facility management
- `/api/rooms/` - Room management
- `/api/navigation/` - Navigation nodes and edges
- `/api/chatbot/` - FAQ and chat endpoints
- `/api/notifications/` - Notifications
- `/api/feedback/` - Feedback submissions

**Database**: `technopath.db` (SQLite) / PostgreSQL (production)

**Run Command**:
```bash
cd backend_django
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### 2. Flask Chatbot Backend (`chatbot_flask/`)

**Main File**: `chatbot_flask/app.py`

**Purpose**: AI-powered chatbot service with SEAIT campus knowledge base

**Features**:
- Rule-based response generation with keyword matching
- Campus knowledge base (buildings, rooms, offices, facilities)
- Chat history storage in SQLite
- CORS enabled for cross-origin requests
- Support for English and Tagalog queries

**Endpoints**:
- `/health` - Service health check
- `/chat` - POST endpoint for chat messages

**Response Patterns**:
| Input Pattern | Response |
|--------------|----------|
| "hello", "hi", "kumusta" | Greeting + help offer |
| "cl1", "cl2", etc. | Classroom location guidance |
| "rst", "mst", "jst" | Building information |
| "where is", "locate", "nasaan" | Navigation guidance |
| Default | Campus guide capabilities list |

**Run Command**:
```bash
cd chatbot_flask
python app.py
# Runs at http://localhost:5000
```

---

## Database Structure

### Main Database (Django ORM)

**Tables**:

1. **admin_users** - Administrator accounts
   - `id` (INTEGER PRIMARY KEY)
   - `username` (VARCHAR 150, UNIQUE)
   - `password` (VARCHAR 128, hashed)
   - `role` (VARCHAR 20) - super_admin, dean, program_head, basic_ed_head
   - `department` (VARCHAR 50)
   - `is_active` (BOOLEAN)
   - `created_at` (DATETIME)
   - `updated_at` (DATETIME)

2. **facilities** - Campus buildings
   - `id` (INTEGER PRIMARY KEY)
   - `name` (VARCHAR 200)
   - `code` (VARCHAR 20, UNIQUE) - e.g., RST, MST, JST
   - `description` (TEXT)
   - `map_svg_id` (VARCHAR 100) - SVG element reference
   - `total_floors` (INTEGER)
   - `is_deleted` (BOOLEAN, soft delete)
   - `created_at` (DATETIME)

3. **rooms** - Classrooms and labs
   - `id` (INTEGER PRIMARY KEY)
   - `facility_id` (INTEGER, FK → facilities)
   - `name` (VARCHAR 200)
   - `code` (VARCHAR 50)
   - `floor` (INTEGER)
   - `map_svg_id` (VARCHAR 100)
   - `room_type` (VARCHAR 50) - classroom, office, lab, facility, staircase, restroom, other
   - `is_crucial` (BOOLEAN)
   - `search_count` (INTEGER)
   - `is_deleted` (BOOLEAN)
   - `created_at` (DATETIME)

4. **navigation_nodes** - Waypoints for pathfinding
   - `id` (INTEGER PRIMARY KEY)
   - `name` (VARCHAR 200)
   - `node_type` (VARCHAR 20) - room, facility, waypoint, entrance, staircase, elevator, junction
   - `facility_id` (INTEGER, FK → facilities)
   - `room_id` (INTEGER, FK → rooms)
   - `x` (FLOAT) - X coordinate
   - `y` (FLOAT) - Y coordinate
   - `floor` (INTEGER)
   - `is_deleted` (BOOLEAN)

5. **navigation_edges** - Connections between nodes
   - `id` (INTEGER PRIMARY KEY)
   - `from_node_id` (INTEGER, FK → navigation_nodes)
   - `to_node_id` (INTEGER, FK → navigation_nodes)
   - `distance` (INTEGER) - Distance in meters
   - `is_bidirectional` (BOOLEAN)
   - `is_deleted` (BOOLEAN)

6. **faq_entries** - Chatbot knowledge base
   - `id` (INTEGER PRIMARY KEY)
   - `question` (TEXT)
   - `answer` (TEXT)
   - `category` (VARCHAR 50) - location, schedule, academic, services, general
   - `keywords` (TEXT) - Comma-separated for offline matching
   - `usage_count` (INTEGER)
   - `is_deleted` (BOOLEAN)

7. **notifications** - Push notifications
   - `id` (INTEGER PRIMARY KEY)
   - `title` (VARCHAR 200)
   - `message` (TEXT)
   - `type` (VARCHAR 30) - info, success, warning, error, emergency, facility_update, etc.
   - `priority` (INTEGER) - 1=Low, 2=Medium, 3=High, 4=Urgent
   - `is_read` (BOOLEAN)
   - `created_at` (DATETIME)

8. **feedback** - User feedback
   - `id` (INTEGER PRIMARY KEY)
   - `rating` (INTEGER 1-5)
   - `comment` (TEXT)
   - `category` (VARCHAR 30)
   - `facility_id` (INTEGER, FK → facilities)
   - `room_id` (INTEGER, FK → rooms)
   - `created_at` (DATETIME)

9. **announcements** - Department announcements
   - `id` (INTEGER PRIMARY KEY)
   - `title` (VARCHAR 200)
   - `content` (TEXT)
   - `source_label` (VARCHAR 200)
   - `status` (VARCHAR 20) - pending_approval, published, rejected, archived
   - `created_at` (DATETIME)

---

## Key Features

### 1. Interactive Campus Map
- **Format**: SVG-based 2D map with zoom and pan
- **Zoom**: 0.5x to 4.0x with pinch gestures (mobile) or buttons (desktop)
- **Pan**: Full drag navigation
- **Markers**: Dynamic markers for buildings and rooms
- **Filter**: Show/hide by facility or room type
- **Floor Selector**: Multi-floor navigation support

### 2. QR Code Navigation
- **Scanner**: jsQR library (browser-based)
- **Purpose**: Quick location access via QR codes
- **Action**: Scan → Open map at specific entry point
- **Offline**: Works offline once app is installed

### 3. AI Chatbot
- **Backend**: Flask server (Python)
- **Pattern Matching**: Keyword-based responses with campus knowledge base
- **History**: IndexedDB storage for conversation logs
- **Offline Mode**: FAQ fallback when offline
- **Language Support**: English and Tagalog queries

### 4. Search Functionality
- **Type**: Full-text search across all locations
- **Scope**: Facilities, rooms, descriptions
- **Results**: Filtered list with icons and details
- **Recent Searches**: Cached in IndexedDB

### 5. Rating System
- **Scale**: 1-5 stars
- **Feedback**: Optional text comments
- **Storage**: Local (IndexedDB) and server-side sync
- **Admin View**: Dashboard statistics

### 6. Notifications
- **Badge**: Unread count on home screen
- **Types**: System updates, navigation alerts, announcements
- **Storage**: IndexedDB with server sync
- **Priority Levels**: Low, Medium, High, Urgent, Emergency

### 7. Offline Navigation (Dijkstra Algorithm)
- **Algorithm**: Dijkstra's shortest path (JavaScript implementation)
- **Data Source**: IndexedDB (navigation_nodes, navigation_edges)
- **Features**: Multi-floor pathfinding, real-time route calculation
- **GPS Integration**: Web Geolocation API for current position

### 8. Admin Panel (Django)
- **Authentication**: JWT-based secure login
- **Role-based Access**:
  - **Safety and Security Office** — full system control
  - **Program Head** — department rooms and announcements
  - **Dean** — oversight and validation
- **Dashboard**: User statistics, ratings, usage analytics
- **Management**: Edit buildings, rooms, navigation nodes
- **Approval Workflow**: Announcement approval system

### 9. PWA Features
- **Installable**: Add to home screen on Android/iOS
- **Offline Support**: Full functionality without internet
- **Background Sync**: Queue actions when offline, sync when connected
- **Push Notifications**: Web Push API (future enhancement)
- **Responsive**: Mobile-first design with desktop support

---

## File Structure

```
version4_technopath/
├── backend_django/         # Django REST API
│   ├── manage.py
│   ├── requirements.txt
│   ├── technopath/         # Project settings
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   └── apps/               # Django apps
│       ├── users/
│       ├── facilities/
│       ├── rooms/
│       ├── navigation/
│       ├── chatbot/
│       ├── notifications/
│       └── feedback/
├── frontend/               # Vue.js PWA
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   ├── public/
│   │   ├── manifest.json
│   │   └── maps/           # SVG map files
│   └── src/
│       ├── main.js
│       ├── App.vue
│       ├── router/
│       │   └── index.js
│       ├── stores/         # Pinia stores
│       │   ├── mapStore.js
│       │   ├── chatbotStore.js
│       │   └── syncStore.js
│       ├── services/
│       │   ├── api.js        # Axios HTTP client
│       │   ├── db.js         # IndexedDB (Dexie)
│       │   ├── geolocation.js
│       │   └── pathfinder.js # Dijkstra algorithm
│       ├── views/
│       │   ├── HomeView.vue
│       │   ├── NavigateView.vue
│       │   ├── ChatbotView.vue
│       │   ├── ExploreView.vue
│       │   ├── SettingsView.vue
│       │   └── NotificationsView.vue
│       ├── components/
│       │   ├── MapCanvas.vue
│       │   ├── FloorMapSVG.vue
│       │   ├── NavigationPanel.vue
│       │   ├── ChatbotWidget.vue
│       │   ├── QRScanner.vue
│       │   └── NotificationBadge.vue
│       └── assets/           # CSS and static assets
│           ├── main.css
│           ├── homeview.css
│           ├── navigate.css
│           └── ...
├── chatbot_flask/          # Python chatbot service
│   ├── app.py
│   ├── requirements.txt
│   └── chatbot.db
├── assets/                 # Map images and static assets
│   └── maps/
├── _flutter_archive/       # Original Flutter app (reference)
├── .windsurf/              # Windsurf IDE settings
├── .gitignore
├── README.md
└── SYSTEM_DOCUMENTATION.md
```

---

## Setup & Installation

### Prerequisites
- Python 3.11+
- Node.js 20+
- Git

### Backend Setup (Django)

```bash
# 1. Navigate to backend
cd backend_django

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run migrations
python manage.py migrate

# 6. Create superuser (optional)
python manage.py createsuperuser

# 7. Start server
python manage.py runserver
# Runs at http://localhost:8000
```

### Frontend Setup (Vue.js PWA)

```bash
# 1. Navigate to frontend
cd frontend

# 2. Install dependencies
npm install

# 3. Start development server
npm run dev
# Runs at http://localhost:5173

# 4. Build for production
npm run build
```

### Chatbot Setup (Flask)

```bash
# 1. Navigate to chatbot
cd chatbot_flask

# 2. Install dependencies (use same venv or create new)
pip install -r requirements.txt

# 3. Start server
python app.py
# Runs at http://localhost:5000
```

### Platform-Specific Notes

**Android (Chrome)**:
- Access PWA at `http://<computer-ip>:5173`
- Use "Add to Home Screen" for installable app experience
- Ensure devices are on same network

**iOS (Safari)**:
- Access PWA at `http://<computer-ip>:5173`
- Use "Share → Add to Home Screen"
- Camera permissions for QR scanning (granted via browser)

**Desktop**:
- Chrome/Edge: Install via address bar PWA icon
- Admin panel: http://localhost:8000/admin/

---

## API Reference

### API Service (`frontend/src/services/api.js`)

Base URL: `http://localhost:8000/api`

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/login/` | JWT token obtain |
| POST | `/auth/refresh/` | JWT token refresh |
| GET | `/users/` | List admin users |
| GET | `/facilities/` | List facilities |
| GET | `/facilities/:id/rooms/` | Rooms by facility |
| GET | `/rooms/` | List rooms |
| GET | `/navigation/nodes/` | Navigation nodes |
| GET | `/navigation/edges/` | Navigation edges |
| GET | `/chatbot/faq/` | FAQ entries |
| GET | `/notifications/` | Notifications |
| POST | `/feedback/` | Submit feedback |

### Chatbot API

Base URL: `http://localhost:5000`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Service health check |
| POST | `/chat` | Send chat message |

**Chat Request Format**:
```json
{
  "message": "Where is the library?"
}
```

**Chat Response Format**:
```json
{
  "reply": "The Library is located at the ground floor of the main building, left wing. Open the Map tab to see its location on the campus layout."
}
```

---

## Dependencies

### Frontend Dependencies (`frontend/package.json`)

| Package | Version | Purpose |
|---------|---------|---------|
| `vue` | ^3.4.0 | Core framework |
| `vue-router` | ^4.3.0 | Routing |
| `pinia` | ^2.1.0 | State management |
| `axios` | ^1.6.0 | HTTP client |
| `leaflet` | ^1.9.4 | Map rendering |
| `dexie` | ^3.2.0 | IndexedDB wrapper |
| `fuse.js` | ^7.0.0 | Fuzzy search |
| `jsqr` | ^1.4.0 | QR code scanning |

### Dev Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `vite` | ^5.0.0 | Build tool |
| `@vitejs/plugin-vue` | ^5.0.0 | Vue plugin for Vite |
| `vite-plugin-pwa` | ^0.19.0 | PWA generation |

### Python Dependencies (`backend_django/requirements.txt`)

```
django>=4.2
djangorestframework>=3.15
djangorestframework-simplejwt>=5.3
django-cors-headers>=4.3
python-decouple>=3.8
Pillow>=10.0
```

### Chatbot Dependencies (`chatbot_flask/requirements.txt`)

```
flask>=3.0
flask-cors>=4.0
requests>=2.31.0
```

---

## Development Guidelines

### Adding New Features
1. Update models in appropriate Django app
2. Create/update serializers and views
3. Add API endpoints in `urls.py`
4. Create/update Vue components in frontend
5. Update Pinia stores if state management needed
6. Update service worker config for offline support

### Theme Customization
Primary color: `#FF9800` (Orange)
- Update CSS variables in `frontend/src/assets/main.css`
- Affects all UI components automatically

### Database Migrations
1. Update models in Django app
2. Run `python manage.py makemigrations`
3. Run `python manage.py migrate`
4. Test on clean installation and upgrade paths

### Offline-First Development
1. Ensure features work with IndexedDB
2. Add sync logic in `syncStore.js`
3. Update service worker caching strategy in `vite.config.js`
4. Test with network throttling/offline mode

---

## Future Enhancements

- **Real-time GPS Navigation**: Enhanced outdoor navigation with live GPS tracking
- **Web Push Notifications**: Firebase Cloud Messaging integration
- **Multi-language Support**: Full localization for international students
- **AR Navigation**: Augmented reality waypoints (WebXR)
- **Voice Commands**: Speech-to-text for accessibility
- **Building 3D Models**: Three.js integration for 3D campus view
- **Offline Map Tile Caching**: Pre-cached map tiles for offline use

---

## Support & Contact

For technical support or feature requests, contact the SEAIT IT Department.

**Version**: 4.0.0
**Last Updated**: April 2026
**License**: Private (SEAIT Internal Use)

---

*This documentation is maintained by the SEAIT Campus Guide Development Team.*
