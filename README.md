# ShareBite - Food Waste Reduction Platform

A comprehensive marketplace platform connecting food providers (restaurants, grocery stores, households) with receivers (NGOs, individuals) to redistribute surplus food and reduce waste.

## 🌟 Features

### Backend (Django + PostgreSQL)
- **User Authentication**: JWT-based authentication with role-based access (Provider, Receiver, NGO)
- **Food Listings**: CRUD operations for surplus food with expiry tracking
- **Claims Management**: Request and claim food items with status tracking
- **Real-time Notifications**: Twilio SMS integration for pickup alerts
- **Analytics Dashboard**: Track meals saved, carbon footprint reduced, and community impact
- **REST API**: Comprehensive API with Swagger documentation

### Frontend (React Native + Expo)
- **Cross-platform**: Works on iOS and Android
- **Authentication**: Login and registration with role selection
- **Provider Features**:
  - Create and manage food listings
  - Track claims and pickups
  - View impact statistics
- **Receiver Features**:
  - Browse available food with search
  - Claim food items
  - Track claimed items
  - View personal impact
- **Analytics Dashboard**: Personal and global impact visualization

## 🚀 Quick Start

### Backend Setup

1. **Navigate to backend directory**:
   ```bash
   cd sharebite_backend
   ```

2. **Activate virtual environment**:
   ```bash
   source venv/bin/activate
   ```

3. **Run migrations** (already completed):
   ```bash
   ./venv/bin/python manage.py migrate
   ```

4. **Create a superuser** (optional):
   ```bash
   ./venv/bin/python manage.py createsuperuser
   ```

5. **Start the development server**:
   ```bash
   ./venv/bin/python manage.py runserver
   ```

   The API will be available at `http://localhost:8000`

6. **Access API Documentation**:
   - Swagger UI: `http://localhost:8000/api/docs/`
   - ReDoc: `http://localhost:8000/api/redoc/`
   - Admin Panel: `http://localhost:8000/admin/`

### Frontend Setup

1. **Navigate to mobile directory**:
   ```bash
   cd sharebite_mobile
   ```

2. **Update API URL** (if needed):
   - Edit `src/services/api.js`
   - Change `API_URL` to your backend URL

3. **Start Expo**:
   ```bash
   npm start
   ```

4. **Run on device/emulator**:
   - Press `i` for iOS simulator
   - Press `a` for Android emulator
   - Scan QR code with Expo Go app for physical device

## 📱 User Flows

### Provider Flow
1. Register as Provider
2. Create food listings with expiry details
3. Receive notifications when food is claimed
4. Mark listings as completed
5. View impact dashboard

### Receiver Flow
1. Register as Receiver
2. Browse available food
3. Claim desired items
4. Track pickup status
5. View personal impact

## 🔧 Configuration

### Environment Variables (.env)

The backend uses a `.env` file for configuration:

```env
# Database (SQLite enabled by default for demo)
USE_SQLITE=True

# Twilio (optional for demo)
TWILIO_ACCOUNT_SID=your_sid
TWILIO_AUTH_TOKEN=your_token
TWILIO_PHONE_NUMBER=your_number

# Django
DEBUG=True
SECRET_KEY=your-secret-key
```

### Database Options

**SQLite (Default - for demo)**:
- Already configured in `.env`
- No additional setup required

**PostgreSQL (Production)**:
1. Install PostgreSQL
2. Create database: `createdb sharebite_db`
3. Update `.env`:
   ```env
   USE_SQLITE=False
   DB_NAME=sharebite_db
   DB_USER=postgres
   DB_PASSWORD=your_password
   ```

### Twilio Setup (Optional)

1. Sign up at [twilio.com](https://www.twilio.com)
2. Get Account SID, Auth Token, and Phone Number
3. Update `.env` with credentials
4. Notifications will be sent automatically on claims

## 📊 API Endpoints

### Authentication
- `POST /api/auth/register/` - Register new user
- `POST /api/auth/login/` - Login and get JWT tokens
- `GET /api/auth/profile/` - Get user profile
- `PATCH /api/auth/profile/` - Update profile

### Listings
- `GET /api/listings/` - List all available food
- `POST /api/listings/` - Create new listing
- `GET /api/listings/{id}/` - Get listing details
- `PATCH /api/listings/{id}/` - Update listing
- `DELETE /api/listings/{id}/` - Delete listing
- `GET /api/listings/my_listings/` - Get user's listings
- `POST /api/listings/{id}/mark_completed/` - Mark as completed

### Claims
- `GET /api/claims/` - List user's claims
- `POST /api/claims/` - Create new claim
- `POST /api/claims/{id}/confirm/` - Confirm claim (provider)
- `POST /api/claims/{id}/complete/` - Complete claim
- `POST /api/claims/{id}/cancel/` - Cancel claim

### Analytics
- `GET /api/analytics/dashboard/` - Get user dashboard
- `GET /api/analytics/global_impact/` - Get global statistics

## 🏗️ Project Structure

```
sharebite/
├── sharebite_backend/          # Django backend
│   ├── accounts/               # User management
│   ├── listings/               # Food listings
│   ├── claims/                 # Claims management
│   ├── notifications/          # Twilio integration
│   ├── analytics/              # Impact tracking
│   ├── sharebite/              # Django settings
│   └── manage.py
│
└── sharebite_mobile/           # React Native frontend
    ├── src/
    │   ├── screens/            # App screens
    │   ├── services/           # API integration
    │   └── components/         # Reusable components
    └── App.js                  # Main app component
```

## 🎯 Demo Accounts

Create test accounts with different roles:

**Provider Account**:
- Username: `restaurant1`
- Role: Provider
- Can create listings

**Receiver Account**:
- Username: `receiver1`
- Role: Receiver
- Can browse and claim food

## 🌍 Impact Tracking

The platform automatically calculates:
- **Meals Saved**: Based on completed claims
- **Weight**: Total kg of food redistributed
- **Carbon Footprint**: CO₂ equivalent reduced (calculated per food type)

## 🔒 Security Features

- JWT authentication with token refresh
- Password validation
- CORS configuration
- Role-based permissions
- Input validation and sanitization

## 📈 Scalability

The platform is designed to scale:
- PostgreSQL for production database
- AWS/Heroku deployment ready
- Stateless API design
- Efficient database indexing
- Pagination for large datasets

## 🛠️ Technologies Used

### Backend
- Django 4.2.9
- Django REST Framework
- PostgreSQL / SQLite
- Twilio API
- JWT Authentication
- Swagger/ReDoc

### Frontend
- React Native
- Expo
- React Navigation
- Axios
- AsyncStorage

## 📝 License

This project is built for demonstration purposes.

## 🤝 Contributing

This is a demo project showcasing a food waste reduction platform.

## 📧 Support

For questions or issues, please refer to the API documentation at `/api/docs/`.
