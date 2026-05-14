import { Component, input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-stats-card',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './stats-card.html',
  styleUrl: './stats-card.scss',
})
export class StatsCard {
  title = input<string>('');
  value = input<string | number>('');
  icon = input<string>('');
  color = input<'primary' | 'success' | 'warning' | 'danger' | 'info' | 'accent' | 'highlight'>('primary');
}
