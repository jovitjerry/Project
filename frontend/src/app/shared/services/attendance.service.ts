import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../../environments/environment';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AttendanceService {
  private apiUrl = `${environment.apiUrl}/attendance`;

  constructor(private http: HttpClient) {}

  markAttendance(data: any): Observable<any> {
    return this.http.post(this.apiUrl, data);
  }

  markAttendanceBulk(data: any[]): Observable<any> {
    return this.http.post(`${this.apiUrl}/bulk`, data);
  }

  getStudentAttendance(studentId: number): Observable<any> {
    return this.http.get(`${this.apiUrl}/student/${studentId}`);
  }

  getStudentReport(studentId: number): Observable<any> {
    return this.http.get(`${this.apiUrl}/report/student/${studentId}`);
  }
}
