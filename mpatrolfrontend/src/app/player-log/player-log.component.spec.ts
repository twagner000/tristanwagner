import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { PlayerLogComponent } from './player-log.component';

describe('PlayerLogComponent', () => {
  let component: PlayerLogComponent;
  let fixture: ComponentFixture<PlayerLogComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ PlayerLogComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(PlayerLogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
