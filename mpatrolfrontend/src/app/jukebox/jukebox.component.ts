import { Component, OnInit, TemplateRef } from '@angular/core';
import { BsModalService } from 'ngx-bootstrap/modal';
import { BsModalRef } from 'ngx-bootstrap/modal/bs-modal-ref.service';
import { MpatrolService } from '../mpatrol.service';

@Component({
  selector: 'app-jukebox',
  templateUrl: './jukebox.component.html',
  styleUrls: ['./jukebox.component.css']
})

export class JukeboxComponent implements OnInit {
	modalRef: BsModalRef;
	
	constructor(
		public mps: MpatrolService,
		private modalService: BsModalService
	) { }

	ngOnInit() { }
	
	openModal(template: TemplateRef<any>) {
		this.modalRef = this.modalService.show(template);
	}
	
	closeModal() {
		this.modalRef.hide();
	}
	
}
