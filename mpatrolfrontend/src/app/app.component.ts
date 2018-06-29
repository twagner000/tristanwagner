import { Component, OnInit } from '@angular/core';
import { MpatrolService, Message } from './mpatrol.service';

@Component({
    selector: 'app-root',
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.css']
    })

export class AppComponent {
    title = 'Mossflower Patrol Game';

	constructor(
		public mps: MpatrolService
	) { }
}