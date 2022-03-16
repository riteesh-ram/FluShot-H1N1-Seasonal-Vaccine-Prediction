import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { LoginServiceService } from '../services/login-service.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {

  constructor(private ls :LoginServiceService, private route: Router) { }

  ngOnInit(): void {
  }

  username= "";
  password= "";
  passwordVar:any;
  match="";
  token="";

   getDetails(){
    console.log(this.username,this.password);
    this.ls.sLogin(this.username,this.password).subscribe(
      response=>{
        this.match=response['message'];
        this.token = response['token'];
        sessionStorage.setItem('token',response['token'])
        sessionStorage.setItem('username', response['username']);
        if(this.match == "True"){
          this.ls.setLoginStatus(true);
          this.route.navigate(['/dash']);
        }
        else{
          alert("Invalid User Credentials")
        }
        console.log(this.match,this.username);
      },error => {
        alert("Invalid User Credentials");
        console.log(error.error.message);
      }
    );
  }


  h1n1_concern;
  h1n1_knowledge;
  behavioral_antiviral_meds;
  behavioral_avoidance;
  behavioral_face_mask;
  behavioral_wash_hands;
  behavioral_large_gatherings;
  behavioral_outside_home;
  behavioral_touch_face;
  doctor_recc_h1n1;
  doctor_recc_seasonal;
  chronic_med_condition;
  child_under_6_months;
  health_worker;
  health_insurance;
  opinion_h1n1_vacc_effective;
  opinion_h1n1_risk;
  opinion_h1n1_sick_from_vacc;
  opinion_seas_vacc_effective;
  opinion_seas_risk;
  opinion_seas_sick_from_vacc;
  age_group;
  education;
  race;
  sex;
  income_poverty;
  marital_status;
  rent_or_own;
  employment_status;
  hhs_geo_region;
  census_msa;
  household_adults;
  household_children;
  employment_industry;
  employment_occupation;
  
  dur;


  dataUpload()
  {
    // console.log(this.h1n1_concern, this.h1n1_knowledge, this.behavioral_antiviral_meds, this.behavioral_avoidance,  this.behavioral_face_mask, this.behavioral_wash_hands, this.behavioral_large_gatherings, this.behavioral_outside_home, this.behavioral_touch_face, this.doctor_recc_h1n1, this.doctor_recc_seasonal, this.chronic_med_condition, this.child_under_6_months, this.health_worker, this.health_insurance, this.opinion_h1n1_vacc_effective, this.opinion_h1n1_risk, this.opinion_h1n1_sick_from_vacc, this.opinion_seas_vacc_effective, this.opinion_seas_risk, this.opinion_seas_sick_from_vacc, this.age_group, this.education, this.race, this.sex, this.income_poverty, this.marital_status, this.rent_or_own, this.employment_status, this.hhs_geo_region, this.census_msa, this.household_adults, this.household_children, this.employment_industry, this.employment_occupation);
    this.ls.sdataUpload(this.h1n1_concern, this.h1n1_knowledge, this.behavioral_antiviral_meds, this.behavioral_avoidance,  this.behavioral_face_mask, this.behavioral_wash_hands, this.behavioral_large_gatherings, this.behavioral_outside_home, this.behavioral_touch_face, this.doctor_recc_h1n1, this.doctor_recc_seasonal, this.chronic_med_condition, this.child_under_6_months, this.health_worker, this.health_insurance, this.opinion_h1n1_vacc_effective, this.opinion_h1n1_risk, this.opinion_h1n1_sick_from_vacc, this.opinion_seas_vacc_effective, this.opinion_seas_risk, this.opinion_seas_sick_from_vacc, this.age_group, this.education, this.race, this.sex, this.income_poverty, this.marital_status, this.rent_or_own, this.employment_status, this.hhs_geo_region, this.census_msa, this.household_adults, this.household_children, this.employment_industry, this.employment_occupation).subscribe(
      response=>{
        this.dur = response['message'];
      }
    ),error=>{
      alert("Please Try Again");
    };
  }

}
