import sqlite3
conn = sqlite3.connect("instance/resume.db")
conn.execute("PRAGMA foreign_keys = 1")

# drop table 
conn.execute("DROP TABLE IF EXISTS education;") 
  
# Generate education database
educationCol = [
    "id INTEGER PRIMARY KEY AUTOINCREMENT ",
    "university VARCHAR",
    "startDate DATETIME",
    "endDate DATETIME",
    "gpa DECIMAL(2,1)",
    "location VARCHAR",
    "degree VARCHAR" 
]

create_table_cmd = f"CREATE TABLE education ({','.join(educationCol)})"
conn.execute(create_table_cmd)

educationData = [
    "1, 'Canadian International School of Hong Kong', date('2015-09-01'), date('2017-04-30'), 3.8, 'Hong Kong', 'High school diploma'",
    "2, 'The University of Toronto', date('2017-09-01'), date('2021-04-30'), 3.79, 'Toronto, ON, Canada', 'Bachelor of Science'",
    "3, 'The University of British Columbia', date('2021-09-01'), date('2024-01-01'), 4.0 , 'Vancouver, BC, Canada', 'Master of Science'",
]

for school in educationData:
    insert_cmd = f"INSERT INTO education VALUES ({school})"
    conn.execute(insert_cmd)


### CONTACT INFO
# drop table 
conn.execute("DROP TABLE IF EXISTS email;") 
  
# Generate contact database
emailCol = [
    "id INTEGER PRIMARY KEY AUTOINCREMENT ",
    "emailType VARCHAR UNIQUE",
    "email DATETIME UNIQUE" 
]

create_table_cmd = f"CREATE TABLE email ({','.join(emailCol)})"
conn.execute(create_table_cmd)

emailData = [
    "1, 'Personal', 'glennkengmanchang@gmail.com'",
    "2, 'School', 'glenn03@student.ubc.ca'",
    "3, 'Work', 'glchang@bcgsc.ca'",
    "4, 'Spam', 'gc032787@gmail.com'",
    "5, 'School_old', 'glenn.chang@mail.utoronto.ca'"
]

for email in emailData:
    insert_cmd = f"INSERT INTO email VALUES ({email})"
    conn.execute(insert_cmd)

### Link 
conn.execute("DROP TABLE IF EXISTS link;")

# Generate link database
linkCol = [
    "id INTEGER PRIMARY KEY AUTOINCREMENT",
    "linkType VARCHAR UNIQUE",
    "link VARCHAR UNIQUE"
]

create_table_cmd = f"CREATE TABLE link ({','.join(linkCol)})"
conn.execute(create_table_cmd)

linkData = [
    "1, 'linkedin', 'https://www.linkedin.com/in/glenn-chang-a26ab3197/'",
    "2, 'github', 'https://github.com/Glenn032787/'"
]

for link in linkData:
    insert_cmd = f"INSERT INTO link VALUES ({link})"
    conn.execute(insert_cmd)


### Transcript
tableName = "transcript"
conn.execute(f"DROP TABLE IF EXISTS {tableName}")

transcripCol = [
    "id INTEGER PRIMARY KEY AUTOINCREMENT",
    "school INTEGER",
    "courseCode VARCHAR UNIQUE",
    "courseTitle VARCHAR",
    "grade INTEGER",
    "semester INTEGER",
    "FOREIGN KEY (school) REFERENCES education (ID)"
]

create_table_cmd = f"CREATE TABLE {tableName} ({','.join(transcripCol)})"
conn.execute(create_table_cmd)

