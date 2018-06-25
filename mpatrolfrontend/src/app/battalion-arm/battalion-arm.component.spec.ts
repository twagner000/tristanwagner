import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { BattalionArmComponent } from './battalion-arm.component';

describe('BattalionArmComponent', () => {
  let component: BattalionArmComponent;
  let fixture: ComponentFixture<BattalionArmComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ BattalionArmComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(BattalionArmComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
