from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session, make_response
import re
# Python Imaging Library
from PIL import Image
from io import BytesIO
from preprocess_Classify import *
from Database import *
#Python plotting library
import matplotlib
#generating plots without a graphical display
matplotlib.use('Agg')  
import matplotlib.pyplot as plt
#HTML to PDF conversion
import pdfkit



app = Flask(__name__)
app.config['SECRET_KEY'] = 'FYP_PneumoniaEXpert_Team'
config = pdfkit.configuration(wkhtmltopdf='C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')



#initializing or setting up a database
init_db()

#####################################################################################################################################################################################################################
#########################################################################>  SignUp <#################################################################################################################################
#####################################################################################################################################################################################################################
            
@app.route('/check_username')
def check_username():
    username = request.args.get('username')
    exists = username_exists(username)
    return jsonify({'exists': exists})


@app.route('/check_email')
def check_email():
    email = request.args.get('email')
    exists = email_exists(email)
    return jsonify({'exists': exists})

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':

        username = request.form['username']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if not is_valid_email(email):
            flash('Invalid email address.')
        elif password!= confirm_password:
            flash('Passwords do not match.')
        elif email_exists(email):
            flash('Email is already in use.')
        elif username_exists(username):
            flash('Username is already in use.')
        elif not is_strong_password(password):
            flash('Password must be at least 8 characters long and contain at least one digit.')
            
        else:
            user = User(username=username, email=email, phone=phone, password=password, type="patient")
            create_user(user)
            flash('Account created successfully. Please log in.')
            
            return redirect(url_for('login'))

    return render_template('signup.html')


#####################################################################################################################################################################################################################
########################################################################> Login/logout <#############################################################################################################################
#####################################################################################################################################################################################################################


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user, session['Log_ID'] = authenticate_user(email, password)
        if user:
            session["username"] = user.username
            session['Utype'] = user.type
            return redirect(url_for('index'))
        else:
            flash('Login failed. Please check your credentials.')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('Log_ID', None)  # Remove 'Log_ID' from session
    session.pop('username', None)  # Remove 'username' from session if needed
    return redirect(url_for('login'))

#####################################################################################################################################################################################################################
#########################################################################> Admin Control <###########################################################################################################################
#####################################################################################################################################################################################################################

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':

        username = request.form['username']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if not is_valid_email(email):
            flash('Invalid email address.')
            print(f'\n\n***************\n1\n*************\n')
        elif password!= confirm_password:
            flash('Passwords do not match.')
            print(f'\n\n***************\n2\n*************\n')
        elif email_exists(email):
            flash('Email is already in use.')
            print(f'\n\n***************\n3\n*************\n')
        elif username_exists(username):
            flash('Username is already in use.')
        elif not is_strong_password(password):
            flash('Password must be at least 8 characters long and contain at least one digit.')
            print(f'\n\n***************\n4\n*************\n')
        else:
            user = User(username=username, email=email, phone=phone, password=password, type=request.form['userType'])
            create_user(user)
            print(f'\n\n***************\n5\n*************\n')

    userCount = count_all_patients()
    doctorCount = count_all_doctors()
    PCases = count_all_pneumoniaCases()
    PnCases = count_all_nonPneumoniaCases()
    # Creating side-by-side bar chart
    labels = ['Pneumonia', 'Non-Pneumonia']
    values = [PCases, PnCases]

    fig, ax = plt.subplots()
    # transparent background
    fig.patch.set_alpha(0)
    ax.patch.set_alpha(0)
    # remove y_axis
    ax.axes.get_yaxis().set_visible(False)
    # remove all the spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)  # no y axis
    ax.spines['bottom'].set_visible(False)
    
    
    ax.bar(labels, values)
    for index, value in enumerate(values):
        plt.text(index, value, str(value), ha='center', va='bottom')
    ax.set_ylabel('Count')
    ax.set_xlabel('Cases')
    ax.set_title('Pneumonia vs. Non-Pneumonia')
    # show count inside the bar
    

    # Save the plot to a file
    plot_filename = './static/plots/pneumonia_comparison.png'
    try:
        plt.savefig(plot_filename)
        print(f"Plot saved successfully at: {plot_filename}")
    except Exception as e:
        print(f"Error occurred while saving the plot: {e}")

    
    return render_template('Admin.html',username=session.get('username','Guest'),UC = userCount,DC = doctorCount,C=PCases+PnCases)

