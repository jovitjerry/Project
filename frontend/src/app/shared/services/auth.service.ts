import { Injectable, signal } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../../environments/environment';
import { Observable, tap, of } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private apiUrl = `${environment.apiUrl}/auth`;
  
  // Reactive user state
  currentUser = signal<any>(this.getUserFromStorage());

  constructor(private http: HttpClient) {}

  private getUserFromStorage() {
    const token = localStorage.getItem('token');
    if (!token) return null;
    return {
      token,
      role: localStorage.getItem('role'),
      userId: localStorage.getItem('userId'),
      email: localStorage.getItem('userEmail'),
      name: localStorage.getItem('userName')
    };
  }

  login(credentials: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/login`, credentials).pipe(
      tap((response: any) => {
        const data = response.data;
        if (data && data.access_token) {
          localStorage.setItem('token', data.access_token);
          localStorage.setItem('refresh_token', data.refresh_token);
          localStorage.setItem('role', data.role);
          localStorage.setItem('userId', data.userId);
          localStorage.setItem('userEmail', data.email);
          localStorage.setItem('userName', data.full_name);
          
          this.currentUser.set({
            token: data.access_token,
            role: data.role,
            userId: data.userId,
            email: data.email,
            name: data.full_name
          });
        }
      })
    );
  }

  refreshToken(): Observable<any> {
    const refresh_token = localStorage.getItem('refresh_token');
    if (!refresh_token) return of(null);
    
    return this.http.post(`${this.apiUrl}/refresh`, { refresh_token }).pipe(
      tap((response: any) => {
        const data = response.data;
        if (data && data.access_token) {
          localStorage.setItem('token', data.access_token);
          if (data.refresh_token) {
            localStorage.setItem('refresh_token', data.refresh_token);
          }
          this.currentUser.update(user => user ? { ...user, token: data.access_token } : null);
        }
      })
    );
  }

  logout() {
    localStorage.clear();
    this.currentUser.set(null);
  }

  isLoggedIn(): boolean {
    return !!this.currentUser();
  }

  getRole(): string | null {
    return this.currentUser()?.role || null;
  }

  getToken(): string | null {
    return this.currentUser()?.token || null;
  }

  getUserName(): string | null {
    return this.currentUser()?.name || null;
  }
}
