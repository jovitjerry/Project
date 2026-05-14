import { Component, OnInit, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { CourseService } from '../../../shared/services/course.service';
import { TeacherService } from '../../../shared/services/teacher.service';
import { MOCK_DATA } from '../../../shared/mock-data';

@Component({
  selector: 'app-manage-courses',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './manage-courses.html',
  styleUrl: './manage-courses.scss',
})
export class ManageCourses implements OnInit {
  private courseService = inject(CourseService);
  private teacherService = inject(TeacherService);

  protected courses = signal<any[]>([]);
  protected teachers = signal<any[]>([]);
  protected departments = signal(MOCK_DATA.departments);
  
  protected selectedFilterDepartment = signal<string>('All Departments');
  protected selectedCourse = signal<any>(null);
  protected isEditMode = signal<boolean>(false);
  protected isLoading = signal<boolean>(false);

  ngOnInit() {
    this.loadCourses();
    this.loadTeachers();
  }

  loadCourses() {
    this.isLoading.set(true);
    const dept = this.selectedFilterDepartment() === 'All Departments' ? undefined : this.selectedFilterDepartment();
    this.courseService.getCourses(dept).subscribe({
      next: (data) => {
        this.courses.set(data.items || data);
        this.isLoading.set(false);
      },
      error: (err) => {
        console.error('Error loading courses', err);
        this.isLoading.set(false);
      }
    });
  }

  loadTeachers() {
    this.teacherService.getTeachers().subscribe(res => {
      this.teachers.set(res.items || res);
    });
  }

  onFilterChange() {
    this.loadCourses();
  }

  openAddModal() {
    this.isEditMode.set(false);
    this.selectedCourse.set({
      course_id: 'C' + Math.floor(Math.random() * 1000),
      course_name: '',
      course_code: '',
      credits: 3,
      department: 'Computer Science',
      teacher_id: null
    });
  }

  deleteCourse(id: number) {
    if (confirm('Are you sure you want to delete this course?')) {
      this.courseService.deleteCourse(id).subscribe(() => {
        this.loadCourses();
      });
    }
  }

  editCourse(course: any) {
    this.isEditMode.set(true);
    this.selectedCourse.set({ ...course });
  }

  saveCourse() {
    const course = this.selectedCourse();
    if (course) {
      this.isLoading.set(true);
      if (this.isEditMode()) {
        this.courseService.updateCourse(course.id, course).subscribe({
          next: () => {
            this.loadCourses();
            this.closeModal();
          },
          error: (err) => {
            console.error('Error updating course', err);
            this.isLoading.set(false);
          }
        });
      } else {
        this.courseService.createCourse(course).subscribe({
          next: () => {
            this.loadCourses();
            this.closeModal();
          },
          error: (err) => {
            console.error('Error creating course', err);
            this.isLoading.set(false);
          }
        });
      }
    }
  }

  getTeacherName(teacherId: number) {
    const teacher = this.teachers().find(t => t.id === teacherId);
    return teacher ? teacher.name : 'Not Assigned';
  }

  closeModal() {
    this.selectedCourse.set(null);
    const closeBtn = document.getElementById('closeCourseModal');
    if (closeBtn) closeBtn.click();
  }
}
