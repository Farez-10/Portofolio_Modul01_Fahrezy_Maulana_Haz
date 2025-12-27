# Enterprise Recruitment Management System – PT Rimbo Peraduan

## 📌 Overview
This project is an **Enterprise Recruitment Management System** developed as part of a professional software portfolio.  
The system is designed to support **internal HR recruitment operations** at **PT Rimbo Peraduan**, focusing on structured data management, process efficiency, and traceability.

Built using **Python and MySQL**, this application demonstrates practical implementation of recruitment workflows commonly used in corporate environments.

---

## 🎯 Project Objectives
- Provide a structured system to manage employee recruitment data
- Simulate real-world HR recruitment workflows
- Demonstrate enterprise-ready CRUD operations
- Ensure data consistency, validation, and auditability
- Serve as a professional portfolio project (non-academic)

---

## 🏢 Business Context
Recruitment departments require accurate, consistent, and traceable applicant data to support hiring decisions.  
This system addresses those needs by offering a **centralized recruitment data management solution** suitable for internal HR use.

### Business Value
- Centralized applicant records  
- Reduced manual errors  
- Clear recruitment status tracking  
- Data modification audit trail  
- Improved administrative efficiency  

---

## 👥 Intended Users
- HR Administrators  
- Recruitment Officers  
- HR Operations Staff  

---

## ⚙️ System Features

### 🔐 Authentication & Access Control
- Admin login system
- Controlled access to recruitment data
- Session-based user activity tracking

### ➕ Applicant Data Management (Create)
- Automatic applicant ID generation
- Mandatory input validation
- Email and phone number format validation
- Confirmation before data submission

### 📄 Data Viewing & Search (Read)
- Display all applicant records in tabular format
- Search applicants by unique ID
- Clean and readable console output

### ✏️ Data Update (Update)
- Modify applicant personal and recruitment information
- Controlled recruitment status updates
- Automatic change logging

### ❌ Data Removal (Delete)
- Delete individual or multiple records
- Confirmation prompts to prevent accidental deletion

### 🕒 Audit Trail & History Logging
- Records every modification with:
  - Timestamp
  - Admin username
  - Applicant ID
  - Modified field
  - Previous and updated values

### 📤 Data Export
- Export recruitment data to CSV for reporting and analysis

---

## 🗂️ Data Structure
The system uses **Python classes**, **lists**, and **dictionaries**, combined with **MySQL database integration** for persistent data storage.

### Applicant Data Includes:
- Applicant ID  
- Full Name  
- Position Applied  
- Education  
- Work Experience  
- Contact Number  
- Email Address  
- Recruitment Status  

---

## 🛠️ Technology Stack
- **Programming Language:** Python  
- **Database:** MySQL  
- **Libraries & Tools:**  
  - `datetime` (audit logging)
  - `csv` (data export)

---

## ▶️ How to Run the Application
1. Ensure **Python 3.x** and **MySQL** are installed
2. Configure database connection settings
3. Run the application:
   ```bash
   python portal_pelamar.py
