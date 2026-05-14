import { Component, OnInit, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HodService } from '../../../shared/services/hod.service';

@Component({
  selector: 'app-hod-timetable',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div class="animate-slide-up">
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h2 class="fw-800 text-slate-900 mb-0">Department Timetables</h2>
      </div>

      <!-- Upload Section -->
      <div class="card-premium rounded-4 p-4 mb-5">
        <h5 class="fw-bold mb-3">Upload New Timetable</h5>
        <div class="row g-3 align-items-end">
          <div class="col-md-3">
            <label class="form-label text-slate-600 small fw-bold">Semester</label>
            <input type="text" class="form-control" [(ngModel)]="newSemester" placeholder="e.g. S4">
          </div>
          <div class="col-md-7">
            <label class="form-label text-slate-600 small fw-bold">File (PDF, Image, etc.)</label>
            <input type="file" class="form-control" (change)="onFileSelect($event)">
          </div>
          <div class="col-md-2">
            <button class="btn btn-primary w-100" [disabled]="!selectedFile || !newSemester || isUploading()" (click)="uploadTimetable()">
              {{ isUploading() ? 'Uploading...' : 'Upload' }}
            </button>
          </div>
        </div>
      </div>

      <!-- List Section -->
      <h5 class="fw-bold mb-3">Available Timetables</h5>
      <div class="row g-4">
        <div class="col-md-6 col-lg-4" *ngFor="let t of timetables()">
          <div class="card-premium rounded-4 p-4 h-100">
            <div class="d-flex justify-content-between align-items-start mb-3">
              <h5 class="fw-bold text-slate-900 mb-0">Sem {{ t.semester }}</h5>
              <button class="btn btn-sm btn-outline-danger" (click)="deleteTimetable(t.id)"><i class="bi bi-trash"></i></button>
            </div>
            <div class="text-slate-500 small mb-4 d-flex align-items-center gap-2">
              <i class="bi bi-file-earmark-text"></i> {{ t.original_filename }}
            </div>
            <a [href]="'http://localhost:8000' + t.file_url" target="_blank" class="btn btn-outline-primary w-100">
              View Timetable
            </a>
          </div>
        </div>
        
        <div *ngIf="timetables().length === 0 && !isLoading()" class="col-12 text-center py-5">
          <p class="text-slate-500">No timetables uploaded yet.</p>
        </div>
      </div>
    </div>
  `
})
export class HodTimetable implements OnInit {
  private hodService = inject(HodService);
  
  timetables = signal<any[]>([]);
  isLoading = signal<boolean>(false);
  isUploading = signal<boolean>(false);
  
  newSemester = '';
  selectedFile: File | null = null;

  ngOnInit() {
    this.loadTimetables();
  }

  loadTimetables() {
    this.isLoading.set(true);
    this.hodService.getTimetables().subscribe({
      next: (data) => {
        this.timetables.set(data);
        this.isLoading.set(false);
      },
      error: () => this.isLoading.set(false)
    });
  }

  onFileSelect(event: any) {
    if (event.target.files.length > 0) {
      this.selectedFile = event.target.files[0];
    }
  }

  uploadTimetable() {
    if (!this.selectedFile || !this.newSemester) return;
    this.isUploading.set(true);
    this.hodService.uploadTimetable(this.newSemester, this.selectedFile).subscribe({
      next: () => {
        this.isUploading.set(false);
        this.selectedFile = null;
        this.newSemester = '';
        this.loadTimetables();
      },
      error: () => this.isUploading.set(false)
    });
  }

  deleteTimetable(id: number) {
    if (confirm('Are you sure you want to delete this timetable?')) {
      this.hodService.deleteTimetable(id).subscribe({
        next: () => this.loadTimetables()
      });
    }
  }
}
