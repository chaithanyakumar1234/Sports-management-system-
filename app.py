from flask import Flask, render_template, request, redirect, url_for, session
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor
from datetime import datetime

app = Flask(__name__)

# Set a secret key for session management
app.secret_key = 'Hello123$'  # Replace 'your_secret_key_here' with a secret key

# Configure MySQL
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'chaithu@1432'
app.config['MYSQL_DATABASE_DB'] = 'chaithu'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql = MySQL(app)

# Routes

@app.route('/')

def index():
    return render_template('signup.html')

def authenticate_user(table, email, password):
    cursor = mysql.get_db().cursor()
    cursor.execute(f"SELECT * FROM {table} WHERE {table[:-1]}_email = %s AND {table[:-1]}_password = %s", (email, password))
    user = cursor.fetchone()
    return user

def is_username_exists(table, username):
    cursor = mysql.get_db().cursor()
    cursor.execute(f"SELECT COUNT(*) FROM {table} WHERE {table[:-1]}_name = %s", (username,))
    result = cursor.fetchone()
    return result[0] > 0

def is_email_exists(table, email):
    cursor = mysql.get_db().cursor()
    cursor.execute(f"SELECT COUNT(*) FROM {table} WHERE {table[:-1]}_email = %s", (email,))
    result = cursor.fetchone()
    return result[0] > 0

def check_existing_credentials(table, name, email):
    if is_username_exists(table, name):
        return f"{table[:-1].title()} name already exists"
    elif is_email_exists(table, email):
        return f"{table[:-1].title()} email already exists"
    return None

@app.route('/signup', methods=['POST'])
def signup():
    try:
        if 'user-signup' in request.form:
            # User signup form submission
            user_id = request.form['user-id']
            user_name = request.form['user-name']
            user_email = request.form['user-email']

            # Check if username or email already exists
            error_message = check_existing_credentials('users', user_name, user_email)
            if error_message:
                #error_message = "Username or email already exists."
                return render_template('signup.html', error=error_message)
            
            user_password = request.form['user-password']
            first_name = request.form['first-name']
            last_name = request.form['last-name']
            user_phone = request.form['user-phone']
            user_address = request.form['user-address']

            print(f"Received User Signup Data: {user_id}, {user_name}, {user_email}, {first_name}, {last_name}, {user_phone}, {user_address}")

            # Save user data to MySQL
            cursor = mysql.get_db().cursor()
            cursor.execute(
                'INSERT INTO users (user_id, user_name, user_email, user_password, first_name, last_name, user_phone, user_address) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
                (user_id, user_name, user_email, user_password, first_name, last_name, user_phone, user_address)
            )
            mysql.get_db().commit()
            print("User data successfully inserted into the database")

        elif 'admin-signup' in request.form:
            # admin signup form submission
            admin_id = request.form['admin-id']
            admin_name = request.form['admin-name']
            admin_email = request.form['admin-email']

            # Check if admin name or email already exists
            error_message = check_existing_credentials('admins', admin_name, admin_email)
            if error_message:
                return render_template('signup.html', error=error_message)
            
            admin_password = request.form['admin-password']
            admin_phone = request.form['admin-phone']
            admin_address = request.form['admin-address']

            print(f"Received admin Signup Data: {admin_id}, {admin_name}, {admin_email}, {admin_phone}, {admin_address}")

            # Save admin data to MySQL
            cursor = mysql.get_db().cursor()
            cursor.execute(
                'INSERT INTO admins (admin_id, admin_name, admin_email, admin_password, admin_phone, admin_address) VALUES (%s, %s, %s, %s, %s, %s)',
                (admin_id, admin_name, admin_email, admin_password, admin_phone, admin_address)
            )
            mysql.get_db().commit()
            print("admin data successfully inserted into the database")

        return redirect(url_for('signin'))

    except Exception as e:
        # Handle errors appropriately
        print(str(e))
        return redirect(url_for('index'))

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'GET':
        return render_template('signin.html')

    try:
        if 'user-signin' in request.form:
            # User sign-in form submission
            user_email = request.form['user-email']
            user_password = request.form['user-password']

            # Authenticate user
            user = authenticate_user('users', user_email, user_password)
            if user:
                # Successful sign-in, you can store user information in the session if needed
                print("Successful user signin")
                user_id, user_name, user_email, user_password, first_name, last_name, user_phone, user_address = user

                # Store user information in the session
                session['user_id'] = user_id
                session['user_name'] = user_name

                # Redirect to the user dashboard
                return redirect(url_for('user_dashboard'))

            else:
                error_message = "Invalid email or password. Please try again."
                return render_template('signin.html', user_error=error_message)

        elif 'admin-signin' in request.form:
            # Admin sign-in form submission
            admin_email = request.form['admin-email']
            admin_password = request.form['admin-password']

            # Authenticate admin
            admin = authenticate_user('admins', admin_email, admin_password)
            if admin:
                # Successful sign-in, store admin information in the session
                print("Successful admin signin")
                admin_id, admin_name, admin_email, admin_password, admin_phone, admin_address = admin

                # Store admin information in the session
                session['admin_id'] = admin_id
                session['admin_name'] = admin_name

                # Redirect to the admin dashboard
                return redirect(url_for('admin_dashboard'))

            else:
                error_message = "Invalid email or password. Please try again."
                return render_template('signin.html', admin_error=error_message)

        return redirect(url_for('signin'))

    except Exception as e:
        # Handle errors appropriately
        print(str(e))
        return redirect(url_for('signin'))
    

