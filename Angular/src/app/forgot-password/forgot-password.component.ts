import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { LoginServiceService } from '../services/login-service.service';

@Component({
  selector: 'app-forgot-password',
  templateUrl: './forgot-password.component.html',
  styleUrls: ['./forgot-password.component.css']
})
export class ForgotPasswordComponent implements OnInit {

  constructor(private ls: LoginServiceService, private route:Router) { }

  ngOnInit(): void {
  }

  username;
  sQues;
  sAns;
  password;

  getDetails()
  {
    console.log(this.username,this.sAns,this.sQues,this.password);
    this.ls.sForgotPassword(this.username,this.password,this.sQues,this.sAns).subscribe(
      response=>{
        alert(response['message']);
        if(response['message'] === "passwordUpdated"){
          this.route.navigate(['/login']);
        }
      }
    )

  }

}
