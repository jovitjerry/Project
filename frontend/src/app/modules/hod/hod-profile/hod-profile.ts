import { Component, OnInit, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AuthService } from '../../../shared/services/auth.service';
import { HodService } from '../../../shared/services/hod.service';
import { StatsCard } from '../../../shared/components/stats-card/stats-card';

@Component({
  selector: 'app-hod-profile',
  standalone: true,
  imports: [CommonModule, StatsCard],
  template: `
    <div class="animate-slide-up">
      <div class="d-flex justify-content-between align-items-center mb-5">
        <h2 class="fw-800 text-slate-900 mb-0">My Profile</h2>
      </div>

      <div class="row g-5">
        <!-- Profile Card -->
        <div class="col-lg-4">
          <div class="card-premium rounded-4 p-4 text-center">
            <img src="https://ui-avatars.com/api/?name={{ hodName() }}&background=06B6D4&color=fff&size=120" 
                 alt="HOD Profile" class="rounded-circle shadow-lg mb-4">
            <h4 class="fw-bold text-slate-900 mb-1">{{ hodName() }}</h4>
            <div class="text-accent fw-bold small mb-3">Head of Department</div>
            
            <div class="d-flex flex-column gap-2 text-start mt-4">
              <div class="d-flex align-items-center gap-3 p-3 bg-slate-50 rounded-3 border border-slate-100">
                <i class="bi bi-envelope-fill text-slate-400 fs-5"></i>
                <div>
                  <div class="small text-slate-400">Email</div>
                  <div class="fw-bold text-slate-700">{{ email() }}</div>
                </div>
              </div>
              <div class="d-flex align-items-center gap-3 p-3 bg-slate-50 rounded-3 border border-slate-100">
                <i class="bi bi-building text-slate-400 fs-5"></i>
                <div>
                  <div class="small text-slate-400">Department</div>
                  <div class="fw-bold text-slate-700">{{ stats().department || '...' }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Department Performance Summary -->
        <div class="col-lg-8">
          <h4 class="fw-bold text-slate-900 mb-4"><i class="bi bi-bar-chart-line-fill text-accent me-2"></i>Department Summary</h4>
          
          <div class="row g-4 mb-4">
            <div class="col-md-6">
              <app-stats-card title="Total Students" [value]="stats().total_students" icon="bi-people-fill" color="primary"></app-stats-card>
            </div>
            <div class="col-md-6">
              <app-stats-card title="Total Faculty" [value]="stats().total_faculty" icon="bi-person-badge-fill" color="highlight"></app-stats-card>
            </div>
            <div class="col-md-6">
              <app-stats-card title="Department Pass %" [value]="stats().pass_percentage + '%'" icon="bi-trophy-fill" color="success"></app-stats-card>
            </div>
            <div class="col-md-6">
              <app-stats-card title="Average CGPA" [value]="stats().avg_cgpa" icon="bi-award-fill" color="info"></app-stats-card>
            </div>
          </div>

          <div class="card-premium rounded-4 p-4">
            <h5 class="fw-bold text-slate-900 mb-3">Attendance Statistics</h5>
            <div class="d-flex align-items-end gap-3 mb-2">
              <span class="display-6 fw-800" [ngClass]="stats().attendance_percentage >= 75 ? 'text-success' : 'text-danger'">
                {{ stats().attendance_percentage }}%
              </span>
              <span class="text-slate-400 mb-2">Overall department attendance</span>
            </div>
            <div class="progress" style="height: 10px;">
              <div class="progress-bar" [ngClass]="stats().attendance_percentage >= 75 ? 'bg-success' : 'bg-danger'"
                   [style.width.%]="stats().attendance_percentage"></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  `
})
export class HodProfile implements OnInit {
  private authService = inject(AuthService);
  private hodService = inject(HodService);

  hodName = signal<string>(this.authService.getUserName() || 'HOD');
  email = signal<string>('hod@college.com'); // Could extract from token if available
  stats = signal<any>({
    department: '', total_students: 0, total_faculty: 0, 
    attendance_percentage: 0, pass_percentage: 0, avg_cgpa: 0
  });

  ngOnInit() {
    this.hodService.getStats().subscribe({
      next: (data) => { if (data) this.stats.set(data); }
    });
  }
}
