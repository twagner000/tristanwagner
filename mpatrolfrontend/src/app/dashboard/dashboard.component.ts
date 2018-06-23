import { Component, OnInit } from '@angular/core';
import { Creature } from '../creature';
import { CreatureService } from '../creature.service';
import { Player } from '../mpatrol';
import { MpatrolService } from '../mpatrol.service';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: [ './dashboard.component.css' ]
})
export class DashboardComponent implements OnInit {
	creatures: Creature[] = [];

	player: Player;

	constructor(
		private creatureService: CreatureService,
		private mps: MpatrolService
	) { }

	ngOnInit() {
		this.mps.getPlayer()
			.subscribe(player => this.player = player);
		this.player = this.mps.refreshPlayerIfNeeded();
		this.getCreatures();
	}

	getCreatures(): void {
		this.creatureService.getCreatures()
			.subscribe(creatures => this.creatures = creatures.slice(1, 5));
	}
}