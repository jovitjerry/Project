import { Component, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MOCK_DATA } from '../../../shared/mock-data';

@Component({
  selector: 'app-manage-departments',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './manage-departments.html',
  styleUrl: './manage-departments.scss',
})
export class ManageDepartments {
  protected departments = signal(MOCK_DATA.departments);
  
  protected selectedDepartment = signal<any>(null);
  protected isEditMode = signal<boolean>(false);
  
  protected viewedDepartment = signal<any>(null);
  protected deptFaculty = signal<any[]>([]);
  protected deptStudents = signal<any[]>([]);

  viewDepartment(dept: any) {
    this.viewedDepartment.set(dept);
    this.deptFaculty.set(MOCK_DATA.faculty.filter(f => f.department === dept.name));
    this.deptStudents.set(MOCK_DATA.students.filter(s => s.department === dept.name));
  }

  getStudentCount(deptName: string): number {
    return MOCK_DATA.students.filter(s => s.department === deptName).length;
  }

  getFacultyCount(deptName: string): number {
    return MOCK_DATA.faculty.filter(f => f.department === deptName).length;
  }

  openAddModal() {
    this.isEditMode.set(false);
    this.selectedDepartment.set({
      id: Date.now(),
      name: '',
      hod: '',
      students: 0,
      faculty: 0
    });
  }

  deleteDepartment(id: number) {
    if (confirm('Are you sure you want to delete this department?')) {
      const idx = MOCK_DATA.departments.findIndex(d => d.id === id);
      if (idx !== -1) {
        MOCK_DATA.departments.splice(idx, 1);
        this.departments.set([...MOCK_DATA.departments]);
      }
    }
  }

  editDepartment(dept: any) {
    this.isEditMode.set(true);
    this.selectedDepartment.set({ ...dept });
  }

  saveDepartment() {
    const dept = this.selectedDepartment();
    if (dept) {
      if (this.isEditMode()) {
        const index = MOCK_DATA.departments.findIndex(d => d.id === dept.id);
        if (index !== -1) {
          MOCK_DATA.departments[index] = { ...dept };
        }
      } else {
        MOCK_DATA.departments.unshift({ ...dept });
      }
      this.departments.set([...MOCK_DATA.departments]);
      this.selectedDepartment.set(null);
      
      const closeBtn = document.getElementById('closeDeptModal');
      if (closeBtn) closeBtn.click();
    }
  }
}
