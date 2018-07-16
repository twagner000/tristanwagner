import { Component, OnInit, Input, TemplateRef } from '@angular/core';
import { BsModalService } from 'ngx-bootstrap/modal';
import { BsModalRef } from 'ngx-bootstrap/modal/bs-modal-ref.service';
import { MpatrolService } from '../mpatrol.service';
import { Player, PlayerLog } from '../mpatrol';

@Component({
  selector: 'app-player-log',
  templateUrl: './player-log.component.html',
  styleUrls: ['./player-log.component.css']
})
export class PlayerLogComponent implements OnInit {
	@Input() player: Player;
	modalRef: BsModalRef;
	battleLogs: PlayerLog[];
	espionageLogs: PlayerLog[];
	incomeLogs: PlayerLog[];
	selectedLog: PlayerLog;
	logType: string = 'attack';
	
	constructor(
		private mps: MpatrolService,
		private modalService: BsModalService
	) { }

	ngOnInit() {
		this.mps.getPlayerLogs()
			.subscribe(logs => {				
				this.battleLogs = [];
				this.espionageLogs = [];
				this.incomeLogs = [];
				if (logs != null) {
					for (let l of logs) {
						if (l.action == 'attack' || l.action == 'was-attacked')
							this.battleLogs.push(l);
						if (l.action == 'spy' || l.action == 'spied-on')
							this.espionageLogs.push(l);
						if (l.action == 'work' || l.action == 'interest')
							this.incomeLogs.push(l);
					}
				}
			});
	}
	
	openModal(template: TemplateRef<any>, log: PlayerLog = null) {
		this.selectedLog = log;
		this.modalRef = this.modalService.show(template);
	}
	
	closeModal() {
		this.modalRef.hide();
	}
}