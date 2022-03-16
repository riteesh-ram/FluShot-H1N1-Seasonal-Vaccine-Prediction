import { Component, OnInit } from '@angular/core';
import { FileLikeObject, FileUploader } from 'ng2-file-upload';
import { DashServiceService } from '../services/dash-service.service';
import * as fileSaver from 'file-saver';
import { LoaderService } from '../services/loader.service';
import { Router } from '@angular/router';
import { LoginServiceService } from '../services/login-service.service';

@Component({
  selector: 'app-dash',
  templateUrl: './dash.component.html',
  styleUrls: ['./dash.component.css']
})
export class DashComponent implements OnInit {

  constructor(private ds :DashServiceService, public loaderser :LoaderService,private ls :LoginServiceService,  private route: Router) {
   }

  ngOnInit(): void {
    this.username = sessionStorage.getItem('username');
    this.getAllDetails();
  }
  dModelName:string="";
  dH1N1Acc:string="";
  dSesAcc:string="";
  pH1N1:string="";
  pses:string="";


  spinnerloading= false;

  allProjects: any;
  projectSelected:any;
  personal=false;
  username = 'string';
  newProjectName:any;
  loading=false;
  projectcreated = false;
  projectSelection = false;
  depButton=false;
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


  getAllDetails(){
    this.personal = false;
    this.projectSelection = false;
    this.depButton = false;
    this.ds.sAllProjects().subscribe(
      response=>{
        this.allProjects = response;
      })
      // console.log(this.allProjects);
  }
  getDeployedProjects(){
    this.personal = true;
    this.depButton = false;
    this.projectSelection = false;
    this.ds.sDeployedProjects(this.username).subscribe(
      response=>{
        this.allProjects = response;
      }
    )
    // console.log(this.allProjects);
  }
  getUnDeployedProjects(){
    this.personal = true;
    this.depButton = true;
    this.projectSelection = false;
    this.ds.sUnDeployedProjects(this.username).subscribe(
      response=>{
        this.allProjects = response;
      }
    )
    // console.log(this.allProjects);
  }
  selectProject(tmp:string){
    this.projectSelected = tmp;
    this.projectSelection = true;
    console.log(this.projectSelected);
  }

  deleteProject(project:string)
  {
    // console.log("In Project");
    // console.log(project);
    this.ds.sDeleteProject(this.username,project).subscribe(
      response=>{
        this.getAllDetails();
        alert(response['message']);
      }
    );
  }


  addProject(projectname:string){
    this.loading = true;
    this.ds.sAddProject(this.username, projectname).subscribe(
      response=>{
        this.loading = false;
        this.projectcreated = true;
      },error => {
        this.loading = false;
        alert(error.error.message);
        console.log(error.error.message);
      });
      this.getUnDeployedProjects();
  }

  getFiles2(): FileLikeObject[] {
    return this.uploaderImage.queue.map(fileItem => {
      return fileItem.file;
    });
  }

  // image upload multiple
  imageuploaded = false;
  public uploaderImage: FileUploader = new FileUploader({});
  uploadImage() {
    this.loading = true;
    let files = this.getFiles2();
    files.forEach(file => {
      let formData = new FormData();
      formData.append("project_name", this.projectSelected);
      formData.append("file", file.rawFile, file.name);

      this.ds.sUploadfiles(formData).subscribe(response => {
        console.log("image upload response",response);
        this.loading = false;
        this.imageuploaded = true;
        // mandatory to calling these 3 services in order
      }, error => {
        alert(error.error.message);
        console.log(error.error.message);
      });
    });
  }

  predictCSV(){
    this.spinnerloading= true;
    this.loading = true;
    let files = this.getFiles2();
    files.forEach(file => {
      let formData = new FormData();
      formData.append("project_name", this.projectSelected);
      formData.append("file", file.rawFile, file.name);
      console.log(file.name);
      
      this.ds.sPredictCSV(formData).subscribe(response => 
        {
          let blob:any = new Blob([response], { type: 'text/csv; charset=utf-8' });
          fileSaver.saveAs(blob, file.name);
          this.loading = false;
          this.imageuploaded = true;
      }, error => {
        alert(error.error.message);
        console.log(error.error.message);
      });
    });

    this.loading = false;
    this.spinnerloading= false;
    this.imageuploaded = true;
  }






  deployModel(){
    this.ds.sDeployModel(this.username,this.projectSelected).subscribe(
      response=>{
        this.getAllDetails();
        alert(response['message']);
      }, error=>{
        console.log(error.error.message);
      }
      
    );
  }


