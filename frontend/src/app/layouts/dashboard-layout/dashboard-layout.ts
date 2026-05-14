import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { Topnav } from '../topnav/topnav';

@Component({
  selector: 'app-dashboard-layout',
  standalone: true,
  imports: [RouterOutlet, Topnav],
  templateUrl: './dashboard-layout.html',
  styleUrl: './dashboard-layout.scss',
})
export class DashboardLayout {}
