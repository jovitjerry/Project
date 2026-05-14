import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { StatsCard } from '../../../shared/components/stats-card/stats-card';

@Component({
  selector: 'app-student-dashboard',
  standalone: true,
  imports: [CommonModule, StatsCard],
  templateUrl: './student-dashboard.html',
  styleUrl: './student-dashboard.scss',
})
export class StudentDashboard {}
