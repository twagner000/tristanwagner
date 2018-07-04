import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { ModalModule } from 'ngx-bootstrap/modal';
import { AlertModule } from 'ngx-bootstrap/alert';

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
import { ChoosePlayerComponent } from './choose-player/choose-player.component';
import { ForbiddenComponent } from './forbidden/forbidden.component';
import { JukeboxComponent } from './jukebox/jukebox.component';

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
        BattalionArmComponent,
        ChoosePlayerComponent,
        ForbiddenComponent,
        JukeboxComponent,
    ],
    imports: [
        BrowserModule ,
        FormsModule,
		AppRoutingModule,
		HttpClientModule,
		ModalModule.forRoot(),
		AlertModule.forRoot()
    ],
    providers: [{provide: APP_BASE_HREF, useValue : '/mpatrol' }],
    bootstrap: [AppComponent]
    })
    export class AppModule { }