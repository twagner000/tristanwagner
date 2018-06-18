import { Component, OnInit } from '@angular/core';
import { Creature } from '../creature';
import { CreatureService } from '../creature.service';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: [ './dashboard.component.css' ]
})
export class DashboardComponent implements OnInit {
  creatures: Creature[] = [];

  constructor(private creatureService: CreatureService) { }

  ngOnInit() {
    this.getCreatures();
  }

  getCreatures(): void {
    this.creatureService.getCreatures()
      .subscribe(creatures => this.creatures = creatures.slice(1, 5));
  }
}