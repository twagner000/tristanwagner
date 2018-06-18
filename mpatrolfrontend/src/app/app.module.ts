import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';

import { AppComponent } from './app.component';
import { CreaturesComponent } from './creatures/creatures.component';
import { CreatureDetailComponent } from './creature-detail/creature-detail.component';
import { MessagesComponent } from './messages/messages.component';
import { AppRoutingModule } from './/app-routing.module';
import { DashboardComponent } from './dashboard/dashboard.component';
import {APP_BASE_HREF} from '@angular/common';
import { ActionsComponent } from './actions/actions.component';
import { UpgradesComponent } from './upgrades/upgrades.component';
import { BattalionsComponent } from './battalions/battalions.component';
import { MailComponent } from './mail/mail.component';
import { UpgradeLeaderlevelComponent } from './upgrade-leaderlevel/upgrade-leaderlevel.component';

    @NgModule({
    declarations: [
        AppComponent,
        CreaturesComponent,
        CreatureDetailComponent,
        MessagesComponent,
        DashboardComponent,
        ActionsComponent,
        UpgradesComponent,
        BattalionsComponent,
        MailComponent,
        UpgradeLeaderlevelComponent
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