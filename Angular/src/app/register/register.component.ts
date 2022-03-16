import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { LoginComponent } from '../login/login.component';
import { LoginServiceService } from '../services/login-service.service';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent implements OnInit {

  constructor(private ls :LoginServiceService, private route: Router) { }

  ngOnInit(): void {
  }
  firstname;
  lastname;
  password;
  cPassword;
  gender;
  sQues;
  sAns;
  username;
  phone;
  role;

  getRegister(){
    this.ls.sSignUp(this.username,this.password,this.role, this.firstname,this.lastname,this.sQues,this.sAns).subscribe(
      response=>{
        // console.log(response['message'])
        if(response['message']==="userCreated"){
          this.route.navigate(['/login']);
        }
        else{
          alert(response['message'])
        }
      }
    )
  }

}
