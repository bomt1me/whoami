import { Component, OnInit } from "@angular/core";
import { WhoAmIService } from "../whoami.service";

@Component({
  selector: "app-toolbar",
  template: `
    <mat-toolbar color="primary">
      <mat-toolbar-row>
        <button mat-button routerLink="/home">{{ fullName }}</button>
        <span class="example-fill-remaining-space"></span>
      </mat-toolbar-row>
    </mat-toolbar>
  `,
  styles: [
    `
      .example-fill-remaining-space {
        flex: 1 1 auto;
      }
    `
  ]
})
export class ToolbarComponent implements OnInit {
  public fullName: string = "";

  constructor(private whoAmIService: WhoAmIService) {}

  ngOnInit() {
    this.whoAmIService.getUser().subscribe(
      {
        next: (data) => {
          this.fullName = `${data.first_name} ${data.last_name}`;
        }
      }
    );
  }
}
