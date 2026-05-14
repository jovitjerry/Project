import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { environment } from '../../../environments/environment';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class TeacherService {
  private apiUrl = `${environment.apiUrl}/teachers`;

  constructor(private http: HttpClient) {}

  getTeachers(options: { department?: string, search?: string, skip?: number, limit?: number } = {}): Observable<any> {
    let params = new HttpParams();
    if (options.department) params = params.set('department', options.department);
    if (options.search) params = params.set('search', options.search);
    if (options.skip !== undefined) params = params.set('skip', options.skip.toString());
    if (options.limit !== undefined) params = params.set('limit', options.limit.toString());
    
    return this.http.get(this.apiUrl, { params });
  }

  getTeacher(id: number): Observable<any> {
    return this.http.get(`${this.apiUrl}/${id}`);
  }

  createTeacher(teacher: any): Observable<any> {
    return this.http.post(this.apiUrl, teacher);
  }

  updateTeacher(id: number, teacher: any): Observable<any> {
    return this.http.put(`${this.apiUrl}/${id}`, teacher);
  }

  deleteTeacher(id: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/${id}`);
  }
}
