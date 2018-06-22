import { Component, OnInit, Input } from '@angular/core';
import { Router } from '@angular/router';
import { Player, PlayerUpgrade, Structure } from '../player';
import { StructureService } from '../structure.service';
import { PlayerService } from '../player.service';

@Component({
	selector: 'app-upgrade-structure',
	templateUrl: './upgrade-structure.component.html',
	styleUrls: ['./upgrade-structure.component.css']
})
export class UpgradeStructureComponent implements OnInit {

	@Input() player: Player;
	structures: Structure[];
	selectedUpgrade: Structure;

	constructor(
		private structureService: StructureService,
		private playerService: PlayerService,
		private router: Router,
	) { }

	ngOnInit() {
		this.getStructures();
		this.getPlayer();
	}
	
	getStructures(): void {
		this.structureService.getStructures()
			.subscribe(structures => this.structures = structures);
	}
  
	getPlayer(): void {
		this.playerService.getPlayer()
			.subscribe(player => this.player = player);
	}
	
	save(): void {
		var upgrade = new PlayerUpgrade();
		upgrade.player_id = this.player.id;
		upgrade.upgrade_type = 'structure';
		upgrade.upgrade_id = this.selectedUpgrade.id;
		this.playerService.upgradePlayer(upgrade)
			.subscribe(() => this.router.navigate(['/dashboard']));
	}
	
}