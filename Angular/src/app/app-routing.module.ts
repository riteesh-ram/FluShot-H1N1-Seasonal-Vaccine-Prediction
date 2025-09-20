import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { DashComponent } from './dash/dash.component';
import { ForgotPasswordComponent } from './forgot-password/forgot-password.component';
import { LoginComponent } from './login/login.component';
import { RegisterComponent } from './register/register.component';
import { RouteGuard2Guard } from './routeGuards/route-guard2.guard';

const routes: Routes = [
  {path:'', component:LoginComponent},
  {path:'register', component: RegisterComponent},
  {path:'login', component: LoginComponent},
  {path:'forgot', component: ForgotPasswordComponent},
  {path:'dash', component: DashComponent, canActivate :[RouteGuard2Guard], canDeactivate:[RouteGuard2Guard]},
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
