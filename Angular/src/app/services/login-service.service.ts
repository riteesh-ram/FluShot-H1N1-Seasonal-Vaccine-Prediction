import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class LoginServiceService {

  constructor(private http: HttpClient) { }

  sLogin(usr:string,password:string){
    return this.http.post('http://127.0.0.1:8000/login', {"username": usr, "password": password})
    // return this.http.get('http://127.0.0.1:8000/login',{params:{username : usr,password : password}})
  }

  sSignUp(username: string,password: string,role: string, firstName: string,lastName: string,securityQuestion:string,securityAnswer:string){
    return this.http.post('http://127.0.0.1:8000/signUp', {
      "username": username,
      "password": password,
      "role": role,
      "firstName": firstName,
      "lastName": lastName,
      "securityQuestion": securityQuestion,
      "securityAnswer": securityAnswer,
    })
  }

  sForgotPassword(username: string,password: string,securityQuestion:string,securityAnswer:string)
  {
    return this.http.put('http://127.0.0.1:8000/updatePassword', {
      "username": username,
      "password": password,
      "securityQuestion": securityQuestion,
      "securityAnswer": securityAnswer,
    })
  }

  sdataUpload(h1n1_concern,h1n1_knowledge,behavioral_antiviral_meds,behavioral_avoidance,behavioral_face_mask,behavioral_wash_hands,behavioral_large_gatherings,behavioral_outside_home,behavioral_touch_face,doctor_recc_h1n1,doctor_recc_seasonal,chronic_med_condition,child_under_6_months,health_worker,health_insurance,opinion_h1n1_vacc_effective,opinion_h1n1_risk,opinion_h1n1_sick_from_vacc,opinion_seas_vacc_effective,opinion_seas_risk,opinion_seas_sick_from_vacc,age_group,education,race,sex,income_poverty,marital_status,rent_or_own,employment_status,hhs_geo_region,census_msa,household_adults,household_children,employment_industry,employment_occupation){
    return this.http.post('http://127.0.0.1:8000/dataUpload',{"h1n1_concern":h1n1_concern,"h1n1_knowledge":h1n1_knowledge,"behavioral_antiviral_meds":behavioral_antiviral_meds,"behavioral_avoidance":behavioral_avoidance,"behavioral_face_mask":behavioral_face_mask,"behavioral_wash_hands":behavioral_wash_hands,"behavioral_large_gatherings":behavioral_large_gatherings,"behavioral_outside_home":behavioral_outside_home,"behavioral_touch_face":behavioral_touch_face,"doctor_recc_h1n1":doctor_recc_h1n1,"doctor_recc_seasonal":doctor_recc_seasonal,"chronic_med_condition":chronic_med_condition,"child_under_6_months":child_under_6_months,"health_worker":health_worker,"health_insurance":health_insurance,"opinion_h1n1_vacc_effective":opinion_h1n1_vacc_effective,"opinion_h1n1_risk":opinion_h1n1_risk,"opinion_h1n1_sick_from_vacc":opinion_h1n1_sick_from_vacc,"opinion_seas_vacc_effective":opinion_seas_vacc_effective,"opinion_seas_risk":opinion_seas_risk,"opinion_seas_sick_from_vacc":opinion_seas_sick_from_vacc,"age_group":age_group,"education":education,"race":race,"sex":sex,"income_poverty":income_poverty,"marital_status":marital_status,"rent_or_own":rent_or_own,"employment_status":employment_status,"hhs_geo_region":hhs_geo_region,"census_msa":census_msa,"household_adults":household_adults,"household_children":household_children,"employment_industry":employment_industry,"employment_occupation":employment_occupation});
  }


  loginstatus =false;
  setLoginStatus(status : boolean){
    this.loginstatus = status;
  }

  getLoginStatus(){
    return(this.loginstatus)
  }

}
