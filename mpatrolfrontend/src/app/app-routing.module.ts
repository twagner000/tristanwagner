import { NgModule }             from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { DashboardComponent }   from './dashboard/dashboard.component';
import { UpgradeLeaderlevelComponent }   from './upgrade-leaderlevel/upgrade-leaderlevel.component';
import { UpgradeTechnologyComponent }   from './upgrade-technology/upgrade-technology.component';
import { UpgradeStructureComponent }   from './upgrade-structure/upgrade-structure.component';

import { CreaturesComponent }      from './creatures/creatures.component';
import { CreatureDetailComponent }  from './creature-detail/creature-detail.component';

const routes: Routes = [
  { path: '', redirectTo: '/dashboard', pathMatch: 'full' },
  { path: 'dashboard', component: DashboardComponent },
  { path: 'upgrade', children: [
	  { path: '', redirectTo: '/dashboard', pathMatch: 'full' },
	  { path: 'leaderlevel', component: UpgradeLeaderlevelComponent },
	  { path: 'technology', component: UpgradeTechnologyComponent },
	  { path: 'structure', component: UpgradeStructureComponent }
  ]},
  { path: 'detail/:pk', component: CreatureDetailComponent },
  { path: 'creatures', component: CreaturesComponent }
];

@NgModule({
  imports: [ RouterModule.forRoot(routes) ],
  exports: [ RouterModule ]
})
export class AppRoutingModule {}