# Peer Review Django Project

This repository contains the code for a class project developed as part of **UVA's CS 3240: Software Engineering**. The project is a **Peer Review Web Application** built using Django. The application enables users to collaborate on projects through file uploads, comments, and role-based permissions. It integrates features such as Google login, Amazon S3 for file storage, and PostgreSQL for metadata management, with deployment on Heroku.

## Project Description

The goal of this project was to create a community board where users could share projects, upload files, and provide peer feedback. Key features include:
- User authentication via Google login.
- File uploads to Amazon S3 with associated metadata.
- Project details, user roles, and comments stored in PostgreSQL.
- Role-based access for administrators, members, and anonymous users.
- Deployment on Heroku for accessibility.

## Authors

The project was developed collaboratively by the following team members:
- **Aleya Banthavong**
- **Ahmed Mohamed**
- **Catherine Brockenbrough**
- **Ryan Leyhe**
- **Kyle Phillips**

## My Contributions (Catherine Brockenbrough)

1. **Role-Based Permissions and Views**  
   - Designed and implemented role-based functionality, distinguishing PMA administrators, common users, and anonymous users.  
   - Built custom dashboards and project views tailored to user roles, ensuring appropriate access and functionality.  

2. **File and Project Search Features**  
   - Implemented the file search feature, enabling users to filter files by name or keywords.  
   - Developed and refined the project search functionality, including building the search partial for seamless integration into various pages.  
   - Fixed bugs related to search visibility and role-based access for administrators and anonymous users.

3. **Prompts and Discussion Board Features**  
   - Added functionality to create, display, and delete prompts and responses.  
   - Improved the discussion board’s interactivity with no-page-refresh updates for a smoother user experience.  

4. **Profile and Settings Pages**  
   - Created the profile and settings pages, allowing users to view and edit their personal information.  
   - Built the edit profile page with pre-filled forms for easier updates and enforced unique usernames on the settings page.  

5. **UI/UX Enhancements**  
   - Redesigned the popular projects page for better usability and visual appeal.  
   - Improved the UI for project lists, dashboards, and file views, ensuring consistency and clarity.  
   - Fixed layout bugs, such as ensuring the footer sticks to the bottom of pages.  

6. **Bug Fixes and Code Maintenance**  
   - Fixed various critical bugs, including issues with search functionality, popular projects upvote counts, and compatibility between requests and invitations.  
   - Refactored and cleaned up the codebase by removing unused methods and redundant elements.  