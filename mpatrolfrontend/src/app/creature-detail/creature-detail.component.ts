import { Component, OnInit, Input } from '@angular/core';
import { Creature } from '../creature';

import { ActivatedRoute } from '@angular/router';

import { CreatureService }  from '../creature.service';

@Component({
  selector: 'app-creature-detail',
  templateUrl: './creature-detail.component.html',
  styleUrls: ['./creature-detail.component.css']
})
export class CreatureDetailComponent implements OnInit {
	@Input() creature: Creature;
	
	constructor(
		private route: ActivatedRoute,
		private creatureService: CreatureService,
	) {}

	ngOnInit() {
		this.getCreature();
	}
	
	getCreature(): void {
		const pk = +this.route.snapshot.paramMap.get('pk');
		this.creatureService.getCreature(pk)
			.subscribe(creature => this.creature = creature);
	}
}
