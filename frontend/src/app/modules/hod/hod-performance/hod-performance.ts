import { Component, OnInit, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HodService } from '../../../shared/services/hod.service';
import { StatsCard } from '../../../shared/components/stats-card/stats-card';

@Component({
  selector: 'app-hod-performance',
  standalone: true,
  imports: [CommonModule, StatsCard],
  template: `
    <div class="animate-slide-up">
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h2 class="fw-800 text-slate-900 mb-0">Department Performance Dashboard</h2>
      </div>

      <div *ngIf="isLoading()" class="text-slate-400 mb-4">Loading performance analytics...</div>

      <!-- CGPA Overview Cards -->
      <div class="row g-4 mb-5" *ngIf="cgpaStats()">
        <div class="col-md-4">
          <app-stats-card title="Department Avg CGPA" [value]="cgpaStats().avg_cgpa" icon="bi-award-fill" color="primary"></app-stats-card>
        </div>
        <div class="col-md-4">
          <app-stats-card title="Highest CGPA" [value]="cgpaStats().highest_cgpa" icon="bi-graph-up-arrow" color="success"></app-stats-card>
        </div>
        <div class="col-md-4">
          <app-stats-card title="Lowest CGPA" [value]="cgpaStats().lowest_cgpa" icon="bi-graph-down-arrow" color="danger"></app-stats-card>
        </div>
      </div>

      <div class="row g-5 mb-5">
        <!-- Top Performing Students -->
        <div class="col-lg-6">
          <h4 class="fw-bold text-slate-900 mb-3"><i class="bi bi-star-fill text-warning me-2"></i>Top Performing Students</h4>
          <div class="card-premium rounded-4 p-0 overflow-hidden">
            <table class="table-premium mb-0">
              <thead><tr><th>Student</th><th>ID</th><th>CGPA</th></tr></thead>
              <tbody>
                <tr *ngFor="let s of topStudents()">
                  <td class="fw-bold">{{ s.name }}</td>
                  <td class="small text-slate-500">{{ s.student_id }}</td>
                  <td class="text-success fw-bold">{{ s.cgpa | number:'1.2-2' }}</td>
                </tr>
                <tr *ngIf="topStudents().length === 0"><td colspan="3" class="text-center py-3">No data</td></tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Students Needing Attention -->
        <div class="col-lg-6">
          <h4 class="fw-bold text-slate-900 mb-3"><i class="bi bi-exclamation-triangle-fill text-danger me-2"></i>Needs Attention (< 6.0)</h4>
          <div class="card-premium rounded-4 p-0 overflow-hidden">
            <table class="table-premium mb-0">
              <thead><tr><th>Student</th><th>ID</th><th>CGPA</th><th>Attendance</th></tr></thead>
              <tbody>
                <tr *ngFor="let s of lowStudents()">
                  <td class="fw-bold">{{ s.name }}</td>
                  <td class="small text-slate-500">{{ s.student_id }}</td>
                  <td class="text-danger fw-bold">{{ s.cgpa | number:'1.2-2' }}</td>
                  <td class="text-danger fw-bold">{{ s.attendance_percentage }}%</td>
                </tr>
                <tr *ngIf="lowStudents().length === 0"><td colspan="4" class="text-center py-3">No students below threshold</td></tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  `
})
export class HodPerformance implements OnInit {
  private hodService = inject(HodService);
  
  cgpaStats = signal<any>(null);
  topStudents = signal<any[]>([]);
  lowStudents = signal<any[]>([]);
  
  isLoading = signal<boolean>(false);

  ngOnInit() {
    this.isLoading.set(true);
    this.hodService.getPerformance().subscribe({
      next: (data) => {
        this.cgpaStats.set(data.cgpa_stats || null);
        this.topStudents.set(data.top_students || []);
        this.lowStudents.set(data.low_students || []);
        this.isLoading.set(false);
      },
      error: () => this.isLoading.set(false)
    });
  }
}
