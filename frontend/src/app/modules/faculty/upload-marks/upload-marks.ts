import { Component, OnInit, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MarksService } from '../../../shared/services/marks.service';
import { StudentService } from '../../../shared/services/student.service';
import { CourseService } from '../../../shared/services/course.service';

@Component({
  selector: 'app-upload-marks',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './upload-marks.html',
  styleUrl: './upload-marks.scss',
})
export class UploadMarks implements OnInit {
  private marksService = inject(MarksService);
  private studentService = inject(StudentService);
  private courseService = inject(CourseService);

  protected students = signal<any[]>([]);
  protected courses = signal<any[]>([]);
  protected selectedCourseId = signal<number | null>(null);
  protected marksMap = signal<{ [key: number]: number }>({});
  protected isLoading = signal<boolean>(false);

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
    this.studentService.getStudents().subscribe(res => {
      const data = res.items || res;
      this.students.set(data);
      const map: { [key: number]: number } = {};
      data.forEach((s: any) => map[s.id] = 0);
      this.marksMap.set(map);
    });
  }

  updateMark(studentId: number, mark: number) {
    this.marksMap.update(map => ({ ...map, [studentId]: mark }));
  }

  submitMarks() {
    const courseId = this.selectedCourseId();
    if (!courseId) {
      alert('Please select a course');
      return;
    }
    this.isLoading.set(true);
    let completedCount = 0;
    const studentList = this.students();
    
    studentList.forEach(student => {
      const record = {
        student_id: student.id,
        course_id: Number(courseId),
        marks_obtained: this.marksMap()[student.id],
        total_marks: 100
      };
      this.marksService.addMarks(record).subscribe({
        next: () => {
          completedCount++;
          if (completedCount === studentList.length) {
            alert('Marks uploaded successfully');
            this.isLoading.set(false);
          }
        },
        error: () => {
          completedCount++;
          if (completedCount === studentList.length) {
            this.isLoading.set(false);
          }
        }
      });
    });
  }
}
