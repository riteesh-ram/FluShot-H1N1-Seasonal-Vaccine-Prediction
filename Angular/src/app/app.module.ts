import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { LoginComponent } from './login/login.component';
import { RegisterComponent } from './register/register.component';
import { DashComponent } from './dash/dash.component';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { FileUploadModule } from 'ng2-file-upload';
import { SpinnerComponent } from './spinner/spinner.component';
import { InterceptorService } from './services/interceptor.service';
import { ForgotPasswordComponent } from './forgot-password/forgot-password.component';

@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    RegisterComponent,
    DashComponent,
    SpinnerComponent,
    ForgotPasswordComponent
  ],
  imports: [
    HttpClientModule,
    BrowserModule,
    FileUploadModule,
    AppRoutingModule,
    FormsModule
  ],
  providers: [
    {provide:HTTP_INTERCEPTORS, useClass:InterceptorService, multi:true}
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
