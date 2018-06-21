import { Component, OnInit, Input } from '@angular/core';
import { Router } from '@angular/router';
import { Player, LeaderLevel } from '../player';
import { LeaderLevelService } from '../leader-level.service';
import { PlayerService } from '../player.service';

@Component({
	selector: 'app-upgrade-leaderlevel',
	templateUrl: './upgrade-leaderlevel.component.html',
	styleUrls: ['./upgrade-leaderlevel.component.css']
})
export class UpgradeLeaderlevelComponent implements OnInit {

	@Input() player: Player;
	leaderlevels: LeaderLevel[];

	constructor(
		private leaderLevelService: LeaderLevelService,
		private playerService: PlayerService,
		private router: Router,
	) { }

	ngOnInit() {
		this.getLeaderLevels();
		this.getPlayer();
	}
	
	getLeaderLevels(): void {
		this.leaderLevelService.getLeaderLevels()
			.subscribe(leaderlevels => this.leaderlevels = leaderlevels);
	}
  
	getPlayer(): void {
		this.playerService.getPlayer()
			.subscribe(player => this.player = player);
	}
	
	save(): void {
		this.playerService.upgradePlayer({
				'player_id': this.player.id,
				'upgrade_type': 'll',
				'upgrade_id': this.player.ll_upgrade.id
			})
			.subscribe(() => this.router.navigate(['/dashboard']));
	}
	
}