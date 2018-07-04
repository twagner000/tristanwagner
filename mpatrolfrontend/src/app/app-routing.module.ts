import { NgModule }             from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { DashboardComponent }   from './dashboard/dashboard.component';
import { ChoosePlayerComponent }   from './choose-player/choose-player.component';
import { UpgradeLeaderlevelComponent }   from './upgrade-leaderlevel/upgrade-leaderlevel.component';
import { UpgradeTechnologyComponent }   from './upgrade-technology/upgrade-technology.component';
import { UpgradeStructureComponent }   from './upgrade-structure/upgrade-structure.component';
import { BattalionHireComponent }   from './battalion-hire/battalion-hire.component';
import { BattalionTrainComponent }   from './battalion-train/battalion-train.component';
import { BattalionArmComponent }   from './battalion-arm/battalion-arm.component';

const routes: Routes = [
  { path: '', redirectTo: '/dashboard', pathMatch: 'full' },
  { path: 'dashboard', component: DashboardComponent },
  { path: 'choose', component: ChoosePlayerComponent },
  { path: 'upgrade', children: [
	  { path: '', redirectTo: '/dashboard', pathMatch: 'full' },
	  { path: 'leaderlevel', component: UpgradeLeaderlevelComponent },
	  { path: 'technology', component: UpgradeTechnologyComponent },
	  { path: 'structure', component: UpgradeStructureComponent }
  ]},
  { path: 'battalion/:battalion_number', children: [
	  { path: '', redirectTo: '/dashboard', pathMatch: 'full' },
	  { path: 'hire', component: BattalionHireComponent },
	  { path: 'train', component: BattalionTrainComponent },
	  { path: 'arm', component: BattalionArmComponent }
  ]}
];

@NgModule({
  imports: [ RouterModule.forRoot(routes) ],
  exports: [ RouterModule ]
})
export class AppRoutingModule {}