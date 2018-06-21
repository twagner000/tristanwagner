import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { UpgradeTechnologyComponent } from './upgrade-technology.component';

describe('UpgradeTechnologyComponent', () => {
  let component: UpgradeTechnologyComponent;
  let fixture: ComponentFixture<UpgradeTechnologyComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ UpgradeTechnologyComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(UpgradeTechnologyComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
