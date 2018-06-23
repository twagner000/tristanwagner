import { Component, OnInit, Input } from '@angular/core';
import { Router } from '@angular/router';
import { Player, Structure } from '../mpatrol';
import { MpatrolService, PlayerUpgrade } from '../mpatrol.service';

@Component({
	selector: 'app-upgrade-structure',
	templateUrl: './upgrade-structure.component.html',
	styleUrls: ['./upgrade-structure.component.css']
})
export class UpgradeStructureComponent implements OnInit {
	player: Player;
	structures: Structure[];
	selectedUpgrade: Structure;

	constructor(
		private mps: MpatrolService,
		private router: Router
	) { }

	ngOnInit() {
		this.mps.getPlayer()
			.subscribe(player => this.player = player);
		this.player = this.mps.refreshPlayerIfNeeded();
		this.mps.getStructures()
			.subscribe(structures => this.structures = structures);
	}
	
	save(): void {
		this.mps.upgradePlayer(new PlayerUpgrade(
				this.player.id,
				'structure',
				this.selectedUpgrade.id)
			).subscribe(() => this.router.navigate(['/dashboard']));
	}
	
}