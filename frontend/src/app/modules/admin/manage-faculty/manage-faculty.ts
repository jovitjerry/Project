import { Component, OnInit, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { TeacherService } from '../../../shared/services/teacher.service';
import { MOCK_DATA } from '../../../shared/mock-data';

@Component({
  selector: 'app-manage-faculty',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './manage-faculty.html',
  styleUrl: './manage-faculty.scss',
})
export class ManageFaculty implements OnInit {
  private teacherService = inject(TeacherService);

  protected facultyList = signal<any[]>([]);
  protected filteredFacultyList = signal<any[]>([]);
  protected departments = signal(MOCK_DATA.departments);
  
  protected selectedFilterDepartment = signal<string>('All Departments');
  protected searchQuery = signal<string>('');
  protected selectedFaculty = signal<any>(null);
  protected isEditMode = signal<boolean>(false);
  protected isLoading = signal<boolean>(false);

  ngOnInit() {
    this.loadFaculty();
  }

  loadFaculty() {
    this.isLoading.set(true);
    const dept = this.selectedFilterDepartment() === 'All Departments' ? undefined : this.selectedFilterDepartment();
    this.teacherService.getTeachers({
      department: dept,
      search: this.searchQuery()
    }).subscribe({
      next: (res) => {
        const data = res.items || res;
        this.facultyList.set(data);
        this.filteredFacultyList.set(data);
        this.isLoading.set(false);
      },
      error: (err) => {
        console.error('Error loading faculty', err);
        this.isLoading.set(false);
      }
    });
  }

  onFilterChange() {
    this.loadFaculty();
  }

  onSearch() {
    this.loadFaculty();
  }

  openAddModal() {
    this.isEditMode.set(false);
    this.selectedFaculty.set({
      teacher_id: 'TCH' + Math.floor(Math.random() * 1000),
      name: '',
      email: '',
      department: 'Computer Science',
      subject: '',
      phone: '',
      salary: 0
    });
  }

  deleteFaculty(id: number) {
    if (confirm('Are you sure you want to delete this faculty member?')) {
      this.teacherService.deleteTeacher(id).subscribe(() => {
        this.loadFaculty();
      });
    }
  }

  editFaculty(faculty: any) {
    this.isEditMode.set(true);
    this.selectedFaculty.set({ ...faculty });
  }

  saveFaculty() {
    const faculty = this.selectedFaculty();
    if (faculty) {
      this.isLoading.set(true);
      if (this.isEditMode()) {
        this.teacherService.updateTeacher(faculty.id, faculty).subscribe({
          next: () => {
            this.loadFaculty();
            this.closeModal();
          },
          error: (err) => {
            console.error('Error updating faculty', err);
            this.isLoading.set(false);
          }
        });
      } else {
        this.teacherService.createTeacher(faculty).subscribe({
          next: () => {
            this.loadFaculty();
            this.closeModal();
          },
          error: (err) => {
            console.error('Error creating faculty', err);
            this.isLoading.set(false);
          }
        });
      }
    }
  }

  closeModal() {
    this.selectedFaculty.set(null);
    const closeBtn = document.getElementById('closeFacultyModal');
    if (closeBtn) closeBtn.click();
  }
}
