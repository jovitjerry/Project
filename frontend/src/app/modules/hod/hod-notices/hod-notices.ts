import { Component, OnInit, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HodService } from '../../../shared/services/hod.service';

@Component({
  selector: 'app-hod-notices',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div class="animate-slide-up">
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h2 class="fw-800 text-slate-900 mb-0">Department Notices</h2>
        <button class="btn btn-primary" (click)="showCreateForm = !showCreateForm">
          <i class="bi" [ngClass]="showCreateForm ? 'bi-x' : 'bi-plus-lg'"></i> 
          {{ showCreateForm ? 'Cancel' : 'New Notice' }}
        </button>
      </div>

      <!-- Create Form -->
      <div class="card-premium rounded-4 p-4 mb-5 animate-slide-up" *ngIf="showCreateForm">
        <h5 class="fw-bold mb-3">Create Notice</h5>
        <div class="row g-3">
          <div class="col-md-8">
            <label class="form-label text-slate-600 small fw-bold">Title</label>
            <input type="text" class="form-control" [(ngModel)]="newNotice.title">
          </div>
          <div class="col-md-4">
            <label class="form-label text-slate-600 small fw-bold">Date</label>
            <input type="date" class="form-control" [(ngModel)]="newNotice.date">
          </div>
          <div class="col-12">
            <label class="form-label text-slate-600 small fw-bold">Description</label>
            <textarea class="form-control" rows="3" [(ngModel)]="newNotice.description"></textarea>
          </div>
          <div class="col-12 text-end">
            <button class="btn btn-primary px-4" 
                    [disabled]="!newNotice.title || !newNotice.description || !newNotice.date || isSaving()" 
                    (click)="createNotice()">
              {{ isSaving() ? 'Saving...' : 'Publish Notice' }}
            </button>
          </div>
        </div>
      </div>

      <!-- Notices List -->
      <div class="row g-4">
        <div class="col-12" *ngFor="let n of notices()">
          <div class="card-premium rounded-4 p-4 position-relative">
            <div class="d-flex justify-content-between align-items-start mb-2">
              <h5 class="fw-bold text-slate-900 mb-0">{{ n.title }}</h5>
              <button class="btn btn-sm btn-outline-danger" (click)="deleteNotice(n.id)"><i class="bi bi-trash"></i></button>
            </div>
            <div class="text-accent small fw-bold mb-3"><i class="bi bi-calendar-event me-1"></i> {{ n.date | date }}</div>
            <p class="text-slate-600 mb-0">{{ n.description }}</p>
          </div>
        </div>
        
        <div *ngIf="notices().length === 0 && !isLoading()" class="col-12 text-center py-5">
          <p class="text-slate-500">No notices found.</p>
        </div>
      </div>
    </div>
  `
})
export class HodNotices implements OnInit {
  private hodService = inject(HodService);
  
  notices = signal<any[]>([]);
  isLoading = signal<boolean>(false);
  isSaving = signal<boolean>(false);
  showCreateForm = false;
  
  newNotice = {
    title: '',
    description: '',
    date: new Date().toISOString().split('T')[0]
  };

  ngOnInit() {
    this.loadNotices();
  }

  loadNotices() {
    this.isLoading.set(true);
    this.hodService.getNotices().subscribe({
      next: (data) => {
        this.notices.set(data);
        this.isLoading.set(false);
      },
      error: () => this.isLoading.set(false)
    });
  }

  createNotice() {
    this.isSaving.set(true);
    this.hodService.createNotice(this.newNotice).subscribe({
      next: () => {
        this.isSaving.set(false);
        this.showCreateForm = false;
        this.newNotice = { title: '', description: '', date: new Date().toISOString().split('T')[0] };
        this.loadNotices();
      },
      error: () => this.isSaving.set(false)
    });
  }

  deleteNotice(id: number) {
    if (confirm('Are you sure you want to delete this notice?')) {
      this.hodService.deleteNotice(id).subscribe({
        next: () => this.loadNotices()
      });
    }
  }
}
