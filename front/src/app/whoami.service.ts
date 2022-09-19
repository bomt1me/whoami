import { Inject, Injectable, isDevMode } from "@angular/core";
import { HttpClient } from "@angular/common/http";
import { User } from "./user";
import { Observable } from "rxjs";
import { APP_BASE_HREF } from "@angular/common";
import { environment as DevEnv } from "src/environments/environment";
import { environment as ProdEnv } from "src/environments/environment.prod";

@Injectable({
  providedIn: "root"
})
export class WhoAmIService {
  distantUrl: string;

  constructor(@Inject(APP_BASE_HREF) private baseHref: string, private http: HttpClient) {
    if (isDevMode()) {
      this.distantUrl = DevEnv.whoami_url;
    } else {
      this.distantUrl = ProdEnv.whoami_url;
    }

    console.log(this.distantUrl);
  }

  public getUser(): Observable<User> {
    return this.http.get<User>(`${this.distantUrl}user`);
  }

  public getUserHeadshot(): Observable<Blob> {
    return this.http.get(`${this.distantUrl}user/headshot`, { responseType: 'blob' });
  }
}