#####################################################################################################################################################################################################################
##############################################################################> Report Routines Management <#########################################################################################################
#####################################################################################################################################################################################################################


# @app.route('/download_report_as_pdf/<int:report_id>', methods=['GET'])
# def display_report(report_id):
#     # Fetch the report details from the database using the report_id
#     # Replace this with your logic to fetch the report details
#     report = fetch_report_from_database(report_id)  # Implement this function

#     if report:
#         # Render the display_report.html template with the report details
#         html = render_template('display_report.html', report=report)

#         # Create PDF from HTML using WeasyPrint
#         pdf = HTML(string=html).write_pdf()

#         # Create a response object with the PDF
#         response = make_response(pdf)
#         response.headers['Content-Type'] = 'application/pdf'
#         response.headers['Content-Disposition'] = 'attachment; filename=report.pdf'  # Change the filename if needed

#         # Redirect to the index page after initiating the download
#         return response

#     return "Report not found or error occurred."
@app.route('/download_report_as_pdf/<int:report_id>', methods=['GET'])
def display_report(report_id):
    # Fetch the report details from the database using the report_id
    # Replace this with your logic to fetch the report details
    report = fetch_report_from_database(report_id)  # Implement this function

    if report:
        # Render the display_report.html template with the report details
        html = render_template('display_report.html', report=report)

        # Set up options for pdfkit (path to wkhtmltopdf may vary based on your installation)
        options = {
            'page-size': 'Letter',
            'margin-top': '0.75in',
            'margin-right': '0.75in',
            'margin-bottom': '0.75in',
            'margin-left': '0.75in',
            'enable-local-file-access':""
        }
        print(f"\n\n\n\n#################n\n\n\n")

        # Generate PDF from HTML using pdfkit
        pdf = pdfkit.from_string(html, False, configuration=config,options=options)
        print(f"\n\n\n\n******************\n\n\n\n")
        # Create a response object with the PDF
        response = make_response(pdf)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'attachment; filename=report.pdf'  # Change the filename if needed

        # Redirect to the index page after initiating the download
        return response

    return "Report not found or error occurred."


@app.route('/report', methods=['GET', 'POST'])
def report():
    if 'Log_ID' in session and session['Log_ID']:

        if request.method == 'POST':
            # Retrieve form data from the POST request
            # Ensure the names match those in the HTML form
            symptoms = ", ".join(request.form.getlist('symptoms[]'))
            symptom_duration = str(request.form['symptom_duration'])
            breathing_difficulty = str(request.form['breathing_difficulty'])
            coughing_mucus = str(request.form['coughing_mucus'])
            mucus_color_consistency = str(request.form['mucus_color_consistency'])
            chest_pain = str(request.form['chest_pain'])
            chest_pain_description = str(request.form['chest_pain_description'])
            medical_conditions = ", ".join(request.form.getlist('medical_conditions[]'))
            smoking = str(request.form['smoking'])
            smoking_details = str(request.form['smoking_details'])
            family_history = str(request.form['family_history'])
            

            user_id = session.get('Log_ID')
            username = session.get("username")
            print("****************************\n\n\n\n",username, "\n\n\n\n****************************",)
            if 'file' in request.files:
                    image_file = request.files['file']
                    if image_file:
                        try:
                            image_data = image_file.read()
                            image = Image.open(BytesIO(image_data))

                            predicted_class = classify_image(image)

                            if predicted_class == 'Non-X-Ray':
                                # Ask the user to upload another image
                                return render_template('nonXray.html',predicted_class=predicted_class, username=username)

                            elif predicted_class == 'X-Ray':
                                # Check for pneumonia
                                predicted_class_pneumonia = classify_image_pneumo(image)
                                print(predicted_class_pneumonia)
                            # Creating a Report object with the form data
                                report = Report(U_ID=user_id, symptoms=symptoms, symptom_duration=symptom_duration,
                                                breathing_difficulty=breathing_difficulty, coughing_mucus=coughing_mucus,
                                                mucus_color_consistency=mucus_color_consistency, chest_pain=chest_pain,
                                                chest_pain_description=chest_pain_description, medical_conditions=medical_conditions,
                                                smoking=smoking, smoking_details=smoking_details, family_history=family_history,
                                                result=f'Pneumonia {predicted_class_pneumonia}.')

                                create_record(report)
                                                            
                                report_IDtime = fetch_most_recent_report(session.get("Log_ID"))
                                return render_template('display_report.html', report=report_IDtime, username=username)
                        except Exception as e:
                            print("Error:", e)
                            print("Error.............")
                            flash('Invalid image file.')
                            return render_template('report.html', username=username)
        
        return render_template('report.html')
    
    else:
        return redirect(url_for('login'))

