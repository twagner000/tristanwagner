import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';

import { AppComponent } from './app.component';
import { MessagesComponent } from './messages/messages.component';
import { AppRoutingModule } from './/app-routing.module';
import { DashboardComponent } from './dashboard/dashboard.component';
import {APP_BASE_HREF} from '@angular/common';
import { ActionsComponent } from './actions/actions.component';
import { UpgradesComponent } from './upgrades/upgrades.component';
import { BattalionsComponent } from './battalions/battalions.component';
import { MailComponent } from './mail/mail.component';
import { UpgradeLeaderlevelComponent } from './upgrade-leaderlevel/upgrade-leaderlevel.component';
import { UpgradeStructureComponent } from './upgrade-structure/upgrade-structure.component';
import { UpgradeTechnologyComponent } from './upgrade-technology/upgrade-technology.component';
import { BattalionHireComponent } from './battalion-hire/battalion-hire.component';
import { BattalionTrainComponent } from './battalion-train/battalion-train.component';
import { BattalionArmComponent } from './battalion-arm/battalion-arm.component';

    @NgModule({
    declarations: [
        AppComponent,
        MessagesComponent,
        DashboardComponent,
        ActionsComponent,
        UpgradesComponent,
        BattalionsComponent,
        MailComponent,
        UpgradeLeaderlevelComponent,
        UpgradeStructureComponent,
        UpgradeTechnologyComponent,
        BattalionHireComponent,
        BattalionTrainComponent,
        BattalionArmComponent
    ],
    imports: [
        BrowserModule ,
        FormsModule,
		AppRoutingModule,
		HttpClientModule
    ],
    providers: [{provide: APP_BASE_HREF, useValue : '/mpatrol/a' }],
    bootstrap: [AppComponent]
    })
    export class AppModule { }