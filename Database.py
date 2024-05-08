import sqlite3
from UsersData import *
#support regular expression
import re

######
    # Admin can only be created by uncommenting line 69 in code
######

#name of database
DB_FILE = 'database.db'

def init_db():

    #establish connection btw sqlite and databasefile
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    #create user(admin,dr,patient) table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS User (
            id INTEGER PRIMARY KEY UNIQUE,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            phone TEXT NOT NULL,
            password TEXT NOT NULL,
            userType TEXT NOT NULL
        )
    ''')

    #Create table to save report
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Report (
            id INTEGER PRIMARY KEY UNIQUE,
            report_date DATETIME DEFAULT CURRENT_TIMESTAMP,
            user_id INTEGER NOT NULL,
            symptoms TEXT,
            symptom_duration TEXT,
            breathing_difficulty TEXT,
            coughing_mucus TEXT,
            mucus_color_consistency TEXT,
            chest_pain TEXT,
            chest_pain_description TEXT,
            medical_conditions TEXT,
            smoking TEXT,
            smoking_details TEXT,
            family_history TEXT,
            Result TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES User(id)
        )
    ''')

    #create table for response 
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Response (
            id INTEGER PRIMARY KEY UNIQUE,
            user_id INTEGER,
            doctor_id INTEGER,
            report_id INTEGER,
            response TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES User(id),
            FOREIGN KEY(doctor_id) REFERENCES User(id),
            FOREIGN KEY(report_id) REFERENCES Report(id)
        )
    ''')

    conn.commit()
    conn.close()
    # create_user(User("Admin","Admin@pneumoxpert.com","123890218","Admin123",type="admin"),type="admin")
    


# Load user data from the database based on a user ID
def load_user(user_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM User WHERE id = ?', (user_id))
    user_data = cursor.fetchone()
    conn.close()
    if user_data:
        return User(user_data[1], user_data[2], user_data[3], user_data[4],user_data[5])
    return None, None




# Function to check if an email already exists in the database
def email_exists(email):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT email FROM User WHERE email = ?', (email.lower(),))
    result = cursor.fetchone()
    conn.close()
    return result is not None





# Function to check if a username already exists in the database
def username_exists(username):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT username FROM User WHERE username = ?', (username,))
    result = cursor.fetchone()
    conn.close()
    return result is not None





# Check if email is valid using a simple regex pattern
def is_valid_email(email):
    return re.match(r'^[\w\.-]+@[\w\.-]+$', email) is not None





# Check if password is strong enough
def is_strong_password(password):
    '''Password must contain 8-15 characters with lowercase, uppercase, and numbers'''

    if len(password) < 8 or len(password) > 15:
        return False
    elif not re.search("[a-z]", password):
        return False
    elif not re.search("[A-Z]", password):
        return False
    elif not re.search("[0-9]", password):
        return False
    else:
        return True





# Authenticate the user by checking and comparing email and pass in the database
def authenticate_user(email, password):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM User WHERE email = ?', (email.lower(),))
    user_data = cursor.fetchone()
    conn.close()

    if user_data and password == user_data[4]:
        return User(user_data[1], user_data[2], user_data[3], user_data[4], user_data[5]), user_data[0]
    return None,None





# Create a new user(patient) and add to the database
def create_user(user,type = "patient"):
    conn = None
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO User (username, email, phone, password , userType
                               ) 
            VALUES (?, ?, ?, ?, ?)
        ''', (
            user.username, user.email.lower(), user.phone, user.password, user.type
        ))
        conn.commit()
    except sqlite3.Error as e:
        print("Database error:", str(e))
        raise e
    finally:
        if conn:
            conn.close()






# create report and insert data into report
def create_record(report):
    conn = None
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Report (user_id, symptoms, symptom_duration, breathing_difficulty, 
            coughing_mucus, mucus_color_consistency, chest_pain, chest_pain_description, 
            medical_conditions, smoking, smoking_details, family_history, Result
                               )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''',
                    (report.U_ID, report.symptoms, report.symptom_duration, report.breathing_difficulty, 
                     report.coughing_mucus, report.mucus_color_consistency, report.chest_pain, report.chest_pain_description, 
                     report.medical_conditions, report.smoking, report.smoking_details, report.family_history, report.result))
        
        conn.commit()
        print("inserted successfully")
    except Exception as e:
        print("Database error:", str(e))
        raise e
    finally:
        if conn:
            conn.close()
            
            




#fetching most recent report         
def fetch_most_recent_report(user_id):
    conn = None
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM Report WHERE user_id = ? ORDER BY report_date DESC LIMIT 1
        ''', (user_id,))
        report_data = cursor.fetchone()
        conn.close()
        if report_data:
            return Report(report_data[2], report_data[3], report_data[4], report_data[5], report_data[6], report_data[7], report_data[8], report_data[9], report_data[10], report_data[11], report_data[12], report_data[13], report_data[14]),(report_data[0],report_data[1])
        return None
    except Exception as e:
        print("Database error:", str(e))
        raise e
    finally:
        if conn:
            conn.close()





