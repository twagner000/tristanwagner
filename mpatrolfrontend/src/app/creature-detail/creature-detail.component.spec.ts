import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { CreatureDetailComponent } from './creature-detail.component';

describe('CreatureDetailComponent', () => {
  let component: CreatureDetailComponent;
  let fixture: ComponentFixture<CreatureDetailComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ CreatureDetailComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(CreatureDetailComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
