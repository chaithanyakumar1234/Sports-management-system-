USE chaithu;

-- Drop the existing 'teams' table
DROP TABLE IF EXISTS teams;

-- Create the modified 'teams' table
CREATE TABLE teams (
    team_id INT,
    athlete_id INT,
    team_name VARCHAR(255) NOT NULL,
    player_name VARCHAR(255) NOT NULL,
    sport_type VARCHAR(255) NOT NULL,
    player_role VARCHAR(255) NOT NULL,
    PRIMARY KEY (athlete_id, team_id),
    FOREIGN KEY (athlete_id) REFERENCES athletes(athlete_id)
);

CREATE TABLE matches (
    match_id INT PRIMARY KEY,
    team1 VARCHAR(255) NOT NULL,
    team2 VARCHAR(255) NOT NULL,
    date DATE NOT NULL,
    time TIME NOT NULL,
    venue VARCHAR(255) NOT NULL,
    match_number INT NOT NULL,
    action VARCHAR(20) NOT NULL
);


CREATE TABLE tournaments (
    tournament_id INT PRIMARY KEY,
    tournament_name VARCHAR(255) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    location VARCHAR(255) NOT NULL
);


DROP TABLE IF EXISTS athletes;

-- Create the athletes table with the new 'athlete_player_role' column
CREATE TABLE athletes (
    athlete_id INT PRIMARY KEY,
    athlete_name VARCHAR(255) NOT NULL,
    athlete_dob DATE NOT NULL,
    athlete_nationality VARCHAR(255) NOT NULL,
    athlete_sport_type VARCHAR(255) NOT NULL,
    athlete_player_role VARCHAR(255) NOT NULL,  -- New column for Player Role
    athlete_gender VARCHAR(10) NOT NULL,
    athlete_height VARCHAR(20) NOT NULL,
    athlete_weight VARCHAR(20) NOT NULL
);

-- Create the admins table
CREATE TABLE admins (
    admin_id INT PRIMARY KEY,
    admin_name VARCHAR(255) NOT NULL,
    admin_email VARCHAR(255) NOT NULL,
    admin_password VARCHAR(255) NOT NULL,
    admin_phone VARCHAR(20) NOT NULL,
    admin_address VARCHAR(255) NOT NULL
);

-- Create the users table
CREATE TABLE users (
    user_id INT PRIMARY KEY,
    user_name VARCHAR(255) NOT NULL,
    user_email VARCHAR(255) NOT NULL,
    user_password VARCHAR(255) NOT NULL,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    user_phone VARCHAR(20) NOT NULL,
    user_address VARCHAR(255) NOT NULL
);