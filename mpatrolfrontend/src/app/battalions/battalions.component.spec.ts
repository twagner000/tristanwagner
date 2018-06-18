import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { BattalionsComponent } from './battalions.component';

describe('BattalionsComponent', () => {
  let component: BattalionsComponent;
  let fixture: ComponentFixture<BattalionsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ BattalionsComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(BattalionsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
