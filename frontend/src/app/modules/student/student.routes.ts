import { Routes } from '@angular/router';
import { StudentDashboard } from './student-dashboard/student-dashboard';
import { AttendanceView } from './attendance-view/attendance-view';
import { Results } from './results/results';

export const STUDENT_ROUTES: Routes = [
  { path: '', redirectTo: 'dashboard', pathMatch: 'full' },
  { path: 'dashboard', component: StudentDashboard },
  { path: 'attendance', component: AttendanceView },
  { path: 'results', component: Results },
];
