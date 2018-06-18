import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
//import { HttpModule } from '@angular/http';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';

import { AppComponent } from './app.component';
import { CreaturesComponent } from './creatures/creatures.component';
import { CreatureDetailComponent } from './creature-detail/creature-detail.component';
import { MessagesComponent } from './messages/messages.component';
import { AppRoutingModule } from './/app-routing.module';
import { DashboardComponent } from './dashboard/dashboard.component';

    @NgModule({
    declarations: [
        AppComponent,
        CreaturesComponent,
        CreatureDetailComponent,
        MessagesComponent,
        DashboardComponent
    ],
    imports: [
        BrowserModule ,
        FormsModule,
		AppRoutingModule,
		//HttpModule,
		HttpClientModule
    ],
    providers: [],
    bootstrap: [AppComponent]
    })
    export class AppModule { }