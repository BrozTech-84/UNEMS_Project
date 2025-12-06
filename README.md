📌 University Notice & Event Management System (UNEMS)
Project Overview

The University Notice & Event Management System is a web-based application designed to efficiently manage university notices,
events, notifications, and payments. The system allows students, staff, and administrators to access real-time updates,
register for events, and receive push notifications. It enhances communication across the university and improves event management efficiency.

#######Features
#####Core Features

Notice Management: Post, view, and categorize notices 

Event Management: 

Push Notifications: Users receive real-time notifications for new notices or events.

User Roles: Role-based access for Students, Staff, and Admins.

Database: SQLite to store all application data.

##### Advanced Features included ######

Payment Integration: M-Pesa API integration for paid event registrations.

File Uploads: Attachments and event posters.

User Profiles: Detailed user profiles with department, role, and contact info.

Search & Filtering: Search notices and events by category or date.

####💻 Technology Stack  ###
Component:	Technology
Frontend	HTML, CSS, Bootstrap
Backend	Python, Django
Database	SQLite
Notifications	Django push logic
Payment API	M-Pesa API


           ##IMPLEMENTATION SUMMARY##
  1. Authentication & User Management (theUsers App)
         ✅ Implemented Features

User Registration with:

     Username
     Email
    Password
    Role (Admin / Staff / Student)
    User Login & Logout
    Dashboard view after login
    Landing Page for unauthenticated users and guests
    Role-based access control

✅ Working Behavior

    New users are created successfully.
    Profiles are created after registering
    Logged-in users are redirected to the dashboard.
    Logged-out users are redirected to the landing page.

  ✅ Tested URLs

    / → Landing Page
    /theUsers/register/ → Registration
    /theUsers/login/ → Login
    /logout/ → Logout
    /dashboard/ → User Dashboard

 2. Notice Management System (notices App)
        ✅ Implemented Features

        Create Notice (Admin & Staff only)
        Upload Notice with title, content, and attachments
        Admin Approval System
        Public Notice Viewing 
        Staff/Admin Access Control

✅ Working Behavior

    Notices created by staff/admin are saved as pending.
    Pending notices only appear in Admin Dashboard.
    Once approved, notices appear in:
        -Logged-in user notice list
        -Public notice page (no login required)

  ✅ Tested URLs

     /notices/create/ → Create Notice
    /notices/admin/dashboar✅ Tested URLs

/notifications/ → Notification Listd/ → Admin Dashboard
    /notices/public/ → Public Notices
    /notices/admin/approve/<id>/ → Approve Notice

  3. Notification System (notifications App)
     ✅ Implemented Features

    Automatic notification creation when notices are approved
    Notification dropdown in the navbar
    Unread notification counter  

  ✅ Tested URLs
      
    /notifications/ → Notification List

4. Event Management System (events App)
    ✅ Implemented Features

  Event Model with:
     
     Title
    Venue
    Date
    Time
    Description
    Organizer
  Admin CRUD Management **
  Student Event Registration
  Attendance Tracking via EventRegistration

  ✅ Working Behavior

    Events can be created via Admin Panel.
    Students can register for events.

✅ Tested URLs

    /events/ → Event List
    /events/register/<id>/ → Register for Event

5. Landing Page Integration (homePage App)
    ✅ Implemented Features

       First page shown to all users before login
       Login and Register buttons
       Public Notices link

✅ Working Behavior

    Unauthenticated users see landing page
    After registration or login, users move to dashboard
    After logout, users return to landing page
       
