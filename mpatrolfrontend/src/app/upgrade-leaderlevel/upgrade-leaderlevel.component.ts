import { Component, OnInit, Input } from '@angular/core';
import { Location } from '@angular/common';
import { PlayerUpgradeLeaderLevel } from '../player';
import { PlayerService } from '../player.service';

@Component({
	selector: 'app-upgrade-leaderlevel',
	templateUrl: './upgrade-leaderlevel.component.html',
	styleUrls: ['./upgrade-leaderlevel.component.css']
})
export class UpgradeLeaderlevelComponent implements OnInit {

	upgrade: PlayerUpgradeLeaderLevel;

	constructor(
		private playerService: PlayerService,
		private location: Location
	) { }

	ngOnInit() {
		this.getPlayerUpgradeLeaderLevel();
	}

	getPlayerUpgradeLeaderLevel(): void {
		this.playerService.getPlayerUpgradeLeaderLevel()
			.subscribe(upgrade => this.upgrade = upgrade);
	}
	
	save(): void {
		this.upgrade.upgrade_id = this.upgrade.next_ll.id;
		this.playerService.updatePlayerUpgradeLeaderLevel(this.upgrade)
		.subscribe(() => this.location.back());
	}
	
}