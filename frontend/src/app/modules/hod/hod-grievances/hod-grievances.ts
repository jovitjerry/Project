import { Component, OnInit, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HodService } from '../../../shared/services/hod.service';

@Component({
  selector: 'app-hod-grievances',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div class="animate-slide-up">
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h2 class="fw-800 text-slate-900 mb-0">Department Grievances</h2>
      </div>

      <div class="row g-4">
        <div class="col-md-6" *ngFor="let g of grievances()">
          <div class="card-premium rounded-4 p-4 h-100 position-relative">
            <span class="badge position-absolute top-0 end-0 m-3" 
                  [ngClass]="g.status === 'Pending' ? 'bg-warning text-dark' : 'bg-success'">
              {{ g.status }}
            </span>
            <h5 class="fw-bold text-slate-900 mb-2 pe-5">{{ g.title }}</h5>
            <p class="text-slate-600 mb-3 small">{{ g.description }}</p>
            
            <div class="d-flex justify-content-between align-items-center mt-auto pt-3 border-top border-slate-100">
              <div class="text-slate-500 small">
                <strong>{{ g.submitted_by }}</strong> ({{ g.submitter_type }})<br>
                {{ g.created_at | date }}
              </div>
              <button class="btn btn-sm" 
                      [ngClass]="g.status === 'Pending' ? 'btn-success' : 'btn-outline-secondary'"
                      (click)="toggleStatus(g)">
                {{ g.status === 'Pending' ? 'Mark Resolved' : 'Mark Pending' }}
              </button>
            </div>
          </div>
        </div>
        
        <div *ngIf="grievances().length === 0 && !isLoading()" class="col-12 text-center py-5">
          <p class="text-slate-500">No grievances found.</p>
        </div>
      </div>
    </div>
  `
})
export class HodGrievances implements OnInit {
  private hodService = inject(HodService);
  
  grievances = signal<any[]>([]);
  isLoading = signal<boolean>(false);

  ngOnInit() {
    this.loadGrievances();
  }

  loadGrievances() {
    this.isLoading.set(true);
    this.hodService.getGrievances().subscribe({
      next: (data) => {
        this.grievances.set(data);
        this.isLoading.set(false);
      },
      error: () => this.isLoading.set(false)
    });
  }

  toggleStatus(g: any) {
    const newStatus = g.status === 'Pending' ? 'Resolved' : 'Pending';
    this.hodService.updateGrievanceStatus(g.id, newStatus).subscribe({
      next: () => this.loadGrievances()
    });
  }
}
