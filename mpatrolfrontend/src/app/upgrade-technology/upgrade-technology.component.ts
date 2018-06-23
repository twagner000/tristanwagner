import { Component, OnInit, Input } from '@angular/core';
import { Router } from '@angular/router';
import { Player, Technology } from '../mpatrol';
import { MpatrolService, PlayerUpgrade } from '../mpatrol.service';

@Component({
  selector: 'app-upgrade-technology',
  templateUrl: './upgrade-technology.component.html',
  styleUrls: ['./upgrade-technology.component.css']
})
export class UpgradeTechnologyComponent implements OnInit {
	player: Player;
	technologies: Technology[];
	selectedUpgrade: Technology;

	constructor(
		private mps: MpatrolService,
		private router: Router
	) { }

	ngOnInit() {
		this.mps.getPlayer()
			.subscribe(player => this.player = player);
		this.player = this.mps.refreshPlayerIfNeeded();
		this.mps.getTechnologies()
			.subscribe(technologies => this.technologies = technologies);
	}
	
	save(): void {
		this.mps.upgradePlayer(new PlayerUpgrade(
				this.player.id,
				'technology',
				this.selectedUpgrade.id)
			).subscribe(() => this.router.navigate(['/dashboard']));
	}
	
}