@app.route('/user_dashboard', methods=['GET', 'POST'])
def user_dashboard():

    if request.method == 'GET':
        return render_template('user_dashboard.html')

    # Inside the 'user_dashboard' route
    elif request.method == 'POST':
        try:
            athlete_id = request.form['athlete-id']
            athlete_name = request.form['athlete-name']
            athlete_dob = request.form['athlete-dob']
            athlete_nationality = request.form['athlete-nationality']
            athlete_sport_type = request.form['athlete-sport-type']
            athlete_player_role = request.form['athlete-player-role']  # Added line for Player Role
            athlete_gender = request.form['athlete-gender']
            athlete_height = request.form['athlete-height']
            athlete_weight = request.form['athlete-weight']

            # Insert athlete data into the database
            cursor = mysql.get_db().cursor()
            cursor.execute(
                'INSERT INTO athletes (athlete_id, athlete_name, athlete_dob, athlete_nationality, athlete_sport_type, athlete_player_role, athlete_gender, athlete_height, athlete_weight) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)',
                (athlete_id, athlete_name, athlete_dob, athlete_nationality, athlete_sport_type, athlete_player_role, athlete_gender, athlete_height, athlete_weight)
            )
            mysql.get_db().commit()
            print("Athlete data entered into database")

            # Show success message
            return render_template('user_dashboard.html', athlete_success=True)

        except Exception as e:
            # Handle errors appropriately
            print(str(e))


    return render_template('user_dashboard.html', athlete_success=False)

@app.route('/admin_dashboard')
def admin_dashboard():
    return render_template('admin_dashboard.html')  # You can modify this to suit your admin dashboard template


@app.route('/admin_tournament', methods=['GET', 'POST'])
def admin_tournament():
    try:
        if request.method == 'GET':
            return render_template('admin_tournament.html')

        elif request.method == 'POST':
            # Retrieve data from the form
            tournament_id = request.form['tournamentId']
            tournament_name = request.form['tournamentName']
            start_date = request.form['startDate']
            end_date = request.form['endDate']
            location = request.form['location']

            # Convert date strings to datetime objects
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d')

            # Save tournament data to MySQL
            cursor = mysql.get_db().cursor()
            cursor.execute(
                'INSERT INTO tournaments (tournament_id, tournament_name, start_date, end_date, location) VALUES (%s, %s, %s, %s, %s)',
                (tournament_id, tournament_name, start_date, end_date, location)
            )
            mysql.get_db().commit()

            print("Tournament details entered into database successfully!!")

            # Redirect to a success page or display a success message
            return render_template('admin_tournament.html', success_message="Tournament details entered successfully!")

    except Exception as e:
        # Handle errors appropriately
        print(str(e))
        # Redirect to an error page or display an error message
        return render_template('admin_dashboard.html', error_message="Error entering tournament details.")

