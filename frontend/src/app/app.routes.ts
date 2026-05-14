import { Routes } from '@angular/router';
import { AuthLayout } from './layouts/auth-layout/auth-layout';
import { DashboardLayout } from './layouts/dashboard-layout/dashboard-layout';
import { authGuard } from './shared/guards/auth.guard';
import { roleGuard } from './shared/guards/role.guard';

export const routes: Routes = [
  { path: '', redirectTo: 'auth/login', pathMatch: 'full' },
  {
    path: 'auth',
    component: AuthLayout,
    loadChildren: () => import('./modules/auth/auth.routes').then(m => m.AUTH_ROUTES)
  },
  {
    path: 'admin',
    component: DashboardLayout,
    canActivate: [authGuard, roleGuard],
    data: { expectedRoles: ['admin'] },
    loadChildren: () => import('./modules/admin/admin.routes').then(m => m.ADMIN_ROUTES)
  },
  {
    path: 'student',
    component: DashboardLayout,
    canActivate: [authGuard, roleGuard],
    data: { expectedRoles: ['student', 'admin'] },
    loadChildren: () => import('./modules/student/student.routes').then(m => m.STUDENT_ROUTES)
  },
  {
    path: 'faculty',
    component: DashboardLayout,
    canActivate: [authGuard, roleGuard],
    data: { expectedRoles: ['teacher', 'admin'] },
    loadChildren: () => import('./modules/faculty/faculty.routes').then(m => m.FACULTY_ROUTES)
  },
  {
    path: 'hod',
    component: DashboardLayout,
    canActivate: [authGuard, roleGuard],
    data: { expectedRoles: ['hod', 'admin'] },
    loadChildren: () => import('./modules/hod/hod.routes').then(m => m.HOD_ROUTES)
  },
  { path: '**', redirectTo: 'auth/login' }
];
