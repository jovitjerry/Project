import { Component, OnInit, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { StudentService } from '../../../shared/services/student.service';
import { MOCK_DATA } from '../../../shared/mock-data';

@Component({
  selector: 'app-manage-students',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './manage-students.html',
  styleUrl: './manage-students.scss',
})
export class ManageStudents implements OnInit {
  private studentService = inject(StudentService);

  protected students = signal<any[]>([]);
  protected filteredStudents = signal<any[]>([]);
  protected departments = signal(MOCK_DATA.departments);
  
  protected selectedFilterDepartment = signal<string>('All Departments');
  protected searchQuery = signal<string>('');
  protected selectedStudent = signal<any>(null);
  protected isEditMode = signal<boolean>(false);
  protected isLoading = signal<boolean>(false);

  ngOnInit() {
    this.loadStudents();
  }

  loadStudents() {
    this.isLoading.set(true);
    const dept = this.selectedFilterDepartment() === 'All Departments' ? undefined : this.selectedFilterDepartment();
    this.studentService.getStudents({ 
      department: dept,
      search: this.searchQuery() 
    }).subscribe({
      next: (res) => {
        const data = res.items || res;
        this.students.set(data);
        this.filteredStudents.set(data);
        this.isLoading.set(false);
      },
      error: (err) => {
        console.error('Error loading students', err);
        this.isLoading.set(false);
      }
    });
  }

  onFilterChange() {
    this.loadStudents();
  }

  onSearch() {
    this.loadStudents();
  }

  openAddModal() {
    this.isEditMode.set(false);
    this.selectedStudent.set({
      student_id: 'ST' + Math.floor(Math.random() * 1000),
      name: '',
      email: '',
      department: 'Computer Science',
      semester: 1,
      phone: '',
      date_of_birth: '',
      address: ''
    });
  }

  deleteStudent(id: number) {
    if (confirm('Are you sure you want to delete this student?')) {
      this.studentService.deleteStudent(id).subscribe(() => {
        this.loadStudents();
      });
    }
  }

  editStudent(student: any) {
    this.isEditMode.set(true);
    this.selectedStudent.set({ ...student });
  }

  saveStudent() {
    const student = this.selectedStudent();
    if (student) {
      this.isLoading.set(true);
      if (this.isEditMode()) {
        this.studentService.updateStudent(student.id, student).subscribe({
          next: () => {
            this.loadStudents();
            this.closeModal();
          },
          error: (err) => {
            console.error('Error updating student', err);
            this.isLoading.set(false);
          }
        });
      } else {
        this.studentService.createStudent(student).subscribe({
          next: () => {
            this.loadStudents();
            this.closeModal();
          },
          error: (err) => {
            console.error('Error creating student', err);
            this.isLoading.set(false);
          }
        });
      }
    }
  }

  closeModal() {
    this.selectedStudent.set(null);
    const closeBtn = document.getElementById('closeEditModal');
    if (closeBtn) closeBtn.click();
  }
}