  downloadfile(fileN:string){
    this.ds.sDownloadFile(this.projectSelected,fileN).subscribe(
      response => {
        if(fileN==="training_set_features.csv")
        {
          let blob:any = new Blob([response], { type: 'text/csv; charset=utf-8' });
          fileSaver.saveAs(blob, 'training_set_features.csv');
        }
        else
        {
          let blob:any = new Blob([response], { type: 'text/html; charset=utf-8' });
          fileSaver.saveAs(blob, fileN);
        }
        
      }
    ),error => {console.log('Error downloading the file'),
    () => console.info('File downloaded successfully');
    }
  }

  image1;
  image2;
  getModelDetails(project:string){
    this.ds.sGetProjectDetails(project).subscribe(
      response=>{
        this.image1 ="data:image/jpeg;base64,"+ response['img1'];
        this.image2 = "data:image/jpeg;base64,"+ response['img2'];
        this.dModelName=response['modelName'];
        this.dH1N1Acc= response['Accuracy_h1n1'];
        this.dSesAcc = response['Accuracy_ses'];
      }
    ),error=>{
      alert("Try Again");
    };
  }

  trainModel()
  {
    this.loaderser.isLoading.next(true);
    // this.spinnerloading= true;
    this.ds.sTrainMOdel(this.projectSelected,"string",false).subscribe(
      response=>{
        alert(response['message']);
        this.loaderser.isLoading.next(false);
        this.spinnerloading= false;
      }
    ),error=>{
      alert("Model not Built Sucessfully");
      this.loaderser.isLoading.next(false);
      this.spinnerloading= false;
    };
    
  }

  predictInd()
  {
    this.spinnerloading= true;
    // console.log(this.h1n1_concern, this.h1n1_knowledge, this.behavioral_antiviral_meds, this.behavioral_avoidance,  this.behavioral_face_mask, this.behavioral_wash_hands, this.behavioral_large_gatherings, this.behavioral_outside_home, this.behavioral_touch_face, this.doctor_recc_h1n1, this.doctor_recc_seasonal, this.chronic_med_condition, this.child_under_6_months, this.health_worker, this.health_insurance, this.opinion_h1n1_vacc_effective, this.opinion_h1n1_risk, this.opinion_h1n1_sick_from_vacc, this.opinion_seas_vacc_effective, this.opinion_seas_risk, this.opinion_seas_sick_from_vacc, this.age_group, this.education, this.race, this.sex, this.income_poverty, this.marital_status, this.rent_or_own, this.employment_status, this.hhs_geo_region, this.census_msa, this.household_adults, this.household_children, this.employment_industry, this.employment_occupation);
    this.ds.sPredictInd(this.h1n1_concern, this.h1n1_knowledge, this.behavioral_antiviral_meds, this.behavioral_avoidance,  this.behavioral_face_mask, this.behavioral_wash_hands, this.behavioral_large_gatherings, this.behavioral_outside_home, this.behavioral_touch_face, this.doctor_recc_h1n1, this.doctor_recc_seasonal, this.chronic_med_condition, this.child_under_6_months, this.health_worker, this.health_insurance, this.opinion_h1n1_vacc_effective, this.opinion_h1n1_risk, this.opinion_h1n1_sick_from_vacc, this.opinion_seas_vacc_effective, this.opinion_seas_risk, this.opinion_seas_sick_from_vacc, this.age_group, this.education, this.race, this.sex, this.income_poverty, this.marital_status, this.rent_or_own, this.employment_status, this.hhs_geo_region, this.census_msa, this.household_adults, this.household_children, this.employment_industry, this.employment_occupation, this.projectSelected).subscribe(
      response=>{
        this.pH1N1 = response['h1n1'];
        this.pses = response['sesonal']
      }
    ),error=>{
      alert("Please Try Again");
    };
    this.spinnerloading= false;

  }

  dtale()
  {
    this.ds.sDatale(this.projectSelected).subscribe(
      response=>{
        console.log(response);
        if(response['message']==='0'){
          alert("Dataset Error")
        }
        else{
          window.open("http://127.0.0.1:8080/dtale/main/" +response['message'] , '_blank');
        }
      }
    )
  }

  signOut(){
    sessionStorage.clear();
    console.log(sessionStorage)
    this.ls.setLoginStatus(false);
    this.route.navigate(['']);
  }

}
