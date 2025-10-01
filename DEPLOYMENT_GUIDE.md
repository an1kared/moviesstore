# PythonAnywhere Deployment Guide - Movie Store with Petitions

## 🚀 Complete Deployment Guide for Movie Store + Petition System

### Prerequisites
- PythonAnywhere account (free tier works)
- Your project files ready for upload

---

## Step 1: Prepare Your Files for Upload

### Files to Upload
Upload these folders/files to PythonAnywhere:
```
moviesstore/
├── accounts/
├── cart/
├── home/
├── movies/
├── petitions/          # ← NEW: Petition system
├── moviesstore/
├── media/
├── manage.py
├── requirements.txt
└── db.sqlite3 (if you have existing data)
```

### ⚠️ Important: Include the petitions folder!
Make sure to upload the entire `petitions/` folder with all its contents:
- `models.py` (with MoviePetition and PetitionVote models)
- `views.py` (with petition views)
- `forms.py` (with form validation)
- `urls.py` (with petition URLs)
- `templates/petitions/` (with the new templates)
- `migrations/` (with the new migration files)

---

## Step 2: Clone from Git Repository (Recommended)

### 🎯 Your Repository is Ready!
Your code is now available at: **https://github.com/an1kared/moviesstore.git**

### Clone the Repository
Open a **Bash console** in PythonAnywhere and run:
```bash
cd /home/yourusername/
git clone https://github.com/an1kared/moviesstore.git
```

This will create a `moviesstore` folder with all your code including the petition system!

### Alternative: Using PythonAnywhere File Manager
If you prefer to upload manually:
1. Go to PythonAnywhere dashboard
2. Click "Files" tab
3. Navigate to `/home/yourusername/`
4. Upload your `moviesstore` folder
5. Extract if it's a zip file

---

## Step 3: Install Dependencies

Open a **Bash console** in PythonAnywhere and run:
```bash
cd /home/yourusername/moviesstore
pip3.10 install --user -r requirements.txt
```

**Required packages:**
- Django 5.0
- Pillow (for image handling)
- Any other dependencies in requirements.txt

---

## Step 4: Database Setup

Run these commands in the console:
```bash
cd /home/yourusername/moviesstore

# Create migrations for all apps (including petitions)
python3.10 manage.py makemigrations

# Apply all migrations
python3.10 manage.py migrate

# Collect static files
python3.10 manage.py collectstatic --noinput
```

### 🆕 New: Petitions Migration
The petitions app will create these tables:
- `petitions_moviepetition` (stores petition data)
- `petitions_petitionvote` (prevents duplicate voting)

---

## Step 5: Create Superuser (Optional but Recommended)

```bash
python3.10 manage.py createsuperuser
```
Follow the prompts to create an admin account.

---

## Step 6: Configure Web App

### 6.1 Create New Web App
1. Go to the "Web" tab in PythonAnywhere
2. Click "Add a new web app"
3. Choose "Manual Configuration" → "Python 3.10"
4. Set the source code directory: `/home/yourusername/moviesstore`
5. Set the working directory: `/home/yourusername/moviesstore`

### 6.2 WSGI Configuration
Edit the WSGI file and replace the content with:
```python
import os
import sys

# Add your project directory to the Python path
path = '/home/yourusername/moviesstore'
if path not in sys.path:
    sys.path.append(path)

# Set the Django settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'moviesstore.settings'

# Get the Django WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

**Replace `yourusername` with your actual PythonAnywhere username!**

---

## Step 7: Configure Static and Media Files

### Static Files
In the "Static files" section, add:
- **URL:** `/static/`
- **Directory:** `/home/yourusername/moviesstore/staticfiles`

### Media Files
In the "Static files" section, add:
- **URL:** `/media/`
- **Directory:** `/home/yourusername/moviesstore/media`

---

## Step 8: Update Settings (if needed)

Check your `settings.py` file. The `ALLOWED_HOSTS` should include your domain:
```python
ALLOWED_HOSTS = ['yourusername.pythonanywhere.com', '127.0.0.1', 'localhost']
```

---

## Step 9: Reload and Test

1. Click the green "Reload" button in the Web tab
2. Visit your site: `https://yourusername.pythonanywhere.com`
3. Test the petition feature:
   - Go to `/petitions/`
   - Create a new petition
   - Vote on petitions

---

## 🆕 Testing the Petition Feature

### Test Checklist:
- [ ] Navigate to `/petitions/` - should show petition list
- [ ] Click "Start a New Petition" - should require login
- [ ] Create a petition with valid data
- [ ] Vote on the petition
- [ ] Verify vote count increases
- [ ] Try voting again - should show "already voted" message
- [ ] Check that petitions are sorted by vote count

---

## Common Issues & Solutions

### Issue: 500 Error
**Solution:**
1. Check the error log in the "Web" tab
2. Make sure all migrations are applied:
   ```bash
   python3.10 manage.py migrate
   ```
3. Verify your domain is in `ALLOWED_HOSTS`

### Issue: Petitions Page Not Found (404)
**Solution:**
1. Make sure you uploaded the `petitions/` folder
2. Check that `petitions` is in `INSTALLED_APPS` in settings.py
3. Verify the URL patterns are correct

### Issue: Static Files Not Loading
**Solution:**
1. Run: `python3.10 manage.py collectstatic --noinput`
2. Check static files configuration in Web tab
3. Make sure the staticfiles directory exists

### Issue: Media Files Not Loading
**Solution:**
1. Verify media files are uploaded to the correct directory
2. Check media files configuration in Web tab
3. Ensure proper file permissions

### Issue: Database Errors
**Solution:**
1. Make sure migrations are applied: `python3.10 manage.py migrate`
2. Check if the database file exists and has proper permissions
3. Verify all apps are in `INSTALLED_APPS`

### Issue: Form Validation Errors
**Solution:**
1. Check that the petitions app is properly installed
2. Verify form templates are uploaded
3. Make sure CSRF tokens are working

---

## 🎯 New Features Available After Deployment

### Petition System Features:
1. **Create Petitions**: Users can request movies to be added
2. **Vote on Petitions**: One vote per user per petition
3. **View Results**: Petitions sorted by popularity
4. **User Feedback**: Success/error messages
5. **Responsive Design**: Works on all devices

### Navigation:
- "Petitions" link in main navigation
- Accessible at `/petitions/`
- Create new petitions at `/petitions/new/`

---

## Important Notes

- **Replace `yourusername`** with your actual PythonAnywhere username throughout
- **Make sure paths match** your actual project location
- **Test thoroughly** - create accounts, petitions, and votes
- **The petition system requires login** for creating and voting
- **All existing features** (movies, cart, accounts) remain unchanged

---

## 🎉 You're Done!

Your Movie Store with the new Petition System should now be live at:
`https://yourusername.pythonanywhere.com`

**Test the complete user story:**
1. Register/Login
2. Go to Petitions
3. Create a petition for a movie
4. Vote on petitions
5. See the results!

Happy deploying! 🚀


