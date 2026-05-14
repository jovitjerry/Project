import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { environment } from '../../../environments/environment';
import { Observable, map } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class HodService {
  private apiUrl = `${environment.apiUrl}/hod`;

  constructor(private http: HttpClient) {}

  getStats(): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/stats`).pipe(map(res => res.data));
  }

  getFaculty(search = '', skip = 0, limit = 50): Observable<any> {
    let params = new HttpParams().set('skip', skip).set('limit', limit);
    if (search) params = params.set('search', search);
    return this.http.get<any>(`${this.apiUrl}/faculty`, { params }).pipe(map(res => res.data));
  }

  getStudents(search = '', skip = 0, limit = 50): Observable<any> {
    let params = new HttpParams().set('skip', skip).set('limit', limit);
    if (search) params = params.set('search', search);
    return this.http.get<any>(`${this.apiUrl}/students`, { params }).pipe(map(res => res.data));
  }

  getPerformance(): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/performance`).pipe(map(res => res.data));
  }

  // Timetable
  getTimetables(): Observable<any[]> {
    return this.http.get<any>(`${this.apiUrl}/timetable`).pipe(map(res => res.data || []));
  }

  uploadTimetable(semester: string, file: File): Observable<any> {
    const formData = new FormData();
    formData.append('semester', semester);
    formData.append('file', file);
    return this.http.post<any>(`${this.apiUrl}/timetable`, formData);
  }

  deleteTimetable(id: number): Observable<any> {
    return this.http.delete<any>(`${this.apiUrl}/timetable/${id}`);
  }

  // Grievances
  getGrievances(status?: string): Observable<any[]> {
    let params = new HttpParams();
    if (status) params = params.set('status', status);
    return this.http.get<any>(`${this.apiUrl}/grievances`, { params }).pipe(map(res => res.data || []));
  }

  updateGrievanceStatus(id: number, status: string): Observable<any> {
    return this.http.put<any>(`${this.apiUrl}/grievances/${id}`, { status });
  }

  // Notices
  getNotices(): Observable<any[]> {
    return this.http.get<any>(`${this.apiUrl}/notices`).pipe(map(res => res.data || []));
  }

  createNotice(notice: any): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/notices`, notice);
  }

  updateNotice(id: number, notice: any): Observable<any> {
    return this.http.put<any>(`${this.apiUrl}/notices/${id}`, notice);
  }

  deleteNotice(id: number): Observable<any> {
    return this.http.delete<any>(`${this.apiUrl}/notices/${id}`);
  }
}
