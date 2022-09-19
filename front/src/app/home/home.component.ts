import { Component, OnInit } from '@angular/core';
import { WhoAmIService } from '../whoami.service';

@Component({
  selector: 'app-home',
  template: `
    <div class="home">
      <div class="home-image">
        <img
          width="180vw"
          height="220vh"
          [src]="userHeadshot"
          alt="WhoAmI"
        />
      </div>
      <div class="home-center">
        <h1>{{ fullName }}</h1>
        <p>{{ job }}</p>
      </div>
    </div>
  `,
  styles: [
    `
      .home {
        margin: 10px;
      }
    `,
    `
      .home-center {
        text-align: center;
      }
    `,
    `
      .home-image {
        margin: 10px;
        text-align: center;
      }
    `
  ]
})
export class HomeComponent implements OnInit {
  public userHeadshot: any;
  public isImageLoading: boolean = false;
  public fullName: string = "";
  public job: string = "Software Engineer";

  constructor(private whoAmIService: WhoAmIService) { }

  ngOnInit() {
    this.getImageFromService();
    this.getUserFromService();
  }

  createImageFromBlob(image: Blob) {
    let reader = new FileReader();
    reader.addEventListener("load", () => {
       this.userHeadshot = reader.result;
    }, false);

    if (image) {
       reader.readAsDataURL(image);
    }
  }

  getImageFromService() {
    this.isImageLoading = true;
    this.whoAmIService.getUserHeadshot().subscribe(
      {
        next: (data) => {
          this.createImageFromBlob(data);
          this.isImageLoading = false;
        },
        error: () => this.isImageLoading = false,
      }
    );
  }
  
  getUserFromService() {
    this.whoAmIService.getUser().subscribe(
      {
        next: (data) => {
          this.fullName = `${data.first_name} ${data.last_name}`;
        }
      }
    );
  }
}
