import sqlite3
import os

# Define the database name
DB_NAME = "college_gpt.db"

def init_database():
    """Initializes the SQLite database, creates tables, and seeds official college data."""
    print(f"Initializing database: {DB_NAME}...")
    
    # Establish connection
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # ==========================================
    # 1. TABLE CREATION
    # ==========================================

    # Students Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            reg_no TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            department TEXT NOT NULL,
            year TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    # HODs Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS hods (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            department TEXT UNIQUE NOT NULL,
            hod_name TEXT NOT NULL,
            designation TEXT NOT NULL,
            specialization TEXT NOT NULL,
            email TEXT NOT NULL
        )
    ''')

    # Rules Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS rules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rule TEXT NOT NULL
        )
    ''')

    # Admissions Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course TEXT UNIQUE NOT NULL,
            details TEXT NOT NULL,
            eligibility TEXT NOT NULL
        )
    ''')

    # Bus Routes Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bus_routes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            route_no TEXT UNIQUE NOT NULL,
            route_name TEXT NOT NULL,
            stops TEXT NOT NULL,
            timing TEXT NOT NULL
        )
    ''')

    print("Tables created successfully.")

    # ==========================================
    # 2. SEED DATA INSERTION
    # ==========================================

    # --- Seed: Official HODs & Key Faculty ---
    hods_data = [
        ("Information Technology", "Dr. S. Selvi, P.hD", "Professor & HOD", "Machine Learning, Grid and Cloud Computing", "drsacoe@aei.edu.in"),
        ("Electronics and Communication Engineering", "Dr. A. Beno", "Associate Professor & Faculty", "Optical and Microwave Engineering, Antenna Design, SoC – VLSI, Image Processing", "beno@drsacoe.com"),
        ("Civil Engineering", "Dr. V.S. TAMILARASAN", "Associate Professor & HOD", "Structural Engineering", "drsacoe@aei.edu.in"),
        ("Electrical and Electronics Engineering", "Dr. S. Sivananaithaperumal, ME, Ph.D", "Professor", "Control System", "sivananaithaperumal@drsacoe.com"),
        ("Mechanical Engineering", "Dr. A. Maniram Kumar, B.E., M.E., PhD", "HOD", "Industrial Safety", "drsacoe@aei.edu.in"),
        ("Artificial Intelligence & Data Science", "P. Subashree Kasi Thangam M.E.(PhD)", "Assistant Professor & HOD", "Deep Learning", "drsacoe@aei.edu.in"),
        ("Management Studies (MBA)", "Dr. P. Amirtha Gowri", "Head & Associate Professor", "HR, Finance", "drsacoe@aei.edu.in"),
        ("Chemistry", "Dr. T. Jothy Stella", "Assistant Professor (Sr) / HOD", "Biopolymers", "drsacoe@aei.edu.in"),
        ("Physics", "Dr. P. Chandrasekar", "Assistant Professor", "Nanoscience and Nanotechnology", "p.chandrasekar@drsacoe.com")
    ]
    cursor.executemany('''
        INSERT OR IGNORE INTO hods (department, hod_name, designation, specialization, email)
        VALUES (?, ?, ?, ?, ?)
    ''', hods_data)

    # --- Seed: Comprehensive Rules & Regulations ---
    rules_data = [
        ("Students in class should all stand when a visitor enters the room. They should remain standing unless told to sit, and stand again when the visitor leaves."),
        ("Always stand smartly when speaking to a faculty or elders and avoid keeping hands in the pant pocket."),
        ("Treat old people with respect, and help them whenever they need it."),
        ("It would be courteous to say 'Can I help you?' to any stranger in the college campus, who obviously does not know the way or need some help."),
        ("If a faculty or any adult drops anything, it is polite to pick it up for him."),
        ("If you are seated in a crowded bus and an old person gets in and finds no vacant seats, it is polite for you to stand up and offer yours."),
        ("When greeting people it is better to say 'Good Morning', 'Good Afternoon' etc., than 'Hello'."),
        ("If you have to pass close in front of anyone always say 'Excuse me'."),
        ("When speaking to visitors in college, address a lady as 'Madam'/'Mam' and Gentlemen as 'Sir'."),
        ("Chewing (gum, sweet, etc.) in public is not polite and is forbidden in the classroom & seminar hall."),
        ("Cultivate the habit of quite controlled movement and speech."),
        ("If you do not hear properly what was said to you, say 'I beg your pardon'."),
        ("Say 'Thank you' for any service rendered to you."),
        ("Maintain silence in the library."),
        ("If you MUST cough or sneeze in public, do it quietly in a handkerchief."),
        ("Students are expected to wear neat decent & simple dress. Wearing jeans pant, Printed Shirts and T shirts are not permitted."),
        ("Wearing Black shoes and College ID card is must inside the campus."),
        ("Students shall not loiter in groups in the lobby or along corridor or anywhere in the campus during college hours."),
        ("Students should cultivate the habit of reading notices on the college & Hostel Notice Boards."),
        ("Students are not permitted to leave the campus during working hours without a valid gate pass."),
        ("Students are not permitted to have mobile phones with them when they are inside the campus."),
        ("In case of late arrival, students must register with security and deposit their ID cards. The ID can only be retrieved from the Principal after justification."),
        ("The morning session commences with a prayer. Students will assemble in their respective classes and meditate."),
        ("No student is allowed to leave the class room without the permission of the staff concerned."),
        ("Writing on the walls, black boards, desks and throwing scraps of paper anywhere in the premises are totally forbidden."),
        ("Smoking and consuming alcoholic drinks/drugs are strictly forbidden."),
        ("Students should handle college property with care to avoid common breakages of switch boards, name boards, wash basins, etc."),
        ("No student shall take part in politics or engage in activities that disrupt National integrity."),
        ("Students are forbidden to organize or attend any meeting in the college premises or to collect money for any purpose without permission."),
        ("Violation of co-education rules will be strictly dealt with. Students involved in love affairs are liable to be expelled."),
        ("Students involving in Ragging, Eve teasing, unlawful & criminal activities or serious breach of discipline are liable for dismissal from college."),
        ("Students should not indulge in the misuse of Social Medias that malign the name and fame of the institution.")
    ]
    cursor.execute("SELECT COUNT(*) FROM rules")
    if cursor.fetchone()[0] == 0:
        cursor.executemany('INSERT INTO rules (rule) VALUES (?)', [(r,) for r in rules_data])

    # --- Seed: Course Admissions & Eligibility ---
    admissions_data = [
        ("B.E. / B.Tech. Programs (Regular)", 
         "Under Graduate Courses Available: B.E. (Civil, Mechanical, CSE, EEE, ECE) & B.Tech. (IT, AI & DS). Highlights: NBA Accredited, Good Placement Track Record, University Ranks.", 
         "Pass in Higher Secondary Examinations of (10+2) Curriculum (Academic Stream) with Mathematics, Physics, and Chemistry as three of the four subjects, or pass in Higher Secondary Examination of Vocational stream (Vocational groups in Engineering / Technology) prescribed by the Govt of Tamil Nadu / Anna University."),
        
        ("B.E. / B.Tech. Programs (Lateral Entry)", 
         "Direct Admission into the Third Semester (2nd Year) of the relevant engineering branch.", 
         "Candidates possessing a Diploma in Engineering / Technology awarded by the State Board of Technical Education, Tamil Nadu (or equivalent) OR candidates possessing a B.Sc. Degree (10+2+3 stream) with Mathematics as a subject at the B.Sc. level (B.Sc. candidates must undergo two additional Engineering subjects in 3rd & 4th semesters)."),
        
        ("Post Graduation Courses (M.E. / MBA)", 
         "Master of Engineering (M.E. in CSE, VLSI Design) and Master of Business Administration (M.B.A.).", 
         "As per Anna University and Government of Tamil Nadu structural framework criteria for post-graduate admissions.")
    ]
    cursor.executemany('''
        INSERT OR IGNORE INTO admissions (course, details, eligibility)
        VALUES (?, ?, ?)
    ''', admissions_data)

    # --- Seed: Official Bus Routes ---
    bus_routes_data = [
        ("BR-01", "SPIC / ANNA NAGAR ROUTE", 
         "Anna Nagar -> Millerpuram -> Ganesh Nagar -> 3rd Mile -> Polytechnic -> Madaththur -> Korampallam -> Bypass -> Camp 1 -> Kovil stop -> Bulk -> Spic -> Saveriyaarpuram -> Mullakadu -> Nesamony -> Palayakayal -> Mukkani -> North Authoor -> Santhanamari-Sankar Hospital -> South Authoor -> Keeranoor -> College", 
         "Departs Anna Nagar 6:50 AM | Arrives College 8:40 AM | Departs College 5:05 PM"),
        
        ("BR-02", "TIRUNELVELI ROUTE", 
         "Kodeeswaran Nagar -> Tirunelveli Town -> Thachanallur -> Vannarpettai -> Reliance bulk -> NGO Colony Bulk -> Palai Bus stand -> SP Office -> Samathanapuram -> Law college (court) -> Seenivasan nagar -> VM Chatram -> Krishnapuram -> Seiydunganallur -> Karungulam -> Adhichanallur -> Pudhukudi -> Alwar -> Palkulam -> Thenthiruperai -> Kurumbur -> Alagappapuram -> Nallur -> Ammanpuram -> Sonaganvilai -> College", 
         "Departs Kodeeswaran Nagar 6:30 AM | Arrives College 8:40 AM | Departs College 5:05 PM"),
        
        ("BR-03", "PATMANAGARAM / KAYALPATTANAM ROUTE", 
         "Patmanagaram -> Srivaikundam -> Arumuganeri Bus Stop -> SRS Garden -> Peyanvilai -> Lakshmi puram -> Kayalpattinam Bus Stop -> Post Office Stop -> Beach Stop -> KMT Hospital -> Veerapandianpatnam -> Annam Hospital -> CSC Computer centre -> Indian Bank -> Tiruchendur GH Stop -> Jeyanthi Nagar -> Kumarapuram -> College", 
         "Departs Patmanagaram 7:00 AM | Arrives College 8:40 AM | Departs College 5:05 PM"),
        
        ("BR-04", "ITAMOZHI ROUTE", 
         "Ittamozhi -> Sankarankudiruppu -> Sathankulam Court Stop -> Sathankulam old bus stand -> Sathankulam Church -> Pannamparai -> Meignanapuram -> Maruthur Karai -> Kumarasamy puram -> Rama Krishna school -> State bank -> Paramankurichi -> Kayamozhi -> Thalavaipuram -> College", 
         "Departs Ittamozhi 7:20 AM | Arrives College 8:40 AM | Departs College 5:05 PM"),
        
        ("BR-05", "TUTICORIN NEW BUS STAND ROUTE", 
         "New bus stand -> SB Colony -> Kandasamypuram -> American Hospital -> Muthukrishnapuram -> Roundana -> Davispuram -> Boopalrayarpuram -> Therespuram -> Mattakadai -> Mathura Coats -> Fire Service -> Sumangali Mandapam -> Kamaraj College -> Annammal college -> Shanmugapuram -> College", 
         "Departs New Bus Stand 6:50 AM | Arrives College 8:40 AM | Departs College 5:05 PM"),
        
        ("BR-06", "NAVALADI / UDANKUDI ROUTE", 
         "Navaladi -> Mudhumuthan mozhi -> Nursing college -> Thisayanvilai bus stop -> Ramakrishna School -> EB Stop -> Idachi vilai bus stop -> Anantha hospital -> Thattarmadam -> Valathoor -> Muthaloor Govt Hospital -> CST church -> Pothakalanvilai Bus top -> Nesapuram -> Pandara chetti vilai -> Villikudiruppu -> Police station -> Mutharamman kovil -> Teacher Training School -> Udankudi Mandapam -> Udankudi Marakadai ->Kulasai-Laxmungallamman Kovil -> Thappakulam -> College", 
         "Departs Navaladi 6:30 AM | Arrives College 8:40 AM | Departs College 5:05 PM"),
        
        ("BR-07", "THOOTHUKUDI SPECIAL ROUTE (ONE DAY)", 
         "Anna Nagar -> New Bus Stand -> Annammal College -> North Authoor -> Santhanamari-Sankar Hospital -> South Authoor -> Keeranoor -> College", 
         "Departs Anna Nagar 7:00 AM | Arrives College 8:40 AM | Early Departure College 1:20 PM")
    ]
    cursor.executemany('''
        INSERT OR IGNORE INTO bus_routes (route_no, route_name, stops, timing)
        VALUES (?, ?, ?, ?)
    ''', bus_routes_data)

    # ==========================================
    # 3. STUDENT RECORDS INSERTION
    # ==========================================
    
    students_data = [
        ("950523205302", "NATARAJAN M", "Information Technology", "Final Year", "saco1234"),
        ("950523205301", "MOHAMED FAZIL INZAF S A", "Information Technology", "Final Year", "saco1234"),
        ("950523205060", "Vishwa S", "Information Technology", "Final Year", "saco1234"),
        ("950523205059", "Vetrivel Murugan P", "Information Technology", "Final Year", "saco1234"),
        ("950523205058", "Vana Stalini M", "Information Technology", "Final Year", "saco1234"),
        ("950523205057", "Uthaya Muthulakshmi B", "Information Technology", "Final Year", "saco1234"),
        ("950523205056", "Uthaya kumar M", "Information Technology", "Final Year", "saco1234"),
        ("950523205055", "Uchini Makali A", "Information Technology", "Final Year", "saco1234"),
        ("950523205054", "K Sri Dharshniha", "Information Technology", "Final Year", "saco1234"),
        ("950523205053", "Sooriyaa MA", "Information Technology", "Final Year", "saco1234"),
        ("950523205052", "Siva Sankar S", "Information Technology", "Final Year", "saco1234"),
        ("950523205051", "Shri Nithi M A", "Information Technology", "Final Year", "saco1234"),
        ("950523205050", "Shiyamala Devi A", "Information Technology", "Final Year", "saco1234"),
        ("950523205049", "Selva Sindhuja S", "Information Technology", "Final Year", "saco1234"),
        ("950523205048", "Selva Sathya M", "Information Technology", "Final Year", "saco1234"),
        ("950523205047", "Sathasivam A", "Information Technology", "Final Year", "saco1234"),
        ("950523205046", "Sanjay S", "Information Technology", "Final Year", "saco1234"),
        ("950523205045", "Sanjai S", "Information Technology", "Final Year", "saco1234"),
        ("950523205044", "Saniya S", "Information Technology", "Final Year", "saco1234"),
        ("950523205043", "Sandhya B", "Information Technology", "Final Year", "saco1234"),
        ("950523205042", "Sam Nitish L", "Information Technology", "Final Year", "saco1234"),
        ("950523205041", "Raja Raghavi G", "Information Technology", "Final Year", "saco1234"),
        ("950523205040", "Rajalakshmi P", "Information Technology", "Final Year", "saco1234"),
        ("950523205039", "PrawinSK", "Information Technology", "Final Year", "saco1234"),
        ("950523205038", "Praja J", "Information Technology", "Final Year", "saco1234"),
        ("950523205034", "Muthumaheswaran M", "Information Technology", "Final Year", "saco1234"),
        ("950523205037", "Poorana Selvi T", "Information Technology", "Final Year", "saco1234"),
        ("950523205036", "Padmavathy P", "Information Technology", "Final Year", "saco1234"),
        ("950523205035", "Nandhini S", "Information Technology", "Final Year", "saco1234"),
        ("950523205033", "Muthulakshmi S", "Information Technology", "Final Year", "saco1234"),
        ("950523205032", "Muthukumaran P", "Information Technology", "Final Year", "saco1234"),
        ("950523205031", "Mohana Priya P", "Information Technology", "Final Year", "saco1234"),
        ("950523205030", "Mohammed Thanzeer S", "Information Technology", "Final Year", "saco1234"),
        ("950523205029", "Mazo Selva Saran C", "Information Technology", "Final Year", "saco1234"),
        ("950523205028", "Mahalakshmi T", "Information Technology", "Final Year", "saco1234"),
        ("950523205027", "Maha Lakshmi S", "Information Technology", "Final Year", "saco1234"),
        ("950523205026", "Maha Lakshmi M", "Information Technology", "Final Year", "saco1234"),
        ("950523205025", "Madhumalar A", "Information Technology", "Final Year", "saco1234"),
        ("950523205024", "Lokshana E", "Information Technology", "Final Year", "saco1234"),
        ("950523205023", "Lakshmi S", "Information Technology", "Final Year", "saco1234"),
        ("950523205022", "Krithika Devi M", "Information Technology", "Final Year", "saco1234"),
        ("950523205021", "Krishna Gowsalya M", "Information Technology", "Final Year", "saco1234"),
        ("950523205020", "Kishore S", "Information Technology", "Final Year", "saco1234"),
        ("950523205019", "KAVIYA S", "Information Technology", "Final Year", "saco1234"),
        ("950523205018", "Kaviya K", "Information Technology", "Final Year", "saco1234"),
        ("950523205017", "Kavisha Raji S", "Information Technology", "Final Year", "saco1234"),
        ("950523205016", "Karthika R", "Information Technology", "Final Year", "saco1234"),
        ("950523205015", "Karishma S", "Information Technology", "Final Year", "saco1234"),
        ("950523205014", "Jeevanantham S", "Information Technology", "Final Year", "saco1234"),
        ("950523205013", "Indhurani M", "Information Technology", "Final Year", "saco1234"),
        ("950523205012", "Harshini S", "Information Technology", "Final Year", "saco1234"),
        ("950523205011", "Harini Jeyashree A", "Information Technology", "Final Year", "saco1234"),
        ("950523205010", "Chandhini P", "Information Technology", "Final Year", "saco1234"),
        ("950523205009", "Bhagavathi Devi V", "Information Technology", "Final Year", "saco1234"),
        ("950523205008", "Balasiva B", "Information Technology", "Final Year", "saco1234"),
        ("950523205007", "Augustin Rajkumar S", "Information Technology", "Final Year", "saco1234"),
        ("950523205006", "Atchaya L", "Information Technology", "Final Year", "saco1234"),
        ("950523205005", "Aswin V", "Information Technology", "Final Year", "saco1234"),
        ("950523205004", "Ashwin B", "Information Technology", "Final Year", "saco1234"),
        ("950523205003", "Arun X", "Information Technology", "Final Year", "saco1234"),
        ("950523205002", "Arnesh lingam L", "Information Technology", "Final Year", "saco1234"),
        ("950523205001", "Abinaya C", "Information Technology", "Final Year", "saco1234")
    ]
    
    cursor.executemany('''
        INSERT OR IGNORE INTO students (reg_no, name, department, year, password)
        VALUES (?, ?, ?, ?, ?)
    ''', students_data)

    # Commit transactions and shut connection down cleanly
    conn.commit()
    conn.close()
    print("Database compiled and seeded successfully with live college metrics!")

if __name__ == "__main__":
    init_database()