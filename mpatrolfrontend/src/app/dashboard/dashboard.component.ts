import { Component, OnInit } from '@angular/core';
import { Player } from '../mpatrol';
import { MpatrolService } from '../mpatrol.service';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: [ './dashboard.component.css' ]
})
export class DashboardComponent implements OnInit {
	player: Player;

	constructor(
		private mps: MpatrolService
	) { }

	ngOnInit() {
		this.mps.getPlayer()
			.subscribe(player => this.player = player);
	}
}