import { Component, OnInit, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { DashboardService } from '../../../shared/services/dashboard.service';
import { StudentService } from '../../../shared/services/student.service';
import { MOCK_DATA } from '../../../shared/mock-data';
import { StatsCard } from '../../../shared/components/stats-card/stats-card';

@Component({
  selector: 'app-admin-dashboard',
  standalone: true,
  imports: [CommonModule, StatsCard],
  templateUrl: './admin-dashboard.html',
  styleUrl: './admin-dashboard.scss',
})
export class AdminDashboard implements OnInit {
  private dashboardService = inject(DashboardService);
  private studentService = inject(StudentService);

  protected stats = signal<any>({
    total_students: 1250,
    total_teachers: 85,
    total_courses: 42,
    attendance_percentage: 92
  });
  
  protected recentStudents = signal<any[]>([]);
  protected notices = signal(MOCK_DATA.notices);
  protected isLoading = signal<boolean>(false);

  ngOnInit() {
    this.loadStats();
    this.loadRecentStudents();
  }

  loadStats() {
    this.isLoading.set(true);
    this.dashboardService.getStats().subscribe({
      next: (data) => {
        if (data) this.stats.set(data);
        this.isLoading.set(false);
      },
      error: (err) => {
        console.error('Error loading dashboard stats', err);
        this.isLoading.set(false);
      }
    });
  }

  loadRecentStudents() {
    this.studentService.getStudents({ limit: 5 }).subscribe({
      next: (res) => {
        this.recentStudents.set(res.items || res);
      },
      error: (err) => {
        console.error('Error loading recent students', err);
      }
    });
  }

  protected selectedNotice = signal<any>(null);

  showNoticeDetails(notice: any) {
    this.selectedNotice.set(notice);
  }
}
