import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { MpatrolService } from '../mpatrol.service';
import { GamePlayer } from '../mpatrol';

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
	
	constructor(
		private mps: MpatrolService,
		private router: Router
	) { }

	ngOnInit() {
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
	}
	
	resumeGame() {
		this.mps.setPlayer(this.resume.player.id)
			.subscribe((player) => this.router.navigate(['/']));
	}
	
	joinGame() {
		console.log('Not yet implemented');
	}
	
	get diagnostic() {
		return JSON.stringify(this.games);
	}
	
	/*save(): void {
		this.processing = true;
		this.mps.playerAction(this.player.id, new PlayerAction(action, (action == 'spy' || action == 'attack') ? this.targetPlayer.id : null))
			.subscribe(() => {
				this.processing = false;
				this.closeModal();
			});
	}*/
}
