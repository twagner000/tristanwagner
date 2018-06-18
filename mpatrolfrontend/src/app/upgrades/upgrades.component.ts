import { Component, OnInit, Input } from '@angular/core';
import { Player } from '../player';

@Component({
	selector: 'app-upgrades',
	templateUrl: './upgrades.component.html',
	styleUrls: ['./upgrades.component.css']
})
export class UpgradesComponent implements OnInit {
	@Input() player: Player;

	constructor() { }

	ngOnInit() {
	}

}
