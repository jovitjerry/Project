import { Routes } from '@angular/router';
import { FacultyDashboard } from './faculty-dashboard/faculty-dashboard';
import { MarkAttendance } from './mark-attendance/mark-attendance';
import { UploadMarks } from './upload-marks/upload-marks';

export const FACULTY_ROUTES: Routes = [
  { path: '', redirectTo: 'dashboard', pathMatch: 'full' },
  { path: 'dashboard', component: FacultyDashboard },
  { path: 'mark-attendance', component: MarkAttendance },
  { path: 'upload-marks', component: UploadMarks },
];