@app.route('/admin_match', methods=['GET', 'POST'])
def admin_match():
    try:
        if request.method == 'GET':
            return render_template('admin_match.html')
        
        elif request.method == 'POST':
            # Retrieve data from the form
            team1 = request.form['team1']
            team2 = request.form['team2']
            match_id = request.form['match_id']
            date = request.form['date']
            time = request.form['time']
            venue = request.form['venue']
            match_number = request.form['match_number']
            action = request.form['action']

            # Convert date and time strings to Python datetime object
            match_datetime = datetime.strptime(f"{date} {time}", '%Y-%m-%d %H:%M')

            # Save match data to MySQL
            cursor = mysql.get_db().cursor()
            cursor.execute(
                'INSERT INTO matches (match_id, team1, team2, date, time, venue, match_number, action) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
                (match_id, team1, team2, date, match_datetime, venue, match_number, action)
            )
            mysql.get_db().commit()

            print("Match details entered into the database successfully!!")

            # Redirect to a success page or display a success message
            return render_template('admin_dashboard.html', success_message="Match details entered successfully!")

    except Exception as e:
        # Handle errors appropriately
        print(str(e))
        # Redirect to an error page or display an error message
        return render_template('admin_match.html', error_message="Error entering match details.")
    
    return render_template('admin_match.html')

@app.route('/admin_team', methods=['GET', 'POST'])
def admin_team():
    if request.method == 'GET':
        return render_template('admin_team.html')

    elif request.method == 'POST':
        try:
            team_id = request.form['teamID']
            athlete_id = request.form['athleteID']
            team_name = request.form['teamName']
            player_name = request.form['playerName']
            sport_type = request.form['sporttype']
            player_role = request.form['playerRole']

            print("Hiiiiiii")
            # Save team data to MySQL
            cursor = mysql.get_db().cursor()
            cursor.execute(
                'INSERT INTO teams (team_id, athlete_id, team_name, player_name, sport_type, player_role) VALUES (%s, %s, %s, %s, %s, %s)',
                (team_id, athlete_id, team_name, player_name, sport_type, player_role)
            )
            mysql.get_db().commit()

            print("Team details entered into the database successfully!!")

            # Redirect to a success page or display a success message
            return render_template('admin_dashboard.html', success_message="Team details entered successfully!")

        except Exception as e:
            # Handle errors appropriately
            print(str(e))
            # Redirect to an error page or display an error message
            return render_template('admin_team.html', error_message="Error entering team details.")

    return render_template('admin_team.html')

@app.route('/user_tournaments')
def user_tournaments():
    try:
        # Fetch tournament data from the database
        cursor = mysql.get_db().cursor(DictCursor)
        cursor.execute('SELECT * FROM tournaments')
        tournaments = cursor.fetchall()

        return render_template('user_tournaments.html', tournaments=tournaments)

    except Exception as e:
        # Handle errors appropriately
        print(str(e))
        return render_template('error.html', error_message="Error fetching tournament details.")

@app.route('/user_matches')
def user_matches():
    # Fetch the matches data from the database
    cursor = mysql.get_db().cursor(dictionary=True)
    cursor.execute('SELECT * FROM matches')
    matches = cursor.fetchall()

    # Render the user_matches.html template with the matches data
    return render_template('user_matches.html', matches=matches)

@app.route('/user_teams')
def user_teams():
    try:
        # Fetch the teams data from the database
        cursor = mysql.get_db().cursor()
        cursor.execute('SELECT * FROM teams')
        teams_data = cursor.fetchall()

        # Create a dictionary to structure the data by team_id
        teams = {}
        for team_data in teams_data:
            team_id = team_data[0]  # Assuming the first column is team_id
            if team_id not in teams:
                teams[team_id] = {
                    'team_name': team_data[2],  # Assuming the third column is team_name
                    'players': []
                }
            teams[team_id]['players'].append({
                'player_name': team_data[3]  # Assuming the fourth column is player_name
            })

        # Render the user_teams.html template with the structured teams data
        return render_template('user_teams.html', teams=teams.values())

    except Exception as e:
        # Handle errors appropriately
        print(str(e))
        return render_template('error.html', error_message="Error fetching team details.")

@app.route('/sign_out')
def sign_out():
    # Clear user-related session data
    session.pop('user_id', None)
    session.pop('user_name', None)

    # Redirect to the sign-in page
    return redirect(url_for('signin'))


@app.route('/admin_sign_out')
def admin_sign_out():
    # Clear admin-related session data
    session.pop('admin_id', None)
    session.pop('admin_name', None)

    # Redirect to the admin sign-in page
    return redirect(url_for('signin'))


if __name__ == '__main__':
    app.run(debug=True)