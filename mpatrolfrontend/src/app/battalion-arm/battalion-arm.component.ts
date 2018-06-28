import { Component, OnInit, Input } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { Player, Battalion, WeaponBase, WeaponMaterial, BriefWeaponBase, BriefWeaponMaterial } from '../mpatrol';
import { MpatrolService, BattalionUpdate } from '../mpatrol.service';

@Component({
  selector: 'app-battalion-arm',
  templateUrl: './battalion-arm.component.html',
  styleUrls: ['./battalion-arm.component.css']
})

export class BattalionArmComponent implements OnInit {
	@Input() battalion: Battalion;
	player: Player;
	weapon_bases: WeaponBase[];
	weapon_materials: WeaponMaterial[];
	selectedWeaponBase: BriefWeaponBase;
	selectedWeaponMaterial: BriefWeaponMaterial;
	
	constructor(
		private mps: MpatrolService,
		private router: Router,
		private route: ActivatedRoute
	) { }

	ngOnInit() {
		this.mps.getPlayer()
			.subscribe(player => {
				this.player = player;
				const battalion_number = +this.route.snapshot.paramMap.get('battalion_number');
				if (player) {
					this.mps.getBattalion(player.id, battalion_number)
						.subscribe(battalion => {
							this.battalion = battalion;
							if (battalion.weapon_base)
								for (let w of battalion.up_opts_weapon_base)
									if (w.id == battalion.weapon_base.id)
										this.selectedWeaponBase = w;
							if (battalion.weapon_material)
								for (let w of battalion.up_opts_weapon_material)
									if (w.id == battalion.weapon_material.id)
										this.selectedWeaponMaterial = w;
						});
				}
			});
		this.mps.getWeaponBases()
			.subscribe(weapon_bases => this.weapon_bases = weapon_bases);
		this.mps.getWeaponMaterials()
			.subscribe(weapon_materials => this.weapon_materials = weapon_materials);
	}
	
	playerHasTechNamed(technology_name: string) : boolean {
		if (!this.player) return null;
		for (let t of this.player.technologies)
			if (t.name == technology_name)
				return true;
		return false;
	}
	
	playerHasStructNamed(structure_name: string) : boolean {
		if (!this.player) return null;
		for (let s of this.player.structures)
			if (s.name == structure_name)
				return true;
		return false;
	}
	
	get cost() : number {
		if (!this.battalion || !this.selectedWeaponBase || !this.selectedWeaponMaterial) return null;
		let cur_weapons_gold = 0
		if (this.battalion.weapon_base && this.battalion.weapon_material)
			cur_weapons_gold = this.battalion.weapon_base.cost_gold*this.battalion.weapon_material.cost_mult;
		return this.battalion.count*(this.selectedWeaponBase.cost_gold*this.selectedWeaponMaterial.cost_mult - cur_weapons_gold);
	}
	
	save(): void {
		this.mps.updateBattalion(
				this.player.id,
				this.battalion.battalion_number,
				'arm',
				new BattalionUpdate(
					null,
					null,
					null,
					this.selectedWeaponBase.id,
					this.selectedWeaponMaterial.id
				)
			).subscribe(() => this.router.navigate(['/dashboard']));
	}

}
