import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { ModalModule, AlertModule, TabsModule, ButtonsModule } from 'ngx-bootstrap';

import { AppComponent } from './app.component';
import { AppRoutingModule } from './/app-routing.module';
import { DashboardComponent } from './dashboard/dashboard.component';
import {APP_BASE_HREF} from '@angular/common';
import { ActionsComponent } from './actions/actions.component';
import { UpgradesComponent } from './upgrades/upgrades.component';
import { BattalionsComponent } from './battalions/battalions.component';
import { UpgradeLeaderlevelComponent } from './upgrade-leaderlevel/upgrade-leaderlevel.component';
import { UpgradeStructureComponent } from './upgrade-structure/upgrade-structure.component';
import { UpgradeTechnologyComponent } from './upgrade-technology/upgrade-technology.component';
import { BattalionHireComponent } from './battalion-hire/battalion-hire.component';
import { BattalionTrainComponent } from './battalion-train/battalion-train.component';
import { BattalionArmComponent } from './battalion-arm/battalion-arm.component';
import { ChoosePlayerComponent } from './choose-player/choose-player.component';
import { JukeboxComponent } from './jukebox/jukebox.component';
import { PlayerLogComponent } from './player-log/player-log.component';

    @NgModule({
    declarations: [
        AppComponent,
        DashboardComponent,
        ActionsComponent,
        UpgradesComponent,
        BattalionsComponent,
        UpgradeLeaderlevelComponent,
        UpgradeStructureComponent,
        UpgradeTechnologyComponent,
        BattalionHireComponent,
        BattalionTrainComponent,
        BattalionArmComponent,
        ChoosePlayerComponent,
        JukeboxComponent,
        PlayerLogComponent,
    ],
    imports: [
        BrowserModule ,
        FormsModule,
		AppRoutingModule,
		HttpClientModule,
		ModalModule.forRoot(),
		AlertModule.forRoot(),
		TabsModule.forRoot(),
		ButtonsModule.forRoot(),
    ],
    providers: [{provide: APP_BASE_HREF, useValue : '/mpatrol' }],
    bootstrap: [AppComponent]
    })
    export class AppModule { }