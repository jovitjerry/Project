import { Component, OnInit, inject, signal, computed } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AuthService } from '../../../shared/services/auth.service';
import { HodService } from '../../../shared/services/hod.service';
import { StatsCard } from '../../../shared/components/stats-card/stats-card';

@Component({
  selector: 'app-hod-dashboard',
  standalone: true,
  imports: [CommonModule, StatsCard],
  templateUrl: './hod-dashboard.html',
  styleUrl: './hod-dashboard.scss',
})
export class HodDashboard implements OnInit {
  private authService = inject(AuthService);
  private hodService  = inject(HodService);

  // ── Signals ──────────────────────────────────────────────────────────
  protected hodName    = signal<string>(this.authService.getUserName() || 'HOD');
  protected isLoading  = signal<boolean>(false);

  protected stats = signal<any>({
    department: '',
    total_students: 0,
    total_faculty: 0,
    total_courses: 0,
    attendance_percentage: 0,
    pass_percentage: 0,
    avg_cgpa: 0,
    semester_distribution: {}
  });



  ngOnInit() {
    this.loadAll();
  }

  private loadAll() {
    this.isLoading.set(true);

    // Stats
    this.hodService.getStats().subscribe({
      next: data => { 
        if (data) this.stats.set(data); 
        this.isLoading.set(false);
      },
      error: err  => {
        console.error('HOD stats error', err);
        this.isLoading.set(false);
      }
    });
  }
}
