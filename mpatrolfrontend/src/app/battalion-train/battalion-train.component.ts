import { Component, OnInit, Input } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { Player, Battalion } from '../mpatrol';
import { MpatrolService, BattalionUpdate } from '../mpatrol.service';

@Component({
  selector: 'app-battalion-train',
  templateUrl: './battalion-train.component.html',
  styleUrls: ['./battalion-train.component.css']
})

export class BattalionTrainComponent implements OnInit {
	@Input() battalion: Battalion;
	player: Player;
	
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
						.subscribe(battalion => this.battalion = battalion);
				}
			});
	}
	
	save(): void {
		this.mps.updateBattalion(
				this.player.id,
				this.battalion.battalion_number,
				'train',
				new BattalionUpdate(
					null,
					null,
					this.battalion.up_opt_level,
					null,
					null
				)
			).subscribe(() => this.router.navigate(['/dashboard']));
	}

}
