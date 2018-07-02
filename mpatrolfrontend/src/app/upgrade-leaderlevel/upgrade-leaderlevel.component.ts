import { Component, OnInit, Input } from '@angular/core';
import { Router } from '@angular/router';
import { Player, LeaderLevel } from '../mpatrol';
import { MpatrolService, PlayerUpgrade } from '../mpatrol.service';

@Component({
	selector: 'app-upgrade-leaderlevel',
	templateUrl: './upgrade-leaderlevel.component.html',
	styleUrls: ['./upgrade-leaderlevel.component.css']
})
export class UpgradeLeaderlevelComponent implements OnInit {
	player: Player;
	leaderlevels: LeaderLevel[];

	constructor(
		private mps: MpatrolService,
		private router: Router
	) { }

	ngOnInit() {
		this.mps.getPlayer()
			.subscribe(player => this.player = player);
		this.mps.getLeaderLevels()
			.subscribe(leaderlevels => this.leaderlevels = leaderlevels);
	}
	
	save(): void {
		this.mps.upgradePlayer(new PlayerUpgrade(
				'leaderlevel',
				this.player.up_opt_ll.id)
			).subscribe(() => this.router.navigate(['/dashboard']));
	}
	
}