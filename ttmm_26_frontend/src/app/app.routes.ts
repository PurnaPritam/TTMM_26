import { Routes } from '@angular/router';
import { LoginComponent } from './pages/login/login';
import { DashboardComponent } from './pages/dashboard/dashboard';
import { HomeComponent } from './pages/home/home';
import { inject } from '@angular/core';
import { ApiService } from './services/api';
import { Router } from '@angular/router';

const authGuard = () => {
  const api = inject(ApiService);
  const router = inject(Router);
  if (api.isLoggedIn()) return true;
  router.navigate(['/login']);
  return false;
};

export const routes: Routes = [
  { path: '', redirectTo: 'home', pathMatch: 'full' }, // Default to Home
  { path: 'home', component: HomeComponent },          // Public Page
  { path: 'login', component: LoginComponent },        // Login Page
  { path: 'dashboard', component: DashboardComponent, canActivate: [authGuard] } // Investor Only
];