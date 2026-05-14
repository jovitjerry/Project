import { Component, OnInit, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { AttendanceService } from '../../../shared/services/attendance.service';
import { StudentService } from '../../../shared/services/student.service';
import { CourseService } from '../../../shared/services/course.service';

@Component({
  selector: 'app-mark-attendance',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './mark-attendance.html',
  styleUrl: './mark-attendance.scss',
})
export class MarkAttendance implements OnInit {
  private attendanceService = inject(AttendanceService);
  private studentService = inject(StudentService);
  private courseService = inject(CourseService);

  protected students = signal<any[]>([]);
  protected courses = signal<any[]>([]);
  protected selectedCourseId = signal<number | null>(null);
  protected attendanceDate = signal<string>(new Date().toISOString().split('T')[0]);
  protected isLoading = signal<boolean>(false);
  protected attendanceMap = signal<{ [key: number]: boolean }>({});

  ngOnInit() {
    this.loadCourses();
    this.loadStudents();
  }

  loadCourses() {
    this.courseService.getCourses().subscribe(res => {
      this.courses.set(res.items || res);
    });
  }

  loadStudents() {
    this.isLoading.set(true);
    this.studentService.getStudents().subscribe(res => {
      const data = res.items || res;
      this.students.set(data);
      const map: { [key: number]: boolean } = {};
      data.forEach((s: any) => map[s.id] = true);
      this.attendanceMap.set(map);
      this.isLoading.set(false);
    });
  }

  updateAttendance(studentId: number, status: boolean) {
    this.attendanceMap.update(map => ({ ...map, [studentId]: status }));
  }

  saveAttendance() {
    const courseId = this.selectedCourseId();
    if (!courseId) {
      alert('Please select a course');
      return;
    }
    this.isLoading.set(true);
    const records = this.students().map(student => ({
      student_id: student.id,
      course_id: Number(courseId),
      date: this.attendanceDate(),
      status: this.attendanceMap()[student.id]
    }));

    this.attendanceService.markAttendanceBulk(records).subscribe({
      next: () => {
        alert('Attendance marked successfully');
        this.isLoading.set(false);
      },
      error: (err) => {
        console.error('Error marking attendance', err);
        alert('Failed to save attendance');
        this.isLoading.set(false);
      }
    });
  }
}
