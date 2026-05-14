import { Component, OnInit, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HodService } from '../../../shared/services/hod.service';

@Component({
  selector: 'app-hod-faculty',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div class="animate-slide-up">
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h2 class="fw-800 text-slate-900 mb-0">Department Faculty</h2>
        <span class="badge hod-count-badge">{{ total() }} total</span>
      </div>

      <div class="card-premium rounded-4 p-4 mb-4">
        <input type="text" class="form-control" placeholder="Search faculty by name, ID, or email..." 
               [(ngModel)]="searchQuery" (ngModelChange)="onSearch()">
      </div>

      <div class="table-responsive bg-white rounded-4 shadow-sm">
        <table class="table-premium w-100">
          <thead>
            <tr>
              <th>Name</th>
              <th>Faculty ID</th>
              <th>Designation</th>
              <th>Subject</th>
              <th>Contact</th>
            </tr>
          </thead>
          <tbody>
            <tr *ngFor="let f of faculty()" class="animate-slide-up">
              <td>
                <div class="fw-800 text-slate-900">{{ f.name }}</div>
              </td>
              <td>{{ f.teacher_id || 'N/A' }}</td>
              <td><span class="badge hod-role-badge">{{ f.designation || 'Faculty' }}</span></td>
              <td class="text-slate-700 fw-600">{{ f.subject || '—' }}</td>
              <td class="text-slate-400 small">{{ f.email }}<br>{{ f.phone || '—' }}</td>
            </tr>
            <tr *ngIf="faculty().length === 0 && !isLoading()">
              <td colspan="5" class="text-center py-5 text-slate-500">No faculty found.</td>
            </tr>
            <tr *ngIf="isLoading()">
              <td colspan="5" class="text-center py-5 text-slate-500">Loading...</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  `,
  styles: [`
    .hod-count-badge { background: var(--grad-soft); color: var(--cms-accent); border: 1px solid rgba(6, 182, 212, 0.2); font-weight: 700; border-radius: 50px; padding: 0.35rem 0.85rem; font-size: 0.8rem; }
    .hod-role-badge { background: linear-gradient(135deg, rgba(99, 102, 241, 0.1), rgba(139, 92, 246, 0.1)); color: #7c3aed; border: 1px solid rgba(99, 102, 241, 0.2); border-radius: 50px; padding: 0.3rem 0.8rem; font-size: 0.75rem; font-weight: 700; }
  `]
})
export class HodFaculty implements OnInit {
  private hodService = inject(HodService);

  faculty = signal<any[]>([]);
  total = signal<number>(0);
  isLoading = signal<boolean>(false);
  searchQuery = '';
  searchTimeout: any;

  ngOnInit() {
    this.loadFaculty();
  }

  loadFaculty() {
    this.isLoading.set(true);
    this.hodService.getFaculty(this.searchQuery).subscribe({
      next: (res) => {
        this.faculty.set(res?.items || []);
        this.total.set(res?.total || 0);
        this.isLoading.set(false);
      },
      error: () => this.isLoading.set(false)
    });
  }

  onSearch() {
    clearTimeout(this.searchTimeout);
    this.searchTimeout = setTimeout(() => {
      this.loadFaculty();
    }, 500);
  }
}
