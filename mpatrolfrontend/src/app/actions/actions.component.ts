import { Component, OnInit, Input } from '@angular/core';
import { Player } from '../mpatrol';

@Component({
  selector: 'app-actions',
  templateUrl: './actions.component.html',
  styleUrls: ['./actions.component.css']
})
export class ActionsComponent implements OnInit {
	@Input() player: Player;

	constructor() { }

	ngOnInit() {
	}
	
	get action_available() : boolean {
		return false;
	}
}
