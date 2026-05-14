import { Component, inject, signal } from '@angular/core';
import { Router, RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';
import { AuthService } from '../../shared/services/auth.service';
import { MOCK_DATA } from '../../shared/mock-data';

@Component({
  selector: 'app-topnav',
  standalone: true,
  imports: [CommonModule, RouterModule],
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
  protected isMobileNavOpen = signal<boolean>(false);

  constructor() {
    const role = this.userRole();
    if (role === 'student') this.userName.set('John Doe');
    if (role === 'teacher') this.userName.set('Dr. Smith');
  }

  toggleMobileNav() {
    this.isMobileNavOpen.update(v => !v);
  }

  closeMobileNav() {
    this.isMobileNavOpen.set(false);
  }

  showNoticeDetails(notice: any) {
    this.selectedNotice.set(notice);
  }

  getProfileRoute(): string {
    const role = this.userRole();
    return `/${role}/profile`;
  }

  getSettingsRoute(): string {
    const role = this.userRole();
    return `/${role}/settings`;
  }

  logout() {
    this.authService.logout();
    this.router.navigate(['/auth/login']);
  }
}
