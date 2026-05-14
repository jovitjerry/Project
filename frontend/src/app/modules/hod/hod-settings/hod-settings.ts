import { Component, signal, effect } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-hod-settings',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="animate-slide-up">
      <div class="d-flex justify-content-between align-items-center mb-5">
        <h2 class="fw-800 text-slate-900 mb-0">Settings</h2>
      </div>

      <div class="row g-4">
        <div class="col-lg-6">
          <div class="card-premium rounded-4 p-4">
            <h4 class="fw-bold text-slate-900 mb-4"><i class="bi bi-palette-fill text-accent me-2"></i>Appearance</h4>
            
            <div class="d-flex align-items-center justify-content-between p-3 border border-slate-100 rounded-4 mb-3" 
                 [ngClass]="{'bg-slate-50': !isDarkMode(), 'border-accent shadow-sm': !isDarkMode()}"
                 (click)="setTheme(false)" style="cursor: pointer;">
              <div class="d-flex align-items-center gap-3">
                <div class="icon-box bg-white shadow-sm rounded-circle d-flex align-items-center justify-content-center" style="width:40px;height:40px;">
                  <i class="bi bi-sun-fill text-warning fs-5"></i>
                </div>
                <div>
                  <div class="fw-bold text-slate-900">Light Mode</div>
                  <div class="small text-slate-500">Default clean appearance</div>
                </div>
              </div>
              <i class="bi bi-check-circle-fill text-accent fs-4" *ngIf="!isDarkMode()"></i>
            </div>

            <div class="d-flex align-items-center justify-content-between p-3 border border-slate-100 rounded-4" 
                 [ngClass]="{'bg-slate-50': isDarkMode(), 'border-accent shadow-sm': isDarkMode()}"
                 (click)="setTheme(true)" style="cursor: pointer;">
              <div class="d-flex align-items-center gap-3">
                <div class="icon-box bg-slate-800 text-white shadow-sm rounded-circle d-flex align-items-center justify-content-center" style="width:40px;height:40px;">
                  <i class="bi bi-moon-stars-fill text-info fs-5"></i>
                </div>
                <div>
                  <div class="fw-bold text-slate-900">Dark Mode</div>
                  <div class="small text-slate-500">Easier on the eyes</div>
                </div>
              </div>
              <i class="bi bi-check-circle-fill text-accent fs-4" *ngIf="isDarkMode()"></i>
            </div>
          </div>
        </div>
      </div>
    </div>
  `
})
export class HodSettings {
  isDarkMode = signal<boolean>(false);

  constructor() {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
      this.isDarkMode.set(true);
      document.documentElement.setAttribute('data-theme', 'dark');
    }
  }

  setTheme(dark: boolean) {
    this.isDarkMode.set(dark);
    if (dark) {
      document.documentElement.setAttribute('data-theme', 'dark');
      localStorage.setItem('theme', 'dark');
    } else {
      document.documentElement.removeAttribute('data-theme');
      localStorage.setItem('theme', 'light');
    }
  }
}
