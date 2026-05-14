import { Component, inject, signal } from '@angular/core';
import { Router, RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { AuthService } from '../../../shared/services/auth.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule],
  templateUrl: './login.html',
  styleUrl: './login.scss',
})
export class Login {
  private router = inject(Router);
  private authService = inject(AuthService);

  protected email = signal('');
  protected password = signal('');
  protected isLoading = signal(false);
  protected errorMessage = signal('');
  protected showPassword = signal(false);

  togglePassword() {
    this.showPassword.update(v => !v);
  }

  onLogin() {
    if (!this.email() || !this.password()) {
      this.errorMessage.set('Please enter both email and password.');
      return;
    }
    this.isLoading.set(true);
    this.errorMessage.set('');

    this.authService.login({ email: this.email(), password: this.password() }).subscribe({
      next: (response) => {
        // The backend returns { status: "success", data: { role: "teacher", access_token: "..." } }
        const role = response?.data?.role || response?.role;
        this.isLoading.set(false);

        if (role === 'admin') {
          this.router.navigate(['/admin/dashboard']);
        } else if (role === 'teacher') {
          this.router.navigate(['/faculty/dashboard']);
        } else {
          this.router.navigate(['/student/dashboard']);
        }
      },
      error: (err) => {
        this.isLoading.set(false);
        this.errorMessage.set(err.message || 'Authentication failed. Please check your credentials.');
      }
    });
  }
}
