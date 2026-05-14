import { Component, OnInit, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AttendanceService } from '../../../shared/services/attendance.service';

@Component({
  selector: 'app-attendance-view',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './attendance-view.html',
  styleUrl: './attendance-view.scss',
})
export class AttendanceView implements OnInit {
  private attendanceService = inject(AttendanceService);

  protected attendanceReport = signal<any[]>([]);
  protected isLoading = signal<boolean>(false);

  ngOnInit() {
    this.loadReport();
  }

  loadReport() {
    this.isLoading.set(true);
    const studentId = parseInt(localStorage.getItem('userId') || '1');
    this.attendanceService.getStudentReport(studentId).subscribe({
      next: (data) => {
        this.attendanceReport.set(data);
        this.isLoading.set(false);
      },
      error: (err) => {
        console.error('Error loading attendance report', err);
        this.isLoading.set(false);
      }
    });
  }
}
