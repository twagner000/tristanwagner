import { Component, OnInit, Input, TemplateRef } from '@angular/core';
import { BsModalService } from 'ngx-bootstrap/modal';
import { BsModalRef } from 'ngx-bootstrap/modal/bs-modal-ref.service';
import { MpatrolService, PlayerAction } from '../mpatrol.service';
import { Player } from '../mpatrol';

@Component({
  selector: 'app-actions',
  templateUrl: './actions.component.html',
  styleUrls: ['./actions.component.css']
})
export class ActionsComponent implements OnInit {
	@Input() player: Player;
	modalRef: BsModalRef;
	processing: boolean = false;
	
	constructor(
		private mps: MpatrolService,
		private modalService: BsModalService
	) { }

	ngOnInit() {
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
		console.log('saveWork()');
		this.processing = true;
		setTimeout(() => {
				this.processing = false;
				this.closeModal();
			}, 1000);
		/*this.mps.playerAction(
				this.player.id,
				new PlayerAction(
					'work',
					null
				)
			).subscribe(() => this.router.navigate(['/dashboard']));*/
	}
}
