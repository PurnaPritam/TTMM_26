import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { ApiService } from '../../services/api';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './login.html',
})
export class LoginComponent {
  username = '';
  password = '';
  errorMsg = '';

  constructor(private api: ApiService, private router: Router) {}

  onLogin() {
    this.api.login({ username: this.username, password: this.password }).subscribe({
      next: (res: any) => {
        this.api.saveToken(res.access);
        this.router.navigate(['/dashboard']);
      },
      error: (err) => {
        this.errorMsg = 'Invalid Credentials';
      }
    });
  }
}