transcriptData = [
    "1, 2, 'BIO120', 'Adaptation & Biodiv', 80, 1",
    "2, 2, 'CCR199', 'Public Arts', 82, 1",
    "3, 2, 'CHM136', 'Intro Onganic Chemistry I', 80, 1",
    "4, 2, 'MAT135', 'Calculus I', 80, 1",
    "5, 2, 'PSY100', 'Intro Psychology', 80, 1",
    "6, 2, 'BCH210', 'Biochemistry I', '80', 3",
    "7, 2, 'BIO230', 'Genes to Organisms', 88, 3",
    "8, 2, 'HMB265', 'General & Human Genetics', 80, 3",
    "9, 2, 'PHL281', 'Bioethics', 78, 3",
    "10, 2, 'STA220', 'Prac of Statistic I', 81, 3",
    "11, 2, 'BCH311', 'Biochemistry II', 77, 4",
    "12, 2, 'BIO220', 'Genomes to Ecosystem', 85, 4",
    "13, 2, 'HMB201', 'Intro Genomics', 85, 4",
    "14, 2, 'PSY240', 'Intro Abnormal Psychology', 71, 4",
    "15, 2, 'PSY280', 'Sensation & Perception', 80, 4",
    "16, 2, 'CSB349', 'Eukaryotic Gene Expression', 90, 5",
    "17, 2, 'HMB311', 'Laboratory in Genomics', 88, 5",
    "18, 2, 'MGY377', 'Microbiology I', 7, 5",
    "19, 2, 'PSY333', 'Health Psychology', 76, 5",
    "20, 2, 'PSY390', 'Behavioural Genetics', 78, 5",
    "21, 2, 'CSB352', 'Bioinformatic Methods', 85, 6",
    "22, 2, 'CSB459', 'Plant Molecular Biology', 87, 6",
    "23, 2, 'HMB321', 'Topics in Genetics', 90, 6",
    "24, 2, 'MGY470', 'Human Molecular Genetics', 84, 6",
    "25, 2, 'PSY290', 'Physiology Psychology', 89, 6",
    "26, 2, 'CSB340', 'Plant Development', 89, 7",
    "27, 2, 'CSB452', 'Molecular Plant-Microbiome Interaction', 91, 7",
    "28, 2, 'HMB360', 'Neurogenomics', 92, 7",
    "29, 2, 'HMB441', 'Genetics Human Disease', 85, 7",
    "30, 2, 'HMB496', 'Thesis project', 93, 8",
    "31, 2, 'NFS284', 'Basic Human Nutrition', 92, 7",
    "32, 2, 'CSB350', 'Molecular Plant Lab', 94, 8",
    "33, 2, 'CSC148', 'Intro to Comp Sci', 93, 8",
    "35, 2, 'NFS400', 'Functional Food & Nutritient', 87, 8",
    "36, 2, 'BIO130', 'Molecular & Cell Biology', 86, 2",
    "37, 2, 'CHM135', 'Chemistry: Physical Principles', 85, 2",
    "38, 2, 'CSC108', 'Intro to Computer Programming', 90, 2",
    "39, 2, 'IMM250', 'Immunity & Infection', 87, 2",
    "40, 2, 'MAT136', 'Calculus I', 87, 2",
    "41, 3, 'STAT545A', 'Exploratory Data Analysis I', 95, 1",
    "42, 3, 'STAT545B', 'Exploratory Data Analysis II', 99, 1",
    "43, 3, 'CPSC330', 'Intro to Applied Machine Learning', 95, 2",
    "44, 3, 'GSAT502', 'Advanced Concepts in Genome Science and Technology', 99, 2",
    "45, 3, 'STAT540', 'Statistical Methods for High Dimensional Biology', 95, 2",
]


for transcript in transcriptData:
    insert_cmd = f"INSERT INTO transcript VALUES ({transcript})"
    conn.execute(insert_cmd)


### Publication
tableName = "publication"
conn.execute(f"DROP TABLE IF EXISTS {tableName}")

publicationCol = [
    "id INTEGER PRIMARY KEY AUTOINCREMENT",
    "title VARCHAR",
    "journal VARCHAR",
    "doi VARCHAR UNIQUE",
    "date DATETIME",
    "status VARCHAR"
]

create_table_cmd = f"CREATE TABLE {tableName} ({','.join(publicationCol)})"
conn.execute(create_table_cmd)

publicationData = [
    "1, 'The genome sequence of the Loggerhead sea turtle, Caretta caretta Linnaeus 1758', 'F1000 Research', 'https://doi.org/10.12688/f1000research.131283.2', date('2023-06-27'), 'published'",
    "2, 'IMPALA: A Comprehensive Pipeline for Detecting and Elucidating Mechanisms of Allele Specific Expression in Cancer', 'Bioinformatics', 'https://doi.org/10.1101/2023.09.11.555771', date('2023-09-12'), 'preprint'",
    "3, 'Oxford Nanopore long-read sequencing of an advanced cancer cohort resolves rearrangements, detangles haplotypes, and reveals methylation landscapes', 'Nature Cancer', NULL, NULL, 'draft'",
]


for publication in publicationData:
    insert_cmd = f"INSERT INTO {tableName} VALUES ({publication})"
    conn.execute(insert_cmd)

### Work
tableName = "work"
conn.execute(f"DROP TABLE IF EXISTS {tableName}")

workCol = [
    "id INTEGER PRIMARY KEY AUTOINCREMENT",
    "jobTitle VARCHAR",
    "company VARCHAR",
    "location VARCHAR",
    "startDate DATETIME",
    "endDate DATETIME"
]

create_table_cmd = f"CREATE TABLE {tableName} ({','.join(workCol)})"
conn.execute(create_table_cmd)

workData = [
    "1, 'Master Bioinformatic Analyst', 'Michael Smith Genome Sciences Centre', 'Vancouver, BC', date('2021-09-01'), date('2024-01-01')",
    "2, 'Teaching Assistant', 'Masters of Data Science (UBC)', 'Vancouver, BC', date('2022-01-01'), date('2023-04-01')",
    "3, 'Undergraduate Medical Image Analyst', 'AK Wong Lab (UBC)', 'Toronto, ON', date('2020-04-01'), date('2021-04-01')",
    "4, 'Senior Circulation Desk Assistant', 'EJ Pratt Library (UBC)', 'Toronto, ON', date('2018-09-01'), date('2020-09-01')",
    "5, 'Research Assistant', 'Laboratory of Neurological Disease (HKU)', 'Hong Kong', date('2018-04-01'), date('2018-09-01')",
    "6, 'Primary School Tutor', 'Great Glory Education Center', 'Hong Kong', date('2016-04-01'), date('2017-09-01')"
]

for work in workData:
    insert_cmd = f"INSERT INTO {tableName} VALUES ({work})"
    conn.execute(insert_cmd)


conn.commit()