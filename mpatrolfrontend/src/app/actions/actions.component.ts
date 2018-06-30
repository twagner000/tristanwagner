import { Component, OnInit, Input, TemplateRef } from '@angular/core';
import { BsModalService } from 'ngx-bootstrap/modal';
import { BsModalRef } from 'ngx-bootstrap/modal/bs-modal-ref.service';
import { MpatrolService, PlayerAction } from '../mpatrol.service';
import { Player, PublicPlayer } from '../mpatrol';

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
	targetPlayer: PublicPlayer;
	
	constructor(
		private mps: MpatrolService,
		private modalService: BsModalService
	) { }

	ngOnInit() {
		this.mps.getPlayers(this.player.game.id)
			.subscribe(playerList => this.playerList = playerList);
	}
	
	get action_available() : boolean {
		return true;
	}
	
	openModal(template: TemplateRef<any>) {
		this.modalRef = this.modalService.show(template);
	}
	
	closeModal() {
		if (!this.processing)
			this.modalRef.hide();
	}
	
	saveWork(): void {
		this.processing = true;
		this.mps.playerAction(
				this.player.id,
				new PlayerAction(
					'work',
					null
				)
			).subscribe(() => {
				this.processing = false;
				this.closeModal();
			});
	}
	
	saveSpy(): void {
		this.processing = true;
		this.mps.playerAction(
				this.player.id,
				new PlayerAction(
					'spy',
					this.targetPlayer.id
				)
			).subscribe(() => {
				this.processing = false;
				this.closeModal();
			});
	}
	
	saveAttack(): void {
		this.mps.addMessage('warning','Attack feature TBD',false);
		this.closeModal();
	}
}
