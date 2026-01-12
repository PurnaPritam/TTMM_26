import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  // These must be public so components like HomeComponent can access them directly
  public baseUrl = 'http://127.0.0.1:8000'; 
  
  constructor(public http: HttpClient) { }

  // --- Authentication ---

  login(data: any): Observable<any> {
    return this.http.post(`${this.baseUrl}/token`, data);
  }

  saveToken(token: string) {
    localStorage.setItem('access_token', token);
  }

  getToken() {
    return localStorage.getItem('access_token');
  }

  isLoggedIn(): boolean {
    return !!this.getToken();
  }

  logout() {
    localStorage.removeItem('access_token');
  }

  // --- Core Game Logic ---

  getPortalControl(): Observable<any> {
    return this.http.get(`${this.baseUrl}/portal_control`);
  }

  placeBid(startupId: number, amount: number): Observable<any> {
    const data = { startup: startupId, bid: amount };
    return this.http.post(`${this.baseUrl}/bidding`, data);
  }

  getMyFunding(): Observable<any> {
    return this.http.get(`${this.baseUrl}/get_own_funding`);
  }
  
  // --- Helpers ---

  // Used by HomeComponent to show investor images
  getImageUrl(relativePath: string): string {
    if (!relativePath) return '';
    if (relativePath.startsWith('http')) return relativePath;
    return `${this.baseUrl}${relativePath}`;
  }
}