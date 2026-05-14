import { Component, OnInit, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MarksService } from '../../../shared/services/marks.service';

@Component({
  selector: 'app-results',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './results.html',
  styleUrl: './results.scss',
})
export class Results implements OnInit {
  private marksService = inject(MarksService);

  protected results = signal<any[]>([]);
  protected isLoading = signal<boolean>(false);
  protected cgpa = signal<number>(0);

  ngOnInit() {
    this.loadResults();
  }

  loadResults() {
    this.isLoading.set(true);
    const studentId = parseInt(localStorage.getItem('userId') || '1');
    this.marksService.getStudentResults(studentId).subscribe({
      next: (data) => {
        this.results.set(data);
        this.calculateCGPA();
        this.isLoading.set(false);
      },
      error: (err) => {
        console.error('Error loading results', err);
        this.isLoading.set(false);
      }
    });
  }

  calculateCGPA() {
    const resultsData = this.results();
    if (resultsData.length === 0) return;
    const totalPoints = resultsData.reduce((acc, curr) => acc + (curr.gpa || 0), 0);
    this.cgpa.set(parseFloat((totalPoints / resultsData.length).toFixed(2)));
  }
}
