import { Component, OnInit, Input } from '@angular/core';
import { Router } from '@angular/router';
import { Player, PlayerUpgrade, Technology } from '../player';
import { TechnologyService } from '../technology.service';
import { PlayerService } from '../player.service';

@Component({
  selector: 'app-upgrade-technology',
  templateUrl: './upgrade-technology.component.html',
  styleUrls: ['./upgrade-technology.component.css']
})
export class UpgradeTechnologyComponent implements OnInit {

	@Input() player: Player;
	technologies: Technology[];
	selectedUpgrade: Technology;

	constructor(
		private technologyService: TechnologyService,
		private playerService: PlayerService,
		private router: Router,
	) { }

	ngOnInit() {
		this.getTechnologies();
		this.getPlayer();
	}
	
	getTechnologies(): void {
		this.technologyService.getTechnologies()
			.subscribe(technologies => this.technologies = technologies);
	}
  
	getPlayer(): void {
		this.playerService.getPlayer()
			.subscribe(player => this.player = player);
	}
	
	save(): void {
		var upgrade = new PlayerUpgrade();
		upgrade.player_id = this.player.id;
		upgrade.upgrade_type = 'technology';
		upgrade.upgrade_id = this.selectedUpgrade.id;
		this.playerService.upgradePlayer(upgrade)
			.subscribe(() => this.router.navigate(['/dashboard']));
	}
	
}
