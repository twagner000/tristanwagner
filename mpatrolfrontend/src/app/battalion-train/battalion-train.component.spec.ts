import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { BattalionTrainComponent } from './battalion-train.component';

describe('BattalionTrainComponent', () => {
  let component: BattalionTrainComponent;
  let fixture: ComponentFixture<BattalionTrainComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ BattalionTrainComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(BattalionTrainComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
