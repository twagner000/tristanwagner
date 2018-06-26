import { Component, OnInit, Input } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { Player, Battalion, BriefCreature, Creature } from '../mpatrol';
import { MpatrolService, BattalionUpdate } from '../mpatrol.service';


@Component({
  selector: 'app-battalion-hire',
  templateUrl: './battalion-hire.component.html',
  styleUrls: ['./battalion-hire.component.css']
})
export class BattalionHireComponent implements OnInit {
	@Input() battalion: Battalion;
	player: Player;
	creatures: Creature[];
	new_action: string;
	new_creature: BriefCreature;
	new_count_delta: number;
	
	constructor(
		private mps: MpatrolService,
		private router: Router,
		private route: ActivatedRoute
	) { }

	ngOnInit() {
		this.new_action = 'hire';
		this.new_count_delta = 1;
		this.mps.getPlayer()
			.subscribe(player => {
				this.player = player;
				const battalion_number = +this.route.snapshot.paramMap.get('battalion_number');
				if (player) {
					this.mps.getBattalion(player.id, battalion_number)
						.subscribe(battalion => {
							this.battalion = battalion;
							if (battalion.creature) this.new_creature = battalion.creature;
						});
				}
			});
		this.mps.getCreatures()
			.subscribe(creatures => this.creatures = creatures);
	}
	
	get max_hire() {
		if (!this.player || !this.battalion || !this.new_creature) return null;
		var max_gold = this.unit_cost_gold>0 ? Math.floor(this.player.gold/this.unit_cost_gold) : 1000000;
		var max_xp = this.unit_cost_xp>0 ? Math.floor(this.player.xp/this.unit_cost_xp) : 1000000;
		var max_cp = this.new_creature.cost_cp>0 ? Math.floor(this.player.calc.cp_avail/this.new_creature.cost_cp) : 1000000;
		return Math.min(max_gold,max_xp,max_cp);
	}
	
	get invalid_count() {
		if (!this.player || !this.battalion || !this.new_creature) return true;
		if (this.new_count_delta == null) return true;
		if (this.new_count_delta < 1) return true;
		if (this.new_action=='hire' && this.new_count_delta > this.max_hire) return true;
		if (this.new_action=='fire' && this.new_count_delta > this.battalion.count) return true;
		return false;
	}
	
	get unit_cost_gold() {
		if (!this.battalion || !this.new_creature) return null;
		var unit_cost = this.new_creature.cost_gold;
		if (this.battalion.weapon_base && this.battalion.weapon_material)
			unit_cost += this.battalion.weapon_base.cost_gold*this.battalion.weapon_material.cost_mult;
		return unit_cost;
	}
	
	get unit_cost_xp() {
		if (!this.battalion) return null;
		return this.battalion.training_cost_xp_ea*(this.battalion.level-1);
	}
	
	get unit_refund_gold() {
		if (!this.battalion || !this.new_creature || !this.battalion.weapon_base || !this.battalion.weapon_material) return null;
		return this.battalion.weapon_base.cost_gold*this.battalion.weapon_material.cost_mult;
	}
	
	get diagnostic() {
		return JSON.stringify(this.battalion);
	}
	
	save(): void {
		this.mps.updateBattalion(
				this.player.id,
				this.battalion.battalion_number,
				this.new_action,
				new BattalionUpdate(
					this.new_creature.id,
					this.new_count_delta
				)
			).subscribe(() => this.router.navigate(['/dashboard']));
	}

}
