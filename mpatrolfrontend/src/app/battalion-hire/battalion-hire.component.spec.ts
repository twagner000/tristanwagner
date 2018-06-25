import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { BattalionHireComponent } from './battalion-hire.component';

describe('BattalionHireComponent', () => {
  let component: BattalionHireComponent;
  let fixture: ComponentFixture<BattalionHireComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ BattalionHireComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(BattalionHireComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
