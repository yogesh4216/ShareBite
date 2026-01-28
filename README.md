# ShareBite - Food Rescue Platform 🍽️

## 🌟 Overview
ShareBite connects food donors with those in need, reducing waste and fighting hunger through a mobile-first platform.

## 🎥 Demo
- **Live App**: https://expo.dev/preview/update?message=Initial+commit%0A%0AGenerated+by+create-expo-app+3.5.3.&updateRuntimeVersion=1.0.0&createdAt=2026-01-28T16%3A40%3A52.674Z&slug=exp&projectId=9f19d301-00b6-4ab8-9442-102dc0e27e2d&group=3ed14f9c-6090-4236-8060-c3251cff1352
- **Backend API**: https://sharebite-api.onrender.com
- **Demo Video**: [YouTube Link]
- **Screenshots**: See `/screenshots` folder

## 🚀 Quick Start for Judges

### Try the App (No Installation Required)
1. Install **Expo Go** app (iOS/Android)
2. Scan this QR code or visit: exp://exp.host/@username/sharebite
3. Login with demo credentials:
   - Username: `demo_receiver`
   - Password: `demo123`

### Features to Test
- ✅ Browse available food listings
- ✅ Claim food items
- ✅ View impact dashboard
- ✅ Track your claims
- ✅ Donate food (use `demo_provider` / `demo123`)

## 🏗️ Architecture

```
┌─────────────────┐
│  React Native   │
│   Mobile App    │
│   (Expo)        │
└────────┬────────┘
         │
         │ REST API
         │
┌────────▼────────┐
│  Django REST    │
│   Framework     │
└────────┬────────┘
         │
┌────────▼────────┐
│   PostgreSQL    │
│    Database     │
└─────────────────┘
```

## 💻 Tech Stack

### Frontend
- React Native
- Expo
- React Navigation
- Axios
- AsyncStorage

### Backend
- Django 4.2
- Django REST Framework
- PostgreSQL
- JWT Authentication

### Deployment
- Backend: Render.com
- Mobile: Expo Published
- Database: Render PostgreSQL

## 📱 Features

### For Receivers
- Browse available food
- Real-time availability
- Location-based search
- Claim tracking
- Impact dashboard

### For Providers
- List surplus food
- Manage donations
- Track impact
- Notifications

### General
- Professional UI/UX
- Dark mode support
- Offline capability
- Push notifications

## 🛠️ Local Development

### Backend Setup
```bash
cd sharebite_backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Mobile Setup
```bash
cd sharebite_mobile
npm install
npx expo start
```

## 🌍 Impact

- **Food Waste Reduction**: Track CO₂ and water saved
- **Community Support**: Connect donors with receivers
- **Sustainability**: Promote circular economy
- **Social Good**: Fight hunger and waste

## 📊 Metrics

- Real-time impact tracking
- CO₂ emissions prevented
- Water conservation
- Meals saved

## 🔐 Security

- JWT authentication
- Secure API endpoints
- HTTPS encryption
- Data validation

## 📄 License
MIT License

## 👥 Team
[Your Name/Team Name]

## 📞 Contact
[Your Email]

---

**Built for [Hackathon Name] 2026**