#####################################################################################################################################################################################################################
##############################################################################> Doctor method <######################################################################################################################
#####################################################################################################################################################################################################################

@app.route('/doctor', methods=['GET', 'POST'])
def doctor():
    if 'Log_ID' in session and session['Log_ID']:
        if session.get("Utype") == "Doctor":
            user_Preports = fetch_all_reports_pneumonia()
            user_NPreports = fetch_all_reports_nonPneumonia()
            DocResponds = getReportsRespondedBy(session.get("Log_ID"))
            return render_template('Doctor.html', username=session.get('username', 'Guest'),user_Preports=user_Preports, user_NPreports = user_NPreports,user_ResReports=DocResponds)
        elif session.get("Utype") == "patient":
            return redirect(url_for('doctor'))
    else:
        return redirect(url_for('login'))
    
@app.route('/Response/<int:report_id>', methods=['GET'])
def Response(report_id):
    # Fetch the report details from the database using the report_id
    # Replace this with your logic to fetch the report details
    report = fetch_report_from_database(report_id)  # Implement this function

    if report:
        return render_template("respond.html",report = report)

    return "Report not found or error occurred."

@app.route('/SaveResponse', methods=['GET', 'POST'])
def SaveResponse():
    if 'Log_ID' in session and session['Log_ID']:
        if session.get("Utype") == "Doctor":
            if request.method == 'POST':
                # Retrieve form data from the POST request
                # Ensure the names match those in the HTML form
                user_id = request.form['U_ID']
                report_id = request.form['report_id']
                report_comment = str(request.form['prescription'])

                create_Responce(user_id,session.get("Log_ID"),report_id,report_comment)
                return redirect(url_for('doctor'))
        elif session.get("Utype") == "patient":
            return redirect(url_for('doctor'))
    else:
        return redirect(url_for('login'))
    

#####################################################################################################################################################################################################################
#####################################################################################################################################################################################################################
#####################################################################################################################################################################################################################


# Routes
@app.route('/')
def default():
    return render_template('home.html')


@app.route('/home')
def home(): 
    return render_template('home.html')


@app.route('/about_us')
def about_us():
    return render_template('about.html')


@app.route('/index', methods=['GET', 'POST'])
def index():
    if 'Log_ID' not in session or not session['Log_ID']:
        return redirect(url_for('login'))
    else:

        if session.get("Utype") == "admin":
            return redirect(url_for('admin'))
        elif session.get("Utype") == "Doctor":

            return redirect(url_for('doctor'))
        elif session.get("Utype") == "patient":
    
            # create_Responce(1,1,1,"Take Ponstone")
            user_reports = fetch_all_reports_with_comments(session.get("Log_ID"))

            return render_template('index.html', username=session.get('username', 'Guest'),user_reports=user_reports)
        else:
            return redirect(url_for('login'))
            

if __name__ == '__main__':
    app.run(debug=True)
    