#fetching all reports
def fetch_all_reports(user_id):
    conn = None
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM Report WHERE user_id = ? ORDER BY report_date
        ''', (user_id,))
        report_db = cursor.fetchall()
        reports = []
        for report_data in report_db:
            reports.append([report_data[0],report_data[1],report_data[2], report_data[3], report_data[4], report_data[5], report_data[6], report_data[7], report_data[8], report_data[9], report_data[10], report_data[11], report_data[12], report_data[13], report_data[14]])
            # reports["ID_Timestamp"].append([report_data[0],report_data[1]])
        conn.close()
        if reports != []:
            return reports
        return None
    except Exception as e:
        print("Database error:", str(e))
        raise e
    finally:
        if conn:
            conn.close()
    




#fetches a specific report from the database, along with prescription information  
def fetch_report_from_database(report_ID):
    conn = None
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM Report WHERE id = ?
        ''', (report_ID,))
        report_data = cursor.fetchone()
        cursor = conn.cursor()
        cursor.execute('''
        SELECT response FROM Response WHERE user_id = ? AND report_id = ? LIMIT 1
    ''', (report_data[2],report_data[0]))
        prescription = cursor.fetchone()
        if prescription:
            prescription = prescription[0]
           
        else:
            prescription = "Pending"
        conn.close()
        if report_data:
            return Report(report_data[2], report_data[3], report_data[4], report_data[5], report_data[6], report_data[7], report_data[8], report_data[9], report_data[10], report_data[11], report_data[12], report_data[13], report_data[14]),(report_data[0],report_data[1],prescription)
        return None
    except Exception as e:
        print("Database error:", str(e))
        raise e
    finally:
        if conn:
            conn.close()





# fetch all report along with comments from Response table if no comment then return pending
def fetch_all_reports_with_comments(user_id):
    conn = None
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM Report WHERE user_id = ? ORDER BY report_date DESC
        ''', (user_id,))
        report_db = cursor.fetchall()
        reports = []
        for report_data in report_db:
            cursor = conn.cursor()
            cursor.execute('''
            SELECT response FROM Response WHERE user_id = ? AND report_id = ? LIMIT 1
        ''', (report_data[2],report_data[0]))
            prescription = cursor.fetchone()
            if prescription:
                prescription = prescription[0]
            else:
                prescription = "Pending"
            reports.append([report_data[0],report_data[1],report_data[2], report_data[3], report_data[4], report_data[5], report_data[6], report_data[7], report_data[8], report_data[9], report_data[10], report_data[11], report_data[12], report_data[13], report_data[14],prescription])
            # reports["ID_Timestamp"].append([report_data[0],report_data[1]])
        conn.close()
        if reports != []:
            return reports
        return None
    except Exception as e:
        print("Database error:", str(e))
        raise e
    finally:
        if conn:
            conn.close()






#create a new response entry in the Response table of the database
def create_Responce(U_ID,D_ID,R_ID,Response):
    conn = None
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Response (user_id, doctor_id, report_id, response
                               )
            VALUES (?, ?, ?, ?)
        ''', (U_ID,D_ID,R_ID,Response))
        conn.commit()
    except sqlite3.Error as e:
        print("Database error:", str(e))
        raise e
    finally:
        if conn:
            conn.close()
            




