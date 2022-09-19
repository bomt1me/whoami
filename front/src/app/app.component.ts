import { Component } from "@angular/core";

@Component({
  selector: "app-root",
  template: `
    <app-toolbar></app-toolbar>
    <router-outlet></router-outlet>
    <app-footer></app-footer>
  `,
  styles: [``]
})
export class AppComponent {
  public title = "whoami";
}
