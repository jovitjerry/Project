import { Routes } from '@angular/router';
import { AdminDashboard } from './admin-dashboard/admin-dashboard';
import { ManageStudents } from './manage-students/manage-students';
import { ManageFaculty } from './manage-faculty/manage-faculty';
import { ManageCourses } from './manage-courses/manage-courses';

export const ADMIN_ROUTES: Routes = [
  { path: '', redirectTo: 'dashboard', pathMatch: 'full' },
  { path: 'dashboard', component: AdminDashboard },
  { path: 'manage-students', component: ManageStudents },
  { path: 'manage-faculty', component: ManageFaculty },
  { path: 'manage-courses', component: ManageCourses },
];
