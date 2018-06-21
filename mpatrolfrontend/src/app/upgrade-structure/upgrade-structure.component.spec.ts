import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { UpgradeStructureComponent } from './upgrade-structure.component';

describe('UpgradeStructureComponent', () => {
  let component: UpgradeStructureComponent;
  let fixture: ComponentFixture<UpgradeStructureComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ UpgradeStructureComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(UpgradeStructureComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
