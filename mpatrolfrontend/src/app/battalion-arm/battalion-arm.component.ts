import { Component, OnInit, Input } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { Player, Battalion, WeaponBase, WeaponMaterial } from '../mpatrol';
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
	selectedWeaponBase: WeaponBase;
	selectedMaterialMaterial: WeaponMaterial;
	
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
						});
				}
			});
		this.mps.getWeaponBases()
			.subscribe(weapon_bases => this.weapon_bases = weapon_bases);
		this.mps.getWeaponMaterials()
			.subscribe(weapon_materials => this.weapon_materials = weapon_materials);
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
					this.selectedMaterialBase.id,
					this.selectedMaterialMaterial.id
				)
			).subscribe(() => this.router.navigate(['/dashboard']));
	}

}
