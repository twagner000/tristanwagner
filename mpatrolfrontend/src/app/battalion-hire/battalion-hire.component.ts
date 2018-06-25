import { Component, OnInit, Input } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { Player, Battalion, Creature } from '../mpatrol';
import { MpatrolService } from '../mpatrol.service';


@Component({
  selector: 'app-battalion-hire',
  templateUrl: './battalion-hire.component.html',
  styleUrls: ['./battalion-hire.component.css']
})
export class BattalionHireComponent implements OnInit {
	@Input() battalion: Battalion;
	player: Player;
	creatures: Creature[];
	selectedCreature: Creature;
	update: Object;
	
	constructor(
		private mps: MpatrolService,
		private router: Router,
		private route: ActivatedRoute
	) { }

	ngOnInit() {
		this.update = new Object();
		this.update.creature = null;
		this.update.action = 'hire';
		this.update.count = null;
		this.mps.getPlayer()
			.subscribe(player => {
				this.player = player;
				const battalion_number = +this.route.snapshot.paramMap.get('battalion_number');
				if (player) {
					this.mps.getBattalion(player.id, battalion_number)
						.subscribe(battalion => {
							this.battalion = battalion;
							if (battalion.creature) this.update.creature = battalion.creature;
							/*if (battalion.creature) {
								this.update.count = battalion.count;
								for (var i=0; i<battalion.up_opts_creature.length; i++)
									if (battalion.up_opts_creature[i].id == battalion.creature.id)
										this.update.creature = battalion.up_opts_creature[i];
							}*/
						});
				}
			});
		this.mps.getCreatures()
			.subscribe(creatures => this.creatures = creatures);
	}
	
	get max_hire() {
		if (!this.update.creature) return null;
		var max_gold = this.unit_cost_gold>0 ? Math.floor(this.player.gold/this.unit_cost_gold) : 1000000;
		var max_xp = this.unit_cost_xp>0 ? Math.floor(this.player.xp/this.unit_cost_xp) : 1000000;
		var max_cp = this.update.creature.cost_cp>0 ? Math.floor(this.player.calc.cp_avail/this.update.creature.cost_cp) : 1000000;
		return Math.min(max_gold,max_xp,max_cp);
	}
	
	get invalid_count() {
		if (!this.update.action || !this.update.creature) return true;
		if (this.update.count == null) return true;
		if (this.update.count < 1) return true;
		if (this.update.action=='hire' && this.update.count > this.max_hire) return true;
		if (this.update.action=='fire' && this.update.count > this.battalion.count) return true;
		return false;
	}
	
	get unit_cost_gold() {
		if (!this.update.creature) return null;
		var unit_cost = this.update.creature.cost_gold;
		if (this.battalion.weapon_base && this.battalion.weapon_material)
			unit_cost += this.battalion.weapon_base.cost_gold*this.battalion.weapon_material.cost_mult;
		return unit_cost;
	}
	
	get unit_cost_xp() {
		return 10*(this.battalion.level-1);
	}
	
	get unit_refund_gold() {
		if (!this.update.creature || !this.battalion.weapon_base || !this.battalion.weapon_material) return null;
		return this.battalion.weapon_base.cost_gold*this.battalion.weapon_material.cost_mult;
	}
	
	get diagnostic() {
		return JSON.stringify(this.update);
	}
	
	/*save(): void {
		this.mps.upgradePlayer(new PlayerUpgrade(
				this.player.id,
				'leaderlevel',
				this.player.up_opt_ll.id)
			).subscribe(() => this.router.navigate(['/dashboard']));
	}*/

}
