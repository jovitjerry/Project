import { Component, OnInit, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HodService } from '../../../shared/services/hod.service';

@Component({
  selector: 'app-hod-students',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div class="animate-slide-up">
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h2 class="fw-800 text-slate-900 mb-0">Department Students</h2>
        <span class="badge hod-count-badge">{{ total() }} total</span>
      </div>

      <div class="card-premium rounded-4 p-4 mb-4">
        <input type="text" class="form-control" placeholder="Search students by name, ID, or email..." 
               [(ngModel)]="searchQuery" (ngModelChange)="onSearch()">
      </div>

      <div class="table-responsive bg-white rounded-4 shadow-sm">
        <table class="table-premium w-100">
          <thead>
            <tr>
              <th>Name</th>
              <th>Student ID</th>
              <th>Email</th>
              <th>Semester</th>
              <th>Attendance</th>
              <th>CGPA</th>
            </tr>
          </thead>
          <tbody>
            <tr *ngFor="let s of students()" class="animate-slide-up">
              <td><div class="fw-800 text-slate-900">{{ s.name }}</div></td>
              <td>{{ s.student_id }}</td>
              <td class="text-slate-400 small">{{ s.email }}</td>
              <td class="fw-600 text-slate-700">Sem {{ s.semester }}</td>
              <td class="fw-600" [ngClass]="s.attendance_percentage >= 75 ? 'text-success' : 'text-danger'">
                {{ s.attendance_percentage }}%
              </td>
              <td class="fw-800" [ngClass]="s.cgpa >= 6.0 ? 'text-primary' : 'text-danger'">
                {{ s.cgpa | number:'1.2-2' }}
              </td>
            </tr>
            <tr *ngIf="students().length === 0 && !isLoading()">
              <td colspan="6" class="text-center py-5 text-slate-500">No students found.</td>
            </tr>
            <tr *ngIf="isLoading()">
              <td colspan="6" class="text-center py-5 text-slate-500">Loading...</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  `,
  styles: [`
    .hod-count-badge { background: var(--grad-soft); color: var(--cms-accent); border: 1px solid rgba(6, 182, 212, 0.2); font-weight: 700; border-radius: 50px; padding: 0.35rem 0.85rem; font-size: 0.8rem; }
  `]
})
export class HodStudents implements OnInit {
  private hodService = inject(HodService);

  students = signal<any[]>([]);
  total = signal<number>(0);
  isLoading = signal<boolean>(false);
  searchQuery = '';
  searchTimeout: any;

  ngOnInit() {
    this.loadStudents();
  }

  loadStudents() {
    this.isLoading.set(true);
    this.hodService.getStudents(this.searchQuery).subscribe({
      next: (res) => {
        this.students.set(res?.items || []);
        this.total.set(res?.total || 0);
        this.isLoading.set(false);
      },
      error: () => this.isLoading.set(false)
    });
  }

  onSearch() {
    clearTimeout(this.searchTimeout);
    this.searchTimeout = setTimeout(() => {
      this.loadStudents();
    }, 500);
  }
}
