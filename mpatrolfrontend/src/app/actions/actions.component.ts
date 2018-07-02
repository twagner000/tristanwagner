import { Component, OnInit, Input, TemplateRef } from '@angular/core';
import { BsModalService } from 'ngx-bootstrap/modal';
import { BsModalRef } from 'ngx-bootstrap/modal/bs-modal-ref.service';
import { MpatrolService, PlayerAction } from '../mpatrol.service';
import { Player, PublicPlayer, PlayerScore } from '../mpatrol';

@Component({
  selector: 'app-actions',
  templateUrl: './actions.component.html',
  styleUrls: ['./actions.component.css']
})
export class ActionsComponent implements OnInit {
	@Input() player: Player;
	modalRef: BsModalRef;
	processing: boolean = false;
	playerList: PublicPlayer[];
	top5: PlayerScore[];
	targetPlayer: PublicPlayer;
	
	constructor(
		private mps: MpatrolService,
		private modalService: BsModalService
	) { }

	ngOnInit() {
		this.mps.getPlayers(this.player.game.id)
			.subscribe(playerList => this.playerList = playerList);
		this.mps.getTop5(this.player.game.id)
			.subscribe(top5 => this.top5 = top5);
	}
	
	openModal(template: TemplateRef<any>) {
		this.modalRef = this.modalService.show(template);
	}
	
	closeModal() {
		if (!this.processing)
			this.modalRef.hide();
	}
	
	save(action: string): void {
		this.processing = true;
		this.mps.playerAction(this.player.id, new PlayerAction(action, (action == 'spy' || action == 'attack') ? this.targetPlayer.id : null))
			.subscribe(() => {
				this.processing = false;
				this.closeModal();
			});
	}
}
