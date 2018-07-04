import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { MpatrolService } from '../mpatrol.service';
import { Player, GamePlayer } from '../mpatrol';

@Component({
  selector: 'app-choose-player',
  templateUrl: './choose-player.component.html',
  styleUrls: ['./choose-player.component.css']
})

export class ChoosePlayerComponent implements OnInit {
	resumeGames: GamePlayer[] = [];
	joinGames: GamePlayer[] = [];
	resume: GamePlayer;
	join: GamePlayer;
	character_name: string;
	joining: boolean = false;
	errors = null;
	
	constructor(
		private mps: MpatrolService,
		private router: Router
	) { }

	ngOnInit() {
		this.mps.clearPlayer();
		this.mps.getGames()
			.subscribe(games => {
				for (let g of games) {
					if (g.player)
						this.resumeGames.push(g);
					else
						this.joinGames.push(g);
				}
				if (this.resumeGames)
					this.resume = this.resumeGames[0];
				if (this.joinGames)
					this.join = this.joinGames[0];
			});
		this.mps.getPlayer()
			.subscribe(player => { if (player) this.router.navigate(['/']); });
		this.mps.getErrors()
			.subscribe(errors => this.errors = errors);
	}
	
	resumeGame() {
		this.mps.setPlayer(this.resume.player.id);
	}
	
	joinGame() {
		this.joining = true;
		this.mps.joinGame(this.join.id, this.character_name)
			.subscribe(result => {
				if (result)
					this.mps.setPlayer(result["player_id"]);
				else
					this.joining = false;
			});
	}
}