# fetch all reports that has PNEUMONIC results and are not responded to yet
def fetch_all_reports_pneumonia():
    conn = None
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM Report WHERE Result LIKE '%Pneumonia Detected.%' AND id NOT IN (SELECT report_id FROM Response)
        ''')
        report_db = cursor.fetchall()
        reports = []
        for report_data in report_db:
            cursor = conn.cursor()
            cursor.execute('''
            SELECT response FROM Response WHERE user_id = ? AND report_id = ? LIMIT 1
        ''', (report_data[2],report_data[0]))
            prescription = cursor.fetchone()
            if prescription:
                prescription = prescription[0]
            else:
                prescription = "Pending"
            reports.append([report_data[0],report_data[1],report_data[2], report_data[3], report_data[4], report_data[5], report_data[6], report_data[7], report_data[8], report_data[9], report_data[10], report_data[11], report_data[12], report_data[13], report_data[14],prescription])
            # reports["ID_Timestamp"].append([report_data[0],report_data[1]])
        conn.close()
        if reports != []:
            return reports
        return None
    except Exception as e:
        print("Database error:", str(e))
        raise e
    finally:
        if conn:
            conn.close()






#fetching reports that has NON-PNEUMONIC results
def fetch_all_reports_nonPneumonia():
    conn = None
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM Report WHERE Result LIKE '%Pneumonia Not Detected.%' AND id NOT IN (SELECT report_id FROM Response)
        ''')
        report_db = cursor.fetchall()
        reports = []
        for report_data in report_db:
            cursor = conn.cursor()
            cursor.execute('''
            SELECT response FROM Response WHERE user_id = ? AND report_id = ? LIMIT 1
        ''', (report_data[2],report_data[0]))
            prescription = cursor.fetchone()
            if prescription:
                prescription = prescription[0]
            else:
                prescription = "Pending"
            reports.append([report_data[0],report_data[1],report_data[2], report_data[3], report_data[4], report_data[5], report_data[6], report_data[7], report_data[8], report_data[9], report_data[10], report_data[11], report_data[12], report_data[13], report_data[14],prescription])
            # reports["ID_Timestamp"].append([report_data[0],report_data[1]])
        conn.close()
        if reports != []:
            return reports
        return None
    except Exception as e:
        print("Database error:", str(e))
        raise e
    finally:
        if conn:
            conn.close()
            







#fetches reports that are already responded by doctor
def getReportsRespondedBy(Doctor_Id):
    conn = None
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * 
            FROM Report 
            WHERE id IN (
                SELECT report_id 
                FROM Response 
                WHERE doctor_id = ?
            )
        ''',(Doctor_Id,))
        report_db = cursor.fetchall()
        reports = []
        for report_data in report_db:
            cursor = conn.cursor()
            cursor.execute('''
            SELECT response FROM Response WHERE user_id = ? AND report_id = ? LIMIT 1
        ''', (report_data[2],report_data[0]))
            prescription = cursor.fetchone()
            if prescription:
                prescription = prescription[0]
            else:
                prescription = "Pending"
            reports.append([report_data[0],report_data[1],report_data[2], report_data[3], report_data[4], report_data[5], report_data[6], report_data[7], report_data[8], report_data[9], report_data[10], report_data[11], report_data[12], report_data[13], report_data[14],prescription])
        conn.close()
        if reports != []:
            return reports
        return None
    except Exception as e:
        print("Database error:", str(e))
        raise e
    finally:
        if conn:
            conn.close()
            







#counting num of patients            
def count_all_patients():
    conn = None
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT COUNT(*) FROM User WHERE userType = 'patient'
        ''')
        count = cursor.fetchone()
        conn.close()
        if count:
            return count[0]
        return None
    except Exception as e:
        print("Database error:", str(e))
        raise e
    finally:
        if conn:
            conn.close()





#counting num of doctors          
def count_all_doctors():
    conn = None
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT COUNT(*) FROM User WHERE userType = 'Doctor'
        ''')
        count = cursor.fetchone()
        conn.close()
        if count:
            return count[0]
        return None
    except Exception as e:
        print("Database error:", str(e))
        raise e
    finally:
        if conn:
            conn.close()
            




#counting PNEUMONIC cases
def count_all_pneumoniaCases():
    conn = None
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT COUNT(*) FROM Report WHERE Result LIKE '%Pneumonia Detected.%'
        ''')
        count = cursor.fetchone()
        conn.close()
        if count:
            return count[0] if count[0]>0 else 0
        return None
    except Exception as e:
        print("Database error:", str(e))
        raise e
    finally:
        if conn:
            conn.close()






#counting NON-PNEUMONIC cases        
def count_all_nonPneumoniaCases():
    conn = None
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT COUNT(*) FROM Report WHERE Result LIKE '%Pneumonia Not Detected.%'
        ''')
        count = cursor.fetchone()
        conn.close()
        if count:
            return count[0] if count[0]>0 else 0
        return None
    except Exception as e:
        print("Database error:", str(e))
        raise e
    finally:
        if conn:
            conn.close()
            
    