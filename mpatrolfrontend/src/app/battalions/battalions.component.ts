import { Component, OnInit, Input } from '@angular/core';
import { Router } from '@angular/router';
import { Player } from '../mpatrol';
import { MpatrolService } from '../mpatrol.service';

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
