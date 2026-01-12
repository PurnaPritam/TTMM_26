import { Component, OnInit, OnDestroy, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService } from '../../services/api';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './home.html',
  styleUrls: ['./home.css']
})
export class HomeComponent implements OnInit, OnDestroy {
  startupName: string = '';
  totalSum: number = 0;      
  displayedSum: number = 0;  
  progressPercentage: number = 0;
  contributors: any[] = [];
  allInvestors: any[] = []; 
  intervalId: any;

  constructor(public api: ApiService, private cd: ChangeDetectorRef) {}

  ngOnInit() {
    this.api.http.get(`${this.api.baseUrl}/investor_fetch`).subscribe((res: any) => {
      this.allInvestors = res;
      this.refreshData(); 
    });

    this.intervalId = setInterval(() => {
      this.refreshData();
    }, 2000);
  }

  ngOnDestroy() {
    if (this.intervalId) clearInterval(this.intervalId);
  }

  refreshData() {
    this.api.http.get(`${this.api.baseUrl}/get_startup_investors`).subscribe({
      next: (res: any) => {
        if (!res) return;

        this.startupName = res.startup_name || 'Waiting...';
        const newTotal = res.total_bid || 0;

        // If data changed, start animation
        if (newTotal !== this.totalSum) {
          // Both CSS and JS now use 1500ms duration
          this.animateValue(this.displayedSum, newTotal, 1500); 
          this.totalSum = newTotal;
        }
        
        this.progressPercentage = Math.min((this.totalSum / 50) * 100, 100);

        const funderIds = res.investors || [];
        if (this.allInvestors.length > 0) {
            this.contributors = this.allInvestors.filter(inv => funderIds.includes(inv.id));
        }
        
        this.cd.detectChanges();
      },
      error: () => console.log('Waiting for backend...')
    });
  }

  // UPDATED: Now uses Ease-Out logic to match the CSS bar
  animateValue(start: number, end: number, duration: number) {
    let startTimestamp: any = null;
    
    const step = (timestamp: any) => {
      if (!startTimestamp) startTimestamp = timestamp;
      
      // Calculate linear progress (0 to 1)
      const linearProgress = Math.min((timestamp - startTimestamp) / duration, 1);
      
      // Convert to "Ease Out" progress (starts fast, slows down)
      // Formula: 1 - (1 - t) * (1 - t)
      const easedProgress = 1 - Math.pow(1 - linearProgress, 2); 
      
      // Calculate number based on Eased progress
      this.displayedSum = Math.floor(start + (end - start) * easedProgress);
      
      this.cd.detectChanges();

      if (linearProgress < 1) {
        window.requestAnimationFrame(step);
      }
    };
    
    window.requestAnimationFrame(step);
  }
}