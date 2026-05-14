import { Routes } from '@angular/router';
import { HodDashboard } from './hod-dashboard/hod-dashboard';
import { HodFaculty } from './hod-faculty/hod-faculty';
import { HodStudents } from './hod-students/hod-students';
import { HodPerformance } from './hod-performance/hod-performance';
import { HodTimetable } from './hod-timetable/hod-timetable';
import { HodGrievances } from './hod-grievances/hod-grievances';
import { HodNotices } from './hod-notices/hod-notices';
import { HodProfile } from './hod-profile/hod-profile';
import { HodSettings } from './hod-settings/hod-settings';

export const HOD_ROUTES: Routes = [
  { path: '', redirectTo: 'dashboard', pathMatch: 'full' },
  { path: 'dashboard', component: HodDashboard },
  { path: 'faculty', component: HodFaculty },
  { path: 'students', component: HodStudents },
  { path: 'performance', component: HodPerformance },
  { path: 'timetable', component: HodTimetable },
  { path: 'grievances', component: HodGrievances },
  { path: 'notices', component: HodNotices },
  { path: 'profile', component: HodProfile },
  { path: 'settings', component: HodSettings },
];
