import { Component, OnInit, Input } from '@angular/core';
import { Player } from '../mpatrol';

@Component({
  selector: 'app-battalions',
  templateUrl: './battalions.component.html',
  styleUrls: ['./battalions.component.css']
})
export class BattalionsComponent implements OnInit {
	@Input() player: Player;

	constructor() { }

	ngOnInit() {
	}

}
