export const MOCK_DATA = {
  faculty: [
    { id: 1, name: "Dr. Rajesh Kumar", role: "Principal", department: "Administration", designation: "Principal", qualification: "PhD in Computer Science", experience: 22, email: "principal@college.edu", phone: "+91 9876543210" },
    { id: 101, name: "Anita Menon", role: "Faculty", department: "Computer Science", designation: "Assistant Professor", qualification: "M.Tech", experience: 6, email: "anita@college.edu", phone: "+91 9876500001" },
    { id: 102, name: "Rahul Nair", role: "Faculty", department: "Mechanical Engineering", designation: "Associate Professor", qualification: "PhD", experience: 12, email: "rahul@college.edu", phone: "+91 9876500002" },
    { id: 103, name: "Sneha Joseph", role: "Faculty", department: "Electronics", designation: "Assistant Professor", qualification: "M.Tech", experience: 5, email: "sneha@college.edu", phone: "+91 9876500003" },
    { id: 104, name: "Arjun Das", role: "Faculty", department: "Civil Engineering", designation: "Professor", qualification: "PhD", experience: 15, email: "arjun@college.edu", phone: "+91 9876500004" },
    { id: 105, name: "Megha Pillai", role: "Faculty", department: "Computer Science", designation: "Lecturer", qualification: "MCA", experience: 3, email: "megha@college.edu", phone: "+91 9876500005" },
    { id: 106, name: "Vishnu Prasad", role: "Faculty", department: "Electrical Engineering", designation: "Assistant Professor", qualification: "M.Tech", experience: 8, email: "vishnu@college.edu", phone: "+91 9876500006" },
    { id: 107, name: "Aiswarya Krishnan", role: "Faculty", department: "Information Technology", designation: "Associate Professor", qualification: "PhD", experience: 11, email: "aiswarya@college.edu", phone: "+91 9876500007" },
    { id: 108, name: "Nikhil Varma", role: "Faculty", department: "Artificial Intelligence", designation: "Assistant Professor", qualification: "M.Tech AI", experience: 4, email: "nikhil@college.edu", phone: "+91 9876500008" },
    { id: 109, name: "Gayathri Menon", role: "Faculty", department: "Mathematics", designation: "Professor", qualification: "PhD Mathematics", experience: 18, email: "gayathri@college.edu", phone: "+91 9876500009" },
    { id: 110, name: "Sanjay Kumar", role: "Faculty", department: "Physics", designation: "Assistant Professor", qualification: "M.Sc Physics", experience: 7, email: "sanjay@college.edu", phone: "+91 9876500010" }
  ],
  students: [
    { id: 201, name: "Jovit Thomas", rollNumber: "CSE2024001", department: "Computer Science", semester: 2, attendance: 94, cgpa: 9.1, email: "jovit@student.edu" },
    { id: 202, name: "Akhil Raj", rollNumber: "ME2024002", department: "Mechanical Engineering", semester: 4, attendance: 88, cgpa: 8.2, email: "akhil@student.edu" },
    { id: 203, name: "Meera Nair", rollNumber: "EC2024003", department: "Electronics", semester: 6, attendance: 91, cgpa: 8.9, email: "meera@student.edu" },
    { id: 204, name: "Adithya S", rollNumber: "IT2024004", department: "Information Technology", semester: 1, attendance: 97, cgpa: 9.4, email: "adithya@student.edu" },
    { id: 205, name: "Neha Joseph", rollNumber: "CSBS2024005", department: "Computer Science and Business Systems", semester: 3, attendance: 89, cgpa: 8.5, email: "neha@student.edu" },
    { id: 206, name: "Alan George", rollNumber: "EEE2024006", department: "Electrical Engineering", semester: 5, attendance: 84, cgpa: 7.9, email: "alan@student.edu" },
    { id: 207, name: "Riya Mathew", rollNumber: "AI2024007", department: "Artificial Intelligence", semester: 2, attendance: 96, cgpa: 9.3, email: "riya@student.edu" },
    { id: 208, name: "Kiran Babu", rollNumber: "CIV2024008", department: "Civil Engineering", semester: 7, attendance: 81, cgpa: 7.5, email: "kiran@student.edu" },
    { id: 209, name: "Sandra Paul", rollNumber: "ECE2024009", department: "Electronics", semester: 4, attendance: 92, cgpa: 8.7, email: "sandra@student.edu" },
    { id: 210, name: "Vivek Mohan", rollNumber: "CSE2024010", department: "Computer Science", semester: 8, attendance: 86, cgpa: 8.1, email: "vivek@student.edu" }
  ],
  departments: [
    { id: 1, name: "Computer Science", hod: "Anita Menon", students: 320, faculty: 24 },
    { id: 2, name: "Mechanical Engineering", hod: "Rahul Nair", students: 280, faculty: 20 },
    { id: 3, name: "Electronics", hod: "Sneha Joseph", students: 250, faculty: 18 },
    { id: 4, name: "Civil Engineering", hod: "Arjun Das", students: 210, faculty: 16 },
    { id: 5, name: "Artificial Intelligence", hod: "Nikhil Varma", students: 180, faculty: 12 },
    { id: 6, name: "Information Technology", hod: "Aiswarya Krishnan", students: 230, faculty: 17 }
  ],
  notices: [
    { id: 1, title: "Semester Exam Registration", date: "2026-05-20", description: "Students must complete exam registration before May 20.", type: "Urgent" },
    { id: 2, title: "Tech Fest 2026", date: "2026-06-10", description: "Annual technical fest will begin from June 10.", type: "Info" },
    { id: 3, title: "Placement Drive", date: "2026-05-25", description: "Top IT companies will conduct campus recruitment.", type: "Important" },
    { id: 4, title: "Holiday Announcement", date: "2026-05-30", description: "College will remain closed due to maintenance work.", type: "Info" },
    { id: 5, title: "Workshop on AI", date: "2026-06-15", description: "A workshop on Machine Learning and AI will be conducted.", type: "Internal" }
  ]
};
