import { Component, inject, signal } from '@angular/core';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { AuthService } from '../../shared/services/auth.service';
import { MOCK_DATA } from '../../shared/mock-data';

@Component({
  selector: 'app-topnav',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './topnav.html',
  styleUrl: './topnav.scss',
})
export class Topnav {
  private authService = inject(AuthService);
  private router = inject(Router);

  protected userName = signal<string>('Admin User');
  protected userRole = signal<string>(this.authService.getRole() || 'admin');
  protected notices = signal(MOCK_DATA.notices);
  protected selectedNotice = signal<any>(null);

  constructor() {
    const role = this.userRole();
    if (role === 'student') this.userName.set('John Doe');
    if (role === 'teacher') this.userName.set('Dr. Smith');
  }

  showNoticeDetails(notice: any) {
    this.selectedNotice.set(notice);
  }

  logout() {
    this.authService.logout();
    this.router.navigate(['/auth/login']);
  }
}
