import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';

@Component({
  selector: 'app-root',
  templateUrl: './app.html',
  standalone: true,
  imports: [RouterOutlet],
  styleUrl: './app.scss',
})
export class App {
  protected readonly title = signal('Rajagiri School of Engineering and Technology');
}
