import { Component, OnDestroy, OnInit, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../../services/api';
import { Router, RouterLink } from '@angular/router';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './dashboard.html',
})
export class DashboardComponent implements OnInit, OnDestroy {
  portalData: any = null; 
  myCurrentBid: number = 0;
  bidInput: number = 0;
  myHistory: any[] = []; 
  intervalId: any;
  message = '';
  username: string = 'Investor';
  
  // NEW: Flag to control the right-side loader
  isLoadingHistory: boolean = true;
  
  constructor(
    public api: ApiService, 
    private router: Router,
    private cd: ChangeDetectorRef 
  ) {}

  ngOnInit() {
    this.fetchData();
    this.fetchProfile();
    this.intervalId = setInterval(() => {
      this.fetchData();
    }, 2000);
  }

  ngOnDestroy() {
    if (this.intervalId) clearInterval(this.intervalId);
  }

  fetchData() {
    this.api.getPortalControl().subscribe({
      next: (res) => {
        this.portalData = res; 
        this.checkMyFunding();
        
        // Fetch history (this handles its own loading state)
        this.fetchMyHistory();
        
        this.cd.detectChanges(); 
      },
      error: (err) => console.error('Connection Error:', err)
    });
  }

  fetchProfile() {
    this.api.http.get(`${this.api.baseUrl}/get_investor_profile`).subscribe({
      next: (res: any) => {
        if (res && res.name) this.username = res.name;
      }
    });
  }

  checkMyFunding() {
    this.api.getMyFunding().subscribe((res: any) => {
      this.myCurrentBid = res.has_bid ? res.bid : 0;
      this.cd.detectChanges();
    });
  }

  fetchMyHistory() {
    // Only show spinner on the very first load (empty list)
    if (this.myHistory.length === 0) {
        this.isLoadingHistory = true;
    }

    this.api.http.get(`${this.api.baseUrl}/get_investor_funded_startups`).subscribe({
      next: (res: any) => {
        this.myHistory = res; 
        this.isLoadingHistory = false; // Stop spinner
        this.cd.detectChanges();
      },
      error: () => {
        this.isLoadingHistory = false;
        this.cd.detectChanges();
      }
    });
  }

  submitBid() {
    if (!this.portalData?.current_startup) return;
    
    this.api.placeBid(this.portalData.current_startup, this.bidInput).subscribe({
      next: (res: any) => {
        this.message = 'Bid Placed Successfully!';
        this.portalData.total_bid = res.total_bid;
        this.checkMyFunding();
        this.fetchMyHistory(); 
        
        setTimeout(() => {
          this.message = '';
          this.cd.detectChanges();
        }, 3000);
      },
      error: (err) => {
        this.message = 'Error placing bid.';
        this.cd.detectChanges();
      }
    });
  }

  logout() {
    this.api.logout();
    this.router.navigate(['/login']);
  }
}