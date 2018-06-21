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
  { path: 'upgrade/leaderlevel', component: UpgradeLeaderlevelComponent },
  { path: 'upgrade/technology', component: UpgradeTechnologyComponent },
  { path: 'upgrade/structure', component: UpgradeStructureComponent },
  { path: 'detail/:pk', component: CreatureDetailComponent },
  { path: 'creatures', component: CreaturesComponent }
];

@NgModule({
  imports: [ RouterModule.forRoot(routes) ],
  exports: [ RouterModule ]
})
export class AppRoutingModule {}