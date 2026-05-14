import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { StatsCard } from '../../../shared/components/stats-card/stats-card';

@Component({
  selector: 'app-faculty-dashboard',
  standalone: true,
  imports: [CommonModule, StatsCard],
  templateUrl: './faculty-dashboard.html',
  styleUrl: './faculty-dashboard.scss',
})
export class FacultyDashboard {}
