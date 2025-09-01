# Testing Plan for Notifications and Live Location Tracking

## Step 1: Install Dependencies
- [ ] Install Python dependencies: `pip install -r requirements.txt`

## Step 2: Database Setup
- [ ] Run migrations: `python manage.py migrate`

## Step 3: Create Test Data (if needed)
- [ ] Create superuser: `python manage.py createsuperuser`
- [ ] Create test users (driver, student/staff) via admin or fixtures

## Step 4: Run Development Server
- [ ] Start server: `python manage.py runserver`

## Step 5: Test Driver Login and Notifications
- [ ] Login as driver user
- [ ] Update location via update_location view
- [ ] Check console for email notification output

## Step 6: Test Live Location Tracking
- [ ] Open live_tracking page as user
- [ ] Select a route
- [ ] Verify map shows driver's location
- [ ] Update driver's location and check real-time updates

## Step 7: Verify WebSocket Functionality
- [ ] Check browser console for WebSocket connection
- [ ] Ensure location updates are broadcasted via WebSocket
