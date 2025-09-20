import { HttpClient, HttpResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';
import {Observable} from 'rxjs';


@Injectable({
  providedIn: 'root'
})
export class DashServiceService {

  constructor(private http: HttpClient) { }

  sAllProjects(){
    return this.http.get('http://127.0.0.1:8000/allProjects',{params:{}})
  }

  sDeployedProjects(usr:string){
    return this.http.get('http://127.0.0.1:8000/deployedprojects',{params:{pid : usr}})
  }

  sUnDeployedProjects(usr:string){
    return this.http.get('http://127.0.0.1:8000/unDeployedprojects',{params:{pid : usr}})
  }

  sAddProject(usr:string,project:string){
    return this.http.post('http://127.0.0.1:8000/addproject', { "projectName": project, "owner": usr, "status": "Undeployed"})
  }

  sUploadfiles(formData: any){
    // console.log("at uploadImage service",formData);
    return this.http.post('http://127.0.0.1:8000/addData', formData);
  }

  sDeleteProject(usr:string,project:string){
    return this.http.delete('http://127.0.0.1:8000/deleteModel',{params:{username : usr, project_name:project}})
  }

  sDeployModel(usr:string,project:string){
    // console.log(usr,project);
    return this.http.put('http://127.0.0.1:8000/deployModel',{"userName" : usr, "projectName":project})
  }

  sDownloadFile(project:string, fileN:string): any {
		return this.http.get('http://127.0.0.1:8000/getcsv',{params:{project_name:project, filename:fileN}, responseType: 'blob'});
  }

  sGetProjectDetails(project:string){
    return this.http.get('http://127.0.0.1:8000/getModelInfo',{params:{project_name : project}})
  }

  sPredictCSV(formData: any): any {
    // console.log("at uploadImage service",formData);
    return this.http.post('http://127.0.0.1:8000/predictCSV', formData, {responseType: 'blob'});
  }

  sTrainMOdel(project:string, algo:string, ptune:boolean){
    return this.http.post('http://127.0.0.1:8000/trainmodel',{"fileName": project,"algo": algo, "pTune": ptune});
  }

  sPredictInd(h1n1_concern,h1n1_knowledge,behavioral_antiviral_meds,behavioral_avoidance,behavioral_face_mask,behavioral_wash_hands,behavioral_large_gatherings,behavioral_outside_home,behavioral_touch_face,doctor_recc_h1n1,doctor_recc_seasonal,chronic_med_condition,child_under_6_months,health_worker,health_insurance,opinion_h1n1_vacc_effective,opinion_h1n1_risk,opinion_h1n1_sick_from_vacc,opinion_seas_vacc_effective,opinion_seas_risk,opinion_seas_sick_from_vacc,age_group,education,race,sex,income_poverty,marital_status,rent_or_own,employment_status,hhs_geo_region,census_msa,household_adults,household_children,employment_industry,employment_occupation,project){
    return this.http.post('http://127.0.0.1:8000/predictINd',{"h1n1_concern":h1n1_concern,"h1n1_knowledge":h1n1_knowledge,"behavioral_antiviral_meds":behavioral_antiviral_meds,"behavioral_avoidance":behavioral_avoidance,"behavioral_face_mask":behavioral_face_mask,"behavioral_wash_hands":behavioral_wash_hands,"behavioral_large_gatherings":behavioral_large_gatherings,"behavioral_outside_home":behavioral_outside_home,"behavioral_touch_face":behavioral_touch_face,"doctor_recc_h1n1":doctor_recc_h1n1,"doctor_recc_seasonal":doctor_recc_seasonal,"chronic_med_condition":chronic_med_condition,"child_under_6_months":child_under_6_months,"health_worker":health_worker,"health_insurance":health_insurance,"opinion_h1n1_vacc_effective":opinion_h1n1_vacc_effective,"opinion_h1n1_risk":opinion_h1n1_risk,"opinion_h1n1_sick_from_vacc":opinion_h1n1_sick_from_vacc,"opinion_seas_vacc_effective":opinion_seas_vacc_effective,"opinion_seas_risk":opinion_seas_risk,"opinion_seas_sick_from_vacc":opinion_seas_sick_from_vacc,"age_group":age_group,"education":education,"race":race,"sex":sex,"income_poverty":income_poverty,"marital_status":marital_status,"rent_or_own":rent_or_own,"employment_status":employment_status,"hhs_geo_region":hhs_geo_region,"census_msa":census_msa,"household_adults":household_adults,"household_children":household_children,"employment_industry":employment_industry,"employment_occupation":employment_occupation,"projectName":project});
  }

  sDatale(project:string){
    project = "http://127.0.0.1:8080/editing/"+project;
    return this.http.get(project);
  }
  

}
